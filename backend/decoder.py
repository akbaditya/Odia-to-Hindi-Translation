from typing import List

import torch
import torch.nn as nn
import torch.nn.functional as F

from config import Config
from vocab import Vocabulary
from text_preprocessing import TextCleaner


class BeamSearchDecoder:
    """Beam search decoder with temperature scaling and length penalty."""

    def __init__(
        self,
        model: nn.Module,
        src_vocab: Vocabulary,
        tgt_vocab: Vocabulary,
        device: torch.device,
        beam_size: int = Config.BEAM_SIZE,
        temperature: float = Config.TEMPERATURE,
        length_penalty: float = Config.LENGTH_PENALTY,
        max_len: int = Config.MAX_DECODE_LEN,
    ):
        self.model = model
        self.src_vocab = src_vocab
        self.tgt_vocab = tgt_vocab
        self.device = device
        self.beam_size = beam_size
        self.temperature = temperature
        self.length_penalty = length_penalty
        self.max_len = max_len

        self.pad_idx = Vocabulary.PAD_IDX
        self.sos_idx = Vocabulary.SOS_IDX
        self.eos_idx = Vocabulary.EOS_IDX

    @torch.no_grad()
    def decode(self, src: torch.Tensor) -> List[int]:
        self.model.eval()
        src = src.to(self.device)

        memory, src_pad_mask = self.model.encode(src)

        B = self.beam_size
        memory = memory.expand(B, -1, -1)
        src_pad_mask = src_pad_mask.expand(B, -1)

        beams = [([self.sos_idx], 0.0)]
        completed = []

        for _ in range(self.max_len):
            if not beams:
                break

            seqs = [b[0] for b in beams]
            lengths = [len(s) for s in seqs]
            max_l = max(lengths)
            tgt_batch = torch.tensor(
                [s + [self.pad_idx] * (max_l - len(s)) for s in seqs],
                dtype=torch.long,
                device=self.device,
            )

            _mem = memory[: len(beams)]
            _smask = src_pad_mask[: len(beams)]
            with torch.amp.autocast("cuda", enabled=Config.USE_AMP):
                out = self.model.decode(tgt_batch, _mem, _smask)

            candidates = []
            for i, (tok_ids, beam_score) in enumerate(beams):
                last_pos = lengths[i] - 1
                logits_i = out[i, last_pos, :] / self.temperature
                log_probs = F.log_softmax(logits_i, dim=-1)
                top_log_probs, top_idxs = log_probs.topk(B)

                for log_p, idx in zip(top_log_probs.tolist(), top_idxs.tolist()):
                    new_score = beam_score + log_p
                    new_ids = tok_ids + [idx]
                    if idx == self.eos_idx:
                        length_pen = ((5 + len(new_ids)) / 6) ** self.length_penalty
                        final_score = new_score / length_pen
                        completed.append((new_ids, final_score))
                    else:
                        candidates.append((new_ids, new_score))

            candidates.sort(key=lambda x: x[1], reverse=True)
            beams = candidates[:B]

            if len(completed) >= B:
                break

        if not completed:
            for tok_ids, score in beams:
                length_pen = ((5 + len(tok_ids)) / 6) ** self.length_penalty
                completed.append((tok_ids + [self.eos_idx], score / length_pen))

        completed.sort(key=lambda x: x[1], reverse=True)
        best_ids = completed[0][0]

        return [t for t in best_ids if t not in (self.sos_idx, self.eos_idx, self.pad_idx)]

    def translate(self, odia_text: str) -> str:
        cleaner = TextCleaner(lang="or")
        cleaned = cleaner.clean(odia_text)
        if not cleaned.strip():
            return ""

        src_ids = self.src_vocab.encode(cleaned, add_special=True)[: Config.MAX_LEN + 2]
        src_tensor = torch.tensor([src_ids], dtype=torch.long)

        tgt_ids = self.decode(src_tensor)

        raw = self.tgt_vocab.decode(tgt_ids, skip_special=True)
        return " ".join(t for t in raw.split() if t != "<unk>")
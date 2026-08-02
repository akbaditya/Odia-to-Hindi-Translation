import math
from typing import Tuple

import torch
import torch.nn as nn

from config import Config
from vocab import Vocabulary


class PositionalEncoding(nn.Module):
    def __init__(self, d_model: int, dropout: float = 0.1, max_len: int = 1024):
        super().__init__()
        self.dropout = nn.Dropout(p=dropout)
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(
            torch.arange(0, d_model, 2, dtype=torch.float) * (-math.log(10000.0) / d_model)
        )
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        self.register_buffer("pe", pe.unsqueeze(0))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.dropout(x + self.pe[:, : x.size(1)])


class TranslatorTransformer(nn.Module):
    """Seq2Seq Transformer for Odia to Hindi translation."""

    def __init__(
        self,
        src_vocab_size: int,
        tgt_vocab_size: int,
        d_model: int = Config.D_MODEL,
        nhead: int = Config.N_HEADS,
        num_enc_layers: int = Config.N_ENC_LAYERS,
        num_dec_layers: int = Config.N_DEC_LAYERS,
        dim_feedforward: int = Config.D_FF,
        dropout: float = Config.DROPOUT,
        max_pos_enc: int = Config.MAX_POS_ENC,
        pad_idx: int = Vocabulary.PAD_IDX,
    ):
        super().__init__()
        self.d_model = d_model
        self.pad_idx = pad_idx

        self.src_embed = nn.Embedding(src_vocab_size, d_model, padding_idx=pad_idx)
        self.tgt_embed = nn.Embedding(tgt_vocab_size, d_model, padding_idx=pad_idx)
        self.pos_enc = PositionalEncoding(d_model, dropout, max_pos_enc)

        self.transformer = nn.Transformer(
            d_model=d_model,
            nhead=nhead,
            num_encoder_layers=num_enc_layers,
            num_decoder_layers=num_dec_layers,
            dim_feedforward=dim_feedforward,
            dropout=dropout,
            batch_first=True,
            norm_first=True,
        )
        self.fc_out = nn.Linear(d_model, tgt_vocab_size)

    def make_src_padding_mask(self, src):
        return src == self.pad_idx

    def make_tgt_padding_mask(self, tgt):
        return tgt == self.pad_idx

    def make_causal_mask(self, tgt_len: int, device: torch.device) -> torch.Tensor:
        return torch.triu(torch.ones(tgt_len, tgt_len, device=device), diagonal=1).bool()

    def encode(self, src: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        src_pad_mask = self.make_src_padding_mask(src)
        src_emb = self.pos_enc(self.src_embed(src) * math.sqrt(self.d_model))
        memory = self.transformer.encoder(src_emb, src_key_padding_mask=src_pad_mask)
        return memory, src_pad_mask

    def decode(
        self, tgt: torch.Tensor, memory: torch.Tensor, src_pad_mask: torch.Tensor
    ) -> torch.Tensor:
        tgt_len = tgt.size(1)
        causal_mask = self.make_causal_mask(tgt_len, tgt.device)
        tgt_pad_mask = self.make_tgt_padding_mask(tgt)
        tgt_emb = self.pos_enc(self.tgt_embed(tgt) * math.sqrt(self.d_model))
        out = self.transformer.decoder(
            tgt_emb,
            memory,
            tgt_mask=causal_mask,
            tgt_key_padding_mask=tgt_pad_mask,
            memory_key_padding_mask=src_pad_mask,
        )
        return self.fc_out(out)

    def forward(self, src: torch.Tensor, tgt: torch.Tensor) -> torch.Tensor:
        memory, src_pad_mask = self.encode(src)
        return self.decode(tgt[:, :-1], memory, src_pad_mask)

    def count_parameters(self) -> int:
        return sum(p.numel() for p in self.parameters() if p.requires_grad)
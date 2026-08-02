import torch

from config import Config
from vocab import Vocabulary
from model import TranslatorTransformer
from decoder import BeamSearchDecoder

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

Config.make_dirs()

src_vocab = Vocabulary.load(Config.VOCAB_SRC_PATH)
tgt_vocab = Vocabulary.load(Config.VOCAB_TGT_PATH)

model = TranslatorTransformer(
    src_vocab_size=src_vocab.size,
    tgt_vocab_size=tgt_vocab.size,
    d_model=Config.D_MODEL,
    nhead=Config.N_HEADS,
    num_enc_layers=Config.N_ENC_LAYERS,
    num_dec_layers=Config.N_DEC_LAYERS,
    dim_feedforward=Config.D_FF,
    dropout=Config.DROPOUT,
    max_pos_enc=Config.MAX_POS_ENC,
    pad_idx=Vocabulary.PAD_IDX,
).to(DEVICE)

model.load_state_dict(torch.load(Config.MODEL_CKPT_PATH, map_location=DEVICE))
model.eval()

decoder = BeamSearchDecoder(
    model=model,
    src_vocab=src_vocab,
    tgt_vocab=tgt_vocab,
    device=DEVICE,
    beam_size=Config.BEAM_SIZE,
    temperature=Config.TEMPERATURE,
    length_penalty=Config.LENGTH_PENALTY,
    max_len=Config.MAX_DECODE_LEN,
)


def translate(odia_text: str) -> str:
    """Translate a single Odia sentence into Hindi."""
    return decoder.translate(odia_text)
import os


class Config:
    """Config: All hyper-parameter values"""

    MODEL_DIR = os.getenv("MODEL_DIR", "./model")
    CKPT_DIR = os.getenv("CKPT_DIR", "./checkpoints")

    VOCAB_SRC_PATH = os.getenv("VOCAB_SRC_PATH", "./vocab/vocab_odia.pkl")
    VOCAB_TGT_PATH = os.getenv("VOCAB_TGT_PATH", "./vocab/vocab_hindi.pkl")
    MODEL_CKPT_PATH = os.getenv("MODEL_CKPT_PATH", "./model/best_model.pt")

    SRC_LANG = "or"
    TGT_LANG = "hi"

    MIN_LEN = 2
    MAX_LEN = 50
    REMOVE_ENG_WORDS = True

    SRC_VOCAB_SIZE = 40000
    TGT_VOCAB_SIZE = 40000
    MIN_FREQ = 2

    PAD = "<pad>"
    SOS = "<sos>"
    EOS = "<eos>"
    UNK = "<unk>"

    D_MODEL = 256
    N_HEADS = 8
    N_ENC_LAYERS = 4
    N_DEC_LAYERS = 4
    D_FF = 1024
    DROPOUT = 0.3
    MAX_POS_ENC = 512

    USE_AMP = True

    BEAM_SIZE = 5
    TEMPERATURE = 1.0
    LENGTH_PENALTY = 1.0
    MAX_DECODE_LEN = 50

    @classmethod
    def make_dirs(cls):
        for d in [cls.MODEL_DIR, cls.CKPT_DIR]:
            os.makedirs(d, exist_ok=True)
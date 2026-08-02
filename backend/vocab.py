import pickle
from typing import Dict, List

from config import Config


class Vocabulary:
    PAD_IDX = 0
    SOS_IDX = 1
    EOS_IDX = 2
    UNK_IDX = 3

    def __init__(self, name: str):
        self.name = name
        self.token2id: Dict[str, int] = {
            Config.PAD: self.PAD_IDX,
            Config.SOS: self.SOS_IDX,
            Config.EOS: self.EOS_IDX,
            Config.UNK: self.UNK_IDX,
        }
        self.id2token: Dict[int, str] = {v: k for k, v in self.token2id.items()}
        self.freq = {}

    @property
    def size(self) -> int:
        return len(self.token2id)

    def encode(self, sentence: str, add_special: bool = True) -> List[int]:
        ids = [self.token2id.get(tok, self.UNK_IDX) for tok in sentence.split()]
        if add_special:
            ids = [self.SOS_IDX] + ids + [self.EOS_IDX]
        return ids

    def decode(self, ids: List[int], skip_special: bool = True) -> str:
        skip = {self.PAD_IDX, self.SOS_IDX, self.EOS_IDX} if skip_special else set()
        tokens = [self.id2token.get(i, Config.UNK) for i in ids if i not in skip]
        return " ".join(tokens)

    @classmethod
    def load(cls, path: str) -> "Vocabulary":
        with open(path, "rb") as f:
            data = pickle.load(f)
        v = cls(data["name"])
        v.token2id = data["token2id"]
        v.id2token = data["id2token"]
        v.freq = data["freq"]
        return v
import re
import html
import unicodedata


SCRIPT_RANGES = {
    "or": [0x0B00, 0x0B7F],
    "hi": [0x0900, 0x097F],
    "bn": [0x0980, 0x09FF],
    "ta": [0x0B80, 0x0BFF],
    "te": [0x0C00, 0x0C7F],
    "kn": [0x0C80, 0x0CFF],
    "ml": [0x0D00, 0x0D7F],
    "gu": [0x0A80, 0x0AFF],
    "pa": [0x0A00, 0x0A7F],
}

DANDA = 0x0964
DOUBLE_DANDA = 0x0965
DANDA_CHAR = chr(DANDA)
DOUBLE_DANDA_CHAR = chr(DOUBLE_DANDA)

ODIA_NUMERALS_RANGE = (0x0B66, 0x0B6F)
ODIA_HALANTA = 0x0B4D
ODIA_ANUSVARA = 0x0B02
ODIA_VISARGA = 0x0B03

HINDI_NUMERALS_RANGE = (0x0966, 0x096F)
HINDI_HALANTA = 0x094D
HINDI_NUKTA = 0x093C


class ScriptUtils:
    """Utility functions for Indic script character classification."""

    @staticmethod
    def get_offset(char: str, lang: str) -> int:
        if lang not in SCRIPT_RANGES:
            return -1
        return ord(char) - SCRIPT_RANGES[lang][0]

    @staticmethod
    def is_in_script(char: str, lang: str) -> bool:
        if lang not in SCRIPT_RANGES:
            return False
        lo, hi = SCRIPT_RANGES[lang]
        cp = ord(char)
        return (lo <= cp <= hi) or cp == DANDA or cp == DOUBLE_DANDA

    @staticmethod
    def is_odia_char(char: str) -> bool:
        cp = ord(char)
        return 0x0B00 <= cp <= 0x0B7F

    @staticmethod
    def is_hindi_char(char: str) -> bool:
        cp = ord(char)
        return 0x0900 <= cp <= 0x097F

    @staticmethod
    def is_latin_char(char: str) -> bool:
        cp = ord(char)
        return (0x0041 <= cp <= 0x005A) or (0x0061 <= cp <= 0x007A)

    @staticmethod
    def is_digit(char: str) -> bool:
        cp = ord(char)
        return (
            (0x0030 <= cp <= 0x0039)
            or (ODIA_NUMERALS_RANGE[0] <= cp <= ODIA_NUMERALS_RANGE[1])
            or (HINDI_NUMERALS_RANGE[0] <= cp <= HINDI_NUMERALS_RANGE[1])
        )

    @staticmethod
    def odia_numeral_to_ascii(text: str) -> str:
        result = []
        for ch in text:
            cp = ord(ch)
            if ODIA_NUMERALS_RANGE[0] <= cp <= ODIA_NUMERALS_RANGE[1]:
                result.append(str(cp - ODIA_NUMERALS_RANGE[0]))
            else:
                result.append(ch)
        return "".join(result)

    @staticmethod
    def hindi_numeral_to_ascii(text: str) -> str:
        result = []
        for ch in text:
            cp = ord(ch)
            if HINDI_NUMERALS_RANGE[0] <= cp <= HINDI_NUMERALS_RANGE[1]:
                result.append(str(cp - HINDI_NUMERALS_RANGE[0]))
            else:
                result.append(ch)
        return "".join(result)


class TextCleaner:
    """Comprehensive text cleaner for Indic language (Odia / Hindi) corpora."""

    _RE_HTML_TAG = re.compile(r"<[^>]+>")
    _RE_HTML_ENTITY = re.compile(r"&[a-zA-Z0-9#]+;")
    _RE_URL = re.compile(r"https?://\S+|www\.\S+")
    _RE_EMAIL = re.compile(r"\S+@\S+\.\S+")
    _RE_HASHTAG = re.compile(r"#\w+")
    _RE_MENTION = re.compile(r"@\w+")
    _RE_MULTI_SPACE = re.compile(r"[ \t]+")
    _RE_MULTI_NL = re.compile(r"\n{2,}")
    _RE_ENG_WORD = re.compile(r"\b[A-Za-z]{2,}\b")
    _RE_PURE_ASCII = re.compile(r"^[\x00-\x7F]+$")
    _RE_PUNCT_NORM = re.compile(r"[!?]+")
    _RE_DANDA = re.compile(r"[।\|]+")
    _RE_DOUBLE_DANDA = re.compile(r"॥+")
    _RE_LONE_DIGIT = re.compile(r"^\d+$")
    _RE_QUOTES = re.compile(r'["""„‟«»]')

    def __init__(
        self,
        lang: str,
        remove_eng_words: bool = True,
        normalize_dandas: bool = True,
        keep_numerals: bool = True,
    ):
        self.lang = lang
        self.remove_eng_words = remove_eng_words
        self.normalize_dandas = normalize_dandas
        self.keep_numerals = keep_numerals
        self._is_script_char = (
            ScriptUtils.is_odia_char if lang == "or" else ScriptUtils.is_hindi_char
        )

    def remove_html(self, text: str) -> str:
        text = self._RE_HTML_TAG.sub(" ", text)
        text = html.unescape(text)
        text = self._RE_HTML_ENTITY.sub(" ", text)
        return text

    def normalize_unicode(self, text: str) -> str:
        return unicodedata.normalize("NFC", text)

    def remove_noise(self, text: str) -> str:
        text = self._RE_URL.sub(" ", text)
        text = self._RE_EMAIL.sub(" ", text)
        text = self._RE_HASHTAG.sub(" ", text)
        text = self._RE_MENTION.sub(" ", text)
        text = self._RE_QUOTES.sub(" ", text)
        return text

    def handle_dandas(self, text: str) -> str:
        if not self.normalize_dandas:
            return text
        text = re.sub(r"\|", "।", text)
        text = self._RE_DOUBLE_DANDA.sub("॥", text)
        text = self._RE_DANDA.sub("।", text)
        text = re.sub(r"([^\s])([।॥])", r"\1 \2", text)
        text = re.sub(r"([।॥])([^\s])", r"\1 \2", text)
        text = text.replace("।", ".").replace("॥", ".")
        return text

    def remove_english_words(self, text: str) -> str:
        if not self.remove_eng_words:
            return text
        text = self._RE_ENG_WORD.sub(" ", text)
        text = re.sub(r"\b[A-Za-z]\b", " ", text)
        return text

    def remove_invalid_chars(self, text: str) -> str:
        result = []
        for ch in text:
            cp = ord(ch)
            keep = (
                self._is_script_char(ch)
                or ch in " .,?!()'-:;"
                or ch.isdigit()
                or cp == DANDA
                or cp == DOUBLE_DANDA
                or ch in "।॥"
                or ch == "\n"
            )
            if keep:
                result.append(ch)
        return "".join(result)

    def normalize_whitespace(self, text: str) -> str:
        text = self._RE_MULTI_SPACE.sub(" ", text)
        return text.strip()

    def normalize_punctuation(self, text: str) -> str:
        text = self._RE_PUNCT_NORM.sub(lambda m: m.group(0)[0], text)
        return text

    def clean(self, text: str) -> str:
        if not isinstance(text, str) or not text.strip():
            return ""
        text = self.remove_html(text)
        text = self.normalize_unicode(text)
        text = self.remove_noise(text)
        text = self.handle_dandas(text)
        text = self.remove_english_words(text)
        text = self.remove_invalid_chars(text)
        text = self.normalize_punctuation(text)
        text = self.normalize_whitespace(text)
        return text
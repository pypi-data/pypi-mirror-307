from fasttext.FastText import _FastText
import json
from collections import defaultdict
import string
import re
import unicodedata
from .blocks import unicodeBlock
from haruka_parser.dictionary.language import FastTextLangeuageList


# def _makeNonAlphaRe():
#     nonAlpha = ["[^"]
#     for i in range(sys.maxunicode):
#         c = chr(i)
#         if c.isalpha():
#             nonAlpha.append(c)
#     nonAlpha.append("]")
#     nonAlpha = "".join(nonAlpha)
#     return re.compile(nonAlpha)


# nonAlphaRe = _makeNonAlphaRe()
spaceRe = re.compile("\s+", re.UNICODE)
PUNCTUATION = string.punctuation
PUNCTUATION += "0123456789！？。＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏."
PUNCTUATION = re.escape(string.punctuation)
nonAlphaRe = re.compile(f"[{PUNCTUATION}]")

# BASIC_LATIN = "en ceb ha so tlh id haw la sw eu nr nso zu xh ss st tn ts".split()
# EXTENDED_LATIN = "cs af pl hr ro sk sl tr hu az et sq ca es fr de nl it da is nb sv fi lv pt ve lt tl cy".split()
# ALL_LATIN = BASIC_LATIN + EXTENDED_LATIN
# CYRILLIC = "ru uk kk uz mn sr mk bg ky".split()
# ARABIC = "ar fa ps ur".split()
# DEVANAGARI = "hi ne".split()

def _get_fasttext_langs(lang):
    return list(filter(lambda x: lang in x, FastTextLangeuageList))

ARABIC = _get_fasttext_langs("Arab")
CYRILLIC = _get_fasttext_langs("Cyrl")
DEVANAGARI = _get_fasttext_langs("Deva")
LATIN = _get_fasttext_langs("Latn")
CHINESE = _get_fasttext_langs("Hans") + _get_fasttext_langs("Hant")

SINGLETONS = [
    ("Armenian", _get_fasttext_langs("Armn")),
    ("Hebrew", _get_fasttext_langs("Hebr")),
    ("Bengali", _get_fasttext_langs("Beng")),
    ("Gurmukhi", _get_fasttext_langs("Guru")),
    ("Greek", _get_fasttext_langs("Grek")),
    ("Gujarati", _get_fasttext_langs("Gujr")),
    ("Oriya", "ori_Orya"),
    ("Tamil", _get_fasttext_langs("Taml")),
    ("Telugu", _get_fasttext_langs("Telu")),
    ("Kannada", _get_fasttext_langs("Knda")),
    ("Malayalam", _get_fasttext_langs("Mlym")),
    ("Sinhala", _get_fasttext_langs("Sinh")),
    ("Thai", _get_fasttext_langs("Thai")),
    ("Lao", _get_fasttext_langs("Laoo")),
    ("Tibetan", _get_fasttext_langs("Tibt")),
    ("Myanmar", _get_fasttext_langs("Mymr")),
    ("Georgian", _get_fasttext_langs("Geor")),
    ("Mongolian", "khk_Cyrl"),
    ("Khmer", _get_fasttext_langs("Khmr")),
]

PT = "pt_BR pt_PT".split()

UNKNOWN = "UNKNOWN"

def normalize(u):
    """Convert to normalized unicode.
    Remove non-alpha chars and compress runs of spaces.
    """
    u = unicodedata.normalize("NFC", u)
    # u = u.translate(str.maketrans("", "", PUNCTUATION))
    u = nonAlphaRe.sub(" ", u)
    u = spaceRe.sub(" ", u)
    u = u.strip()
    return u


def _identify(sample, scripts):
    res = []

    if len(sample) < 3:
        return res

    if "Chinese" in scripts:
        res.extend(CHINESE)

    if "Korea" in scripts:
        res.append("kor_Hang")

    if "Japanese" in scripts:
        res.append("jpn_Jpan")

    if "Cyrillic" in scripts:
        res.extend(CYRILLIC)

    if "Arabic" in scripts:
        res.extend(ARABIC)

    if "Devanagari" in scripts:
        res.extend(DEVANAGARI)

    # Try languages with unique scripts
    for blockName, langName in SINGLETONS:
        if blockName in scripts:
            res.extend(langName)

    if "Latin Extended Additional" in scripts:
        res.extend("vie_Latn")

    if "Extended Latin" in scripts or "Basic Latin" in scripts:
        res.extend(LATIN)

    return res


def find_runs(text):
    """Count the number of characters in each character block"""
    run_types = defaultdict(int)

    totalCount = 0

    for c in text:
        if c.isalpha():
            block = unicodeBlock(c)
            if block.endswith(" Supplement"):
                block = block[:-11]
            if "汉字" in block:
                run_types["Chinese"] += 1
                run_types["Japanese"] += 1
            elif "中日韩" in block:
                run_types["Chinese"] += 1
                run_types["Japanese"] += 1
                run_types["Korea"] += 1
            elif "康熙" in block or "注音" in block:
                run_types["Chinese"] += 1
            elif "平假名" in block or "片假名" in block:
                run_types["Japanese"] += 1
            elif "谚文" in block:
                run_types["Korea"] += 1
            elif "阿拉伯" in block:
                run_types["Arabic"] += 1
            else:
                run_types[block.split("|")[-1]] += 1
            totalCount += 1

    # import pprint
    # pprint.pprint(run_types)

    # return run types that used for 40% or more of the string
    # always return basic latin if found more than 15%
    # and extended additional latin if over 10% (for Vietnamese)
    relevant_runs = []
    for key, value in run_types.items():
        pct = (value * 100) / totalCount
        if pct >= 30:
            relevant_runs.append(key)
        elif key == "Basic Latin" and (pct >= 15):
            relevant_runs.append(key)
        elif key == "Latin Extended Additional" and (pct >= 10):
            relevant_runs.append(key)

    return relevant_runs


def guess_lang(text):
    # text = normalize(text)
    return _identify(text, find_runs(text))


def predict_language(ft_model, text):

    text = normalize(text)
    guess_lang_list = guess_lang(text)

    # If there is only one possibility to return directly (certainly not for Chinese)
    if len(guess_lang_list) == 1:
        return guess_lang_list[0]

    # text = text.replace("\n", " ").replace("\t", " ").strip()
    label = ft_model.predict(text, -1, threshold=0.1) # -1e6

    # If there are multiple guess possibilities, return the one with the highest score
    if len(guess_lang_list) > 1:
        for lang, score in zip(label[0], label[1]):
            lang = lang.split("__label__")[1]
            if score > 0.3 and lang in guess_lang_list:
                return lang

    # If there is no guess, return the one with the highest score; if there is a guess and no guess possibility is larger than 0.3, return unknown (expect to drop data with low confidence)
    if len(guess_lang_list) == 0:
        for lang, score in zip(label[0], label[1]):
            lang = lang.split("__label__")[1]
            if score > 0.65:
                return lang

    return "unknown"


if __name__ == "__main__":
    if "ft_model" not in globals():
        ft_model = _FastText(model_path="model.bin")

    for line in open("zho_Hans.00000000.jsonl").readlines():
        data = json.loads(line)
        content = "\n".join([i for i in data["texts"] if i])
        lang = predict_language(content)
        if lang != "zho_Hans":
            print(lang, normalize(content[:100]))

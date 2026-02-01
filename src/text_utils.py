import re

STOPWORDS = {
    "the", "is", "are", "a", "an", "of", "to", "with", "and",
    "or", "for", "in", "on", "does", "do", "this", "that"
}

NUMBER_WORDS = {
    "zero": "0",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
    "ten": "10"
}

def normalize_numbers(text: str) -> str:
    for word, digit in NUMBER_WORDS.items():
        text = re.sub(rf"\b{word}\b", digit, text)
    return text

def clean_text(text: str) -> str:
    text = text.lower().strip()
    text = normalize_numbers(text)
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text

def tokenize(text: str):
    words = re.findall(r"[a-z0-9]+", text.lower())
    return [
        w for w in words
        if (w not in STOPWORDS and len(w) > 2) or w.isdigit()
    ][:6]
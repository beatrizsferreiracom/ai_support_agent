import re

STOPWORDS = {
    "the", "is", "are", "a", "an", "of", "to", "with", "and",
    "or", "for", "in", "on", "does", "do", "this", "that",
    "it", "you", "your", "my"
}

def tokenize(text: str) -> list[str]:
    words = re.findall(r"[a-z0-9]+", text.lower())
    return [
        w for w in words
        if (w not in STOPWORDS and len(w) > 2) or w.isdigit()
    ][:6]
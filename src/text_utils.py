import re

STOPWORDS = {
    "the", "is", "are", "a", "an", "of", "to", "with", "and",
    "or", "for", "in", "on", "does", "do", "this", "that",
    "it", "you", "your", "my"
}

INTENT_TERMS = {
    # dimensions & weight
    "weight", "weigh",
    "size", "dimensions", "height", "width", "length",

    # electrical
    "voltage", "volt", "110v", "220v",
    "watt", "wattage", "power",

    # performance & operation
    "speed", "noise", "sound", "loud", "quiet",
    "temperature", "heat", "cool",
    "capacity", "range",

    # air & purification
    "air", "purify", "purification",
    "filter", "filters",
    "odor", "odors", "smell",
    "bacteria", "allergies", "dust",

    # energy & battery
    "battery", "batteries",
    "rechargeable", "charge",
    "wireless", "corded",

    # compatibility & usage
    "compatible", "fit", "use", "install",

    # materials & safety (when asked explicitly)
    "material", "plastic", "metal",
    "safe", "toxic",

    # connectivity (when applicable)
    "wifi", "bluetooth"
}

ATTRIBUTE_TERMS = {
    "plastic", "metal", "stainless", "rubber",
    "lightweight", "durable", "portable",
    "waterproof", "compact", "foldable"
}

def extract_intent_terms(text: str) -> set[str]:
    tokens = re.findall(r"[a-z0-9]+", text.lower())
    return {t for t in tokens if t in INTENT_TERMS}

def is_compatible(user_question: str, faq_question: str) -> bool:
    user_terms = extract_intent_terms(user_question)
    faq_terms = extract_intent_terms(faq_question)

    if not user_terms:
        return True

    return bool(user_terms & faq_terms)

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

def tokenize(text: str) -> list[str]:
    words = re.findall(r"[a-z0-9]+", text.lower())
    return [
        w for w in words
        if (w not in STOPWORDS and len(w) > 2) or w.isdigit()
    ][:6]
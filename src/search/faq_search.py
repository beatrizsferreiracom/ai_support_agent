from src.search.keyword_search import keyword_search
from src.search.embedding_search import search_embeddings
import re

CORE_TERMS = {
    "weight", "weigh",
    "voltage", "volt", "110v", "220v",
    "power", "watt",
    "size", "dimensions",
    "noise", "loud",
    "odor", "smell",
    "purify", "purification",
    "capacity"
}

def extract_core_terms(text: str):
    tokens = re.findall(r"[a-z0-9]+", text.lower())
    return {t for t in tokens if t in CORE_TERMS}

def is_compatible(user_question: str, faq_question: str) -> bool:
    user_terms = extract_core_terms(user_question)
    faq_terms = extract_core_terms(faq_question)

    if not user_terms:
        return True

    return bool(user_terms & faq_terms)

def search_faq(question: str, category: str, product=None, limit: int = 5):
    """
    Performs a hybrid FAQ search:
    1. Keyword-based search (fast, precise)
    2. Embedding-based search (semantic fallback)
    """

    keyword_results = keyword_search(
        question, category, product, limit
    )

    compatible = [
        r for r in keyword_results
        if is_compatible(question, r[2])
    ]

    if compatible:
        return compatible
    
    embedding_results = search_embeddings(
        question, category, product, limit
    )

    compatible_embeddings = [
        r for r in embedding_results
        if is_compatible(question, r[2])
    ]

    return compatible_embeddings
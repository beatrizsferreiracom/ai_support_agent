from src.search.keyword_search import keyword_search
from src.search.embedding_search import search_embeddings
from src.text_utils import is_compatible

def search_faq(question: str, category: str, product=None, limit: int = 5):
    """
    Performs a hybrid FAQ search:
    1. Keyword-based search (fast, precise)
    2. Embedding-based search (semantic fallback)
    """

    keyword_results = keyword_search(question, category, product, limit)

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
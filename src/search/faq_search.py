from src.search.keyword_search import keyword_search
from src.search.embedding_search import search_embeddings

def search_faq(question: str, category: str, product=None, limit: int = 5):

    results = []

    keyword_results = keyword_search(question, category, product, limit)

    for r in keyword_results:
        results.append({
            "source": "keyword",
            "product_id": r[0],
            "product_name": r[1],
            "question": r[2],
            "answer": r[3],
            "score": r[4]
        })

    embedding_results = search_embeddings(question, category, product, limit)

    for r in embedding_results:
        results.append({
            "source": "embedding",
            "product_id": r[0],
            "product_name": r[1],
            "question": r[2],
            "answer": r[3],
            "score": r[5]
        })

    return results[:limit]
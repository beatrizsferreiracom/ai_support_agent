from langchain.tools import tool
from src.search.faq_search import search_faq

@tool("Search FAQ Database")
def handle_question(question: str, category: str, product: str) -> dict:
    """
    Searches the FAQ database for a specific product.
    """

    rows = search_faq(question, category, product)

    if not rows:
        return {"type": "NO_RESULTS"}

    return {
        "type": "EVIDENCE",
        "question": question,
        "candidates": [
            {
                "faq_question": r["question"],
                "faq_answer": r["answer"],
                "source": r["source"]
            }
            for r in rows
        ]
    }
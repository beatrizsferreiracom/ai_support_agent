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
    
    strong = [r for r in rows if r["compatibility"] == "STRONG"]

    if strong:
        best = strong[0]
        return {
            "type": "ANSWER",
            "confidence": "HIGH",
            "answer": best["answer"],
            "matched_question": best["question"]
        }
    
    best = rows[0]
    return{
        "type": "PARTIAL",
        "confidence": "LOW",
        "answer": best["answer"],
        "matched_question": best["question"]
    }
from langchain.tools import tool
from src.search.faq_search import search_faq

@tool("Search FAQ Database")
def handle_question(question: str, category: str, product: str) -> str:
    """
    Searches the FAQ database for a specific product.
    """

    rows = search_faq(question, category, product)

    if not rows:
        return "NO_RESULTS"

    best = rows[0]
    return best[3]
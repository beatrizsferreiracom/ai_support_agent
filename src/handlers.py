from langchain.tools import tool
from src.tools import search_faq
from src.resolver import resolve_results

@tool("Search FAQ Database")
def handle_question(question: str, category: str) -> str:
    """
    Searches the internal FAQ database and returns the best possible answer.
    """

    question_clean = question.lower().strip()

    rows = search_faq(question_clean, category)

    if not rows:
        keywords = " ".join(question_clean.split()[:5])
        rows = search_faq(keywords, category)

    result = resolve_results(rows)

    if result["type"] == "NO_RESULTS":
        return "The information was not found in the FAQ database."

    if result["type"] == "ANSWER":
        return result["answer"]

    if result["type"] == "DISAMBIGUATE":
        options_text = "\n".join(
            f"{i+1}. {opt['product_hint']}"
            for i, opt in enumerate(result["options"])
        )

        return (
            "I found information for more than one possible match.\n"
            "Please reply with the number of the option you mean:\n\n"
            f"{options_text}"
        )

    return "The information was not found in the FAQ database."
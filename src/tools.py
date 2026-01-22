import duckdb
import os
import re
from langchain.tools import tool

STOPWORDS = {
    "the","is","it","this","that","can","be","used","with","for",
    "to","of","and","or","a","an","on","over","how","does","do",
    "im","i","am","are","was","were"
}

def extract_terms(text: str) -> list[str]:
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    words = [w for w in text.split() if w not in STOPWORDS and len(w) > 2]
    return list(dict.fromkeys(words))[:6]  # mantém ordem, limita OR

class FAQTools:

    @tool("Search FAQ Database")
    def search_faq(category: str, query: str):
        """
        Search the FAQ database for relevant product questions and answers.

        Inputs:
        - category: Product category (e.g., Appliances)
        - query: User question in natural language

        Returns:
        - A list of related FAQ entries (product_id, question, answer)
        - Or NO_RESULTS if nothing relevant is found
        - Or TOOL_ERROR if a database error occurs
        """
        db_path = os.path.join("data", "faq_dataset.db")
        terms = extract_terms(query)

        if not terms:
            return "NO_RESULTS"

        where_terms = " OR ".join(
            [f"question ILIKE '%{t}%' OR answer ILIKE '%{t}%'" for t in terms]
        )

        sql = f"""
        SELECT product_id, question, answer
        FROM faqs
        WHERE category = ?
        AND ({where_terms})
        LIMIT 30;
        """

        try:
            con = duckdb.connect(db_path, read_only=True)
            rows = con.execute(sql, [category]).fetchall()
            con.close()

            if not rows:
                return "NO_RESULTS"

            return "\n---\n".join(
                f"Product ID: {pid}\nQ: {q}\nA: {a}"
                for pid, q, a in rows
            )

        except Exception as e:
            return f"TOOL_ERROR: {e}"
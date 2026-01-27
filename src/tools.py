import duckdb
import re

DB_PATH = "data/faq_dataset.duckdb"

STOPWORDS = {
    "the", "is", "are", "a", "an", "of", "to", "with", "and",
    "or", "for", "in", "on", "does", "do", "this", "that"
}

VAGUE_KEYWORDS = {
    "how", "much", "many", "weigh", "weight", "does", "do"
}


def tokenize(text: str):
    words = re.findall(r"[a-z0-9]+", text.lower())
    return [
        w for w in words
        if (w not in STOPWORDS and len(w) > 2) or w.isdigit()
    ][:6]


def is_vague_question(tokens):
    """
    Vague question:
    - few tokens
    - or just generic words
    """
    if len(tokens) <= 2:
        return True

    meaningful = [t for t in tokens if t not in VAGUE_KEYWORDS]
    return len(meaningful) == 0


def search_faq(query: str, category: str, limit: int = 20):
    query_clean = query.lower().strip()

    if query_clean.startswith("please reply with"):
        return []

    tokens = tokenize(query_clean)

    if not tokens:
        return []

    if is_vague_question(tokens):
        return []

    question_len = len(query)

    like_clauses = " OR ".join(
        [f"question LIKE '%{t}%'" for t in tokens]
    )

    score_expr = " + ".join(
        [f"(question LIKE '%{t}%')::INT" for t in tokens]
    )

    sql = f"""
    SELECT
        product_id,
        question,
        answer,
        question AS product_hint,
        ({score_expr}) AS score
    FROM faqs
    WHERE category = ?
      AND ({like_clauses})
    ORDER BY
        score DESC,
        abs(length(question) - ?) ASC,
        length(question) ASC
    LIMIT ?
    """

    con = duckdb.connect(DB_PATH)
    results = con.execute(
        sql,
        [category, question_len, limit]
    ).fetchall()
    con.close()

    return results
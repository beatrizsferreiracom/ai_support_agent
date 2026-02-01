import duckdb
from src.text_utils import tokenize

DB_PATH = "data/faq.duckdb"

def keyword_search(question, category, product=None, limit=10):
    tokens = tokenize(question)
    if not tokens:
        return []

    like = " OR ".join([f"question LIKE '%{t}%'" for t in tokens])
    score = " + ".join([f"(question LIKE '%{t}%')::INT" for t in tokens])

    sql = f"""
    SELECT product_id, product_name, question, answer, ({score}) AS score
    FROM faq
    WHERE category = ?
      AND ({like})
    """

    params = [category]

    if product:
        sql += " AND product_name = ?"
        params.append(product)

    sql += " ORDER BY score DESC LIMIT ?"
    params.append(limit)

    con = duckdb.connect(DB_PATH)
    rows = con.execute(sql, params).fetchall()
    con.close()

    return rows
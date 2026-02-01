import duckdb

DB_PATH = "data/faq.duckdb"

def get_categories():
    con = duckdb.connect(DB_PATH)
    rows = con.execute(
        "SELECT DISTINCT category FROM faq ORDER BY category"
    ).fetchall()
    con.close()
    return [r[0] for r in rows]


def get_products_by_category(category: str):
    con = duckdb.connect(DB_PATH)
    rows = con.execute(
        """
        SELECT DISTINCT product_name
        FROM faq
        WHERE category = ?
        ORDER BY product_name
        """,
        [category]
    ).fetchall()
    con.close()
    return [r[0] for r in rows]
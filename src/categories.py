import duckdb

DB_PATH = "data/faq_dataset.duckdb"

def load_categories():
    try:
        con = duckdb.connect(DB_PATH)
        rows = con.execute(
            """
            SELECT DISTINCT category
            FROM faqs
            ORDER BY category
            """
        ).fetchall()
        con.close()

        return [r[0] for r in rows if r[0]]

    except Exception:
        return []
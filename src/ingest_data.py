import duckdb
import os

DB_PATH = os.path.join("data", "faq_dataset.duckdb")
CSV_PATH = os.path.join("data", "faq_dataset.csv")

def ingest_data():
    os.makedirs("data", exist_ok=True)

    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    con = duckdb.connect(DB_PATH)

    print("Creating table...")
    con.sql("""
        CREATE TABLE faqs (
            product_id VARCHAR,
            question   VARCHAR,
            answer     VARCHAR,
            category   VARCHAR
        )
    """)

    print("Loading CSV...")
    con.sql(f"""
        INSERT INTO faqs
        SELECT
            product_id,
            lower(question) AS question,
            answer,
            category
        FROM read_csv(
            '{CSV_PATH}',
            all_varchar=True,
            header=True,
            ignore_errors=True
        )
        WHERE question IS NOT NULL
          AND answer IS NOT NULL
          AND length(question) > 5
          AND length(answer) > 5
    """)

    print("Installing FTS...")
    con.sql("INSTALL fts; LOAD fts;")

    print("Creating FTS index...")
    con.sql("""
        PRAGMA create_fts_index(
            'faqs',
            'question',
            'answer'
        )
    """)

    rows = con.sql("SELECT COUNT(*) FROM faqs").fetchone()[0]
    print(f"Database ready with {rows} rows")

    con.close()

if __name__ == "__main__":
    ingest_data()
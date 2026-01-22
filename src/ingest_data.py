import duckdb
import os

def ingest_data():
    db_path = os.path.join("data", "faq_dataset.db")
    csv_path = os.path.join("data", "faq_dataset.csv")

    if os.path.exists(db_path):
        os.remove(db_path)

    con = duckdb.connect(db_path)

    con.sql("""
        CREATE TABLE faqs (
            product_id VARCHAR,
            question   VARCHAR,
            answer     VARCHAR,
            category   VARCHAR
        )
    """)

    con.sql(f"""
        INSERT INTO faqs
        SELECT * FROM read_csv(
            '{csv_path}',
            all_varchar=True,
            header=True,
            ignore_errors=True
        )
    """)

    con.sql("INSTALL fts; LOAD fts;")
    con.sql("PRAGMA create_fts_index('faqs', 'question', 'answer')")

    rows = con.sql("SELECT COUNT(*) FROM faqs").fetchone()[0]
    print(f"Database ready with {rows} rows")

    con.close()

if __name__ == "__main__":
    ingest_data()
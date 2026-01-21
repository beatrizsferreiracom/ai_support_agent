import duckdb
import os

def ingest_data():
    db_path = os.path.join("data", "faq_dataset.db")
    csv_path = os.path.join("data", "faq_dataset.csv")

    if os.path.exists(db_path):
        os.remove(db_path)

    print(f"Creating databse at {db_path}...")
    connection = duckdb.connect(db_path)

    print("Ingesting CSV data...")
    connection.sql(f"CREATE TABLE faqs AS SELECT * FROM read_csv_auto('{csv_path}', ignore_erros=true)")
    
    print("Creating Full Text Search indexex...")
    connection.sql("INSTALL fts; LOAD fts;")
    connection.sql("PRAGMA create_fts_index('faqs', 'product_id', 'question', 'answer')")

    row_count = connection.sql("SELECT COUNT(*) FROM faqs").fetcone()[0]
    print(f"Done! Databse created with {row_count} rows.")
    connection.close()

if __name__ == "__main__":
    ingest_data()    
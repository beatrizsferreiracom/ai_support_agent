import os
import logging
import duckdb
import pandas as pd
import numpy as np
from src.search.embedding_search import embed

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
logging.getLogger("transformers").setLevel(logging.ERROR)

DB_PATH = "data/faq.duckdb"
CSV_PATH = "data/faq_dataset_curated.csv"

def ingest_data():
    
    try:
        df = pd.read_csv(CSV_PATH, on_bad_lines='skip', quotechar='"')
    except Exception as e:
        print(f"Error: {e}")
        return
    
    df["embedding"] = df["question"].apply(lambda x: embed(str(x)))

    df = df[["product_id", "product_name", "category", "question", "answer", "embedding"]]

    con = duckdb.connect(DB_PATH)

    con.execute("""
    CREATE TABLE IF NOT EXISTS faq (
        product_id TEXT,
        product_name TEXT,
        category TEXT,
        question TEXT,
        answer TEXT,
        embedding DOUBLE[]
    )
    """)

    con.execute("DELETE FROM faq")

    con.execute("INSERT INTO faq SELECT * FROM df")

    con.close()
    print(f"✅ Embeddings ingested")

if __name__ == "__main__":
    ingest_data()
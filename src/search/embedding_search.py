import duckdb
import numpy as np
from sentence_transformers import SentenceTransformer

MODEL = SentenceTransformer("all-MiniLM-L6-v2")
DB_PATH = "data/faq.duckdb"

def embed(text: str):
    return MODEL.encode(text).tolist()

def cosine_similarity(a, b):
    a, b = np.array(a), np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def search_embeddings(question, category, product=None, limit=5):
    q_emb = embed(question)

    con = duckdb.connect(DB_PATH)

    if product:
        rows = con.execute("""
            SELECT product_id, product_name, question, answer, embedding
            FROM faq
            WHERE category = ?
                AND product_name = ?
        """, [category, product]).fetchall()
    else:
        rows = con.execute("""
            SELECT product_id, product_name, question, answer, embedding
            FROM faq
            WHERE category = ?
        """, [category]).fetchall()

    con.close()

    scored = []
    for r in rows:
        score = cosine_similarity(q_emb, r[4])
        scored.append((*r, score))

    scored.sort(key=lambda x: x[5], reverse=True)
    return scored[:limit]
import duckdb
import os
from langchain.tools import tool

class FAQTools:

    @tool("Search FAQ Database")
    def search_faq(category: str, query: str):
        """
        Useful to search for specific product questions and answer in the FAQ database.
        Always provide the 'category' (e.g., Appliances) and the user's 'query' or keywords.
        """
        db_path = os.path.join("data", "faq_database.db")

        try:
            connection = duckdb.connect(db_path, read_only = True)

            sql_query = """
            SELECT product_id, question, answer, score
            FROM (
                SELECT *, fts_main_faqs.match_bm25(product_id, question, answer, ?) AS score
                FROM faqs
                WHERE category = ?
            )
            WHERE score IS NOT NULL
            ORDER BY score DESC
            LIMIT 5;
            """   

            connection.sql("INSTALL fts; LOAD fts;")
            results = connection.execute(sql_query, [query, category]).fetchall()

            connection.close()

            if not results:
                return "No relevant FAQs found for this query in the specified category."
            
            formatted_results = ""
            for res in results: product_id, question, answer, score = res
            formatted_results += f"Product ID: {product_id}\nQ: {question}\nA: {answer}\n(Relevance: {score})\n\---n"

            return formatted_results
        
        except Exception as e:
            return f"Error querying database: {str(e)}"
from sentence_transformers import SentenceTransformer
import psycopg2
import numpy as np
from config import DB_CONFIG

model = SentenceTransformer("all-MiniLM-L6-v2")

def store_dataset_embeddings(dataset_name, description):
    """Store dataset embeddings in PostgreSQL, ensuring compatibility with the 'vector' type."""
    
    if not description:
        description = dataset_name  # Use dataset name if description is missing
    
    vector = model.encode(description).tolist()  # Convert to list (not bytea)

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    # Ensure table exists
    cur.execute("""
        CREATE TABLE IF NOT EXISTS dataset_embeddings (
            dataset_name TEXT PRIMARY KEY,
            embedding vector(384),  -- Ensure the vector size matches your embedding model
            last_updated TIMESTAMP DEFAULT NOW()
        )
    """)

    # Ensure the vector is stored as an explicit array
    vector_str = "[" + ",".join(map(str, vector)) + "]"  # Convert list to PostgreSQL vector format

    cur.execute("""
        INSERT INTO dataset_embeddings (dataset_name, embedding, last_updated)
        VALUES (%s, %s::vector, NOW())
        ON CONFLICT (dataset_name) DO UPDATE 
        SET embedding = EXCLUDED.embedding, last_updated = NOW()
    """, (dataset_name, vector_str))  # Ensure vector is inserted as a string

    conn.commit()
    cur.close()
    conn.close()

    print(f"✅ Stored embeddings for dataset: {dataset_name}")


def find_best_matching_dataset(user_query):
    """Find the most relevant dataset based on semantic similarity."""
    
    query_vector = model.encode(user_query).tolist()

    # Ensure query vector is properly formatted
    query_vector_str = "[" + ",".join(map(str, query_vector)) + "]"

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("""
        SELECT dataset_name, 1 - (embedding <=> %s::vector) AS similarity
        FROM dataset_embeddings
        ORDER BY similarity DESC
        LIMIT 1
    """, (query_vector_str,))  # Ensure vector is passed as a properly formatted string

    result = cur.fetchone()
    cur.close()
    conn.close()

    if result and result[1] > 0.5:  # Ensure similarity is above threshold
        print(f"✅ Best matching dataset: {result[0]} (Similarity: {result[1]:.2f})")
        return result[0]
    else:
        print("❌ No suitable dataset found.")
        return None
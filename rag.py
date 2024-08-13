from itertools import chain
import torch
from pgvector.psycopg import register_vector

from db import get_connection
from embedding import generate_embeddings


def get_retrieval_condition(query_embedding, threshold=0.7):
    # Convert query embedding to a string format for SQL query
    query_embedding_str = ",".join(map(str, query_embedding))

    # SQL condition for cosine similarity
    condition = f"(embeddings <=> '{query_embedding_str}') < {threshold} ORDER BY embeddings <=> '{query_embedding_str}'"
    return condition


def rag_query(tokenizer, model, device, query):
    # Generate query embedding
    query_embedding = generate_embeddings(
        tokenizer=tokenizer, model=model, device=device, text=query
    )[1]

    # Retrieve relevant embeddings from the database
    retrieval_condition = get_retrieval_condition(query_embedding)

    conn = get_connection()
    register_vector(conn)
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT doc_fragment FROM embeddings WHERE {retrieval_condition} LIMIT 5"
    )
    retrieved = cursor.fetchall()

    rag_query = ' '.join([row[0] for row in retrieved])

    return rag_query
from db import VectorDB

def get_retrieval_condition(query_embedding, threshold=0.7):
    # Convert query embedding to a string format for SQL query
    query_embedding_str = ",".join(map(str, query_embedding))

    # SQL condition for cosine similarity
    condition = f"(embeddings <=> '{query_embedding_str}') < {threshold} ORDER BY embeddings <=> '{query_embedding_str}'"
    return condition


def rag_query(tokenizer, model, device, query):
    db = VectorDB()
    conn = db.connect_langchain()
    results = conn.similarity_search(query=query,k=10)

    rag_query = ' '.join([doc.page_content for doc in results])

    return rag_query

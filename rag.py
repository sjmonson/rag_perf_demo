from db import VectorDB

def rag_query(query):
    db = VectorDB()
    conn = db.connect_langchain()
    results = conn.similarity_search(query=query,k=10)

    rag_query = ' '.join([doc.page_content for doc in results])

    return rag_query

from app.services.embedding_service import get_embedding

# def retrieve_chunks(question, vector_store, top_k=3):

#     query_embedding = get_embedding(question)

#     # results = vector_store.search(query_embedding, top_k)
#     results = vector_store.similarity_search_by_vector(query_embedding, top_k)

#     return results

def retrieve_chunks(question, vector_store, top_k=3):

    query_embedding = get_embedding(question)

    import numpy as np

    query_embedding = np.array(query_embedding)

    if query_embedding.ndim == 1:
        query_embedding = query_embedding.reshape(1, -1)

    results = vector_store.search(query_embedding, top_k)

    return results
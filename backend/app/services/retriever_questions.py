from app.services.vector_store import index, question_map
from app.services.embedding_service import get_embedding
import numpy as np

def retrieve_questions(text, top_k=22):

    query_embedding = get_embedding(text)

    query_embedding = np.array(query_embedding)

    # Ensure 2D
    if query_embedding.ndim == 1:
        query_embedding = query_embedding.reshape(1, -1)

    D, I = index.search(np.array(query_embedding), top_k)

    return [question_map[i] for i in I[0]]
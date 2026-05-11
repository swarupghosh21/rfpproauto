from app.services.embedding_service import get_embedding
from app.services.vector_store_rfp import VectorStore

def build_rfp_index(chunks):

    embeddings = [get_embedding(chunk) for chunk in chunks]

    dim = len(embeddings[0])

    store = VectorStore(dim)
    store.add(embeddings, chunks)

    return store
import faiss
import numpy as np
from app.services.embedding_service import get_embedding
from app.utils.prompts import QUESTIONS

# Create embeddings
embeddings = [get_embedding(q) for q in QUESTIONS]

dimension = len(embeddings[0])

index = faiss.IndexFlatL2(dimension)

index.add(np.array(embeddings))

# Map index → question
question_map = {i: q for i, q in enumerate(QUESTIONS)}
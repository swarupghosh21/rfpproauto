def retrieve_relevant_chunks(question, chunks, top_k=3):
    # MVP: simple keyword match
    scored = []

    for chunk in chunks:
        score = sum(word in chunk.lower() for word in question.lower().split())
        scored.append((score, chunk))

    scored.sort(reverse=True)
    return [c[1] for c in scored[:top_k]]
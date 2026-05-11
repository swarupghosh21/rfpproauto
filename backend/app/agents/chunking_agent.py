from app.services.chunker import chunk_text

def chunking_agent(state):
    chunks = chunk_text(state["text"])
    return {**state, "chunks": chunks}
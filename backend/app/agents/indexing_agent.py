from app.services.rfp_indexer import build_rfp_index

def indexing_agent(state):

    store = build_rfp_index(state["chunks"])

    return {**state, "vector_store": store}
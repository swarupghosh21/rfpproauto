from app.services.prebid_service import generate_queries

def prebid_agent(state):
    queries = generate_queries(state["text"])
    return {**state, "queries": queries}
def coordinator_agent(state):

    if not state.get("text"):
        return {**state, "next_task": "intake"}

    if not state.get("chunks"):
        return {**state, "next_task": "chunking"}
    
    if not state.get("vector_store"):
        return {**state, "next_task": "indexing"}

    if not state.get("answers"):
        return {**state, "next_task": "qa"}

    if not state.get("queries"):
        return {**state, "next_task": "prebid"}

    return {**state, "next_task": "end", "status": "done"}
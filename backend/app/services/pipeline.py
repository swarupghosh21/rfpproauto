from app.graph.graph import build_graph

graph = build_graph()

async def run_pipeline(filename):

    state = {
        "filename": filename,
        "text": "",
        "chunks": [],
        "answers": [],
        "queries": [],
        "next_task": None,
        "status": "running"
    }

    result = await graph.ainvoke(state)

    return result
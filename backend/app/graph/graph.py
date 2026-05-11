from langgraph.graph import StateGraph
from app.graph.state import RFPState

from app.agents.coordinator import coordinator_agent
from app.agents.delegator import delegator_agent
from app.agents.intake_agent import intake_agent
from app.agents.chunking_agent import chunking_agent
from app.agents.indexing_agent import indexing_agent
from app.agents.qa_agent import qa_agent
from app.agents.prebid_agent import prebid_agent
from app.agents.end_agent import end_agent

def build_graph():

    graph = StateGraph(RFPState)

    graph.add_node("coordinator", coordinator_agent)
    graph.add_node("delegator", delegator_agent)

    graph.add_node("intake", intake_agent)
    graph.add_node("chunking", chunking_agent)
    graph.add_node("indexing", indexing_agent)
    graph.add_node("qa", qa_agent)
    graph.add_node("prebid", prebid_agent)
    graph.add_node("end", end_agent)

    graph.set_entry_point("coordinator")

    graph.add_edge("coordinator", "delegator")

    graph.add_conditional_edges(
        "delegator",
        lambda state: state["next_task"],
        {
            "intake": "intake",
            "chunking": "chunking",
            "indexing": "indexing",
            "qa": "qa",
            "prebid": "prebid",
            "end": "end"
        }
    )

    graph.add_edge("intake", "coordinator")
    graph.add_edge("chunking", "coordinator")
    graph.add_edge("indexing", "coordinator")
    graph.add_edge("qa", "coordinator")
    graph.add_edge("prebid", "coordinator")

    return graph.compile()
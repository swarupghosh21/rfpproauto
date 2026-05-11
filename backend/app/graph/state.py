from typing import TypedDict, List, Optional

class RFPState(TypedDict):
    filename: str
    text: str
    chunks: List[str]
    vector_store: object
    answers: List[dict]
    queries: List[str]
    next_task: Optional[str]
    status: str
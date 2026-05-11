from fastapi import APIRouter
from app.services.pipeline import run_pipeline

router = APIRouter()

@router.post("/process/{filename}")
async def process_rfp(filename: str):
    result = await run_pipeline(filename)

    return {
        "answers": result["answers"],
        "prebid_queries": result["queries"]
    }
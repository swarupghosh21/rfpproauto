import sys
import os
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# Ensure the app directory is in the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db import SessionLocal
from app.agents.prebid_query_agent import PreBidQueryGeneratorAgent

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/generate-prebid1/{rfp_id}")
def generate_prebid_queries(rfp_id: str, db: Session = Depends(get_db)):
    agent = PreBidQueryGeneratorAgent(db)
    results = agent.generate_for_rfp(rfp_id)
    return results
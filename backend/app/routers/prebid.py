from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import logging

from app.db import SessionLocal
from app.agents.prebid_query_agent import PreBidQueryGeneratorAgent
router = APIRouter()

logger = logging.getLogger(__name__)
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/generate-prebid/{rfp_id}")
# def generate_prebid(rfp_id: str, db: Session = Depends(get_db)):

#     agent = PreBidQueryGeneratorAgent(db)

#     results = agent.generate_queries(rfp_id)

#     return results

def generate_prebid(rfp_id: str, db: Session = Depends(get_db)):
    """
    Generate pre-bid queries for the given rfp_id.
    Returns JSON result or raises HTTPException on error.
    """
    try:
        logger.info("generate_prebid called for rfp_id=%s", rfp_id)
        agent = PreBidQueryGeneratorAgent(db)

        results = agent.generate_queries(rfp_id)

        if results is None:
            logger.warning("No results returned for rfp_id=%s", rfp_id)
            raise HTTPException(status_code=404, detail="No prebid content generated")

        # Optionally validate serializability here
        return results

    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Error generating prebid for rfp_id=%s", rfp_id)
        raise HTTPException(status_code=500, detail=f"Server error: {str(exc)}")
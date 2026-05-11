import shutil
from fastapi import APIRouter, UploadFile, Depends
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models import RFP, RFPSection
from app.parser import parse_document
from app.section_extractor import extract_sections

router = APIRouter()

UPLOAD_DIR = "uploads"


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/upload-rfp")
async def upload_rfp(file: UploadFile, db: Session = Depends(get_db)):

    file_path = f"{UPLOAD_DIR}/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    rfp = RFP(title=file.filename, file_path=file_path)

    db.add(rfp)
    db.commit()
    db.refresh(rfp)

    # parse document
    text = parse_document(file_path)

    # extract sections
    sections = extract_sections(text)

    # store sections
    for sec in sections:
        section_obj = RFPSection(
            rfp_id=rfp.rfp_id,
            section_title=sec["title"],
            content=sec["content"],
            page_number=0
        )

        db.add(section_obj)

    db.commit()

    return {
        "rfp_id": str(rfp.rfp_id),
        "sections_detected": len(sections)
    }
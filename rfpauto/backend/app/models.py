import uuid
from sqlalchemy import Column, String, Text, Integer
from sqlalchemy.dialects.postgresql import UUID
from .db import Base

class RFP(Base):
    __tablename__ = "rfps"

    rfp_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    file_path = Column(String)


class RFPSection(Base):
    __tablename__ = "rfp_sections"

    section_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    rfp_id = Column(UUID(as_uuid=True))
    section_title = Column(String)
    content = Column(Text)
    page_number = Column(Integer)
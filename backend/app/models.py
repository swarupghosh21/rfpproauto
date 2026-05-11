import uuid
from sqlalchemy import UUID, Column, String, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base


class RFP(Base):
    __tablename__ = "rfps"

    rfp_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String)
    file_path = Column(String)

    sections = relationship("RFPSection", back_populates="rfp")


class RFPSection(Base):
    __tablename__ = "rfp_sections"

    section_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    rfp_id = Column(String, ForeignKey("rfps.rfp_id"))

    section_title = Column(String)
    content = Column(Text)
    page_number = Column(Integer)

    rfp = relationship("RFP", back_populates="sections")


class PreBidQuery(Base):
    __tablename__ = "pre_bid_queries"

    query_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    rfp_id = Column(UUID(as_uuid=True))
    page = Column(Integer)
    category = Column(String(100))
    identified_issue = Column(Text)
    suggested_query = Column(Text)
    severity = Column(String(20))

    # query_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    # query_text = Column(Text)
    # category = Column(String)
    


class RFPQueryAnswer(Base):
    __tablename__ = "rfp_query_answers"

    answer_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    rfp_id = Column(String)
    query_id = Column(String)

    answer_text = Column(Text)
    confidence_score = Column(Integer)
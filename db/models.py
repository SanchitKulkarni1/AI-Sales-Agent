from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

from sqlalchemy import (
    Column, Integer, Float, String,
    DateTime, ForeignKey, JSON, Text
)

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True)
    raw_data = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class LeadScore(Base):
    __tablename__ = "lead_scores"

    id = Column(Integer, primary_key=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False)

    rule_score = Column(Float, nullable=False)
    ml_score = Column(Float, nullable=False)
    final_score = Column(Float, nullable=False)
    tier = Column(String(10), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())


class LeadExplanation(Base):
    __tablename__ = "lead_explanations"

    id = Column(Integer, primary_key=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False)

    context = Column(JSON, nullable=False)
    explanation = Column(Text, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

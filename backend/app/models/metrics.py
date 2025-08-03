from sqlalchemy import Column, String, DateTime, Integer, Float, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from datetime import datetime

from app.core.database import Base

class EvaluationMetric(Base):
    __tablename__ = "evaluation_metrics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    query_id = Column(UUID(as_uuid=True), ForeignKey("queries.id"), nullable=False)
    response_id = Column(UUID(as_uuid=True), ForeignKey("responses.id"), nullable=False)
    
    # Similarity scores
    similarity_scores = Column(JSONB, default=dict)  # {provider: score}
    average_similarity = Column(Float)
    
    # Content quality metrics
    originality_score = Column(Float)  # 0.0 to 1.0
    factuality_score = Column(Float)   # 0.0 to 1.0
    readability_score = Column(Float)  # 0.0 to 1.0
    
    # Content analysis
    keyword_count = Column(Integer)
    keyword_list = Column(JSONB, default=list)
    tool_mentions = Column(JSONB, default=list)
    seo_terms = Column(JSONB, default=list)
    
    # Response characteristics
    response_length = Column(Integer)
    response_complexity = Column(Float)
    
    # Metadata
    analysis_version = Column(String(20), default="1.0")
    computed_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    query = relationship("Query", back_populates="metrics")
    response = relationship("Response", back_populates="metrics")
    
    def __repr__(self):
        return f"<EvaluationMetric(id={self.id}, query_id={self.query_id}, response_id={self.response_id})>"
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": str(self.id),
            "query_id": str(self.query_id),
            "response_id": str(self.response_id),
            "similarity_scores": self.similarity_scores,
            "average_similarity": self.average_similarity,
            "originality_score": self.originality_score,
            "factuality_score": self.factuality_score,
            "readability_score": self.readability_score,
            "keyword_count": self.keyword_count,
            "keyword_list": self.keyword_list,
            "tool_mentions": self.tool_mentions,
            "seo_terms": self.seo_terms,
            "response_length": self.response_length,
            "response_complexity": self.response_complexity,
            "analysis_version": self.analysis_version,
            "computed_at": self.computed_at.isoformat() if self.computed_at else None
        } 
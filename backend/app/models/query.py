from sqlalchemy import Column, String, Text, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from datetime import datetime

from app.core.database import Base

class Query(Base):
    __tablename__ = "queries"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    prompt = Column(Text, nullable=False)
    category = Column(String(100))
    tags = Column(JSONB, default=list)
    user_id = Column(String(100))
    status = Column(String(20), default="pending")  # pending, processing, completed, failed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    responses = relationship("Response", back_populates="query", cascade="all, delete-orphan")
    metrics = relationship("EvaluationMetric", back_populates="query", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Query(id={self.id}, prompt='{self.prompt[:50]}...', status='{self.status}')>"
    
    @property
    def response_count(self) -> int:
        """Get the number of responses for this query"""
        return len(self.responses) if self.responses else 0
    
    @property
    def is_complete(self) -> bool:
        """Check if query processing is complete"""
        return self.status in ["completed", "failed"]
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": str(self.id),
            "prompt": self.prompt,
            "category": self.category,
            "tags": self.tags,
            "user_id": self.user_id,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "response_count": self.response_count
        } 
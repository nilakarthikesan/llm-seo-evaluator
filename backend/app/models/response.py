from sqlalchemy import Column, String, Text, DateTime, Integer, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from datetime import datetime

from app.core.database import Base

class Response(Base):
    __tablename__ = "responses"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    query_id = Column(UUID(as_uuid=True), ForeignKey("queries.id"), nullable=False)
    provider = Column(String(50), nullable=False)  # openai, anthropic, perplexity, google
    model = Column(String(100), nullable=False)    # gpt-4, claude-3, etc.
    response_text = Column(Text, nullable=False)
    response_metadata = Column(JSONB, default=dict)
    tokens_used = Column(Integer)
    response_time_ms = Column(Integer)
    error_message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    query = relationship("Query", back_populates="responses")
    metrics = relationship("EvaluationMetric", back_populates="response", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Response(id={self.id}, provider='{self.provider}', model='{self.model}')>"
    
    @property
    def is_successful(self) -> bool:
        """Check if the response was successful"""
        return self.error_message is None
    
    @property
    def word_count(self) -> int:
        """Get word count of response"""
        return len(self.response_text.split()) if self.response_text else 0
    
    @property
    def character_count(self) -> int:
        """Get character count of response"""
        return len(self.response_text) if self.response_text else 0
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": str(self.id),
            "query_id": str(self.query_id),
            "provider": self.provider,
            "model": self.model,
            "response_text": self.response_text,
            "response_metadata": self.response_metadata,
            "tokens_used": self.tokens_used,
            "response_time_ms": self.response_time_ms,
            "error_message": self.error_message,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "is_successful": self.is_successful,
            "word_count": self.word_count,
            "character_count": self.character_count
        } 
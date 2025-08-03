from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from datetime import datetime
from uuid import UUID

class LLMResponse(BaseModel):
    """Schema for LLM response data"""
    id: Optional[str] = Field(None, description="Response ID")
    text: str = Field(..., description="Response text from LLM")
    error: Optional[str] = Field(None, description="Error message if request failed")
    response_time_ms: Optional[int] = Field(None, description="Response time in milliseconds")
    tokens_used: Optional[int] = Field(None, description="Number of tokens used")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata")
    word_count: Optional[int] = Field(None, description="Word count of response")
    character_count: Optional[int] = Field(None, description="Character count of response")
    
    @property
    def is_successful(self) -> bool:
        """Check if the response was successful"""
        return not bool(self.error)

class ResponseBase(BaseModel):
    query_id: UUID
    provider: str = Field(..., description="LLM provider name")
    model: str = Field(..., description="Model name used")
    response_text: str = Field(..., description="Response text from LLM")
    response_metadata: Dict[str, Any] = Field(default_factory=dict, description="Response metadata")
    tokens_used: Optional[int] = Field(None, description="Number of tokens used")
    response_time_ms: Optional[int] = Field(None, description="Response time in milliseconds")
    error_message: Optional[str] = Field(None, description="Error message if failed")

class ResponseCreate(ResponseBase):
    pass

class ResponseUpdate(BaseModel):
    response_text: Optional[str] = None
    response_metadata: Optional[Dict[str, Any]] = None
    tokens_used: Optional[int] = None
    response_time_ms: Optional[int] = None
    error_message: Optional[str] = None

class ResponseResponse(ResponseBase):
    id: UUID
    created_at: datetime
    is_successful: bool
    word_count: int
    character_count: int

    class Config:
        from_attributes = True

class EvaluationMetricBase(BaseModel):
    query_id: UUID
    response_id: UUID
    similarity_scores: Dict[str, float] = Field(default_factory=dict, description="Similarity scores between providers")
    average_similarity: Optional[float] = Field(None, description="Average similarity score")
    originality_score: Optional[float] = Field(None, description="Originality score (0.0 to 1.0)")
    factuality_score: Optional[float] = Field(None, description="Factuality score (0.0 to 1.0)")
    readability_score: Optional[float] = Field(None, description="Readability score (0.0 to 1.0)")
    keyword_count: Optional[int] = Field(None, description="Number of keywords found")
    keyword_list: List[str] = Field(default_factory=list, description="List of keywords found")
    tool_mentions: List[str] = Field(default_factory=list, description="List of tools mentioned")
    seo_terms: List[str] = Field(default_factory=list, description="List of SEO terms found")
    response_length: Optional[int] = Field(None, description="Response length in characters")
    response_complexity: Optional[float] = Field(None, description="Response complexity score")

class EvaluationMetricCreate(EvaluationMetricBase):
    pass

class EvaluationMetricResponse(EvaluationMetricBase):
    id: UUID
    analysis_version: str
    computed_at: datetime

    class Config:
        from_attributes = True

class QueryResults(BaseModel):
    """Complete query results with responses and metrics"""
    query: Dict[str, Any]
    responses: List[ResponseResponse]
    evaluation_metrics: List[EvaluationMetricResponse]

    class Config:
        from_attributes = True 
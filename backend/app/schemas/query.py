from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from uuid import UUID

class QueryBase(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=10000, description="The query prompt to send to LLMs")
    category: str = Field(..., description="Category of the query (technical, content, automation, analytics)")
    tags: List[str] = Field(default_factory=list, description="Tags for categorizing the query")
    providers: List[str] = Field(default_factory=list, description="List of LLM providers to query")

class QueryCreate(QueryBase):
    user_id: Optional[str] = Field(None, description="Optional user identifier")

class QueryUpdate(BaseModel):
    status: Optional[str] = Field(None, description="Query status")
    prompt: Optional[str] = Field(None, description="Updated prompt")
    category: Optional[str] = Field(None, description="Updated category")
    tags: Optional[List[str]] = Field(None, description="Updated tags")
    providers: Optional[List[str]] = Field(None, description="Updated providers")

class QueryResponse(QueryBase):
    id: UUID
    user_id: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime
    response_count: int = 0
    successful_responses: int = 0

    class Config:
        from_attributes = True

class QueryStatus(BaseModel):
    id: UUID
    status: str
    completed_providers: List[str] = Field(default_factory=list)
    total_providers: int
    message: Optional[str] = None
    estimated_completion: Optional[datetime] = None

    class Config:
        from_attributes = True 
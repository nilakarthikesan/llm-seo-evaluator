from typing import List, Dict, Any, Optional
from app.core.supabase import get_supabase
from app.schemas.query import QueryCreate, QueryResponse
from app.schemas.response import ResponseCreate, LLMResponse
import logging
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)

class SupabaseService:
    """Service for interacting with Supabase database"""
    
    def __init__(self):
        self.supabase = get_supabase()
    
    async def create_query(self, query_data: QueryCreate) -> QueryResponse:
        """Create a new query"""
        try:
            query_dict = {
                "id": str(uuid.uuid4()),
                "prompt": query_data.prompt,
                "category": query_data.category,
                "tags": query_data.tags or [],
                "user_id": query_data.user_id,
                "status": "pending",
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            }
            
            response = self.supabase.table('queries').insert(query_dict).execute()
            
            if response.data:
                db_query_data = response.data[0]
                # Add computed fields that don't exist in DB
                db_query_data["response_count"] = 0
                db_query_data["successful_responses"] = 0
                # Add providers from the original request (not stored in DB)
                db_query_data["providers"] = query_data.providers or []
                return QueryResponse(**db_query_data)
            else:
                raise Exception("Failed to create query")
                
        except Exception as e:
            logger.error(f"Error creating query: {e}")
            raise
    
    async def get_query(self, query_id: str) -> Optional[QueryResponse]:
        """Get a query by ID"""
        try:
            response = self.supabase.table('queries').select('*').eq('id', query_id).execute()
            
            if response.data:
                query_data = response.data[0]
                # Get response count and successful responses
                responses = await self.get_responses_for_query(query_id)
                query_data["response_count"] = len(responses)
                query_data["successful_responses"] = len([r for r in responses if r.is_successful])
                return QueryResponse(**query_data)
            return None
            
        except Exception as e:
            logger.error(f"Error getting query {query_id}: {e}")
            raise
    
    async def get_queries(self, limit: int = 100, offset: int = 0) -> List[QueryResponse]:
        """Get all queries with pagination"""
        try:
            response = self.supabase.table('queries').select('*').range(offset, offset + limit - 1).execute()
            
            queries = []
            for query_data in response.data:
                # Get response count and successful responses for each query
                responses = await self.get_responses_for_query(query_data["id"])
                query_data["response_count"] = len(responses)
                query_data["successful_responses"] = len([r for r in responses if r.is_successful])
                queries.append(QueryResponse(**query_data))
            
            return queries
            
        except Exception as e:
            logger.error(f"Error getting queries: {e}")
            raise
    
    async def update_query_status(self, query_id: str, status: str) -> bool:
        """Update query status"""
        try:
            response = self.supabase.table('queries').update({
                "status": status,
                "updated_at": datetime.utcnow().isoformat()
            }).eq('id', query_id).execute()
            
            return len(response.data) > 0
            
        except Exception as e:
            logger.error(f"Error updating query status: {e}")
            raise
    
    async def create_response(self, response_data: ResponseCreate) -> LLMResponse:
        """Create a new response"""
        try:
            response_dict = {
                "id": str(uuid.uuid4()),
                "query_id": str(response_data.query_id),  # Convert UUID to string
                "provider": response_data.provider,
                "model": response_data.model,
                "response_text": response_data.response_text,
                "response_metadata": response_data.response_metadata or {},
                "tokens_used": response_data.tokens_used,
                "response_time_ms": response_data.response_time_ms,
                "error_message": response_data.error_message,
                "created_at": datetime.utcnow().isoformat()
            }
            
            response = self.supabase.table('responses').insert(response_dict).execute()
            
            if response.data:
                # Convert database response to LLMResponse format
                db_response = response.data[0]
                return LLMResponse(
                    id=db_response.get('id'),
                    text=db_response.get('response_text', ''),
                    error=db_response.get('error_message'),
                    response_time_ms=db_response.get('response_time_ms'),
                    tokens_used=db_response.get('tokens_used'),
                    metadata=db_response.get('response_metadata', {}),
                    word_count=len(db_response.get('response_text', '').split()),
                    character_count=len(db_response.get('response_text', ''))
                )
            else:
                raise Exception("Failed to create response")
                
        except Exception as e:
            logger.error(f"Error creating response: {e}")
            raise
    
    async def get_responses_for_query(self, query_id: str) -> List[LLMResponse]:
        """Get all responses for a query"""
        try:
            response = self.supabase.table('responses').select('*').eq('query_id', query_id).execute()
            
            # Convert database responses to LLMResponse format
            llm_responses = []
            for resp in response.data:
                llm_responses.append(LLMResponse(
                    id=resp.get('id'),
                    text=resp.get('response_text', ''),
                    error=resp.get('error_message'),
                    response_time_ms=resp.get('response_time_ms'),
                    tokens_used=resp.get('tokens_used'),
                    metadata=resp.get('response_metadata', {}),
                    word_count=len(resp.get('response_text', '').split()),
                    character_count=len(resp.get('response_text', ''))
                ))
            return llm_responses
            
        except Exception as e:
            logger.error(f"Error getting responses for query {query_id}: {e}")
            raise
    
    async def create_evaluation_metric(self, metric_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create evaluation metrics"""
        try:
            metric_dict = {
                "id": str(uuid.uuid4()),
                "query_id": str(metric_data["query_id"]),  # Convert UUID to string
                "response_id": str(metric_data["response_id"]),  # Convert UUID to string
                "similarity_scores": metric_data.get("similarity_scores", {}),
                "average_similarity": metric_data.get("average_similarity"),
                "originality_score": metric_data.get("originality_score"),
                "factuality_score": metric_data.get("factuality_score"),
                "readability_score": metric_data.get("readability_score"),
                "keyword_count": metric_data.get("keyword_count"),
                "keyword_list": metric_data.get("keyword_list", []),
                "tool_mentions": metric_data.get("tool_mentions", []),
                "seo_terms": metric_data.get("seo_terms", []),
                "response_length": metric_data.get("response_length"),
                "response_complexity": metric_data.get("response_complexity"),
                "analysis_version": metric_data.get("analysis_version", "1.0"),
                "computed_at": datetime.utcnow().isoformat()
            }
            
            response = self.supabase.table('evaluation_metrics').insert(metric_dict).execute()
            
            if response.data:
                return response.data[0]
            else:
                raise Exception("Failed to create evaluation metric")
                
        except Exception as e:
            logger.error(f"Error creating evaluation metric: {e}")
            raise
    
    async def get_evaluation_metrics_for_query(self, query_id: str) -> List[Dict[str, Any]]:
        """Get evaluation metrics for a query"""
        try:
            response = self.supabase.table('evaluation_metrics').select('*').eq('query_id', query_id).execute()
            
            # Convert to list of dicts and ensure UUIDs are strings
            metrics = []
            for metric in response.data:
                metric_dict = dict(metric)
                # Convert UUIDs to strings
                for key, value in metric_dict.items():
                    if hasattr(value, 'hex'):  # Check if it's a UUID
                        metric_dict[key] = str(value)
                    elif hasattr(value, 'isoformat'):  # Check if it's a datetime
                        metric_dict[key] = value.isoformat()
                metrics.append(metric_dict)
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error getting evaluation metrics for query {query_id}: {e}")
            return []
    
    async def get_analytics_data(self) -> Dict[str, Any]:
        """Get analytics data"""
        try:
            # Get total queries
            queries_response = self.supabase.table('queries').select('*', count='exact').execute()
            total_queries = queries_response.count or 0
            
            # Get total responses
            responses_response = self.supabase.table('responses').select('*', count='exact').execute()
            total_responses = responses_response.count or 0
            
            # Get queries by status
            status_response = self.supabase.table('queries').select('status').execute()
            status_counts = {}
            for query in status_response.data:
                status = query.get('status', 'unknown')
                status_counts[status] = status_counts.get(status, 0) + 1
            
            return {
                "total_queries": total_queries,
                "total_responses": total_responses,
                "queries_by_status": status_counts
            }
            
        except Exception as e:
            logger.error(f"Error getting analytics data: {e}")
            raise 
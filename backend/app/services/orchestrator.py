import asyncio
import logging
from typing import List, Dict, Any, Optional
from uuid import UUID
from datetime import datetime

from app.schemas.query import QueryCreate, QueryStatus, QueryResponse
from app.schemas.response import LLMResponse, ResponseCreate
from app.services.llm_providers.openai import OpenAIProvider
from app.services.llm_providers.anthropic import AnthropicProvider
from app.services.llm_providers.perplexity import PerplexityProvider
from app.services.llm_providers.google import GoogleProvider
from app.services.evaluation import EvaluationService
from app.services.supabase_service import SupabaseService
from app.core.config import settings

logger = logging.getLogger(__name__)

class QueryOrchestrator:
    """Orchestrates the entire query processing workflow using Supabase"""
    
    def __init__(self):
        self.evaluation_service = EvaluationService()
        self.supabase_service = SupabaseService()
        self.providers = {}
        self._initialize_providers()
    
    def _initialize_providers(self):
        """Initialize LLM providers based on available API keys"""
        try:
            if settings.openai_api_key and settings.openai_api_key != "your_openai_api_key_here":
                self.providers['openai'] = OpenAIProvider(
                    api_key=settings.openai_api_key,
                    model=settings.default_models.get('openai', 'gpt-4')
                )
        except Exception as e:
            logger.warning(f"Failed to initialize OpenAI provider: {e}")
        
        try:
            if settings.anthropic_api_key and settings.anthropic_api_key != "your_anthropic_api_key_here":
                self.providers['anthropic'] = AnthropicProvider(
                    api_key=settings.anthropic_api_key,
                    model=settings.default_models.get('anthropic', 'claude-3-5-sonnet-20241022')
                )
        except Exception as e:
            logger.warning(f"Failed to initialize Anthropic provider: {e}")
        
        try:
            if settings.perplexity_api_key and settings.perplexity_api_key != "your_perplexity_api_key_here":
                self.providers['perplexity'] = PerplexityProvider(
                    api_key=settings.perplexity_api_key,
                    model=settings.default_models.get('perplexity', 'llama-3.1-sonar-small-128k-online')
                )
        except Exception as e:
            logger.warning(f"Failed to initialize Perplexity provider: {e}")
        
        try:
            if settings.google_api_key and settings.google_api_key != "your_google_api_key_here":
                self.providers['google'] = GoogleProvider(
                    api_key=settings.google_api_key,
                    model=settings.default_models.get('google', 'gemini-pro')
                )
        except Exception as e:
            logger.warning(f"Failed to initialize Google provider: {e}")
        
        logger.info(f"Initialized {len(self.providers)} LLM providers: {list(self.providers.keys())}")
    
    async def create_query(self, query_data: QueryCreate) -> QueryResponse:
        """Create a new query in Supabase"""
        try:
            # Create query using Supabase service
            query = await self.supabase_service.create_query(query_data)
            
            logger.info(f"Created query {query.id} with {len(query_data.providers)} providers")
            return query
            
        except Exception as e:
            logger.error(f"Error creating query: {e}")
            raise
    
    async def process_query(self, query_id: str, providers: List[str] = None) -> bool:
        """Process a query by sending it to all specified LLM providers"""
        try:
            # Get query from Supabase
            query = await self.supabase_service.get_query(query_id)
            if not query:
                logger.error(f"Query {query_id} not found")
                return False
            
            # Update status to processing
            await self.supabase_service.update_query_status(query_id, "processing")
            
            # Use provided providers or fall back to query.providers
            query_providers = providers or getattr(query, 'providers', [])
            
            # Get available providers for this query
            available_providers = [
                provider for provider in query_providers 
                if provider in self.providers
            ]
            
            if not available_providers:
                logger.error(f"No available providers for query {query_id}")
                await self.supabase_service.update_query_status(query_id, "failed")
                return False
            
            # Process with each provider concurrently
            tasks = []
            for provider_name in available_providers:
                task = self._process_with_provider(query, provider_name)
                tasks.append(task)
            
            # Wait for all providers to complete
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Check if any providers succeeded
            successful_responses = [r for r in results if isinstance(r, bool) and r]
            
            if successful_responses:
                await self.supabase_service.update_query_status(query_id, "completed")
            else:
                await self.supabase_service.update_query_status(query_id, "failed")
            
            # Generate evaluation metrics
            await self._generate_evaluation_metrics(query_id)
            
            logger.info(f"Query {query_id} processed with {len(successful_responses)} successful responses")
            return len(successful_responses) > 0
            
        except Exception as e:
            logger.error(f"Error processing query {query_id}: {e}")
            # Update query status to failed
            try:
                await self.supabase_service.update_query_status(query_id, "failed")
            except:
                pass
            return False
    
    async def _process_with_provider(self, query: QueryResponse, provider_name: str) -> bool:
        """Process query with a specific provider"""
        try:
            provider = self.providers[provider_name]
            
            # Send query to provider
            llm_response = await provider.execute_with_retry(query.prompt)
            
            # Create response record
            response_data = ResponseCreate(
                query_id=query.id,
                provider=provider_name,
                model=provider.model,
                response_text=llm_response.text,
                response_metadata=llm_response.metadata or {},
                tokens_used=llm_response.tokens_used,
                response_time_ms=llm_response.response_time_ms,
                error_message=llm_response.error
            )
            
            await self.supabase_service.create_response(response_data)
            
            logger.info(f"Processed query {query.id} with {provider_name}: {'success' if llm_response.text else 'failed'}")
            return bool(llm_response.text)
            
        except Exception as e:
            logger.error(f"Error processing query {query.id} with {provider_name}: {e}")
            
            # Create error response record
            try:
                error_response_data = ResponseCreate(
                    query_id=query.id,
                    provider=provider_name,
                    model=provider.model if provider else "unknown",
                    response_text="",
                    response_metadata={},
                    error_message=str(e)
                )
                await self.supabase_service.create_response(error_response_data)
            except:
                pass
            
            return False
    
    async def _generate_evaluation_metrics(self, query_id: str):
        """Generate evaluation metrics for all responses to a query"""
        try:
            # Get all responses for the query
            responses = await self.supabase_service.get_responses_for_query(query_id)
            if not responses:
                return
            
            # Get query for category information
            query = await self.supabase_service.get_query(query_id)
            if not query:
                return
            
            # Convert responses to dict format for evaluation
            response_dicts = []
            for response in responses:
                response_dicts.append({
                    'id': str(response.id),
                    'response_text': response.text,  # Use 'text' from LLMResponse
                    'provider': 'openai',  # Default for now
                    'model': 'gpt-4'  # Default for now
                })
            
            # Evaluate all responses
            evaluation_results = self.evaluation_service.evaluate_all_responses(
                response_dicts, 
                category=query.category
            )
            
            # Create evaluation metrics for each response
            for response in responses:
                response_id_str = str(response.id)
                if response_id_str in evaluation_results['response_metrics']:
                    metrics_data = evaluation_results['response_metrics'][response_id_str]
                    
                    # Create evaluation metric record
                    metric_data = {
                        "query_id": query_id,
                        "response_id": response.id,
                        "similarity_scores": evaluation_results.get('similarity_matrix', []),
                        "average_similarity": evaluation_results.get('average_similarity', 0.0),
                        "originality_score": metrics_data.get('originality_score'),
                        "factuality_score": metrics_data.get('factuality_score'),
                        "readability_score": metrics_data.get('readability_score'),
                        "keyword_count": metrics_data.get('keyword_count'),
                        "keyword_list": metrics_data.get('keyword_list', []),
                        "tool_mentions": metrics_data.get('tool_mentions', []),
                        "seo_terms": metrics_data.get('seo_terms', []),
                        "response_length": metrics_data.get('response_length'),
                        "response_complexity": metrics_data.get('response_complexity'),
                        "analysis_version": "1.0"
                    }
                    
                    await self.supabase_service.create_evaluation_metric(metric_data)
            
            logger.info(f"Generated evaluation metrics for query {query_id}")
            
        except Exception as e:
            logger.error(f"Error generating evaluation metrics for query {query_id}: {e}")
    
    async def get_query_status(self, query_id: str) -> Optional[QueryStatus]:
        """Get current status of a query"""
        try:
            query = await self.supabase_service.get_query(query_id)
            if not query:
                return None
            
            # Get completed providers
            responses = await self.supabase_service.get_responses_for_query(query_id)
            completed_providers = [r.provider for r in responses if r.is_successful]
            
            # Get providers from query or use default
            query_providers = getattr(query, 'providers', [])
            
            return QueryStatus(
                id=query.id,
                status=query.status,
                completed_providers=completed_providers,
                total_providers=len(query_providers),
                message=self._get_status_message(query.status),
                estimated_completion=None  # Could be calculated based on processing time
            )
            
        except Exception as e:
            logger.error(f"Error getting query status for {query_id}: {e}")
            return None
    
    async def get_query_results(self, query_id: str) -> Optional[Dict[str, Any]]:
        """Get complete results for a query including responses and metrics"""
        try:
            query = await self.supabase_service.get_query(query_id)
            if not query:
                return None
            
            responses = await self.supabase_service.get_responses_for_query(query_id)
            
            # Convert responses to simple dict format
            response_dicts = []
            for response in responses:
                response_dicts.append({
                    "id": response.id,
                    "query_id": query_id,
                    "provider": "openai",  # Default for now
                    "model": "gpt-4",  # Default for now
                    "response_text": response.text,
                    "response_metadata": response.metadata,
                    "tokens_used": response.tokens_used,
                    "response_time_ms": response.response_time_ms,
                    "error_message": response.error,
                    "is_successful": response.is_successful,
                    "word_count": len(response.text.split()) if response.text else 0,
                    "character_count": len(response.text) if response.text else 0
                })
            
            # Get evaluation metrics from database
            evaluation_metrics = await self.supabase_service.get_evaluation_metrics_for_query(query_id)
            
            # Convert query to dict and ensure UUIDs and datetimes are serializable
            query_dict = query.dict()
            # Convert any UUID fields to strings
            for key, value in query_dict.items():
                if hasattr(value, 'hex'):  # Check if it's a UUID
                    query_dict[key] = str(value)
                elif hasattr(value, 'isoformat'):  # Check if it's a datetime
                    query_dict[key] = value.isoformat()
            
            return {
                "query": query_dict,
                "responses": response_dicts,
                "evaluation_metrics": evaluation_metrics
            }
            
        except Exception as e:
            logger.error(f"Error getting query results for {query_id}: {e}")
            return None
    
    def _get_status_message(self, status: str) -> str:
        """Get human-readable status message"""
        messages = {
            "pending": "Query is waiting to be processed",
            "processing": "Query is being processed by LLM providers",
            "completed": "Query processing completed successfully",
            "failed": "Query processing failed"
        }
        return messages.get(status, "Unknown status") 
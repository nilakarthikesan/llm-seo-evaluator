from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
from datetime import datetime, timedelta

from app.services.supabase_service import SupabaseService

router = APIRouter()

# Initialize Supabase service
supabase_service = SupabaseService()

@router.get("/trends")
async def get_analytics_trends(days: int = 30):
    """Get analytics trends over time"""
    try:
        # Get analytics data from Supabase service
        analytics_data = await supabase_service.get_analytics_data()
        
        # For now, return basic analytics
        # TODO: Implement more detailed trends with date filtering
        trends = {
            "total_queries": analytics_data.get("total_queries", 0),
            "total_responses": analytics_data.get("total_responses", 0),
            "queries_by_status": analytics_data.get("queries_by_status", {}),
            "provider_distribution": {},
            "category_distribution": {},
            "daily_queries": {}
        }
        
        return trends
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get analytics trends: {str(e)}")

@router.get("/queries/{query_id}/metrics")
async def get_query_metrics(query_id: str):
    """Get detailed metrics for a specific query"""
    try:
        # Get query
        query = await supabase_service.get_query(query_id)
        if not query:
            raise HTTPException(status_code=404, detail="Query not found")
        
        # Get responses
        responses = await supabase_service.get_responses_for_query(query_id)
        
        # Calculate metrics
        query_metrics = {
            "query_id": query_id,
            "total_responses": len(responses),
            "successful_responses": len([r for r in responses if r.is_successful]),
            "failed_responses": len([r for r in responses if not r.is_successful]),
            "avg_response_time": 0.0,
            "avg_tokens_used": 0.0,
            "avg_word_count": 0.0,
            "provider_metrics": {},
            "response_details": []
        }
        
        # Calculate averages
        response_times = [r.response_time_ms for r in responses if r.response_time_ms]
        if response_times:
            query_metrics["avg_response_time"] = sum(response_times) / len(response_times)
        
        token_counts = [r.tokens_used for r in responses if r.tokens_used]
        if token_counts:
            query_metrics["avg_tokens_used"] = sum(token_counts) / len(token_counts)
        
        word_counts = [r.word_count for r in responses]
        if word_counts:
            query_metrics["avg_word_count"] = sum(word_counts) / len(word_counts)
        
        # Provider-specific metrics
        provider_metrics = {}
        for response in responses:
            provider = response.provider
            if provider not in provider_metrics:
                provider_metrics[provider] = {
                    "total_responses": 0,
                    "successful_responses": 0,
                    "avg_response_time": 0.0,
                    "avg_tokens": 0.0,
                    "avg_word_count": 0.0
                }
            
            provider_metrics[provider]["total_responses"] += 1
            if response.is_successful:
                provider_metrics[provider]["successful_responses"] += 1
        
        # Calculate provider averages
        for provider, metrics_data in provider_metrics.items():
            provider_responses = [r for r in responses if r.provider == provider]
            
            response_times = [r.response_time_ms for r in provider_responses if r.response_time_ms]
            if response_times:
                metrics_data["avg_response_time"] = sum(response_times) / len(response_times)
            
            token_counts = [r.tokens_used for r in provider_responses if r.tokens_used]
            if token_counts:
                metrics_data["avg_tokens"] = sum(token_counts) / len(token_counts)
            
            word_counts = [r.word_count for r in provider_responses]
            if word_counts:
                metrics_data["avg_word_count"] = sum(word_counts) / len(word_counts)
        
        query_metrics["provider_metrics"] = provider_metrics
        
        # Response details
        for response in responses:
            response_detail = {
                "id": str(response.id),
                "provider": response.provider,
                "model": response.model,
                "is_successful": response.is_successful,
                "response_time_ms": response.response_time_ms,
                "tokens_used": response.tokens_used,
                "word_count": response.word_count,
                "character_count": response.character_count,
                "error_message": response.error_message
            }
            query_metrics["response_details"].append(response_detail)
        
        return query_metrics
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get query metrics: {str(e)}")

@router.get("/queries/{query_id}/similarity")
async def get_similarity_analysis(query_id: str):
    """Get similarity analysis for a query"""
    try:
        # For now, return basic similarity data
        # TODO: Implement similarity analysis using evaluation metrics
        return {
            "query_id": query_id,
            "similarity_matrix": [],
            "providers": [],
            "average_similarity": 0.0
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get similarity analysis: {str(e)}")

@router.get("/queries/{query_id}/keywords")
async def get_keyword_analysis(query_id: str):
    """Get keyword analysis for a query"""
    try:
        # For now, return basic keyword data
        # TODO: Implement keyword analysis using evaluation metrics
        return {
            "query_id": query_id,
            "keywords": {},
            "tools": {},
            "seo_terms": {},
            "total_keywords": 0,
            "total_tools": 0,
            "total_seo_terms": 0
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get keyword analysis: {str(e)}")

@router.get("/providers/comparison")
async def get_provider_comparison(days: int = 30):
    """Get comparison metrics across all providers"""
    try:
        # Get all responses from Supabase
        # TODO: Implement date filtering
        responses = await supabase_service.get_responses_for_query("all")  # This needs to be implemented
        
        # For now, return basic comparison data
        comparison = {
            "provider_comparison": {},
            "total_responses": 0
        }
        
        return comparison
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get provider comparison: {str(e)}") 
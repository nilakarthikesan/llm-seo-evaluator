from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Optional
from uuid import UUID

from app.schemas.query import QueryCreate, QueryResponse, QueryStatus, QueryUpdate
from app.schemas.response import QueryResults
from app.services.orchestrator import QueryOrchestrator
from app.services.supabase_service import SupabaseService

router = APIRouter()

# Initialize Supabase service
supabase_service = SupabaseService()

# Lazy initialization of orchestrator
_orchestrator = None

def get_orchestrator():
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = QueryOrchestrator()
    return _orchestrator

@router.post("/", response_model=QueryResponse)
async def create_query(
    query_data: QueryCreate,
    background_tasks: BackgroundTasks
):
    """Create a new query and start processing"""
    try:
        # Get orchestrator
        orchestrator = get_orchestrator()
        
        # Create query in Supabase
        query = await orchestrator.create_query(query_data)
        
        # Start processing in background
        background_tasks.add_task(orchestrator.process_query, query.id, query_data.providers)
        
        return query
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create query: {str(e)}")

@router.get("/{query_id}", response_model=QueryResponse)
async def get_query(query_id: str):
    """Get a specific query by ID"""
    try:
        query = await supabase_service.get_query(query_id)
        if not query:
            raise HTTPException(status_code=404, detail="Query not found")
        
        return query
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get query: {str(e)}")

@router.get("/{query_id}/status", response_model=QueryStatus)
async def get_query_status(query_id: str):
    """Get the current status of a query"""
    try:
        orchestrator = get_orchestrator()
        status = await orchestrator.get_query_status(query_id)
        if not status:
            raise HTTPException(status_code=404, detail="Query not found")
        
        return status
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get query status: {str(e)}")

@router.get("/{query_id}/responses")
async def get_query_responses(query_id: str):
    """Get complete results for a query including responses and evaluation metrics"""
    try:
        orchestrator = get_orchestrator()
        results = await orchestrator.get_query_results(query_id)
        if not results:
            raise HTTPException(status_code=404, detail="Query not found")
        
        return results
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get query responses: {str(e)}")

@router.put("/{query_id}", response_model=QueryResponse)
async def update_query(
    query_id: str,
    query_update: QueryUpdate
):
    """Update a query (limited fields)"""
    try:
        query = await supabase_service.get_query(query_id)
        if not query:
            raise HTTPException(status_code=404, detail="Query not found")
        
        # Update allowed fields using Supabase
        update_data = {}
        if query_update.status is not None:
            update_data["status"] = query_update.status
        if query_update.prompt is not None:
            update_data["prompt"] = query_update.prompt
        if query_update.category is not None:
            update_data["category"] = query_update.category
        if query_update.tags is not None:
            update_data["tags"] = query_update.tags
        # Note: providers field is not stored in database, so we skip it
        # if query_update.providers is not None:
        #     update_data["providers"] = query_update.providers
        
        if update_data:
            # Add updated_at timestamp
            from datetime import datetime
            update_data["updated_at"] = datetime.utcnow().isoformat()
            
            # Update in Supabase
            response = supabase_service.supabase.table('queries').update(update_data).eq('id', query_id).execute()
            
            if response.data:
                return QueryResponse(**response.data[0])
            else:
                raise HTTPException(status_code=500, detail="Failed to update query")
        
        return query
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update query: {str(e)}")

@router.post("/{query_id}/retry")
async def retry_query(
    query_id: str,
    background_tasks: BackgroundTasks
):
    """Retry processing a failed query"""
    try:
        query = await supabase_service.get_query(query_id)
        if not query:
            raise HTTPException(status_code=404, detail="Query not found")
        
        # Reset status and start processing
        await supabase_service.update_query_status(query_id, "pending")
        
        # Start processing in background
        orchestrator = get_orchestrator()
        # For retry, we'll use the providers from the original query creation
        # This is a simplified approach - in a real app, you might want to store providers
        background_tasks.add_task(orchestrator.process_query, query_id, ["openai", "anthropic"])
        
        return {"message": "Query retry started", "query_id": query_id}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retry query: {str(e)}")

@router.get("/", response_model=List[QueryResponse])
async def list_queries(skip: int = 0, limit: int = 100):
    """List all queries with pagination"""
    try:
        queries = await supabase_service.get_queries(limit=limit, offset=skip)
        return queries
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list queries: {str(e)}") 
#!/usr/bin/env python3
"""
Test the get_query_results method
"""
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_results():
    """Test getting query results"""
    print("🔍 Testing Query Results")
    print("=" * 40)
    
    try:
        from app.services.orchestrator import QueryOrchestrator
        
        # Create orchestrator
        orchestrator = QueryOrchestrator()
        print(f"✅ Orchestrator created successfully")
        
        # Test getting results for a specific query
        query_id = "8dfbb416-0184-416a-aa5e-a4ef817f8250"
        print(f"\n📊 Getting results for query: {query_id}")
        
        results = await orchestrator.get_query_results(query_id)
        if results:
            print(f"✅ Results retrieved successfully")
            print(f"Query: {results.get('query', {}).get('prompt', 'No prompt')}")
            print(f"Responses count: {len(results.get('responses', []))}")
            
            for i, response in enumerate(results.get('responses', [])):
                print(f"\nResponse {i+1}:")
                print(f"  Provider: {response.get('provider')}")
                print(f"  Model: {response.get('model')}")
                print(f"  Text: {response.get('response_text', '')[:100]}...")
                print(f"  Tokens: {response.get('tokens_used')}")
                print(f"  Time: {response.get('response_time_ms')}ms")
        else:
            print(f"❌ No results found")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_results()) 
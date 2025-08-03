#!/usr/bin/env python3
"""
Test the orchestrator with just OpenAI
"""
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_orchestrator():
    """Test the orchestrator"""
    print("🔍 Testing Orchestrator")
    print("=" * 40)
    
    try:
        from app.services.orchestrator import QueryOrchestrator
        
        # Create orchestrator
        orchestrator = QueryOrchestrator()
        print(f"✅ Orchestrator created successfully")
        print(f"Available providers: {list(orchestrator.providers.keys())}")
        
        # Test creating a query
        from app.schemas.query import QueryCreate
        
        query_data = QueryCreate(
            prompt="What are the best Python automation scripts for SEO in 2025?",
            category="automation",
            tags=["python", "seo", "scripts"],
            providers=["openai"],
            user_id="test-user"
        )
        
        print(f"\n📝 Creating query...")
        query = await orchestrator.create_query(query_data)
        print(f"✅ Query created: {query.id}")
        
        # Test processing the query
        print(f"\n🔄 Processing query...")
        success = await orchestrator.process_query(query.id, ["openai"])
        print(f"✅ Query processing {'succeeded' if success else 'failed'}")
        
        # Get results
        print(f"\n📊 Getting results...")
        results = await orchestrator.get_query_results(query.id)
        if results:
            print(f"✅ Results retrieved")
            print(f"Status: {results.get('status')}")
            print(f"Responses: {len(results.get('responses', []))}")
        else:
            print(f"❌ No results found")
            
    except Exception as e:
        print(f"❌ Orchestrator test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_orchestrator()) 
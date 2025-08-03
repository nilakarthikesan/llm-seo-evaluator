#!/usr/bin/env python3
"""
Test all LLM providers
"""
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_multi_providers():
    """Test all LLM providers"""
    print("🔍 Testing Multi-Provider System")
    print("=" * 50)
    
    try:
        from app.services.orchestrator import QueryOrchestrator
        
        # Create orchestrator
        orchestrator = QueryOrchestrator()
        print(f"✅ Orchestrator created with {len(orchestrator.providers)} providers: {list(orchestrator.providers.keys())}")
        
        # Test each provider
        test_prompt = "What are the best technical SEO practices for 2025?"
        
        for provider_name, provider in orchestrator.providers.items():
            print(f"\n🧪 Testing {provider_name.upper()} provider...")
            
            try:
                response = await provider.query(test_prompt)
                
                if response.is_successful:
                    print(f"✅ {provider_name.upper()} successful!")
                    print(f"📊 Response length: {len(response.text)} characters")
                    print(f"🔢 Tokens used: {response.tokens_used}")
                    print(f"📋 First 150 chars: {response.text[:150]}...")
                else:
                    print(f"❌ {provider_name.upper()} failed: {response.error}")
                    
            except Exception as e:
                print(f"❌ {provider_name.upper()} error: {e}")
        
        # Test multi-provider query
        print(f"\n🚀 Testing multi-provider query...")
        
        # Create a test query
        from app.schemas.query import QueryCreate
        
        query_data = QueryCreate(
            prompt=test_prompt,
            category="technical",
            providers=list(orchestrator.providers.keys()),
            user_id="test-user"
        )
        
        # Create query
        query = await orchestrator.create_query(query_data)
        print(f"✅ Created query: {query.id}")
        
        # Process query with all providers
        success = await orchestrator.process_query(query.id, list(orchestrator.providers.keys()))
        
        if success:
            print(f"✅ Multi-provider processing successful!")
            
            # Get results
            results = await orchestrator.get_query_results(query.id)
            if results:
                print(f"📊 Got {len(results['responses'])} responses")
                print(f"📈 Got {len(results['evaluation_metrics'])} evaluation metrics")
                
                # Show provider comparison
                for response in results['responses']:
                    provider = response.get('provider', 'unknown')
                    word_count = response.get('word_count', 0)
                    print(f"  - {provider}: {word_count} words")
        else:
            print(f"❌ Multi-provider processing failed")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_multi_providers()) 
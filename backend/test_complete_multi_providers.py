#!/usr/bin/env python3
"""
Test complete multi-provider system with all LLM providers
"""
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_complete_multi_providers():
    """Test all LLM providers with API keys"""
    print("🔍 Testing Complete Multi-Provider System")
    print("=" * 60)
    
    # Check API keys
    print("🔑 Checking API Keys:")
    api_keys = {
        "OpenAI": os.getenv('OPENAI_API_KEY'),
        "Anthropic": os.getenv('ANTHROPIC_API_KEY'),
        "Perplexity": os.getenv('PERPLEXITY_API_KEY'),
        "Google": os.getenv('GOOGLE_API_KEY')
    }
    
    for provider, key in api_keys.items():
        if key and key != "your_openai_api_key_here" and key != "your_anthropic_api_key_here" and key != "your_perplexity_api_key_here" and key != "your_google_api_key_here":
            print(f"✅ {provider}: API key found")
        else:
            print(f"❌ {provider}: API key missing or placeholder")
    
    print()
    
    try:
        from app.services.orchestrator import QueryOrchestrator
        
        # Create orchestrator
        orchestrator = QueryOrchestrator()
        print(f"🎯 Orchestrator initialized with {len(orchestrator.providers)} providers: {list(orchestrator.providers.keys())}")
        
        if len(orchestrator.providers) == 0:
            print("❌ No providers initialized. Check your API keys!")
            return
        
        # Test each provider individually
        test_prompt = "What are the top 3 technical SEO factors for 2025?"
        
        print(f"\n🧪 Testing Individual Providers:")
        print("-" * 40)
        
        for provider_name, provider in orchestrator.providers.items():
            print(f"\n📡 Testing {provider_name.upper()}...")
            
            try:
                response = await provider.query(test_prompt)
                
                if response.is_successful:
                    print(f"✅ {provider_name.upper()} SUCCESS!")
                    print(f"📊 Response length: {len(response.text)} characters")
                    print(f"🔢 Tokens used: {response.tokens_used}")
                    print(f"📋 Preview: {response.text[:100]}...")
                else:
                    print(f"❌ {provider_name.upper()} FAILED: {response.error}")
                    
            except Exception as e:
                print(f"❌ {provider_name.upper()} ERROR: {e}")
        
        # Test multi-provider query
        print(f"\n🚀 Testing Multi-Provider Query:")
        print("-" * 40)
        
        # Create a test query with all available providers
        from app.schemas.query import QueryCreate
        
        available_providers = list(orchestrator.providers.keys())
        print(f"📝 Using providers: {available_providers}")
        
        query_data = QueryCreate(
            prompt=test_prompt,
            category="technical",
            providers=available_providers,
            user_id="test-user"
        )
        
        # Create query
        query = await orchestrator.create_query(query_data)
        print(f"✅ Created query: {query.id}")
        
        # Process query with all providers
        print("⏳ Processing with all providers...")
        success = await orchestrator.process_query(query.id, available_providers)
        
        if success:
            print(f"✅ Multi-provider processing successful!")
            
            # Get results
            results = await orchestrator.get_query_results(query.id)
            if results:
                print(f"📊 Results Summary:")
                print(f"  - Query: {results['query']['prompt']}")
                print(f"  - Responses: {len(results['responses'])}")
                print(f"  - Evaluation metrics: {len(results['evaluation_metrics'])}")
                
                # Show provider comparison
                print(f"\n📈 Provider Comparison:")
                for response in results['responses']:
                    provider = response.get('provider', 'unknown')
                    word_count = response.get('word_count', 0)
                    char_count = response.get('character_count', 0)
                    print(f"  - {provider}: {word_count} words, {char_count} chars")
                
                # Show evaluation metrics
                if results['evaluation_metrics']:
                    print(f"\n📊 Evaluation Metrics:")
                    for metric in results['evaluation_metrics']:
                        response_id = metric.get('response_id', 'unknown')
                        originality = metric.get('originality_score', 0)
                        readability = metric.get('readability_score', 0)
                        print(f"  - Response {response_id}: Originality={originality:.3f}, Readability={readability:.3f}")
        else:
            print(f"❌ Multi-provider processing failed")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_complete_multi_providers()) 
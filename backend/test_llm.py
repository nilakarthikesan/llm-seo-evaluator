#!/usr/bin/env python3
"""
Test LLM provider initialization step by step
"""
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_llm_initialization():
    """Test LLM provider initialization"""
    print("🔍 Testing LLM Provider Initialization")
    print("=" * 50)
    
    # Check environment variables
    print("📋 Environment Variables:")
    openai_key = os.getenv('OPENAI_API_KEY')
    anthropic_key = os.getenv('ANTHROPIC_API_KEY')
    
    print(f"OpenAI API Key: {'✅ Set' if openai_key and openai_key != 'your_openai_api_key_here' else '❌ Not set or default'}")
    print(f"Anthropic API Key: {'✅ Set' if anthropic_key and anthropic_key != 'your_anthropic_api_key_here' else '❌ Not set or default'}")
    
    if not openai_key or openai_key == 'your_openai_api_key_here':
        print("\n⚠️  OpenAI API key not set. Please add to your .env file:")
        print("OPENAI_API_KEY=sk-your-actual-key-here")
        return
    
    # Test OpenAI provider initialization
    print("\n🤖 Testing OpenAI Provider:")
    try:
        from app.services.llm_providers.openai import OpenAIProvider
        
        provider = OpenAIProvider(
            api_key=openai_key,
            model="gpt-4"
        )
        print("✅ OpenAI provider initialized successfully")
        print(f"Provider name: {provider.get_provider_name()}")
        print(f"Model: {provider.model}")
        
        # Test a simple query
        print("\n🧪 Testing simple query...")
        response = await provider.execute_with_retry(
            "Say 'Hello, this is a test!' in one sentence."
        )
        
        if response.error:
            print(f"❌ Query failed: {response.error}")
        else:
            print(f"✅ Query successful!")
            print(f"Response: {response.text[:100]}...")
            print(f"Response time: {response.response_time_ms}ms")
            
    except Exception as e:
        print(f"❌ OpenAI provider initialization failed: {e}")
        print(f"Error type: {type(e).__name__}")

if __name__ == "__main__":
    asyncio.run(test_llm_initialization()) 
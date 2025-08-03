#!/usr/bin/env python3
"""
Test Anthropic provider
"""
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_anthropic():
    """Test Anthropic provider"""
    print("🔍 Testing Anthropic Provider")
    print("=" * 40)
    
    # Check environment variables
    anthropic_key = os.getenv('ANTHROPIC_API_KEY')
    
    print(f"Anthropic API Key: {'✅ Set' if anthropic_key and anthropic_key != 'your_anthropic_api_key_here' else '❌ Not set or default'}")
    
    if not anthropic_key or anthropic_key == 'your_anthropic_api_key_here':
        print("\n⚠️  Anthropic API key not set. Please add to your .env file:")
        print("ANTHROPIC_API_KEY=sk-your-actual-key-here")
        return
    
    # Test Anthropic provider
    print("\n🤖 Testing Anthropic Provider:")
    try:
        from app.services.llm_providers.anthropic import AnthropicProvider
        
        provider = AnthropicProvider(
            api_key=anthropic_key,
            model="claude-3-sonnet-20240229"
        )
        print("✅ Anthropic provider initialized successfully")
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
        print(f"❌ Anthropic provider initialization failed: {e}")
        print(f"Error type: {type(e).__name__}")

if __name__ == "__main__":
    asyncio.run(test_anthropic()) 
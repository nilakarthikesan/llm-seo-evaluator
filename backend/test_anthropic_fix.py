#!/usr/bin/env python3
"""
Test Anthropic provider directly
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
    
    try:
        from app.services.llm_providers.anthropic import AnthropicProvider
        
        # Get API key from environment
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            print("❌ ANTHROPIC_API_KEY not found in environment")
            return
        
        # Create provider
        provider = AnthropicProvider(api_key=api_key, model="claude-3-5-sonnet-20241022")
        print("✅ Anthropic provider created successfully")
        
        # Test query
        prompt = "What are the best SEO practices for e-commerce websites?"
        print(f"\n📝 Testing with prompt: {prompt}")
        
        response = await provider.query(prompt)
        
        if response.is_successful:
            print("✅ Anthropic query successful!")
            print(f"📊 Response length: {len(response.text)} characters")
            print(f"🔢 Tokens used: {response.tokens_used}")
            print(f"📋 First 200 chars: {response.text[:200]}...")
        else:
            print(f"❌ Anthropic query failed: {response.error}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_anthropic()) 
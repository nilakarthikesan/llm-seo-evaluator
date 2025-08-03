#!/usr/bin/env python3
"""
Test provider initialization isolation to find which one is hanging
"""
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_provider_isolation():
    """Test each provider initialization separately"""
    print("🔍 Testing Provider Initialization Isolation")
    print("=" * 50)
    
    # Test OpenAI
    print("\n🤖 Testing OpenAI initialization:")
    try:
        from app.services.llm_providers.openai import OpenAIProvider
        provider = OpenAIProvider(
            api_key=os.getenv('OPENAI_API_KEY'),
            model="gpt-4"
        )
        print("✅ OpenAI provider initialized successfully")
    except Exception as e:
        print(f"❌ OpenAI provider failed: {e}")
    
    # Test Anthropic
    print("\n🤖 Testing Anthropic initialization:")
    try:
        from app.services.llm_providers.anthropic import AnthropicProvider
        provider = AnthropicProvider(
            api_key=os.getenv('ANTHROPIC_API_KEY'),
            model="claude-3-5-sonnet-20241022"
        )
        print("✅ Anthropic provider initialized successfully")
    except Exception as e:
        print(f"❌ Anthropic provider failed: {e}")
    
    # Test Perplexity
    print("\n🤖 Testing Perplexity initialization:")
    try:
        from app.services.llm_providers.perplexity import PerplexityProvider
        provider = PerplexityProvider(
            api_key=os.getenv('PERPLEXITY_API_KEY'),
            model="llama-3.1-sonar-small-128k-online"
        )
        print("✅ Perplexity provider initialized successfully")
    except Exception as e:
        print(f"❌ Perplexity provider failed: {e}")
    
    # Test Google
    print("\n🤖 Testing Google initialization:")
    try:
        from app.services.llm_providers.google import GoogleProvider
        provider = GoogleProvider(
            api_key=os.getenv('GOOGLE_API_KEY'),
            model="gemini-pro"
        )
        print("✅ Google provider initialized successfully")
    except Exception as e:
        print(f"❌ Google provider failed: {e}")

if __name__ == "__main__":
    test_provider_isolation() 
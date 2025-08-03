#!/usr/bin/env python3
"""
Minimal test to isolate the proxies issue
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_minimal():
    """Test minimal initialization"""
    print("🔍 Minimal Test")
    print("=" * 30)
    
    # Check if proxies is in environment
    proxies = os.getenv('HTTP_PROXY') or os.getenv('HTTPS_PROXY')
    print(f"HTTP_PROXY: {os.getenv('HTTP_PROXY', 'Not set')}")
    print(f"HTTPS_PROXY: {os.getenv('HTTPS_PROXY', 'Not set')}")
    
    # Test direct OpenAI client creation
    print("\n🤖 Testing direct OpenAI client:")
    try:
        import openai
        
        # Get API key
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key or api_key == 'your_openai_api_key_here':
            print("❌ No valid API key found")
            return
        
        # Try to create client
        client = openai.AsyncOpenAI(api_key=api_key)
        print("✅ OpenAI client created successfully")
        
        # Test our provider
        print("\n🤖 Testing our provider:")
        from app.services.llm_providers.openai import OpenAIProvider
        
        provider = OpenAIProvider(api_key=api_key, model="gpt-4")
        print("✅ Provider created successfully")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"Error type: {type(e).__name__}")

if __name__ == "__main__":
    test_minimal() 
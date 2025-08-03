#!/usr/bin/env python3
"""
Debug script to see what parameters are being passed to OpenAI
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def debug_proxies():
    """Debug the proxies issue"""
    print("🔍 Debugging Proxies Issue")
    print("=" * 40)
    
    # Check all environment variables that might contain proxy info
    proxy_vars = [
        'HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy',
        'NO_PROXY', 'no_proxy', 'ALL_PROXY', 'all_proxy'
    ]
    
    print("📋 Environment Variables:")
    for var in proxy_vars:
        value = os.getenv(var)
        if value:
            print(f"{var}: {value}")
        else:
            print(f"{var}: Not set")
    
    # Check if there are any global configurations
    print("\n🔧 Testing OpenAI client creation:")
    try:
        import openai
        
        # Get API key
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key or api_key == 'your_openai_api_key_here':
            print("❌ No valid API key found")
            return
        
        # Try to create client with explicit parameters
        print("Creating client with explicit parameters...")
        client = openai.AsyncOpenAI(
            api_key=api_key,
            # Don't pass any other parameters
        )
        print("✅ Client created successfully")
        
        # Now test our provider
        print("\n🤖 Testing our provider:")
        from app.services.llm_providers.openai import OpenAIProvider
        
        # Create provider with minimal parameters
        provider = OpenAIProvider(
            api_key=api_key,
            model="gpt-4"
            # Don't pass any kwargs
        )
        print("✅ Provider created successfully")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"Error type: {type(e).__name__}")
        
        # Let's see what's in the kwargs
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_proxies() 
#!/usr/bin/env python3
"""
Minimal test for Anthropic to isolate proxies issue
"""
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_anthropic_simple():
    """Test Anthropic with minimal setup"""
    print("🔍 Testing Anthropic - Minimal Setup")
    print("=" * 40)
    
    try:
        import anthropic
        
        # Get API key
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            print("❌ ANTHROPIC_API_KEY not found")
            return
        
        print("✅ API key found")
        
        # Test direct client creation
        print("🔧 Testing direct client creation...")
        client = anthropic.Anthropic(api_key=api_key)
        print("✅ Direct client creation successful")
        
        # Test message creation
        print("📝 Testing message creation...")
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            messages=[
                {
                    "role": "user",
                    "content": "Hello, can you help me with SEO?"
                }
            ],
            max_tokens=100
        )
        
        print("✅ Message creation successful")
        print(f"📋 Response: {response.content[0].text}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_anthropic_simple()) 
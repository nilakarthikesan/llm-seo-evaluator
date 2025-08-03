#!/usr/bin/env python3
"""
Direct test of the libraries
"""
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_direct():
    """Test direct library usage"""
    print("🔍 Direct Library Test")
    print("=" * 30)
    
    # Test OpenAI directly
    print("\n🤖 Testing OpenAI directly:")
    try:
        import openai
        
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key or api_key == 'your_openai_api_key_here':
            print("❌ No valid API key")
            return
        
        # Set API key
        openai.api_key = api_key
        
        # Test direct call
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[{"role": "user", "content": "Say hello"}],
            max_tokens=10
        )
        print("✅ OpenAI direct call successful")
        print(f"Response: {response.choices[0].message.content}")
        
    except Exception as e:
        print(f"❌ OpenAI direct call failed: {e}")
    
    # Test Anthropic directly
    print("\n🤖 Testing Anthropic directly:")
    try:
        import anthropic
        
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key or api_key == 'your_anthropic_api_key_here':
            print("❌ No valid API key")
            return
        
        # Test direct call
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            messages=[{"role": "user", "content": "Say hello"}],
            max_tokens=10
        )
        print("✅ Anthropic direct call successful")
        print(f"Response: {response.content[0].text}")
        
    except Exception as e:
        print(f"❌ Anthropic direct call failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_direct()) 
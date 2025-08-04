#!/usr/bin/env python3
"""
Simple test to find the correct Perplexity model name
"""
import os
import asyncio
import httpx
from dotenv import load_dotenv

load_dotenv()

async def test_perplexity_model(model_name: str):
    """Test a specific Perplexity model name"""
    api_key = os.getenv('PERPLEXITY_API_KEY')
    if not api_key:
        print("❌ PERPLEXITY_API_KEY not found")
        return False
    
    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model_name,
        "messages": [
            {
                "role": "user",
                "content": "Hello, this is a test message."
            }
        ]
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=data, timeout=10.0)
            
            if response.status_code == 200:
                print(f"✅ SUCCESS: {model_name}")
                return True
            else:
                print(f"❌ FAILED: {model_name} - Status: {response.status_code}")
                if response.status_code == 400:
                    error_text = response.text
                    print(f"   Error: {error_text[:200]}...")
                return False
                
    except Exception as e:
        print(f"❌ ERROR: {model_name} - {str(e)}")
        return False

async def main():
    """Test common Perplexity model names"""
    print("🔍 Testing Perplexity Model Names")
    print("=" * 50)
    
    # Most likely current model names based on Perplexity's naming convention
    models_to_test = [
        # Try the most common current names
        "sonar-small-online",
        "sonar-medium-online", 
        "sonar-large-online",
        "sonar-small",
        "sonar-medium",
        "sonar-large",
        # Try with different prefixes
        "perplexity-sonar-small",
        "perplexity-sonar-medium",
        "perplexity-sonar-large",
        # Try without version numbers
        "llama-sonar-small",
        "llama-sonar-medium",
        "llama-sonar-large",
        # Try with different suffixes
        "sonar-small-128k",
        "sonar-medium-128k",
        "sonar-large-128k",
        # Try the exact error message format
        "llama-3.1-sonar-small-128k-online",
        "llama-3.1-sonar-medium-128k-online",
        "llama-3.1-sonar-large-128k-online",
        # Try without the -online suffix
        "llama-3.1-sonar-small-128k",
        "llama-3.1-sonar-medium-128k",
        "llama-3.1-sonar-large-128k",
        # Try simpler names
        "sonar-small-128k-online",
        "sonar-medium-128k-online",
        "sonar-large-128k-online",
        # Try without any suffixes
        "llama-3.1-sonar-small",
        "llama-3.1-sonar-medium",
        "llama-3.1-sonar-large",
    ]
    
    working_models = []
    
    for model in models_to_test:
        print(f"\n🧪 Testing: {model}")
        if await test_perplexity_model(model):
            working_models.append(model)
            print(f"🎉 Found working model: {model}")
            break  # Stop after finding the first working model
    
    if working_models:
        print(f"\n✅ Working models found: {working_models}")
        return working_models[0]
    else:
        print("\n❌ No working models found")
        return None

if __name__ == "__main__":
    result = asyncio.run(main())
    if result:
        print(f"\n🎯 Recommended model name: {result}")
    else:
        print("\n💡 Try checking the Perplexity documentation at: https://docs.perplexity.ai/getting-started/models") 
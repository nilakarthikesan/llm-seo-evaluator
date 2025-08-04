#!/usr/bin/env python3
"""
Test different Perplexity model names to find the correct ones
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
        ],
        "max_tokens": 50
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=data, timeout=10.0)
            
            if response.status_code == 200:
                print(f"✅ {model_name}: SUCCESS")
                return True
            else:
                print(f"❌ {model_name}: {response.status_code} - {response.text[:200]}")
                return False
    except Exception as e:
        print(f"❌ {model_name}: ERROR - {str(e)[:100]}")
        return False

async def test_all_models():
    """Test various Perplexity model names"""
    print("🔍 Testing Perplexity Model Names")
    print("=" * 50)
    
    # Common Perplexity model names to try
    models_to_test = [
        # Try simpler names
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
        "llama-3.1-sonar-large-128k-online"
    ]
    
    working_models = []
    
    for model in models_to_test:
        success = await test_perplexity_model(model)
        if success:
            working_models.append(model)
        await asyncio.sleep(1)  # Rate limiting
    
    print("\n📊 Results Summary:")
    print("=" * 30)
    if working_models:
        print("✅ Working models:")
        for model in working_models:
            print(f"  - {model}")
    else:
        print("❌ No working models found")
    
    return working_models

if __name__ == "__main__":
    asyncio.run(test_all_models()) 
#!/usr/bin/env python3
"""
Final test to find the correct Perplexity model name
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
    """Test completely different Perplexity model names"""
    print("🔍 Testing Alternative Perplexity Model Names")
    print("=" * 50)
    
    # Try completely different model names that might be current
    models_to_test = [
        # Try with different naming patterns
        "mixtral-8x7b-instruct",
        "llama-2-70b-chat",
        "codellama-34b-instruct",
        "mistral-7b-instruct",
        "llama-2-13b-chat",
        "llama-2-7b-chat",
        # Try with different prefixes
        "perplexity-mixtral-8x7b",
        "perplexity-llama-2-70b",
        "perplexity-codellama-34b",
        # Try with different suffixes
        "mixtral-8x7b-online",
        "llama-2-70b-online",
        "codellama-34b-online",
        # Try with different versions
        "mixtral-8x7b-instruct-v0.1",
        "llama-2-70b-chat-v0.1",
        "codellama-34b-instruct-v0.1",
        # Try with different naming conventions
        "mixtral-8x7b-instruct-online",
        "llama-2-70b-chat-online",
        "codellama-34b-instruct-online",
        # Try with different model families
        "gpt-4",
        "gpt-3.5-turbo",
        "claude-3-sonnet",
        "claude-3-haiku",
        "claude-3-opus",
        # Try with different naming patterns
        "sonar-small-2024",
        "sonar-medium-2024",
        "sonar-large-2024",
        # Try with different suffixes
        "sonar-small-latest",
        "sonar-medium-latest",
        "sonar-large-latest",
        # Try with different prefixes
        "p-sonar-small",
        "p-sonar-medium",
        "p-sonar-large",
        # Try with different naming conventions
        "sonar-small-v1",
        "sonar-medium-v1",
        "sonar-large-v1",
        # Try with different naming patterns
        "sonar-small-beta",
        "sonar-medium-beta",
        "sonar-large-beta",
        # Try with different naming conventions
        "sonar-small-alpha",
        "sonar-medium-alpha",
        "sonar-large-alpha",
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
        print("\n💡 The Perplexity model names seem to have changed significantly.")
        print("💡 Please check the current documentation at: https://docs.perplexity.ai/getting-started/models")
        print("💡 Or try visiting: https://docs.perplexity.ai/guides/model-cards")
        return None

if __name__ == "__main__":
    result = asyncio.run(main())
    if result:
        print(f"\n🎯 Recommended model name: {result}")
    else:
        print("\n💡 For now, let's focus on the working providers (OpenAI and Anthropic)")
        print("💡 We can add Perplexity back once we find the correct model names.") 
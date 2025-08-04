#!/usr/bin/env python3
"""
Quick test to verify 'sonar-pro' model name from Perplexity documentation
"""
import os
import asyncio
import httpx
from dotenv import load_dotenv

load_dotenv()

async def test_sonar_pro():
    """Test the 'sonar-pro' model name from the documentation"""
    api_key = os.getenv('PERPLEXITY_API_KEY')
    if not api_key:
        print("ERROR: PERPLEXITY_API_KEY not found")
        return False
    
    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "sonar-pro",
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
                print("SUCCESS: 'sonar-pro' is the correct model name!")
                result = response.json()
                print(f"Response received: {len(result.get('choices', [{}])[0].get('message', {}).get('content', ''))} characters")
                return True
            else:
                print(f"FAILED: Status: {response.status_code}")
                if response.status_code == 400:
                    error_text = response.text
                    print(f"   Error: {error_text[:200]}...")
                return False
                
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing 'sonar-pro' model name from Perplexity documentation")
    print("=" * 60)
    result = asyncio.run(test_sonar_pro())
    if result:
        print("\nSUCCESS: 'sonar-pro' is the correct Perplexity model name!")
        print("We can now update the configuration and enable Perplexity!")
    else:
        print("\nERROR: 'sonar-pro' is not working. Let me try other variations...") 
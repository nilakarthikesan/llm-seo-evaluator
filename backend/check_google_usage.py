#!/usr/bin/env python3
"""
Check Google API usage and rate limits
"""
import os
import asyncio
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

async def check_google_usage():
    """Check current Google API usage"""
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("❌ GOOGLE_API_KEY not found")
        return
    
    print("🔍 Checking Google API Usage")
    print("=" * 40)
    
    try:
        # Configure Google AI
        genai.configure(api_key=api_key)
        
        # Test different models to see current limits
        models_to_test = [
            "gemini-1.5-pro",
            "gemini-1.5-flash"
        ]
        
        for model_name in models_to_test:
            print(f"\n🧪 Testing {model_name}:")
            try:
                model = genai.GenerativeModel(model_name)
                response = await model.generate_content_async("Test message")
                print(f"✅ {model_name}: Working (no rate limit)")
            except Exception as e:
                error_str = str(e)
                if "429" in error_str:
                    print(f"❌ {model_name}: Rate limited (429 error)")
                    print(f"   This indicates you're on free tier")
                elif "quota" in error_str.lower():
                    print(f"❌ {model_name}: Quota exceeded")
                    print(f"   Consider upgrading to paid plan")
                else:
                    print(f"❌ {model_name}: {error_str}")
        
        print(f"\n💡 Recommendations:")
        print(f"   - If you see 429 errors: You're on free tier")
        print(f"   - If you see quota errors: Consider paid plan")
        print(f"   - If all models work: You might already have paid plan")
        
    except Exception as e:
        print(f"❌ Error checking usage: {e}")

if __name__ == "__main__":
    asyncio.run(check_google_usage()) 
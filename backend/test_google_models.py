#!/usr/bin/env python3
"""
Test different Google Gemini models to find alternatives
"""
import os
import asyncio
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

async def test_google_model(model_name: str):
    """Test a specific Google Gemini model"""
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("ERROR: GOOGLE_API_KEY not found")
        return False
    
    try:
        # Configure Google AI
        genai.configure(api_key=api_key)
        
        # Test the model
        model = genai.GenerativeModel(model_name)
        response = await model.generate_content_async("Hello, this is a test message.")
        
        if response:
            print(f"SUCCESS: {model_name}")
            print(f"Response: {len(response.text)} characters")
            return True
        else:
            print(f"FAILED: {model_name} - No response")
            return False
            
    except Exception as e:
        print(f"ERROR: {model_name} - {str(e)}")
        return False

async def main():
    """Test different Google Gemini models"""
    print("Testing Google Gemini Models")
    print("=" * 40)
    
    # Common Google Gemini models to test
    models_to_test = [
        "gemini-1.5-pro",
        "gemini-1.5-flash", 
        "gemini-1.0-pro",
        "gemini-1.0-flash",
        "gemini-pro",
        "gemini-pro-vision"
    ]
    
    working_models = []
    
    for model in models_to_test:
        print(f"\nTesting: {model}")
        if await test_google_model(model):
            working_models.append(model)
            print(f"Found working model: {model}")
    
    if working_models:
        print(f"\nWorking models: {working_models}")
        print(f"\nRecommendation: Try using {working_models[0]} instead of gemini-1.5-pro")
    else:
        print("\nNo working models found")
        print("\nThis suggests all models are rate limited or API key issues")

if __name__ == "__main__":
    asyncio.run(main()) 
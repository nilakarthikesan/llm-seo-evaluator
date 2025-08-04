#!/usr/bin/env python3
"""
Test to isolate which import is causing the hanging issue
"""
import sys
import time

def test_imports():
    """Test each import individually to find the problematic one"""
    print("🔍 Testing imports individually")
    print("=" * 40)
    
    # Test 1: Basic Python imports
    print("1. Testing basic Python imports...")
    try:
        import os
        import logging
        print("✅ Basic imports successful")
    except Exception as e:
        print(f"❌ Basic imports failed: {e}")
        return
    
    # Test 2: httpx import
    print("2. Testing httpx import...")
    try:
        import httpx
        print(f"✅ httpx import successful (version: {httpx.__version__})")
    except Exception as e:
        print(f"❌ httpx import failed: {e}")
        return
    
    # Test 3: pydantic import
    print("3. Testing pydantic import...")
    try:
        import pydantic
        print(f"✅ pydantic import successful (version: {pydantic.__version__})")
    except Exception as e:
        print(f"❌ pydantic import failed: {e}")
        return
    
    # Test 4: OpenAI import (with timeout)
    print("4. Testing OpenAI import...")
    try:
        import signal
        
        def timeout_handler(signum, frame):
            raise TimeoutError("OpenAI import timed out")
        
        # Set a 10-second timeout
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(10)
        
        import openai
        signal.alarm(0)  # Cancel the alarm
        print(f"✅ OpenAI import successful (version: {openai.__version__})")
    except TimeoutError:
        print("❌ OpenAI import timed out (hanging)")
        return
    except Exception as e:
        print(f"❌ OpenAI import failed: {e}")
        return
    
    # Test 5: Anthropic import
    print("5. Testing Anthropic import...")
    try:
        import anthropic
        print(f"✅ Anthropic import successful (version: {anthropic.__version__})")
    except Exception as e:
        print(f"❌ Anthropic import failed: {e}")
        return
    
    # Test 6: Supabase import
    print("6. Testing Supabase import...")
    try:
        import supabase
        print(f"✅ Supabase import successful")
    except Exception as e:
        print(f"❌ Supabase import failed: {e}")
        return
    
    print("\n🎉 All imports successful!")

if __name__ == "__main__":
    test_imports() 
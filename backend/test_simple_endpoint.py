#!/usr/bin/env python3
"""
Simple test to check JSON serialization
"""
import asyncio
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_json():
    """Test JSON serialization"""
    print("🔍 Testing JSON Serialization")
    print("=" * 40)
    
    try:
        from app.services.orchestrator import QueryOrchestrator
        
        # Create orchestrator
        orchestrator = QueryOrchestrator()
        
        # Get results
        query_id = "8dfbb416-0184-416a-aa5e-a4ef817f8250"
        results = await orchestrator.get_query_results(query_id)
        
        if results:
            print(f"✅ Results retrieved")
            
            # Try to serialize to JSON
            try:
                json_str = json.dumps(results, indent=2)
                print(f"✅ JSON serialization successful")
                print(f"JSON length: {len(json_str)} characters")
                print(f"First 200 chars: {json_str[:200]}...")
            except Exception as e:
                print(f"❌ JSON serialization failed: {e}")
                
                # Check what's causing the issue
                print(f"\n🔍 Checking individual fields:")
                for key, value in results.items():
                    try:
                        json.dumps(value)
                        print(f"  ✅ {key}: serializable")
                    except Exception as e:
                        print(f"  ❌ {key}: {e}")
                        
        else:
            print(f"❌ No results found")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_json()) 
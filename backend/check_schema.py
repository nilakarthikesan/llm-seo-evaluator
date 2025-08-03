#!/usr/bin/env python3
"""
Check the actual database schema to see what columns exist
"""
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def check_schema():
    """Check database schema"""
    try:
        from supabase import create_client
        
        # Get Supabase configuration from environment
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY')
        
        if not supabase_url or not supabase_key:
            print("❌ SUPABASE_URL or SUPABASE_KEY not found in environment")
            return
        
        print(f"🔗 Connecting to: {supabase_url}")
        
        # Create Supabase client
        supabase = create_client(supabase_url, supabase_key)
        
        # Check queries table schema
        print("📋 Checking queries table schema...")
        try:
            # Try to get table info
            response = supabase.table('queries').select('*').limit(1).execute()
            if response.data:
                print("✅ Queries table exists and has data")
                print(f"📊 Sample record keys: {list(response.data[0].keys())}")
                print(f"📊 Sample record: {response.data[0]}")
            else:
                print("⚠️ Queries table exists but is empty")
        except Exception as e:
            print(f"❌ Error accessing queries table: {e}")
        
        # Check responses table schema
        print("\n📋 Checking responses table schema...")
        try:
            response = supabase.table('responses').select('*').limit(1).execute()
            if response.data:
                print("✅ Responses table exists and has data")
                print(f"📊 Sample record keys: {list(response.data[0].keys())}")
            else:
                print("⚠️ Responses table exists but is empty")
        except Exception as e:
            print(f"❌ Error accessing responses table: {e}")
        
        # Check evaluation_metrics table schema
        print("\n📋 Checking evaluation_metrics table schema...")
        try:
            response = supabase.table('evaluation_metrics').select('*').limit(1).execute()
            if response.data:
                print("✅ Evaluation_metrics table exists and has data")
                print(f"📊 Sample record keys: {list(response.data[0].keys())}")
            else:
                print("⚠️ Evaluation_metrics table exists but is empty")
        except Exception as e:
            print(f"❌ Error accessing evaluation_metrics table: {e}")
        
    except Exception as e:
        print(f"❌ Schema check failed: {e}")

if __name__ == "__main__":
    asyncio.run(check_schema()) 
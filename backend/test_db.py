#!/usr/bin/env python3
"""
Test Supabase connection using the proper Supabase client
"""
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_connection():
    """Test Supabase connection"""
    try:
        from supabase import create_client
        
        # Get Supabase configuration from environment
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY')
        
        if not supabase_url or not supabase_key:
            print("❌ SUPABASE_URL or SUPABASE_KEY not found in environment")
            print("Please add these to your .env file:")
            print("SUPABASE_URL=https://jqezixpwdtltgcdjltkn.supabase.co")
            print("SUPABASE_KEY=your_supabase_anon_key_here")
            return
        
        print(f"🔗 Testing Supabase connection to: {supabase_url}")
        
        # Create Supabase client
        supabase = create_client(supabase_url, supabase_key)
        
        # Test connection by querying the queries table
        print("🔄 Testing table query...")
        response = supabase.table('queries').select('*').limit(1).execute()
        
        print("✅ Supabase connection successful!")
        print(f"📊 Found {len(response.data)} records in queries table")
        
        # Test inserting a test record
        print("🔄 Testing insert...")
        test_data = {
            "prompt": "Test query from Supabase client",
            "category": "test",
            "status": "pending"
        }
        
        insert_response = supabase.table('queries').insert(test_data).execute()
        print(f"✅ Insert successful! Created record with ID: {insert_response.data[0]['id']}")
        
        # Clean up - delete the test record
        test_id = insert_response.data[0]['id']
        supabase.table('queries').delete().eq('id', test_id).execute()
        print(f"🧹 Cleaned up test record: {test_id}")
        
        print("✅ All Supabase tests passed!")
        
    except Exception as e:
        print(f"❌ Supabase connection failed: {e}")
        print("\n🔍 Troubleshooting tips:")
        print("1. Check if your Supabase project is active")
        print("2. Verify the SUPABASE_URL is correct")
        print("3. Make sure the SUPABASE_KEY (anon key) is correct")
        print("4. Check if you have the proper permissions")

if __name__ == "__main__":
    asyncio.run(test_connection()) 
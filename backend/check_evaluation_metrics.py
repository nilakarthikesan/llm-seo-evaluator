#!/usr/bin/env python3
"""
Check evaluation metrics in the database
"""
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def check_evaluation_metrics():
    """Check evaluation metrics in the database"""
    print("🔍 Checking Evaluation Metrics")
    print("=" * 40)
    
    try:
        from app.core.supabase import get_supabase
        
        supabase = get_supabase()
        
        # Get all evaluation metrics
        response = supabase.table('evaluation_metrics').select('*').execute()
        
        print(f"📊 Found {len(response.data)} evaluation metrics records")
        
        for i, metric in enumerate(response.data):
            print(f"\n📈 Evaluation Metric {i+1}:")
            print(f"  ID: {metric.get('id')}")
            print(f"  Query ID: {metric.get('query_id')}")
            print(f"  Response ID: {metric.get('response_id')}")
            print(f"  Originality Score: {metric.get('originality_score')}")
            print(f"  Factuality Score: {metric.get('factuality_score')}")
            print(f"  Readability Score: {metric.get('readability_score')}")
            print(f"  Keyword Count: {metric.get('keyword_count')}")
            print(f"  Tools Mentioned: {metric.get('tool_mentions')}")
            print(f"  SEO Terms: {metric.get('seo_terms')}")
            print(f"  Response Length: {metric.get('response_length')}")
            print(f"  Computed At: {metric.get('computed_at')}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(check_evaluation_metrics()) 
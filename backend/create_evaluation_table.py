#!/usr/bin/env python3
"""
Create evaluation metrics table if it doesn't exist
"""
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def create_evaluation_table():
    """Create evaluation metrics table if it doesn't exist"""
    print("🔍 Checking/Creating Evaluation Metrics Table")
    print("=" * 50)
    
    try:
        from app.core.supabase import get_supabase
        
        supabase = get_supabase()
        
        # Check if table exists by trying to query it
        try:
            response = supabase.table('evaluation_metrics').select('*').limit(1).execute()
            print("✅ Evaluation metrics table exists")
            print(f"📊 Found {len(response.data)} records")
        except Exception as e:
            print(f"❌ Evaluation metrics table doesn't exist: {e}")
            print("🔄 Creating evaluation metrics table...")
            
            # Create the table using SQL
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS evaluation_metrics (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                query_id UUID NOT NULL REFERENCES queries(id) ON DELETE CASCADE,
                response_id UUID NOT NULL REFERENCES responses(id) ON DELETE CASCADE,
                similarity_scores JSONB DEFAULT '[]',
                average_similarity FLOAT DEFAULT 0.0,
                originality_score FLOAT DEFAULT 0.0,
                factuality_score FLOAT DEFAULT 0.0,
                readability_score FLOAT DEFAULT 0.0,
                keyword_count INTEGER DEFAULT 0,
                keyword_list TEXT[] DEFAULT '{}',
                tool_mentions TEXT[] DEFAULT '{}',
                seo_terms TEXT[] DEFAULT '{}',
                response_length INTEGER DEFAULT 0,
                response_complexity FLOAT DEFAULT 0.0,
                analysis_version TEXT DEFAULT '1.0',
                computed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
            """
            
            # Execute the SQL
            result = supabase.rpc('exec_sql', {'sql': create_table_sql}).execute()
            print("✅ Evaluation metrics table created successfully")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n📋 Manual table creation required:")
        print("Please create the evaluation_metrics table in your Supabase dashboard with the following SQL:")
        print("""
        CREATE TABLE evaluation_metrics (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            query_id UUID NOT NULL REFERENCES queries(id) ON DELETE CASCADE,
            response_id UUID NOT NULL REFERENCES responses(id) ON DELETE CASCADE,
            similarity_scores JSONB DEFAULT '[]',
            average_similarity FLOAT DEFAULT 0.0,
            originality_score FLOAT DEFAULT 0.0,
            factuality_score FLOAT DEFAULT 0.0,
            readability_score FLOAT DEFAULT 0.0,
            keyword_count INTEGER DEFAULT 0,
            keyword_list TEXT[] DEFAULT '{}',
            tool_mentions TEXT[] DEFAULT '{}',
            seo_terms TEXT[] DEFAULT '{}',
            response_length INTEGER DEFAULT 0,
            response_complexity FLOAT DEFAULT 0.0,
            analysis_version TEXT DEFAULT '1.0',
            computed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        """)

if __name__ == "__main__":
    asyncio.run(create_evaluation_table()) 
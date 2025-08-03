#!/usr/bin/env python3
"""
Test the evaluation service
"""
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_evaluation():
    """Test the evaluation service"""
    print("🔍 Testing Evaluation Service")
    print("=" * 40)
    
    try:
        from app.services.evaluation import EvaluationService
        
        # Create evaluation service
        evaluation_service = EvaluationService()
        print("✅ Evaluation service created successfully")
        
        # Test with sample responses
        sample_responses = [
            {
                'id': '1',
                'response_text': 'SEO optimization involves improving your website for search engines. Key factors include keyword research, content quality, and technical optimization. Tools like Google Analytics and Search Console help track performance.',
                'provider': 'openai',
                'model': 'gpt-4'
            },
            {
                'id': '2', 
                'response_text': 'Search engine optimization requires technical and content improvements. Focus on keywords, meta tags, and user experience. Use Google Analytics and SEMrush for monitoring rankings and traffic.',
                'provider': 'anthropic',
                'model': 'claude-3'
            }
        ]
        
        print(f"\n📊 Evaluating {len(sample_responses)} responses...")
        
        # Evaluate all responses
        results = evaluation_service.evaluate_all_responses(sample_responses, category='technical')
        
        print(f"✅ Evaluation completed")
        print(f"Average similarity: {results['average_similarity']:.3f}")
        print(f"Similarity matrix: {results['similarity_matrix']}")
        
        # Show individual response metrics
        for response_id, metrics in results['response_metrics'].items():
            print(f"\n📈 Response {response_id} metrics:")
            print(f"  Originality: {metrics['originality_score']:.3f}")
            print(f"  Factuality: {metrics['factuality_score']:.3f}")
            print(f"  Readability: {metrics['readability_score']:.3f}")
            print(f"  Keywords: {metrics['keyword_count']}")
            print(f"  Tools mentioned: {metrics['tool_mentions']}")
            print(f"  SEO terms: {metrics['seo_terms']}")
        
        # Show overall metrics
        overall = results['overall_metrics']
        print(f"\n📊 Overall metrics:")
        print(f"  Avg originality: {overall['avg_originality']:.3f}")
        print(f"  Avg factuality: {overall['avg_factuality']:.3f}")
        print(f"  Avg readability: {overall['avg_readability']:.3f}")
        print(f"  Total keywords: {overall['total_keywords']}")
        print(f"  Total tools: {overall['total_tools']}")
        print(f"  Total SEO terms: {overall['total_seo_terms']}")
        
    except Exception as e:
        print(f"❌ Evaluation test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_evaluation()) 
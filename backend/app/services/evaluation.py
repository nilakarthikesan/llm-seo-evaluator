import re
import math
from typing import List, Dict, Any, Tuple
from collections import Counter
import logging
import numpy as np

logger = logging.getLogger(__name__)

# Disable sklearn for now to avoid import issues
SKLEARN_AVAILABLE = False

class EvaluationService:
    """Service for evaluating and comparing LLM responses"""
    
    def __init__(self):
        self.seo_keywords = {
            'technical': ['seo', 'meta tags', 'schema markup', 'structured data', 'robots.txt', 
                         'sitemap', 'canonical', 'redirects', 'page speed', 'core web vitals',
                         'mobile friendly', 'responsive design', 'https', 'ssl', 'domain authority'],
            'content': ['content marketing', 'keyword research', 'content strategy', 'blog posts',
                       'landing pages', 'meta descriptions', 'title tags', 'heading tags', 'alt text',
                       'internal linking', 'content optimization', 'readability', 'engagement'],
            'automation': ['python', 'script', 'automation', 'api', 'web scraping', 'data analysis',
                          'reporting', 'dashboard', 'cron job', 'scheduled task', 'workflow',
                          'integration', 'webhook', 'bot', 'crawler'],
            'analytics': ['google analytics', 'search console', 'semrush', 'ahrefs', 'moz',
                         'screaming frog', 'data visualization', 'kpi', 'metrics', 'reporting',
                         'tracking', 'conversion', 'traffic', 'rankings']
        }
        
        self.seo_tools = [
            'google analytics', 'search console', 'semrush', 'ahrefs', 'moz', 'screaming frog',
            'screaming frog seo spider', 'google tag manager', 'gtm', 'google ads', 'bing ads',
            'facebook ads', 'linkedin ads', 'twitter ads', 'hotjar', 'crazy egg', 'optimizely',
            'vwo', 'unbounce', 'leadpages', 'wordpress', 'shopify', 'woocommerce', 'magento'
        ]
    
    def calculate_similarity_matrix(self, responses: List[Dict[str, Any]]) -> Tuple[List[List[float]], float]:
        """Calculate similarity matrix between all responses"""
        if len(responses) < 2:
            return [[1.0]], 1.0
        
        # Extract response texts
        texts = [resp['response_text'] for resp in responses if resp.get('response_text')]
        
        if len(texts) < 2:
            return [[1.0]], 1.0
        
        if SKLEARN_AVAILABLE:
            # Use TF-IDF and cosine similarity
            try:
                vectorizer = TfidfVectorizer(
                    stop_words='english',
                    ngram_range=(1, 2),
                    max_features=1000
                )
                
                tfidf_matrix = vectorizer.fit_transform(texts)
                similarity_matrix = cosine_similarity(tfidf_matrix)
                
                # Calculate average similarity (excluding self-similarity)
                total_similarity = 0
                count = 0
                for i in range(len(similarity_matrix)):
                    for j in range(len(similarity_matrix[i])):
                        if i != j:
                            total_similarity += similarity_matrix[i][j]
                            count += 1
                
                avg_similarity = total_similarity / count if count > 0 else 1.0
                
                return similarity_matrix.tolist(), avg_similarity
                
            except Exception as e:
                logger.error(f"Error calculating similarity matrix with sklearn: {e}")
                return self._fallback_similarity_calculation(texts)
        else:
            # Use fallback calculation
            return self._fallback_similarity_calculation(texts)
    
    def _fallback_similarity_calculation(self, texts: List[str]) -> Tuple[List[List[float]], float]:
        """Fallback similarity calculation using word overlap"""
        size = len(texts)
        similarity_matrix = [[0.0 for _ in range(size)] for _ in range(size)]
        
        for i in range(size):
            for j in range(size):
                if i == j:
                    similarity_matrix[i][j] = 1.0
                else:
                    # Calculate word overlap similarity
                    words_i = set(texts[i].lower().split())
                    words_j = set(texts[j].lower().split())
                    
                    if words_i and words_j:
                        intersection = len(words_i.intersection(words_j))
                        union = len(words_i.union(words_j))
                        similarity_matrix[i][j] = intersection / union if union > 0 else 0.0
                    else:
                        similarity_matrix[i][j] = 0.0
        
        # Calculate average similarity
        total_similarity = 0
        count = 0
        for i in range(size):
            for j in range(size):
                if i != j:
                    total_similarity += similarity_matrix[i][j]
                    count += 1
        
        avg_similarity = total_similarity / count if count > 0 else 0.0
        
        return similarity_matrix, avg_similarity
    
    def extract_keywords(self, text: str, category: str = None) -> Dict[str, Any]:
        """Extract keywords, tools, and SEO terms from text"""
        if not text:
            return {
                'keywords': [],
                'tools': [],
                'seo_terms': [],
                'keyword_count': 0,
                'tool_count': 0,
                'seo_term_count': 0
            }
        
        # Convert to lowercase for matching
        text_lower = text.lower()
        
        # Extract keywords (words that appear multiple times)
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text_lower)
        word_freq = Counter(words)
        keywords = [word for word, freq in word_freq.items() if freq >= 2]
        
        # Extract tools mentioned
        tools_found = []
        for tool in self.seo_tools:
            if tool.lower() in text_lower:
                tools_found.append(tool)
        
        # Extract SEO terms
        seo_terms = []
        if category and category in self.seo_keywords:
            for term in self.seo_keywords[category]:
                if term.lower() in text_lower:
                    seo_terms.append(term)
        
        return {
            'keywords': keywords,
            'tools': tools_found,
            'seo_terms': seo_terms,
            'keyword_count': len(keywords),
            'tool_count': len(tools_found),
            'seo_term_count': len(seo_terms)
        }
    
    def calculate_readability_score(self, text: str) -> float:
        """Calculate readability score (0.0 to 1.0)"""
        if not text:
            return 0.0
        
        # Simple readability calculation based on sentence and word complexity
        sentences = re.split(r'[.!?]+', text)
        words = text.split()
        
        if not sentences or not words:
            return 0.0
        
        # Average sentence length
        avg_sentence_length = len(words) / len(sentences)
        
        # Word complexity (percentage of long words)
        long_words = [word for word in words if len(word) > 6]
        word_complexity = len(long_words) / len(words) if words else 0
        
        # Calculate readability score (higher is more readable)
        # Normalize sentence length (shorter is better, up to a point)
        sentence_score = max(0, 1 - (avg_sentence_length - 15) / 20)
        complexity_score = max(0, 1 - word_complexity)
        
        # Combine scores
        readability = (sentence_score + complexity_score) / 2
        return max(0.0, min(1.0, readability))
    
    def calculate_originality_score(self, text: str, all_texts: List[str]) -> float:
        """Calculate originality score based on uniqueness compared to other responses"""
        if not text or not all_texts:
            return 1.0
        
        # Simple n-gram based originality
        text_words = set(text.lower().split())
        
        if not text_words:
            return 1.0
        
        # Calculate overlap with other texts
        total_overlap = 0
        for other_text in all_texts:
            if other_text != text:
                other_words = set(other_text.lower().split())
                overlap = len(text_words.intersection(other_words))
                total_overlap += overlap / len(text_words) if text_words else 0
        
        avg_overlap = total_overlap / (len(all_texts) - 1) if len(all_texts) > 1 else 0
        originality = 1 - avg_overlap
        return max(0.0, min(1.0, originality))
    
    def calculate_factuality_score(self, text: str) -> float:
        """Calculate factuality score based on presence of factual indicators"""
        if not text:
            return 0.0
        
        text_lower = text.lower()
        
        # Factual indicators
        factual_indicators = [
            'according to', 'research shows', 'studies indicate', 'data suggests',
            'statistics show', 'analysis reveals', 'evidence suggests', 'findings indicate',
            'report shows', 'survey indicates', 'study found', 'research indicates'
        ]
        
        # Count factual indicators
        factual_count = sum(1 for indicator in factual_indicators if indicator in text_lower)
        
        # Normalize by text length
        word_count = len(text.split())
        if word_count == 0:
            return 0.0
        
        factuality = min(1.0, factual_count / (word_count / 100))  # Per 100 words
        return factuality
    
    def evaluate_response(self, response: Dict[str, Any], all_responses: List[Dict[str, Any]], 
                         category: str = None) -> Dict[str, Any]:
        """Comprehensive evaluation of a single response"""
        text = response.get('response_text', '')
        
        # Extract keywords and tools
        keyword_analysis = self.extract_keywords(text, category)
        
        # Calculate various scores
        readability_score = self.calculate_readability_score(text)
        originality_score = self.calculate_originality_score(text, [r.get('response_text', '') for r in all_responses])
        factuality_score = self.calculate_factuality_score(text)
        
        # Calculate response complexity
        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        response_complexity = len(words) / len(sentences) if sentences and words else 0
        
        return {
            'originality_score': originality_score,
            'factuality_score': factuality_score,
            'readability_score': readability_score,
            'keyword_count': keyword_analysis['keyword_count'],
            'keyword_list': keyword_analysis['keywords'],
            'tool_mentions': keyword_analysis['tools'],
            'seo_terms': keyword_analysis['seo_terms'],
            'response_length': len(text),
            'response_complexity': response_complexity
        }
    
    def evaluate_all_responses(self, responses: List[Dict[str, Any]], category: str = None) -> Dict[str, Any]:
        """Evaluate all responses and generate comprehensive metrics"""
        if not responses:
            return {
                'similarity_matrix': [],
                'average_similarity': 0.0,
                'response_metrics': {},
                'overall_metrics': {}
            }
        
        # Calculate similarity matrix
        similarity_matrix, avg_similarity = self.calculate_similarity_matrix(responses)
        
        # Evaluate each response
        response_metrics = {}
        for response in responses:
            response_id = response.get('id')
            if response_id:
                response_metrics[str(response_id)] = self.evaluate_response(response, responses, category)
        
        # Calculate overall metrics
        all_scores = list(response_metrics.values())
        overall_metrics = {
            'avg_originality': np.mean([m['originality_score'] for m in all_scores]) if all_scores else 0.0,
            'avg_factuality': np.mean([m['factuality_score'] for m in all_scores]) if all_scores else 0.0,
            'avg_readability': np.mean([m['readability_score'] for m in all_scores]) if all_scores else 0.0,
            'total_keywords': sum(m['keyword_count'] for m in all_scores),
            'total_tools': len(set().union(*[set(m['tool_mentions']) for m in all_scores])),
            'total_seo_terms': len(set().union(*[set(m['seo_terms']) for m in all_scores]))
        }
        
        return {
            'similarity_matrix': similarity_matrix,
            'average_similarity': avg_similarity,
            'response_metrics': response_metrics,
            'overall_metrics': overall_metrics
        } 
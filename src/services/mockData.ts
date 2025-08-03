import { QueryResults, LLMResponse, EvaluationMetrics, ProgressUpdate } from '@/types/llm';

// Rich mock data for development and testing
export const mockQueryResults: QueryResults = {
  query: {
    id: "abc-123-def-456",
    prompt: "What are the best Python automation scripts for SEO in 2025?",
    category: "automation",
    tags: ["python", "seo", "scripts", "automation", "2025"],
    providers: ["openai", "claude", "perplexity"],
    created_at: "2025-08-03T10:30:00Z",
    status: "complete"
  },
  responses: [
    {
      id: "resp-openai-1",
      provider: "openai",
      model: "gpt-4",
      response_text: `Here are the top Python SEO automation scripts for 2025:

## 1. Advanced Web Scraping & Analysis
\`\`\`python
import requests
from bs4 import BeautifulSoup
import pandas as pd

def seo_site_analyzer(url):
    """Comprehensive SEO analysis tool"""
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract meta data
    title = soup.find('title').text if soup.find('title') else 'No title'
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    
    return {
        'title': title,
        'title_length': len(title),
        'meta_description': meta_desc.get('content') if meta_desc else None,
        'h1_tags': [h1.text for h1 in soup.find_all('h1')],
        'internal_links': len(soup.find_all('a', href=True))
    }
\`\`\`

## 2. Google Search Console API Integration
- Automate ranking tracking
- Pull click-through rates and impressions
- Monitor Core Web Vitals programmatically

## 3. Schema Markup Generator
Automatically generate structured data for different content types using Python templates.

## 4. Technical SEO Audit Scripts
- Page speed analysis
- Mobile-friendliness testing
- SSL certificate validation
- Sitemap validation

## 5. Content Gap Analysis Tool
Compare your content against competitors to identify opportunities.

These scripts leverage modern libraries like Scrapy, Selenium, and FastAPI to create powerful SEO workflows.`,
      metadata: {
        tokens_used: 487,
        response_time_ms: 15300
      }
    },
    {
      id: "resp-claude-2",
      provider: "claude",
      model: "claude-3-sonnet",
      response_text: `Python SEO automation has evolved significantly in 2025. Here are the essential scripts every SEO professional should have:

## Essential SEO Automation Tools

### 1. Advanced Web Scraping Framework
\`\`\`python
from selenium import webdriver
from selenium.webdriver.common.by import By
import asyncio
import aiohttp

class SEOCrawler:
    def __init__(self):
        self.driver = webdriver.Chrome()
    
    async def analyze_page_speed(self, url):
        """Get Core Web Vitals and performance metrics"""
        # Implementation for Lighthouse integration
        pass
    
    def extract_competitors_keywords(self, domain):
        """Analyze competitor keyword strategies"""
        # Advanced SERP analysis
        pass
\`\`\`

### 2. Content Optimization Pipeline
- Automated keyword density analysis
- Readability score calculation
- Topic clustering and content gaps
- Internal linking recommendations

### 3. Technical SEO Monitoring
- Log file analysis for crawl errors
- Redirect chain detection
- Image optimization checks
- Page load time monitoring

### 4. SERP Tracking & Analysis
Build custom SERP trackers that monitor:
- Position changes over time
- Featured snippet opportunities
- Local pack rankings
- SERP features presence

### 5. Link Building Automation
- Prospect identification scripts
- Email outreach templates
- Backlink monitoring and alerts
- Broken link finding tools

The key is building modular, reusable components that can be combined into powerful SEO workflows. Focus on API integrations with tools like Screaming Frog, Ahrefs, and Google's suite of tools.`,
      metadata: {
        tokens_used: 392,
        response_time_ms: 22100
      }
    },
    {
      id: "resp-perplexity-3",
      provider: "perplexity",
      model: "llama-3.1-sonar-large-128k-online",
      response_text: `Based on the latest developments in SEO automation for 2025, here are the most effective Python scripts:

## 1. AI-Enhanced Content Analysis
\`\`\`python
import openai
from textstat import flesch_reading_ease
import nltk

def ai_content_optimizer(content):
    """Use AI to optimize content for SEO"""
    # Analyze readability
    readability = flesch_reading_ease(content)
    
    # Extract entities and topics
    entities = nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(content)))
    
    # Get AI suggestions for improvement
    prompt = f"Optimize this content for SEO: {content[:500]}..."
    suggestions = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return {
        'readability_score': readability,
        'entities': entities,
        'ai_suggestions': suggestions.choices[0].message.content
    }
\`\`\`

## 2. Real-Time SERP Monitoring
- Track keyword positions across multiple search engines
- Monitor competitor movements
- Alert on ranking changes

## 3. E-A-T Analysis Tools
Scripts that evaluate:
- Author expertise signals
- Content authority indicators  
- Trustworthiness factors
- Citation and reference quality

## 4. Core Web Vitals Automation
- Lighthouse CI integration
- Performance budgets monitoring
- Mobile vs desktop performance comparison
- PageSpeed Insights API automation

## 5. Local SEO Automation
- Google My Business posting automation
- Citation consistency checking
- Local keyword tracking
- Review monitoring and response

## 6. Voice Search Optimization
- Featured snippet optimization
- Long-tail keyword analysis
- Question-based content identification

These tools integrate with modern APIs and leverage machine learning to provide actionable SEO insights. The focus in 2025 is on AI-assisted analysis and real-time monitoring rather than just data collection.`,
      metadata: {
        tokens_used: 445,
        response_time_ms: 28700
      }
    }
  ],
  evaluation_metrics: {
    similarity_matrix: [
      [1.0, 0.73, 0.68],
      [0.73, 1.0, 0.71], 
      [0.68, 0.71, 1.0]
    ],
    response_metrics: {
      "resp-openai-1": {
        originality_score: 0.73,
        similarity_to_others: 0.27,
        keyword_count: 15,
        tool_mentions: ["Scrapy", "Selenium", "FastAPI", "BeautifulSoup", "Google Search Console"],
        readability_score: 0.85
      },
      "resp-claude-2": {
        originality_score: 0.67,
        similarity_to_others: 0.33,
        keyword_count: 18,
        tool_mentions: ["Selenium", "Aiohttp", "Screaming Frog", "Ahrefs", "Google"],
        readability_score: 0.78
      },
      "resp-perplexity-3": {
        originality_score: 0.81,
        similarity_to_others: 0.19,
        keyword_count: 22,
        tool_mentions: ["OpenAI", "NLTK", "Lighthouse", "Google My Business", "PageSpeed Insights"],
        readability_score: 0.82
      }
    },
    cross_comparisons: [
      {
        providers: ["openai", "claude"],
        cosine_similarity: 0.73,
        jaccard_similarity: 0.57,
        common_keywords: ["python", "automation", "SEO", "scripts", "selenium", "analysis"],
        tool_overlap: ["Selenium", "Google"]
      },
      {
        providers: ["openai", "perplexity"],
        cosine_similarity: 0.68,
        jaccard_similarity: 0.51,
        common_keywords: ["python", "automation", "SEO", "monitoring", "optimization"],
        tool_overlap: ["Google"]
      },
      {
        providers: ["claude", "perplexity"],
        cosine_similarity: 0.71,
        jaccard_similarity: 0.63,
        common_keywords: ["automation", "SEO", "monitoring", "analysis", "tools", "AI"],
        tool_overlap: ["Google", "Lighthouse"]
      }
    ]
  }
};

// Mock progress updates for WebSocket simulation
export const mockProgressUpdates: ProgressUpdate[] = [
  {
    status: "processing",
    completed_providers: [],
    total_providers: 3,
    message: "Starting LLM queries...",
    progress_percentage: 0
  },
  {
    status: "processing", 
    completed_providers: ["openai"],
    total_providers: 3,
    message: "OpenAI completed (1/3 providers)",
    progress_percentage: 33
  },
  {
    status: "processing",
    completed_providers: ["openai", "claude"],
    total_providers: 3,
    message: "Claude completed (2/3 providers)",
    progress_percentage: 67
  },
  {
    status: "analyzing",
    completed_providers: ["openai", "claude", "perplexity"],
    total_providers: 3,
    message: "All providers complete. Analyzing responses...",
    progress_percentage: 85
  },
  {
    status: "complete",
    completed_providers: ["openai", "claude", "perplexity"],
    total_providers: 3,
    message: "Analysis complete! Results ready.",
    progress_percentage: 100
  }
];

// Additional mock data for dashboard
export const mockTrendData = {
  monthly_queries: [
    { month: 'Jan', queries: 45, providers: ['openai', 'claude'] },
    { month: 'Feb', queries: 52, providers: ['openai', 'claude', 'perplexity'] },
    { month: 'Mar', queries: 38, providers: ['openai', 'claude'] },
    { month: 'Apr', queries: 67, providers: ['openai', 'claude', 'perplexity'] },
    { month: 'May', queries: 72, providers: ['openai', 'claude', 'perplexity', 'gemini'] },
    { month: 'Jun', queries: 84, providers: ['openai', 'claude', 'perplexity', 'gemini'] }
  ],
  popular_categories: [
    { category: 'automation', percentage: 35, queries: 124 },
    { category: 'technical', percentage: 28, queries: 98 },
    { category: 'content', percentage: 22, queries: 78 },
    { category: 'analytics', percentage: 15, queries: 52 }
  ],
  similarity_trends: [
    { date: '2025-07-01', avg_similarity: 0.72 },
    { date: '2025-07-08', avg_similarity: 0.68 },
    { date: '2025-07-15', avg_similarity: 0.75 },
    { date: '2025-07-22', avg_similarity: 0.71 },
    { date: '2025-07-29', avg_similarity: 0.69 },
    { date: '2025-08-05', avg_similarity: 0.73 }
  ]
};
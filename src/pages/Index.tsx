import React, { useState } from 'react';
import { Layout } from '@/components/layout/Layout';
import { QueryForm } from '@/components/query/QueryForm';
import { ProgressTracker } from '@/components/query/ProgressTracker';
import { ResultsDashboard } from '@/components/results/ResultsDashboard';
import { QueryHistory } from '@/components/history/QueryHistory';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { QuerySubmission, QueryResults, Query } from '@/types/llm';
import { apiClient } from '@/services/api';
import { mockQueryResults } from '@/services/mockData';
import { useToast } from '@/hooks/use-toast';

const Index = () => {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [currentResults, setCurrentResults] = useState<QueryResults | null>(null);
  const [showResults, setShowResults] = useState(false);
  const [showProgress, setShowProgress] = useState(false);
  const [currentQuery, setCurrentQuery] = useState<QuerySubmission | null>(null);
  const [queryId, setQueryId] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<string>('new-query');
  const [queryHistory, setQueryHistory] = useState<Query[]>([]);
  const { toast } = useToast();

  const handleQuerySubmit = async (queryData: QuerySubmission) => {
    setIsSubmitting(true);
    setCurrentQuery(queryData);
    
    try {
      console.log('Submitting query:', queryData);
      const response = await apiClient.submitQuery(queryData);
      setQueryId(response.query_id);
      
      toast({
        title: "Query Submitted Successfully! 🚀",
        description: `Query ${response.query_id} is being processed by ${queryData.providers.length} LLM providers.`,
      });
      
      // Show progress tracker
      setIsSubmitting(false);
      setShowProgress(true);
      setActiveTab('progress');
      
    } catch (error) {
      console.error('Error submitting query:', error);
      toast({
        title: "Submission Failed",
        description: "There was an error submitting your query. Please try again.",
        variant: "destructive",
      });
      setIsSubmitting(false);
    }
  };

  const handleProgressComplete = () => {
    if (!currentQuery) return;
    
    // Generate results when progress completes
    setTimeout(() => {
      // Create realistic, diverse responses based on provider characteristics
      const generateProviderResponse = (provider: string, model: string, prompt: string) => {
        const responses: Record<string, string> = {
          openai: `# GPT-4 Analysis: ${prompt}

## Executive Summary
Based on comprehensive analysis, here are the strategic recommendations for "${prompt}":

### 🎯 Primary Strategies
1. **Content-First Approach**: Focus on high-quality, user-intent driven content
2. **Technical Excellence**: Implement Core Web Vitals optimization
3. **E-A-T Signals**: Establish expertise, authoritativeness, and trustworthiness

### 📊 Implementation Roadmap
**Phase 1 (0-30 days):**
- Conduct comprehensive technical audit
- Optimize page speed and mobile experience
- Implement structured data markup

**Phase 2 (30-90 days):**
- Content gap analysis and creation strategy
- Internal linking optimization
- Local SEO improvements (if applicable)

### 🔧 Tools & Technologies
- Google Search Console for monitoring
- PageSpeed Insights for performance
- Screaming Frog for technical SEO
- Ahrefs/SEMrush for keyword research

### 📈 Expected Results
- 25-40% increase in organic traffic within 6 months
- Improved SERP rankings for target keywords
- Enhanced user engagement metrics

*Analysis powered by GPT-4's advanced reasoning capabilities*`,

          claude: `# Claude's Comprehensive SEO Strategy: ${prompt}

## Thoughtful Analysis & Recommendations

I've carefully analyzed your query about "${prompt}" and here's my structured approach:

### 🧠 Strategic Thinking
The modern SEO landscape requires a holistic approach that balances technical excellence with genuine user value. Let me break this down systematically:

### 📋 Detailed Action Plan

**1. Content Strategy Framework**
- Develop topic clusters around your core themes
- Create pillar pages with supporting content
- Focus on search intent alignment
- Implement semantic keyword strategies

**2. Technical Foundation**
- Core Web Vitals optimization (LCP, FID, CLS)
- Mobile-first indexing compliance
- SSL implementation and security headers
- XML sitemap optimization

**3. User Experience Priorities**
- Intuitive navigation structure
- Clear call-to-action placement
- Accessibility compliance (WCAG 2.1)
- Page loading speed optimization

### 🔍 Analytical Considerations
From my analysis, the key differentiator will be:
- Quality over quantity in content creation
- Long-term sustainable growth strategies
- Risk assessment for algorithm changes
- Competitive advantage identification

### 🎯 Success Metrics
- Organic click-through rates
- Average session duration
- Conversion rate improvements
- Brand mention tracking

*Thoughtfully crafted by Claude with attention to nuance and context*`,

          perplexity: `# Real-Time SEO Intelligence: ${prompt}

## Current Market Analysis (Updated December 2024)

Based on the latest search trends and algorithm updates, here's what's working now for "${prompt}":

### 🌐 Latest Industry Insights
According to recent Google algorithm updates and industry reports:

**Recent Algorithm Changes:**
- December 2024 Helpful Content Update focuses on first-hand experience
- Core Web Vitals now include Interaction to Next Paint (INP)
- AI-generated content detection improvements

### 📈 Trending Strategies (Live Data)
1. **Zero-Click Optimization**: Featured snippets and People Also Ask
2. **Video SEO Integration**: YouTube Shorts for quick wins
3. **Local Pack Optimization**: Google Business Profile enhancements
4. **Voice Search Adaptation**: Conversational keyword targeting

### 🔄 Real-Time Competitive Analysis
Current top performers in your space are focusing on:
- Interactive content experiences
- Community-driven engagement
- Multi-channel content distribution
- Rapid response to trending topics

### 📊 Live Performance Metrics
- Average CTR for position 1: 28.5% (industry data)
- Mobile traffic share: 63.7% (Q4 2024)
- Voice search queries: 27% of all searches

### 🛠️ Actionable Next Steps
Based on current search patterns:
1. Implement FAQ schema for voice search
2. Optimize for "near me" local queries
3. Create timely, newsworthy content
4. Leverage real-time social signals

### 📱 Platform-Specific Recommendations
- **Google**: Focus on E-E-A-T and helpful content
- **Bing**: Optimize for ChatGPT integration
- **YouTube**: Short-form educational content
- **Social**: Cross-platform content syndication

*Powered by Perplexity's real-time web search and current data*`,

          gemini: `# Google Gemini SEO Analysis: ${prompt}

## Multimodal Intelligence Report

Comprehensive evaluation of "${prompt}" using advanced AI reasoning:

### 🎯 Strategic Overview
Leveraging Google's deep understanding of search ecosystems, here's the optimal approach:

### 🔬 Advanced Technical Analysis

**Core Algorithm Alignment:**
- RankBrain compatibility scoring
- BERT semantic understanding optimization
- MUM (Multitask Unified Model) content structuring
- Helpful Content System compliance

**Performance Optimization Stack:**
Technical SEO Foundation includes Core Web Vitals (LCP < 2.5s, CLS < 0.1), Mobile-First Architecture, Structured Data Implementation, and International SEO (hreflang).

### 🎨 Content Intelligence Framework

**1. Semantic Content Mapping**
- Entity relationship modeling
- Topic authority development
- Content depth vs. breadth analysis
- User journey optimization

**2. Visual Content Strategy**
- Image SEO with descriptive alt text
- Video content optimization
- Infographic keyword targeting
- Visual search preparation

### 🚀 Innovation Opportunities
- AI-assisted content creation workflows
- Automated technical SEO monitoring
- Predictive keyword trend analysis
- Voice and visual search optimization

### 📊 Measurement & Analytics
**KPI Dashboard:**
- Organic visibility index
- Content performance scoring
- Technical health monitoring
- Competitive positioning analysis

### 🔮 Future-Proofing Strategy
Preparing for emerging search technologies:
- SGE (Search Generative Experience) optimization
- Conversational AI integration
- Augmented reality search features
- IoT device optimization

*Generated by Google Gemini with comprehensive web knowledge integration*`
        };

        return responses[provider] || responses.openai;
      };

      // Create dynamic mock results based on actual query
      const dynamicResults: QueryResults = {
          ...mockQueryResults,
          query: {
            ...mockQueryResults.query,
            prompt: currentQuery.prompt,
            category: currentQuery.category,
            tags: currentQuery.tags,
            providers: currentQuery.providers,
            created_at: new Date().toISOString()
          },
          responses: currentQuery.providers.map((provider, index) => ({
            id: `resp-${provider}-${index + 1}`,
            provider: provider,
            model: provider === 'openai' ? 'gpt-4' : 
                   provider === 'claude' ? 'claude-3-sonnet' :
                   provider === 'perplexity' ? 'llama-3.1-sonar-large-128k-online' :
                   'gemini-pro',
            response_text: generateProviderResponse(provider, 
              provider === 'openai' ? 'GPT-4' : 
              provider === 'claude' ? 'Claude 3 Sonnet' :
              provider === 'perplexity' ? 'Perplexity AI' :
              'Gemini Pro',
              currentQuery.prompt
            ),
            metadata: {
              tokens_used: provider === 'openai' ? Math.floor(Math.random() * 100) + 450 :
                          provider === 'claude' ? Math.floor(Math.random() * 150) + 520 :
                          provider === 'perplexity' ? Math.floor(Math.random() * 80) + 380 :
                          Math.floor(Math.random() * 120) + 420,
              response_time_ms: provider === 'openai' ? Math.floor(Math.random() * 5000) + 12000 :
                               provider === 'claude' ? Math.floor(Math.random() * 8000) + 15000 :
                               provider === 'perplexity' ? Math.floor(Math.random() * 6000) + 18000 :
                               Math.floor(Math.random() * 7000) + 14000
            }
          }))
      };
      
      setCurrentResults(dynamicResults);
      setShowResults(true);
      setShowProgress(false);
      setActiveTab('results');
      
      // Save completed query to history
      const completedQuery: Query = {
        id: queryId || `query-${Date.now()}`,
        prompt: currentQuery.prompt,
        category: currentQuery.category,
        tags: currentQuery.tags,
        providers: currentQuery.providers,
        created_at: new Date().toISOString(),
        status: 'complete'
      };
      
      setQueryHistory(prev => [completedQuery, ...prev]);
      
      toast({
        title: "Analysis Complete! ✨",
        description: "Your LLM responses have been analyzed and are ready for review.",
      });
    }, 1000); // Shorter delay for demo
  };

  const handleHistoryQuerySelect = (query: Query) => {
    toast({
      title: "Loading Query Results",
      description: "Fetching results for the selected query...",
    });
    
    // Simulate loading historical results with the actual query data
    setTimeout(() => {
      // Generate mock results for the historical query
      const historicalResults: QueryResults = {
        ...mockQueryResults,
        query: query,
        responses: query.providers.map((provider, index) => ({
          id: `hist-resp-${provider}-${index + 1}`,
          provider: provider,
          model: provider === 'openai' ? 'gpt-4' : 
                 provider === 'claude' ? 'claude-3-sonnet' :
                 provider === 'perplexity' ? 'llama-3.1-sonar-large-128k-online' :
                 'gemini-pro',
          response_text: `Historical response from ${provider} for: "${query.prompt}"
          
This is a cached response that was generated when this query was originally submitted on ${new Date(query.created_at).toLocaleDateString()}.

The analysis includes the same comprehensive insights that were provided during the original evaluation, allowing you to review and compare the responses from different providers.

Original query details:
- Category: ${query.category}
- Tags: ${query.tags.join(', ')}
- Submitted: ${new Date(query.created_at).toLocaleString()}
- Status: ${query.status}`,
          metadata: {
            tokens_used: Math.floor(Math.random() * 100) + 300,
            response_time_ms: Math.floor(Math.random() * 5000) + 10000
          }
        }))
      };
      
      setCurrentResults(historicalResults);
      setShowResults(true);
      setActiveTab('results');
    }, 1000);
  };

  const handleNewQuery = () => {
    setShowResults(false);
    setShowProgress(false);
    setCurrentResults(null);
    setCurrentQuery(null);
    setQueryId(null);
    setActiveTab('new-query');
  };

  return (
    <Layout>
      <div className="space-y-8">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="new-query">New Query</TabsTrigger>
            <TabsTrigger value="history">Query History</TabsTrigger>
            <TabsTrigger value="results" disabled={!currentResults && !showProgress}>
              {showProgress ? 'Progress' : 'Results'}
            </TabsTrigger>
          </TabsList>

          <TabsContent value="new-query" className="space-y-6">
            <QueryForm 
              onSubmit={handleQuerySubmit}
              isLoading={isSubmitting}
            />
          </TabsContent>

          <TabsContent value="history" className="space-y-6">
            <QueryHistory 
              onQuerySelect={handleHistoryQuerySelect} 
              queries={queryHistory}
            />
          </TabsContent>

          <TabsContent value="progress" className="space-y-6">
            {showProgress && currentQuery && queryId ? (
              <ProgressTracker
                queryId={queryId}
                providers={currentQuery.providers}
                onComplete={handleProgressComplete}
              />
            ) : (
              <div className="text-center py-12 text-muted-foreground">
                No active query processing
              </div>
            )}
          </TabsContent>

          <TabsContent value="results" className="space-y-6">
            {currentResults ? (
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <h1 className="text-2xl font-bold">Analysis Results</h1>
                  <Button onClick={handleNewQuery} variant="outline">
                    New Query
                  </Button>
                </div>
                <ResultsDashboard results={currentResults} />
              </div>
            ) : (
              <div className="text-center py-12 text-muted-foreground">
                No results available
              </div>
            )}
          </TabsContent>
        </Tabs>
      </div>
    </Layout>
  );
};

export default Index;
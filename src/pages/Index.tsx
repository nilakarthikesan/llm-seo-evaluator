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
      // Create dynamic responses based on actual query
      const generateDynamicResponse = (provider: string, model: string) => {
        const baseResponse = `Based on current trends and analysis for "${currentQuery.prompt}", here are the key insights:

## Top Recommendations for ${new Date().getFullYear()}

### 1. Premium Options
- High-performance solutions with excellent build quality
- Advanced features and cutting-edge technology
- Recommended for professionals and enthusiasts

### 2. Best Value Picks  
- Optimal balance of price and performance
- Great for everyday use and general applications
- Popular among mainstream users

### 3. Budget-Friendly Choices
- Cost-effective options without compromising quality
- Perfect for beginners or casual users
- Excellent entry-level recommendations

### 4. Emerging Trends
- Latest innovations and upcoming technologies
- Future-proof options worth considering
- Industry predictions and market analysis

### Key Factors to Consider:
- Performance requirements and use cases
- Budget constraints and value propositions
- Long-term durability and reliability
- User reviews and expert recommendations
- Compatibility with existing setups

This analysis is based on ${provider}'s comprehensive evaluation using ${model} technology.`;

        return baseResponse;
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
            response_text: generateDynamicResponse(provider, 
              provider === 'openai' ? 'GPT-4' : 
              provider === 'claude' ? 'Claude 3 Sonnet' :
              provider === 'perplexity' ? 'Perplexity AI' :
              'Gemini Pro'
            ),
            metadata: {
              tokens_used: Math.floor(Math.random() * 200) + 300,
              response_time_ms: Math.floor(Math.random() * 10000) + 15000
            }
          }))
      };
      
      setCurrentResults(dynamicResults);
      setShowResults(true);
      setShowProgress(false);
      setActiveTab('results');
      toast({
        title: "Analysis Complete! ✨",
        description: "Your LLM responses have been analyzed and are ready for review.",
      });
    }, 1000); // Shorter delay for demo
  };

  const handleHistoryQuerySelect = (query: Query) => {
    // TODO: Load query results from API
    toast({
      title: "Loading Query Results",
      description: "Fetching results for the selected query...",
    });
    
    // For now, simulate loading historical results
    setTimeout(() => {
      const mockHistoricalResults: QueryResults = {
        ...mockQueryResults,
        query: query
      };
      setCurrentResults(mockHistoricalResults);
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
            <QueryHistory onQuerySelect={handleHistoryQuerySelect} />
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

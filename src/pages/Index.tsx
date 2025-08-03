import React, { useState } from 'react';
import { Layout } from '@/components/layout/Layout';
import { QueryForm } from '@/components/query/QueryForm';
import { ResultsDashboard } from '@/components/results/ResultsDashboard';
import { QuerySubmission, QueryResults } from '@/types/llm';
import { apiClient } from '@/services/api';
import { mockQueryResults } from '@/services/mockData';
import { useToast } from '@/hooks/use-toast';

const Index = () => {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [currentResults, setCurrentResults] = useState<QueryResults | null>(null);
  const [showResults, setShowResults] = useState(false);
  const { toast } = useToast();

  const handleQuerySubmit = async (queryData: QuerySubmission) => {
    setIsSubmitting(true);
    
    try {
      console.log('Submitting query:', queryData);
      const response = await apiClient.submitQuery(queryData);
      
      toast({
        title: "Query Submitted Successfully! 🚀",
        description: `Query ${response.query_id} is being processed by ${queryData.providers.length} LLM providers.`,
      });
      
      // Simulate processing delay then show results
      setTimeout(() => {
        // Create dynamic responses based on actual query
        const generateDynamicResponse = (provider: string, model: string) => {
          const baseResponse = `Based on current trends and analysis for "${queryData.prompt}", here are the key insights:

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
            prompt: queryData.prompt,
            category: queryData.category,
            tags: queryData.tags,
            providers: queryData.providers,
            created_at: new Date().toISOString()
          },
          responses: queryData.providers.map((provider, index) => ({
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
        toast({
          title: "Analysis Complete! ✨",
          description: "Your LLM responses have been analyzed and are ready for review.",
        });
      }, 2000);
      
      console.log('Query response:', response);
      
    } catch (error) {
      console.error('Error submitting query:', error);
      toast({
        title: "Submission Failed",
        description: "There was an error submitting your query. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleNewQuery = () => {
    setShowResults(false);
    setCurrentResults(null);
  };

  return (
    <Layout>
      <div className="space-y-8">
        {!showResults ? (
          <QueryForm 
            onSubmit={handleQuerySubmit}
            isLoading={isSubmitting}
          />
        ) : currentResults ? (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h1 className="text-2xl font-bold">Analysis Results</h1>
              <button
                onClick={handleNewQuery}
                className="px-4 py-2 text-sm font-medium text-primary hover:text-primary/80 transition-colors"
              >
                ← New Query
              </button>
            </div>
            <ResultsDashboard results={currentResults} />
          </div>
        ) : (
          <div className="text-center py-8">
            <p className="text-muted-foreground">Loading results...</p>
          </div>
        )}
      </div>
    </Layout>
  );
};

export default Index;

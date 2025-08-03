import React from 'react';
import { LLMResponse, CrossComparison, LLM_PROVIDERS } from '@/types/llm';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { ArrowRight, Shuffle } from 'lucide-react';

interface ComparisonMatrixProps {
  responses: LLMResponse[];
  crossComparisons: CrossComparison[];
}

export const ComparisonMatrix: React.FC<ComparisonMatrixProps> = ({ 
  responses, 
  crossComparisons 
}) => {
  const getProviderName = (providerKey: string) => {
    return LLM_PROVIDERS[providerKey as keyof typeof LLM_PROVIDERS]?.name || providerKey;
  };

  const getProviderColor = (providerKey: string) => {
    return LLM_PROVIDERS[providerKey as keyof typeof LLM_PROVIDERS]?.color || 'gray-500';
  };

  const getSimilarityColor = (similarity: number) => {
    if (similarity >= 0.8) return 'bg-red-500';
    if (similarity >= 0.6) return 'bg-yellow-500';
    return 'bg-green-500';
  };

  const getSimilarityLabel = (similarity: number) => {
    if (similarity >= 0.8) return 'Very Similar';
    if (similarity >= 0.6) return 'Moderately Similar';
    return 'Diverse';
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center space-x-2">
        <Shuffle className="h-5 w-5" />
        <h3 className="text-lg font-semibold">Response Comparisons</h3>
      </div>

      <div className="grid gap-6">
        {crossComparisons.map((comparison, index) => (
          <Card key={index}>
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className="flex items-center space-x-2">
                    <div className={`w-3 h-3 rounded-full bg-${getProviderColor(comparison.providers[0])}`} />
                    <span className="font-medium">
                      {getProviderName(comparison.providers[0])}
                    </span>
                  </div>
                  <ArrowRight className="h-4 w-4 text-muted-foreground" />
                  <div className="flex items-center space-x-2">
                    <div className={`w-3 h-3 rounded-full bg-${getProviderColor(comparison.providers[1])}`} />
                    <span className="font-medium">
                      {getProviderName(comparison.providers[1])}
                    </span>
                  </div>
                </div>
                <Badge 
                  variant="outline" 
                  className={`${getSimilarityColor(comparison.cosine_similarity)} text-white border-0`}
                >
                  {getSimilarityLabel(comparison.cosine_similarity)}
                </Badge>
              </CardTitle>
            </CardHeader>
            
            <CardContent className="space-y-6">
              {/* Similarity Metrics */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-medium">Cosine Similarity</span>
                    <span className="text-sm font-semibold">
                      {(comparison.cosine_similarity * 100).toFixed(0)}%
                    </span>
                  </div>
                  <Progress value={comparison.cosine_similarity * 100} className="h-2" />
                </div>

                <div className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-medium">Jaccard Similarity</span>
                    <span className="text-sm font-semibold">
                      {(comparison.jaccard_similarity * 100).toFixed(0)}%
                    </span>
                  </div>
                  <Progress value={comparison.jaccard_similarity * 100} className="h-2" />
                </div>
              </div>

              {/* Common Elements */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Common Keywords */}
                <div className="space-y-3">
                  <h4 className="font-medium text-sm">Common Keywords</h4>
                  {comparison.common_keywords.length > 0 ? (
                    <div className="flex flex-wrap gap-1">
                      {comparison.common_keywords.map((keyword, idx) => (
                        <Badge key={idx} variant="secondary" className="text-xs">
                          {keyword}
                        </Badge>
                      ))}
                    </div>
                  ) : (
                    <p className="text-xs text-muted-foreground italic">
                      No common keywords found
                    </p>
                  )}
                </div>

                {/* Tool Overlap */}
                <div className="space-y-3">
                  <h4 className="font-medium text-sm">Shared Tools/Technologies</h4>
                  {comparison.tool_overlap.length > 0 ? (
                    <div className="flex flex-wrap gap-1">
                      {comparison.tool_overlap.map((tool, idx) => (
                        <Badge key={idx} variant="outline" className="text-xs">
                          {tool}
                        </Badge>
                      ))}
                    </div>
                  ) : (
                    <p className="text-xs text-muted-foreground italic">
                      No shared tools mentioned
                    </p>
                  )}
                </div>
              </div>

              {/* Insights */}
              <div className="bg-muted/30 p-4 rounded-lg">
                <h4 className="font-medium text-sm mb-2">Analysis Insights</h4>
                <p className="text-xs text-muted-foreground">
                  {comparison.cosine_similarity >= 0.8 
                    ? `These responses are very similar, suggesting ${comparison.providers[0]} and ${comparison.providers[1]} have similar approaches to this query type.`
                    : comparison.cosine_similarity >= 0.6
                    ? `These responses share some similarities but offer different perspectives and approaches.`
                    : `These responses are quite diverse, indicating different approaches and unique insights from each provider.`
                  }
                  {comparison.tool_overlap.length > 0 && (
                    ` Both responses recommend similar tools like ${comparison.tool_overlap.slice(0, 2).join(' and ')}.`
                  )}
                </p>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};
import React from 'react';
import { LLM_PROVIDERS } from '@/types/llm';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { BarChart3 } from 'lucide-react';

interface SimilarityChartProps {
  similarityMatrix: number[][];
  providers: string[];
}

export const SimilarityChart: React.FC<SimilarityChartProps> = ({ 
  similarityMatrix, 
  providers 
}) => {
  const getProviderName = (providerKey: string) => {
    return LLM_PROVIDERS[providerKey as keyof typeof LLM_PROVIDERS]?.name || providerKey;
  };

  const getProviderColor = (providerKey: string) => {
    return LLM_PROVIDERS[providerKey as keyof typeof LLM_PROVIDERS]?.color || 'gray-500';
  };

  const getSimilarityColor = (similarity: number) => {
    if (similarity === 1.0) return 'bg-blue-500'; // Self-similarity
    if (similarity >= 0.8) return 'bg-red-500';
    if (similarity >= 0.6) return 'bg-yellow-500';
    if (similarity >= 0.4) return 'bg-green-500';
    return 'bg-gray-400';
  };

  const getSimilarityIntensity = (similarity: number) => {
    if (similarity === 1.0) return 'opacity-100';
    const intensity = Math.max(0.3, similarity);
    return `opacity-${Math.round(intensity * 100)}`;
  };

  // Calculate average similarities (excluding self-similarity)
  const avgSimilarities = providers.map((_, providerIndex) => {
    const similarities = similarityMatrix[providerIndex].filter((_, idx) => idx !== providerIndex);
    return similarities.reduce((sum, sim) => sum + sim, 0) / similarities.length;
  });

  return (
    <div className="space-y-6">
      <div className="flex items-center space-x-2">
        <BarChart3 className="h-5 w-5" />
        <h3 className="text-lg font-semibold">Similarity Analysis</h3>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Similarity Matrix Heatmap */}
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Response Similarity Matrix</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {/* Legend */}
              <div className="flex items-center justify-between text-xs">
                <span>Less Similar</span>
                <div className="flex space-x-1">
                  <div className="w-3 h-3 bg-gray-400 rounded"></div>
                  <div className="w-3 h-3 bg-green-500 rounded"></div>
                  <div className="w-3 h-3 bg-yellow-500 rounded"></div>
                  <div className="w-3 h-3 bg-red-500 rounded"></div>
                </div>
                <span>More Similar</span>
              </div>

              {/* Matrix Grid */}
              <div className="space-y-2">
                {/* Header Row */}
                <div className="grid grid-cols-4 gap-1">
                  <div className="text-xs font-medium p-2"></div>
                  {providers.map((provider, idx) => (
                    <div key={idx} className="text-xs font-medium p-2 text-center">
                      {provider.slice(0, 3).toUpperCase()}
                    </div>
                  ))}
                </div>

                {/* Data Rows */}
                {similarityMatrix.map((row, rowIdx) => (
                  <div key={rowIdx} className="grid grid-cols-4 gap-1">
                    <div className="text-xs font-medium p-2 flex items-center">
                      <div className={`w-2 h-2 rounded-full bg-${getProviderColor(providers[rowIdx])} mr-2`} />
                      {providers[rowIdx].slice(0, 3).toUpperCase()}
                    </div>
                    {row.map((similarity, colIdx) => (
                      <div
                        key={colIdx}
                        className={`
                          p-2 text-center text-xs font-medium rounded
                          ${getSimilarityColor(similarity)} text-white
                          ${getSimilarityIntensity(similarity)}
                        `}
                        title={`${providers[rowIdx]} vs ${providers[colIdx]}: ${(similarity * 100).toFixed(0)}%`}
                      >
                        {(similarity * 100).toFixed(0)}%
                      </div>
                    ))}
                  </div>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Provider Rankings */}
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Uniqueness Rankings</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <p className="text-sm text-muted-foreground">
                Providers ranked by how unique their responses are compared to others
              </p>
              
              <div className="space-y-3">
                {providers
                  .map((provider, idx) => ({
                    provider,
                    uniqueness: 1 - avgSimilarities[idx],
                    avgSimilarity: avgSimilarities[idx]
                  }))
                  .sort((a, b) => b.uniqueness - a.uniqueness)
                  .map((item, rank) => (
                    <div key={item.provider} className="space-y-2">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-2">
                          <span className="text-sm font-medium text-muted-foreground">
                            #{rank + 1}
                          </span>
                          <div className={`w-3 h-3 rounded-full bg-${getProviderColor(item.provider)}`} />
                          <span className="font-medium">
                            {getProviderName(item.provider)}
                          </span>
                        </div>
                        <div className="text-right">
                          <div className="text-sm font-semibold">
                            {(item.uniqueness * 100).toFixed(0)}% unique
                          </div>
                          <div className="text-xs text-muted-foreground">
                            {(item.avgSimilarity * 100).toFixed(0)}% similar to others
                          </div>
                        </div>
                      </div>
                      <div className="w-full bg-muted rounded-full h-2">
                        <div 
                          className="bg-primary h-2 rounded-full transition-all"
                          style={{ width: `${item.uniqueness * 100}%` }}
                        />
                      </div>
                    </div>
                  ))}
              </div>

              <div className="mt-4 p-3 bg-muted/30 rounded-lg">
                <p className="text-xs text-muted-foreground">
                  Higher uniqueness scores indicate more distinctive responses with less overlap 
                  in content, keywords, and recommended tools.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};
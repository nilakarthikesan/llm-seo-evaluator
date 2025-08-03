import React from 'react';
import { LLMResponse, EvaluationMetrics } from '@/types/llm';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { TrendingUp, TrendingDown, BarChart3, Users } from 'lucide-react';

interface MetricsOverviewProps {
  responses: LLMResponse[];
  metrics: EvaluationMetrics;
}

export const MetricsOverview: React.FC<MetricsOverviewProps> = ({ responses, metrics }) => {
  // Calculate aggregate metrics
  const responseMetrics = Object.values(metrics.response_metrics);
  const avgOriginality = responseMetrics.reduce((sum, m) => sum + m.originality_score, 0) / responseMetrics.length;
  const avgReadability = responseMetrics.reduce((sum, m) => sum + m.readability_score, 0) / responseMetrics.length;
  const avgSimilarity = metrics.similarity_matrix
    .flat()
    .filter((val, idx, arr) => val !== 1.0) // Exclude diagonal (self-similarity)
    .reduce((sum, val) => sum + val, 0) / (metrics.similarity_matrix.length * (metrics.similarity_matrix.length - 1));

  const totalTokens = responses.reduce((sum, r) => sum + r.metadata.tokens_used, 0);
  const avgResponseTime = responses.reduce((sum, r) => sum + r.metadata.response_time_ms, 0) / responses.length;

  const formatTime = (ms: number) => {
    return ms > 1000 ? `${(ms / 1000).toFixed(1)}s` : `${ms}ms`;
  };

  const getScoreColor = (score: number) => {
    if (score >= 0.8) return 'text-green-600';
    if (score >= 0.6) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreIcon = (score: number) => {
    return score >= 0.7 ? (
      <TrendingUp className="h-4 w-4 text-green-600" />
    ) : (
      <TrendingDown className="h-4 w-4 text-red-600" />
    );
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      {/* Average Originality */}
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Originality Score</CardTitle>
          {getScoreIcon(avgOriginality)}
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            <div className={`text-2xl font-bold ${getScoreColor(avgOriginality)}`}>
              {(avgOriginality * 100).toFixed(0)}%
            </div>
            <Progress value={avgOriginality * 100} className="h-2" />
            <p className="text-xs text-muted-foreground">
              Average uniqueness across all responses
            </p>
          </div>
        </CardContent>
      </Card>

      {/* Response Similarity */}
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Response Similarity</CardTitle>
          <Users className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            <div className={`text-2xl font-bold ${getScoreColor(1 - avgSimilarity)}`}>
              {(avgSimilarity * 100).toFixed(0)}%
            </div>
            <Progress value={avgSimilarity * 100} className="h-2" />
            <p className="text-xs text-muted-foreground">
              How similar responses are to each other
            </p>
          </div>
        </CardContent>
      </Card>

      {/* Average Readability */}
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Readability</CardTitle>
          <BarChart3 className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            <div className={`text-2xl font-bold ${getScoreColor(avgReadability)}`}>
              {(avgReadability * 100).toFixed(0)}%
            </div>
            <Progress value={avgReadability * 100} className="h-2" />
            <p className="text-xs text-muted-foreground">
              Average content readability score
            </p>
          </div>
        </CardContent>
      </Card>

      {/* Performance Stats */}
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Performance</CardTitle>
          <TrendingUp className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            <div className="text-2xl font-bold">
              {formatTime(avgResponseTime)}
            </div>
            <div className="text-xs text-muted-foreground space-y-1">
              <div>Avg response time</div>
              <div className="flex justify-between">
                <span>Total tokens:</span>
                <span className="font-medium">{totalTokens.toLocaleString()}</span>
              </div>
              <div className="flex justify-between">
                <span>Providers:</span>
                <span className="font-medium">{responses.length}</span>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
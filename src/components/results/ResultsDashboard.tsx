import React from 'react';
import { QueryResults } from '@/types/llm';
import { ResponseCard } from './ResponseCard';
import { MetricsOverview } from './MetricsOverview';
import { ComparisonMatrix } from './ComparisonMatrix';
import { SimilarityChart } from './SimilarityChart';
import { ExportPDF } from '@/components/export/ExportPDF';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Clock, CheckCircle2 } from 'lucide-react';

interface ResultsDashboardProps {
  results: QueryResults;
}

export const ResultsDashboard: React.FC<ResultsDashboardProps> = ({ results }) => {
  const { query, responses, evaluation_metrics } = results;

  return (
    <div className="space-y-6">
      {/* Query Summary Header */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div className="space-y-1">
              <CardTitle className="text-xl">Query Results</CardTitle>
              <p className="text-muted-foreground">ID: {query.id}</p>
            </div>
            <div className="flex items-center space-x-2">
              <CheckCircle2 className="h-5 w-5 text-green-500" />
              <Badge variant="secondary" className="capitalize">
                {query.status}
              </Badge>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <h3 className="font-medium mb-2">Search Query</h3>
              <p className="text-foreground bg-muted p-3 rounded-lg">
                {query.prompt}
              </p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <h4 className="font-medium text-sm text-muted-foreground mb-2">Category</h4>
                <Badge variant="outline" className="capitalize">
                  {query.category}
                </Badge>
              </div>
              <div>
                <h4 className="font-medium text-sm text-muted-foreground mb-2">Providers</h4>
                <div className="flex flex-wrap gap-1">
                  {query.providers.map((provider) => (
                    <Badge key={provider} variant="secondary" className="text-xs">
                      {provider}
                    </Badge>
                  ))}
                </div>
              </div>
              <div>
                <h4 className="font-medium text-sm text-muted-foreground mb-2">Completed</h4>
                <div className="flex items-center space-x-1 text-sm text-muted-foreground">
                  <Clock className="h-4 w-4" />
                  <span>{new Date(query.created_at).toLocaleString()}</span>
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Metrics Overview */}
      <MetricsOverview 
        responses={responses}
        metrics={evaluation_metrics}
      />

      {/* Main Content Tabs */}
      <Tabs defaultValue="responses" className="space-y-4">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="responses">LLM Responses</TabsTrigger>
          <TabsTrigger value="comparison">Comparison</TabsTrigger>
          <TabsTrigger value="analysis">Analysis</TabsTrigger>
          <TabsTrigger value="export">Export</TabsTrigger>
        </TabsList>

        <TabsContent value="responses" className="space-y-4">
          <div className="grid gap-6">
            {responses.map((response) => (
              <ResponseCard
                key={response.id}
                response={response}
                metrics={evaluation_metrics.response_metrics[response.provider]}
              />
            ))}
          </div>
        </TabsContent>

        <TabsContent value="comparison" className="space-y-4">
          <ComparisonMatrix 
            responses={responses}
            crossComparisons={evaluation_metrics.cross_comparisons}
          />
        </TabsContent>

        <TabsContent value="analysis" className="space-y-4">
          <SimilarityChart 
            similarityMatrix={evaluation_metrics.similarity_matrix}
            providers={query.providers}
          />
        </TabsContent>

        <TabsContent value="export" className="space-y-4">
          <ExportPDF results={results} />
        </TabsContent>
      </Tabs>
    </div>
  );
};
import React, { useState } from 'react';
import { LLMResponse, ResponseMetrics, LLM_PROVIDERS } from '@/types/llm';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { ChevronDown, ChevronUp, Clock, Zap, BookOpen, Target } from 'lucide-react';
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible';

interface ResponseCardProps {
  response: LLMResponse;
  metrics?: ResponseMetrics;
}

export const ResponseCard: React.FC<ResponseCardProps> = ({ response, metrics }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const provider = LLM_PROVIDERS[response.provider as keyof typeof LLM_PROVIDERS];

  const formatResponseTime = (ms: number) => {
    return ms > 1000 ? `${(ms / 1000).toFixed(1)}s` : `${ms}ms`;
  };

  const getScoreColor = (score: number) => {
    if (score >= 0.8) return 'text-green-600';
    if (score >= 0.6) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <Card className="w-full">
      <CardHeader className="pb-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className={`w-3 h-3 rounded-full bg-${provider?.color || 'gray-500'}`} />
            <CardTitle className="text-lg">
              {provider?.name || response.provider}
            </CardTitle>
            <Badge variant="outline" className="text-xs">
              {response.model}
            </Badge>
          </div>
          <div className="flex items-center space-x-4 text-sm text-muted-foreground">
            <div className="flex items-center space-x-1">
              <Clock className="h-4 w-4" />
              <span>{formatResponseTime(response.metadata.response_time_ms)}</span>
            </div>
            <div className="flex items-center space-x-1">
              <Zap className="h-4 w-4" />
              <span>{response.metadata.tokens_used} tokens</span>
            </div>
          </div>
        </div>
        
        {provider?.description && (
          <p className="text-sm text-muted-foreground">
            {provider.description}
          </p>
        )}
      </CardHeader>

      <CardContent className="space-y-4">
        {/* Metrics Overview */}
        {metrics && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 p-4 bg-muted/30 rounded-lg">
            <div className="space-y-1">
              <div className="flex items-center space-x-1">
                <Target className="h-3 w-3" />
                <span className="text-xs font-medium">Originality</span>
              </div>
              <div className="space-y-1">
                <div className={`text-sm font-semibold ${getScoreColor(metrics.originality_score)}`}>
                  {(metrics.originality_score * 100).toFixed(0)}%
                </div>
                <Progress value={metrics.originality_score * 100} className="h-1" />
              </div>
            </div>

            <div className="space-y-1">
              <div className="flex items-center space-x-1">
                <BookOpen className="h-3 w-3" />
                <span className="text-xs font-medium">Readability</span>
              </div>
              <div className="space-y-1">
                <div className={`text-sm font-semibold ${getScoreColor(metrics.readability_score)}`}>
                  {(metrics.readability_score * 100).toFixed(0)}%
                </div>
                <Progress value={metrics.readability_score * 100} className="h-1" />
              </div>
            </div>

            <div className="space-y-1">
              <span className="text-xs font-medium">Keywords</span>
              <div className="text-sm font-semibold">
                {metrics.keyword_count}
              </div>
            </div>

            <div className="space-y-1">
              <span className="text-xs font-medium">Tools Mentioned</span>
              <div className="text-sm font-semibold">
                {metrics.tool_mentions.length}
              </div>
            </div>
          </div>
        )}

        {/* Tool Mentions */}
        {metrics && metrics.tool_mentions.length > 0 && (
          <div className="space-y-2">
            <h4 className="text-sm font-medium">Tools & Technologies Mentioned</h4>
            <div className="flex flex-wrap gap-1">
              {metrics.tool_mentions.map((tool, index) => (
                <Badge key={index} variant="secondary" className="text-xs">
                  {tool}
                </Badge>
              ))}
            </div>
          </div>
        )}

        {/* Response Content - Collapsible */}
        <Collapsible open={isExpanded} onOpenChange={setIsExpanded}>
          <CollapsibleTrigger asChild>
            <Button variant="outline" className="w-full">
              <span>
                {isExpanded ? 'Hide' : 'Show'} Full Response
              </span>
              {isExpanded ? (
                <ChevronUp className="h-4 w-4 ml-2" />
              ) : (
                <ChevronDown className="h-4 w-4 ml-2" />
              )}
            </Button>
          </CollapsibleTrigger>
          
          <CollapsibleContent className="mt-4">
            <div className="prose prose-sm max-w-none bg-background border rounded-lg p-4">
              <div className="whitespace-pre-wrap font-mono text-sm">
                {response.response_text}
              </div>
            </div>
          </CollapsibleContent>

          {/* Preview when collapsed */}
          {!isExpanded && (
            <div className="mt-2 p-3 bg-muted/30 rounded-lg">
              <p className="text-sm text-muted-foreground line-clamp-3">
                {response.response_text.substring(0, 200)}...
              </p>
            </div>
          )}
        </Collapsible>
      </CardContent>
    </Card>
  );
};
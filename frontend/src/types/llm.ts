// Core types for LLM evaluation system
export interface QuerySubmission {
  prompt: string;
  category: string;
  tags: string[];
  providers: string[];
}

export interface QueryResponse {
  query_id: string;
  status: string;
}

export interface LLMResponse {
  id: string;
  provider: string;
  model: string;
  response_text: string;
  metadata: {
    tokens_used: number;
    response_time_ms: number;
  };
}

export interface ResponseMetrics {
  originality_score: number;
  similarity_to_others: number;
  keyword_count: number;
  tool_mentions: string[];
  readability_score: number;
}

export interface CrossComparison {
  providers: [string, string];
  cosine_similarity: number;
  jaccard_similarity: number;
  common_keywords: string[];
  tool_overlap: string[];
}

export interface EvaluationMetrics {
  similarity_matrix: number[][];
  response_metrics: Record<string, ResponseMetrics>;
  cross_comparisons: CrossComparison[];
}

export interface Query {
  id: string;
  prompt: string;
  category: string;
  tags: string[];
  providers: string[];
  created_at: string;
  status: 'pending' | 'processing' | 'complete' | 'error';
}

export interface QueryResults {
  query: Query;
  responses: LLMResponse[];
  evaluation_metrics: EvaluationMetrics;
}

export interface ProgressUpdate {
  status: string;
  completed_providers: string[];
  total_providers: number;
  message: string;
  progress_percentage: number;
}

export type LLMProvider = 'openai' | 'claude' | 'perplexity' | 'gemini';

export const LLM_PROVIDERS: Record<LLMProvider, { name: string; color: string; description: string }> = {
  openai: {
    name: 'OpenAI GPT-4',
    color: 'provider-openai',
    description: 'Industry-leading language model with strong reasoning'
  },
  claude: {
    name: 'Anthropic Claude',
    color: 'provider-claude', 
    description: 'Advanced AI with excellent safety and longer context'
  },
  perplexity: {
    name: 'Perplexity AI',
    color: 'provider-perplexity',
    description: 'Real-time web search integration with citations'
  },
  gemini: {
    name: 'Google Gemini',
    color: 'provider-gemini',
    description: 'Google\'s multimodal AI with competitive performance'
  }
};

export const SEO_CATEGORIES = [
  { value: 'technical', label: 'Technical SEO', description: 'Site optimization, performance, crawling' },
  { value: 'content', label: 'Content Strategy', description: 'Content creation, optimization, planning' },
  { value: 'automation', label: 'Automation & Scripts', description: 'Python scripts, tools, workflows' },
  { value: 'analytics', label: 'Analytics & Reporting', description: 'Data analysis, tracking, insights' },
  { value: 'link-building', label: 'Link Building', description: 'Backlink strategies, outreach, analysis' },
  { value: 'local-seo', label: 'Local SEO', description: 'Local search optimization, GMB, citations' }
];
import { QuerySubmission, QueryResponse, QueryResults, ProgressUpdate } from '@/types/llm';
import { mockQueryResults, mockProgressUpdates } from './mockData';

// Environment configuration
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const USE_MOCK_DATA = import.meta.env.VITE_USE_MOCK === 'true' || false; // Default to false for real API

console.log('API Configuration:', { API_BASE_URL, USE_MOCK_DATA });

// API Client
class APIClient {
  private baseURL: string;
  private useMock: boolean;

  constructor(baseURL: string, useMock: boolean) {
    this.baseURL = baseURL;
    this.useMock = useMock;
  }

  // Submit query for LLM evaluation
  async submitQuery(queryData: QuerySubmission): Promise<QueryResponse> {
    if (this.useMock) {
      // Simulate API delay
      await this.delay(500);
      return {
        id: mockQueryResults.query.id,
        prompt: queryData.prompt,
        category: queryData.category,
        tags: queryData.tags,
        user_id: queryData.user_id,
        status: 'processing',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        response_count: 0
      };
    }

    try {
      const response = await fetch(`${this.baseURL}/api/v1/queries/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(queryData),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      return response.json();
    } catch (error) {
      console.error('Error submitting query:', error);
      throw error;
    }
  }

  // Get query results with evaluation metrics
  async getQueryResults(queryId: string): Promise<QueryResults> {
    if (this.useMock) {
      await this.delay(800);
      return mockQueryResults;
    }

    try {
      const response = await fetch(`${this.baseURL}/api/v1/queries/${queryId}/responses`);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      return response.json();
    } catch (error) {
      console.error('Error getting query results:', error);
      throw error;
    }
  }

  // Get query status
  async getQueryStatus(queryId: string): Promise<any> {
    if (this.useMock) {
      await this.delay(300);
      return {
        id: queryId,
        status: 'processing',
        completed_providers: ['openai'],
        total_providers: 2,
        message: 'Processing queries...',
        estimated_completion: null
      };
    }

    try {
      const response = await fetch(`${this.baseURL}/api/v1/queries/${queryId}/status`);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      return response.json();
    } catch (error) {
      console.error('Error getting query status:', error);
      throw error;
    }
  }

  // Get analytics data for dashboard
  async getAnalytics(queryId?: string): Promise<any> {
    if (this.useMock) {
      await this.delay(600);
      return {
        trends: mockQueryResults.evaluation_metrics,
        summary: {
          total_queries: 45,
          avg_similarity: 0.71,
          most_popular_category: 'automation',
          top_provider: 'openai'
        }
      };
    }

    try {
      const endpoint = queryId 
        ? `${this.baseURL}/api/v1/analytics/queries/${queryId}/metrics`
        : `${this.baseURL}/api/v1/analytics/trends`;
      
      const response = await fetch(endpoint);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      return response.json();
    } catch (error) {
      console.error('Error getting analytics:', error);
      throw error;
    }
  }

  // Get similarity analysis
  async getSimilarityAnalysis(queryId: string): Promise<any> {
    if (this.useMock) {
      await this.delay(400);
      return {
        query_id: queryId,
        similarity_matrix: [[1, 0.73, 0.45], [0.73, 1, 0.52], [0.45, 0.52, 1]],
        providers: ['openai', 'anthropic', 'perplexity'],
        average_similarity: 0.57
      };
    }

    try {
      const response = await fetch(`${this.baseURL}/api/v1/analytics/queries/${queryId}/similarity`);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      return response.json();
    } catch (error) {
      console.error('Error getting similarity analysis:', error);
      throw error;
    }
  }

  // Get keyword analysis
  async getKeywordAnalysis(queryId: string): Promise<any> {
    if (this.useMock) {
      await this.delay(400);
      return {
        query_id: queryId,
        keywords: { 'seo': 5, 'automation': 3, 'python': 2 },
        tools: { 'screaming frog': 2, 'google analytics': 1 },
        seo_terms: { 'meta tags': 3, 'backlinks': 2 },
        total_keywords: 10,
        total_tools: 3,
        total_seo_terms: 5
      };
    }

    try {
      const response = await fetch(`${this.baseURL}/api/v1/analytics/queries/${queryId}/keywords`);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      return response.json();
    } catch (error) {
      console.error('Error getting keyword analysis:', error);
      throw error;
    }
  }

  // Get provider comparison
  async getProviderComparison(): Promise<any> {
    if (this.useMock) {
      await this.delay(500);
      return {
        provider_comparison: {
          openai: {
            total_responses: 25,
            avg_tokens: 150,
            avg_response_time: 12000,
            avg_word_count: 200,
            models: ['gpt-4', 'gpt-3.5-turbo']
          },
          anthropic: {
            total_responses: 20,
            avg_tokens: 180,
            avg_response_time: 15000,
            avg_word_count: 250,
            models: ['claude-3-sonnet']
          }
        },
        total_responses: 45
      };
    }

    try {
      const response = await fetch(`${this.baseURL}/api/v1/analytics/providers/comparison`);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      return response.json();
    } catch (error) {
      console.error('Error getting provider comparison:', error);
      throw error;
    }
  }

  // Utility method to simulate API delays
  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

// WebSocket client for real-time progress updates
export class ProgressWebSocket {
  private ws: WebSocket | null = null;
  private queryId: string;
  private onUpdate: (update: ProgressUpdate) => void;
  private useMock: boolean;
  private mockIndex: number = 0;
  private pollInterval: NodeJS.Timeout | null = null;

  constructor(queryId: string, onUpdate: (update: ProgressUpdate) => void) {
    this.queryId = queryId;
    this.onUpdate = onUpdate;
    this.useMock = USE_MOCK_DATA;
  }

  connect(): void {
    if (this.useMock) {
      this.simulateMockProgress();
      return;
    }

    // For now, use polling instead of WebSocket since WebSocket isn't implemented yet
    this.startPolling();
  }

  disconnect(): void {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
    if (this.pollInterval) {
      clearInterval(this.pollInterval);
      this.pollInterval = null;
    }
  }

  // Poll for status updates since WebSocket isn't implemented yet
  private startPolling(): void {
    this.pollInterval = setInterval(async () => {
      try {
        const status = await apiClient.getQueryStatus(this.queryId);
        this.onUpdate({
          status: status.status,
          completed_providers: status.completed_providers,
          total_providers: status.total_providers,
          message: status.message,
          estimated_completion: status.estimated_completion
        });
        
        // Stop polling if query is complete
        if (status.status === 'completed' || status.status === 'failed') {
          this.disconnect();
        }
      } catch (error) {
        console.error('Error polling status:', error);
      }
    }, 2000); // Poll every 2 seconds
  }

  // Simulate mock progress updates for development
  private simulateMockProgress(): void {
    const sendNextUpdate = () => {
      if (this.mockIndex < mockProgressUpdates.length) {
        this.onUpdate(mockProgressUpdates[this.mockIndex]);
        this.mockIndex++;
        
        // Varying delays to simulate real processing times
        const delays = [1000, 3000, 5000, 2000, 1000];
        const delay = delays[this.mockIndex - 1] || 1000;
        
        setTimeout(sendNextUpdate, delay);
      }
    };

    setTimeout(sendNextUpdate, 500);
  }
}

// Export singleton instance
export const apiClient = new APIClient(API_BASE_URL, USE_MOCK_DATA);

// Export utility functions
export const createProgressWebSocket = (queryId: string, onUpdate: (update: ProgressUpdate) => void) => {
  return new ProgressWebSocket(queryId, onUpdate);
};

// Helper function to check if we're using mock data
export const isUsingMockData = () => USE_MOCK_DATA;

// Health check endpoint
export const checkAPIHealth = async (): Promise<boolean> => {
  if (USE_MOCK_DATA) return true;
  
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    return response.ok;
  } catch {
    return false;
  }
};
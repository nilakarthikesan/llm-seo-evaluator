import { QuerySubmission, QueryResponse, QueryResults, ProgressUpdate } from '@/types/llm';
import { mockQueryResults, mockProgressUpdates } from './mockData';

// Environment configuration
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const USE_MOCK_DATA = import.meta.env.VITE_USE_MOCK === 'true' || import.meta.env.DEV;

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
        query_id: mockQueryResults.query.id,
        status: 'processing'
      };
    }

    const response = await fetch(`${this.baseURL}/api/v1/queries/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(queryData),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  // Get query results with evaluation metrics
  async getQueryResults(queryId: string): Promise<QueryResults> {
    if (this.useMock) {
      await this.delay(800);
      return mockQueryResults;
    }

    const response = await fetch(`${this.baseURL}/api/v1/queries/${queryId}/responses`);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
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

    const endpoint = queryId 
      ? `${this.baseURL}/api/v1/queries/${queryId}/analytics`
      : `${this.baseURL}/api/v1/analytics/trends`;
    
    const response = await fetch(endpoint);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
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

    const wsUrl = `${API_BASE_URL.replace('http', 'ws')}/ws/queries/${this.queryId}/status`;
    this.ws = new WebSocket(wsUrl);

    this.ws.onopen = () => {
      console.log('WebSocket connected');
    };

    this.ws.onmessage = (event) => {
      const update: ProgressUpdate = JSON.parse(event.data);
      this.onUpdate(update);
    };

    this.ws.onclose = () => {
      console.log('WebSocket disconnected');
    };

    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
  }

  disconnect(): void {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
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
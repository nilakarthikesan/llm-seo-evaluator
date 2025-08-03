import requests
from typing import Dict, Any
import logging
import json

from app.services.llm_providers.base import BaseLLMProvider
from app.schemas.response import LLMResponse

logger = logging.getLogger(__name__)

class PerplexityProvider(BaseLLMProvider):
    """Perplexity AI provider implementation"""
    
    def __init__(self, api_key: str, model: str = "llama-3.1-sonar-small-128k-online", **kwargs):
        super().__init__(api_key, model, **kwargs)
        self.api_url = "https://api.perplexity.ai/chat/completions"
    
    def get_provider_name(self) -> str:
        return "perplexity"
    
    async def query(self, prompt: str, **kwargs) -> LLMResponse:
        """Execute query against Perplexity API"""
        try:
            # Prepare headers
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # Prepare payload
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an expert SEO consultant. Provide detailed, actionable advice for SEO questions. Focus on practical, implementable strategies and current best practices."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": kwargs.get('max_tokens', 2000),
                "temperature": kwargs.get('temperature', 0.7),
                "top_p": kwargs.get('top_p', 1.0)
            }
            
            # Make API call
            import httpx
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.api_url,
                    headers=headers,
                    json=payload
                )
                
                if response.status_code != 200:
                    raise Exception(f"Perplexity API error: {response.status_code} - {response.text}")
                
                data = response.json()
                
                # Extract response
                response_text = data['choices'][0]['message']['content']
                tokens_used = data['usage']['total_tokens'] if 'usage' in data else None
                
                # Prepare metadata
                metadata = {
                    "model": self.model,
                    "finish_reason": data['choices'][0].get('finish_reason'),
                    "usage": data.get('usage', {})
                }
                
                return LLMResponse(
                    text=response_text,
                    tokens_used=tokens_used,
                    metadata=metadata
                )
                
        except Exception as e:
            logger.error(f"Perplexity API error: {e}")
            return LLMResponse(
                text="",
                error=f"Perplexity API error: {str(e)}"
            )
    
    def get_available_models(self) -> list:
        """Get list of available Perplexity models"""
        return [
            "llama-3.1-sonar-small-128k-online",
            "llama-3.1-sonar-small-128k",
            "llama-3.1-sonar-medium-128k-online",
            "llama-3.1-sonar-medium-128k",
            "llama-3.1-sonar-large-128k-online",
            "llama-3.1-sonar-large-128k",
            "mixtral-8x7b-instruct",
            "mistral-7b-instruct",
            "codellama-34b-instruct",
            "pplx-7b-online",
            "pplx-70b-online",
            "pplx-7b-chat",
            "pplx-70b-chat"
        ] 
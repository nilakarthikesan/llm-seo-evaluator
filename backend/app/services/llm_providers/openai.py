import openai
from typing import Dict, Any
import logging

from app.services.llm_providers.base import BaseLLMProvider
from app.schemas.response import LLMResponse

logger = logging.getLogger(__name__)

class OpenAIProvider(BaseLLMProvider):
    """OpenAI GPT provider implementation"""
    
    def __init__(self, api_key: str, model: str = "gpt-4", **kwargs):
        super().__init__(api_key, model, **kwargs)
        # Create client with new API syntax
        self.client = openai.AsyncOpenAI(api_key=api_key)
    
    def get_provider_name(self) -> str:
        return "openai"
    
    async def query(self, prompt: str, **kwargs) -> LLMResponse:
        """Execute query against OpenAI API"""
        try:
            # Prepare the message
            messages = [
                {
                    "role": "system",
                    "content": "You are an expert SEO consultant. Provide detailed, actionable advice for SEO questions. Focus on practical, implementable strategies and current best practices."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
            
            # Make API call using the new openai library syntax
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=kwargs.get('max_tokens', 2000),
                temperature=kwargs.get('temperature', 0.7),
                top_p=kwargs.get('top_p', 1.0),
                frequency_penalty=kwargs.get('frequency_penalty', 0.0),
                presence_penalty=kwargs.get('presence_penalty', 0.0)
            )
            
            # Extract response
            response_text = response.choices[0].message.content
            tokens_used = response.usage.total_tokens if response.usage else None
            
            # Prepare metadata
            metadata = {
                "model": self.model,
                "finish_reason": response.choices[0].finish_reason,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens if response.usage else None,
                    "completion_tokens": response.usage.completion_tokens if response.usage else None,
                    "total_tokens": tokens_used
                } if response.usage else None
            }
            
            return LLMResponse(
                text=response_text,
                tokens_used=tokens_used,
                metadata=metadata
            )
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return LLMResponse(
                text="",
                error=f"OpenAI API error: {str(e)}"
            )
    
    def get_available_models(self) -> list:
        """Get list of available OpenAI models"""
        return [
            "gpt-4",
            "gpt-4-turbo-preview",
            "gpt-3.5-turbo",
            "gpt-3.5-turbo-16k"
        ]

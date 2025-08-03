import anthropic
from typing import Dict, Any
import logging
import os

from app.services.llm_providers.base import BaseLLMProvider
from app.schemas.response import LLMResponse

logger = logging.getLogger(__name__)

class AnthropicProvider(BaseLLMProvider):
    """Anthropic Claude provider implementation"""
    
    def __init__(self, api_key: str, model: str = "claude-3-5-sonnet-20241022", **kwargs):
        super().__init__(api_key, model, **kwargs)
        # Store API key for the anthropic library
        self.api_key = api_key
    
    def get_provider_name(self) -> str:
        return "anthropic"
    
    async def query(self, prompt: str, **kwargs) -> LLMResponse:
        """Execute query against Anthropic API"""
        try:
            # Create client with explicit httpx configuration to avoid proxies issue
            import httpx
            
            # Create a custom httpx client without proxies
            http_client = httpx.Client(
                timeout=httpx.Timeout(self.timeout),
                # Explicitly not passing proxies
            )
            
            # Create Anthropic client with our custom http_client
            client = anthropic.Anthropic(
                api_key=self.api_key,
                http_client=http_client
            )
            
            # Use the correct API for anthropic 0.60.0
            response = client.messages.create(
                model=self.model,
                max_tokens=kwargs.get('max_tokens', 2000),
                temperature=kwargs.get('temperature', 0.7),
                top_p=kwargs.get('top_p', 1.0),
                messages=[
                    {
                        "role": "user",
                        "content": f"""You are an expert SEO consultant. Provide detailed, actionable advice for the following SEO question. Focus on practical, implementable strategies and current best practices.

Question: {prompt}"""
                    }
                ]
            )
            
            # Extract response
            response_text = response.content[0].text
            tokens_used = response.usage.input_tokens + response.usage.output_tokens if response.usage else None
            
            # Prepare metadata
            metadata = {
                "model": self.model,
                "stop_reason": response.stop_reason,
                "usage": {
                    "input_tokens": response.usage.input_tokens if response.usage else None,
                    "output_tokens": response.usage.output_tokens if response.usage else None,
                    "total_tokens": tokens_used
                } if response.usage else None
            }
            
            return LLMResponse(
                text=response_text,
                tokens_used=tokens_used,
                metadata=metadata
            )
            
        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            return LLMResponse(
                text="",
                error=f"Anthropic API error: {str(e)}"
            )
    
    def get_available_models(self) -> list:
        """Get list of available Anthropic models"""
        return [
            "claude-3-5-sonnet-20241022",
            "claude-3-5-haiku-20241022",
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307"
        ] 
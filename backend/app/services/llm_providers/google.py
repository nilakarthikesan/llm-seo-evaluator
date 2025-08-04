import google.generativeai as genai
from typing import Dict, Any
import logging

from app.services.llm_providers.base import BaseLLMProvider
from app.schemas.response import LLMResponse

logger = logging.getLogger(__name__)

class GoogleProvider(BaseLLMProvider):
    """Google Gemini provider implementation"""
    
    def __init__(self, api_key: str, model: str = "gemini-1.5-pro", **kwargs):
        super().__init__(api_key, model, **kwargs)
        # Configure Google AI
        genai.configure(api_key=self.api_key)
    
    def get_provider_name(self) -> str:
        return "google"
    
    async def query(self, prompt: str, **kwargs) -> LLMResponse:
        """Execute query against Google Gemini API"""
        try:
            # Create model
            model = genai.GenerativeModel(self.model)
            
            # Prepare the prompt
            full_prompt = f"""You are an expert SEO consultant. Provide detailed, actionable advice for the following SEO question. Focus on practical, implementable strategies and current best practices.

Question: {prompt}"""
            
            # Generate content
            response = model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=kwargs.get('max_tokens', 2000),
                    temperature=kwargs.get('temperature', 0.7),
                    top_p=kwargs.get('top_p', 1.0)
                )
            )
            
            # Extract response
            response_text = response.text
            
            # Prepare metadata - handle different response structures
            metadata = {
                "model": self.model,
                "finish_reason": response.candidates[0].finish_reason if response.candidates else None,
                "usage": None  # Google API doesn't always provide usage metadata
            }
            
            # Try to get usage metadata if available
            try:
                if hasattr(response, 'usage_metadata') and response.usage_metadata:
                    metadata["usage"] = {
                        "prompt_tokens": getattr(response.usage_metadata, 'prompt_token_count', None),
                        "completion_tokens": getattr(response.usage_metadata, 'candidates_token_count', None),
                        "total_tokens": getattr(response.usage_metadata, 'total_token_count', None)
                    }
            except Exception as e:
                logger.warning(f"Could not extract usage metadata: {e}")
            
            # Calculate tokens (approximate)
            tokens_used = len(response_text.split()) * 1.3  # Rough approximation
            
            return LLMResponse(
                text=response_text,
                tokens_used=int(tokens_used),
                metadata=metadata
            )
            
        except Exception as e:
            logger.error(f"Google Gemini API error: {e}")
            return LLMResponse(
                text="",
                error=f"Google Gemini API error: {str(e)}"
            )
    
    def get_available_models(self) -> list:
        """Get list of available Google Gemini models"""
        return [
            "gemini-pro",
            "gemini-pro-vision",
            "gemini-1.5-pro",
            "gemini-1.5-flash"
        ] 
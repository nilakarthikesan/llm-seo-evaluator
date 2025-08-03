from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import asyncio
import time
import logging

from app.schemas.response import LLMResponse

logger = logging.getLogger(__name__)

class BaseLLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    def __init__(self, api_key: str, model: str, **kwargs):
        self.api_key = api_key
        self.model = model
        self.timeout = kwargs.get('timeout', 30)
        self.max_retries = kwargs.get('max_retries', 3)
        self.retry_delay = kwargs.get('retry_delay', 1)
        # Remove problematic kwargs
        self.kwargs = {k: v for k, v in kwargs.items() if k not in ['proxies']}
    
    @abstractmethod
    async def query(self, prompt: str, **kwargs) -> LLMResponse:
        """Execute query against LLM provider"""
        pass
    
    @abstractmethod
    def get_provider_name(self) -> str:
        """Return provider identification"""
        pass
    
    async def execute_with_retry(self, prompt: str, **kwargs) -> LLMResponse:
        """Execute query with retry logic"""
        last_exception = None
        
        for attempt in range(self.max_retries):
            try:
                start_time = time.time()
                response = await asyncio.wait_for(
                    self.query(prompt, **kwargs),
                    timeout=self.timeout
                )
                response.response_time_ms = int((time.time() - start_time) * 1000)
                return response
                
            except asyncio.TimeoutError:
                last_exception = Exception(f"Timeout after {self.timeout} seconds")
                logger.warning(f"Timeout on attempt {attempt + 1} for {self.get_provider_name()}")
                
            except Exception as e:
                last_exception = e
                logger.warning(f"Error on attempt {attempt + 1} for {self.get_provider_name()}: {e}")
                
            if attempt < self.max_retries - 1:
                await asyncio.sleep(self.retry_delay * (attempt + 1))
        
        # All retries failed
        return LLMResponse(
            text="",
            error=f"Failed after {self.max_retries} attempts: {str(last_exception)}"
        )
    
    def validate_api_key(self) -> bool:
        """Validate that API key is present and valid"""
        return bool(self.api_key and self.api_key.strip())
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the model being used"""
        return {
            "provider": self.get_provider_name(),
            "model": self.model,
            "timeout": self.timeout,
            "max_retries": self.max_retries
        } 
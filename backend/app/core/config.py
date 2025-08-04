from pydantic_settings import BaseSettings
from typing import Optional, List
import os

class Settings(BaseSettings):
    # Application
    app_name: str = "LLM SEO Evaluation Agent"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Supabase Configuration
    supabase_url: str = "https://[YOUR-PROJECT-REF].supabase.co"
    supabase_key: str = "[YOUR-SUPABASE-ANON-KEY]"
    
    # Database - Supabase PostgreSQL connection (fallback)
    database_url: str = "postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres"
    
    # Redis
    redis_url: str = "redis://localhost:6379"
    
    # LLM API Keys
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    perplexity_api_key: Optional[str] = None
    google_api_key: Optional[str] = None
    
    # Security
    secret_key: str = "your-secret-key-change-this-in-production"
    jwt_secret: str = "your-jwt-secret-change-this-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 30
    
    # CORS - Updated for Vite default port
    allowed_origins: List[str] = [
        "http://localhost:5173",  # Vite default port
        "http://127.0.0.1:5173",
        "http://localhost:3000",  # Keep for compatibility
        "http://127.0.0.1:3000"
    ]
    
    # Rate Limiting
    rate_limit_per_hour: int = 100
    
    # LLM Settings
    default_models: dict = {
        "openai": "gpt-4",
        "anthropic": "claude-3-5-sonnet-20241022",
        "perplexity": "sonar-pro",
        "google": "gemini-1.5-pro"
    }
    
    # Evaluation Settings
    similarity_threshold: float = 0.8
    max_response_length: int = 4000
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignore extra environment variables

# Create settings instance
settings = Settings()

# Validate required settings
def validate_settings():
    """Validate that required settings are present"""
    required_keys = [
        "openai_api_key",
        "anthropic_api_key"
    ]
    
    missing_keys = [key for key in required_keys if not getattr(settings, key)]
    
    if missing_keys:
        print(f"⚠️  Warning: Missing API keys: {missing_keys}")
        print("Some LLM providers may not work without proper API keys")
        print("Please set the required environment variables or update your .env file.")
    
    return True

# Validate on import
validate_settings()

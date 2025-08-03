from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
import logging

from app.core.config import settings
from app.core.supabase import init_supabase
from app.api.v1 import queries, analytics

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("🚀 Starting LLM SEO Evaluation Agent Backend...")
    try:
        init_supabase()
        logger.info("✅ Supabase initialized")
    except Exception as e:
        logger.warning(f"⚠️ Supabase initialization failed: {e}")
        logger.info("🔄 Continuing without Supabase connection")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down...")
    logger.info("✅ Application shutdown complete")

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(queries.router, prefix="/api/v1/queries", tags=["queries"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "LLM SEO Evaluation Agent API",
        "version": settings.app_version,
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": settings.app_name}

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="info"
    ) 
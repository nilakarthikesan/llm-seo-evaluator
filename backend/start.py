#!/usr/bin/env python3
"""
Startup script for LLM SEO Evaluation Agent Backend
"""
import os
import sys
import asyncio
import logging
from pathlib import Path

# Add the app directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "app"))

from app.core.config import settings, validate_settings
from app.core.database import init_db, close_db
from app.main import app
import uvicorn

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def startup():
    """Application startup tasks"""
    logger.info("🚀 Starting LLM SEO Evaluation Agent Backend...")
    
    # Validate settings
    validate_settings()
    
    # Initialize database
    try:
        await init_db()
        logger.info("✅ Database initialized successfully")
    except Exception as e:
        logger.error(f"❌ Failed to initialize database: {e}")
        raise
    
    logger.info("✅ Application startup completed")

async def shutdown():
    """Application shutdown tasks"""
    logger.info("🛑 Shutting down application...")
    
    try:
        await close_db()
        logger.info("✅ Database connections closed")
    except Exception as e:
        logger.error(f"❌ Error during shutdown: {e}")

def main():
    """Main entry point"""
    # Set up event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        # Run startup
        loop.run_until_complete(startup())
        
        # Start the server
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=settings.debug,
            log_level="info",
            access_log=True
        )
        
    except KeyboardInterrupt:
        logger.info("Received interrupt signal")
    except Exception as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)
    finally:
        # Run shutdown
        try:
            loop.run_until_complete(shutdown())
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")
        finally:
            loop.close()

if __name__ == "__main__":
    main() 
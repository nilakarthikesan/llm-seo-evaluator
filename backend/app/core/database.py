from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Create async engine for PostgreSQL (Supabase)
# Force IPv4 connection to avoid IPv6 issues
database_url = settings.database_url.replace("postgresql://", "postgresql+asyncpg://")

async_engine = create_async_engine(
    database_url,
    echo=settings.debug,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=1,
    max_overflow=0,
    connect_args={
        "server_settings": {
            "application_name": "llm_seo_evaluator"
        },
        "statement_cache_size": 0
    },
    # Disable prepared statements at SQLAlchemy level
    execution_options={
        "prepared_statement_cache_size": 0
    },
    # Use raw SQL mode to avoid prepared statements
    future=True,
    use_insertmanyvalues=False
)

# Create sync engine for migrations
sync_engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=True,
    pool_recycle=300,
)

# Create session factories
AsyncSessionLocal = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

# Create base class for models
Base = declarative_base()

# Dependency to get database session
async def get_async_db():
    """Get async database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"Database session error: {e}")
            await session.rollback()
            raise
        finally:
            await session.close()

def get_sync_db():
    """Get sync database session"""
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

# Database initialization
async def init_db():
    """Initialize database tables"""
    try:
        # Import all models here to ensure they are registered
        from app.models import query, response, metrics
        
        # Create all tables using a simpler approach
        async with async_engine.begin() as conn:
            # Create all tables
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Database initialization error: {e}")
        # Re-raise the error so the main.py can handle it properly
        raise

async def close_db():
    """Close database connections"""
    await async_engine.dispose()
    logger.info("Database connections closed") 
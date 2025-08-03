import redis.asyncio as redis
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Redis connection pool
redis_pool = None

async def get_redis_connection():
    """Get Redis connection from pool"""
    global redis_pool
    
    if redis_pool is None:
        redis_pool = redis.ConnectionPool.from_url(
            settings.redis_url,
            decode_responses=True,
            max_connections=20
        )
    
    return redis.Redis(connection_pool=redis_pool)

async def init_redis():
    """Initialize Redis connection"""
    try:
        redis_client = await get_redis_connection()
        await redis_client.ping()
        logger.info("Redis connection established successfully")
        return redis_client
    except Exception as e:
        logger.error(f"Failed to connect to Redis: {e}")
        raise

async def close_redis():
    """Close Redis connections"""
    global redis_pool
    if redis_pool:
        await redis_pool.disconnect()
        logger.info("Redis connections closed")

# Cache utilities
async def set_cache(key: str, value: str, expire: int = 3600):
    """Set cache value with expiration"""
    try:
        redis_client = await get_redis_connection()
        await redis_client.setex(key, expire, value)
    except Exception as e:
        logger.error(f"Failed to set cache: {e}")

async def get_cache(key: str) -> str:
    """Get cache value"""
    try:
        redis_client = await get_redis_connection()
        return await redis_client.get(key)
    except Exception as e:
        logger.error(f"Failed to get cache: {e}")
        return None

async def delete_cache(key: str):
    """Delete cache value"""
    try:
        redis_client = await get_redis_connection()
        await redis_client.delete(key)
    except Exception as e:
        logger.error(f"Failed to delete cache: {e}")

# Rate limiting utilities
async def check_rate_limit(user_id: str, limit: int = 100, window: int = 3600) -> bool:
    """Check if user has exceeded rate limit"""
    try:
        redis_client = await get_redis_connection()
        key = f"rate_limit:{user_id}"
        
        # Get current count
        current = await redis_client.get(key)
        if current is None:
            # First request in window
            await redis_client.setex(key, window, 1)
            return True
        
        current_count = int(current)
        if current_count >= limit:
            return False
        
        # Increment counter
        await redis_client.incr(key)
        return True
        
    except Exception as e:
        logger.error(f"Rate limit check failed: {e}")
        return True  # Allow request if rate limiting fails 
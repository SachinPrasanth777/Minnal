from typing import Callable, List, Optional
from pydantic import BaseModel
from redis.asyncio import Redis
import functools


class CacheConfig(BaseModel):
    REDIS_URL: str
    REDIS_PASSWORD: Optional[str] = None
    REDIS_DB: int = 0
    POOL_SIZE: int = 10
    SOCKET_TIMEOUT: int = 5
    SOCKET_CONNECT_TIMEOUT: int = 5
    RETRY_ON_TIMEOUT: bool = True
    HEALTH_CHECK_INTERVAL: int = 30


class CacheService:
    def __init__(self, config: CacheConfig):
        self.config = config
        self.redis: Optional[Redis] = None

    async def initialize(self):
        self.redis = Redis(
            host=self.config.REDIS_URL,
            password=self.config.REDIS_PASSWORD,
            db=self.config.REDIS_DB,
            socket_connect_timeout=self.config.SOCKET_CONNECT_TIMEOUT,
            retry_on_timeout=self.config.RETRY_ON_TIMEOUT,
            health_check_interval=self.config.HEALTH_CHECK_INTERVAL,
        )

    async def set(self, key: str, value: str, expire: Optional[str] = None):
        if not self.redis:
            raise RuntimeError("Cache Service Failed")
        await self.redis.set(key, value, ex=expire)

    async def get(self, key: str):
        if not self.redis:
            raise RuntimeError("Cache Service Failed")
        return await self.redis.get(key)

    async def delete(
        self, prefix: Optional[str] = None, function_name: Optional[str] = None
    ):
        if not self.redis:
            raise RuntimeError("Cache Service Failed")
        pattern = f"{prefix or '*'}:{function_name or '*'}*"
        keys = await self.redis.keys(pattern)
        if keys:
            await self.redis.delete(*keys)

    async def health_check(self):
        if not self.redis:
            return False
        try:
            return await self.redis.ping()
        except Exception:
            return False

    def cache(
        self,
        expire: int = 300,
        include_params: Optional[List[str]] = None,
        key_prefix: Optional[str] = None,
    ):
        def decorator(func: Callable):
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                key_components = [key_prefix or func.__name__]
                if include_params:
                    for param in include_params:
                        key_components.append(str(kwargs.get(param, "missing")))
                key = ":".join(key_components)

                cached_value = await self.get(key)
                if cached_value:
                    return cached_value

                result = await func(*args, **kwargs)
                await self.set(key, result, expire)
                return result

            return wrapper

        return decorator

    async def clear(self):
        if not self.redis:
            raise RuntimeError("CacheService not initialized")
        await self.redis.flushdb()

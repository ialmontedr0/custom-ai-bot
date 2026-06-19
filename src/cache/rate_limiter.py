import time

from src.cache.client import get_redis


class RateLimiter:
    def __init__(self, max_requests: int = 1, window: int = 1) -> None:
        self.max_requests = max_requests
        self.window = window

    async def check(self, user_id: str) -> bool:
        client = await get_redis()
        key = f"rateLimit:{user_id}"
        now = time.time()
        window_start = now - self.window

        await client.zremrangebyscore(key, 0, window_start)

        request_coun = await client.zcard(key)

        if request_coun >= self.max_requests:
            return False

        await client.zadd(key, {str(now): now})
        await client.expire(key, self.window)
        return True

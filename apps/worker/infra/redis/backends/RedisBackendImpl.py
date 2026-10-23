import json
import redis
from datetime import datetime, timezone
from typing import Optional
from config import settings
from ..base import RedisBackend

class RedisBackendImpl(RedisBackend):

    def __init__(self):
        self.redis = redis.Redis.from_url(
            settings.REDIS_URL,
            decode_responses=True,
        )

    def get(self, key: str) -> str | None:
        value = self.redis.get(key)

        if value is None:
            return None

        if isinstance(value, bytes):
            return value.decode("utf-8")

        return value

    def set(
        self,
        key: str,
        value: str,
        ttl_seconds: Optional[int] = None,
    ) -> None:

        self.redis.set(
            key,
            value,
            ex=ttl_seconds,
        )

    def delete(self, key: str) -> None:
        self.redis.delete(key)

    def acquire_lock(
        self,
        key: str,
        ttl_seconds: int,
    ) -> bool:

        result = self.redis.set(
            key,
            "1",
            nx=True,
            ex=ttl_seconds,
        )

        return bool(result)

    def release_lock(self, key: str) -> None:
        self.redis.delete(key)

    def log(
        self,
        job_id: str,
        message: str,
        level: str,
    ) -> None:

        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": level,
            "message": message,
        }

        key = f"quillstream:logs:{job_id}"

        self.redis.lpush(
            key,
            json.dumps(entry),
        )
from enum import StrEnum

class RedisBackendType(StrEnum):
    REDIS = "redis"
    UPSTASH = "upstash"
    VALKEY = "valkey"
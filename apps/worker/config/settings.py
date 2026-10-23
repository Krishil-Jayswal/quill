from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict
from .enums import (
    LLMProvider, 
    TranscriptionProviderType,
    FrameReductionProviderType,
    OcrProviderType,
    WorkerType, 
    RedisBackendType,
    KafkaBackendType,
    StorageBackendType,
    LoggerBackendType,
    KafkaSaslMechanism,
    KafkaSecurityProtocol,
)

class Settings(BaseSettings):
    # Worker Config
    WORKER_TYPE: WorkerType = WorkerType.MEDIA

    # Infra Config
    REDIS_BACKEND: RedisBackendType = RedisBackendType.REDIS
    KAFKA_BACKEND: KafkaBackendType = KafkaBackendType.KAFKA
    STORAGE_BACKEND: StorageBackendType = StorageBackendType.MINIO
    LOGGER_BACKEND: LoggerBackendType = LoggerBackendType.KAFKA

    # Provider config
    TRANSCRIPTION_PROVIDER: TranscriptionProviderType = TranscriptionProviderType.WHISPER
    FRAME_REDUCTION_PROVIDER: FrameReductionProviderType = FrameReductionProviderType.MOBILE_NET
    OCR_PROVIDER: OcrProviderType = OcrProviderType.GROQ
    LLM_PROVIDER: LLMProvider = LLMProvider.GROQ

    GROQ_API_KEY: str = ""

    REDIS_URL: str = ""

    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    KAFKA_SECURITY_PROTOCOL: KafkaSecurityProtocol = KafkaSecurityProtocol.PLAINTEXT
    KAFKA_SASL_MECHANISM: KafkaSaslMechanism = KafkaSaslMechanism.PLAIN
    KAFKA_SASL_USERNAME: str = ""
    KAFKA_SASL_PASSWORD: str = ""
    KAFKA_CLIENT_ID: str = "quill-worker"

    MINIO_ENDPOINT: str = "http://localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET: str = "quill"
    MINIO_REGION: str = "us-east-1"
    MINIO_SECURE: bool = False
    
    # Environment
    ENVIRONMENT: str = "development"

    # Env file setting
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()

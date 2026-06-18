from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False
    )

    # Telegram
    telegram_bot_token: str = ""
    telegram_webhook_secret: str = ""
    telegram_webhook_url: str = ""

    # Database
    database_url: str = "postgresql+asyncpg://botuser:botpass@postgres:5432/telegram_bot"

    # Redis
    redis_url: str = "redis://:redispass@redis:6379/0"

    # Qdrant
    qdrant_url: str = "http://qdrant:6333"
    qdrant_grpc_port: int = 6334

    # vLLM
    vllm_url: str = "http://vllm:8001/v1"
    vllm_model_name: str = "Qwen/Qwen2.5-7B-Instruct"

    # Embeddings
    embedding_model: str = "paraphrase-multilingual-MiniLM-L12-v2"

    # Memory
    memory_window_size: int = 20

    # Rate limiting
    rate_limit_msg_per_min: int = 10

    # Sentry
    sentry_dsn: str = ""

    # Search
    search_api_key: str = ""
    search_api_url: str = ""

    # Environment
    environment: str = "development"

    # Log
    log_level: str = "INFO"

    @property
    def is_production(self) -> bool:
        return self.environment == "production"

    @property
    def is_development(self) -> bool:
        return self.environment == "development"


settings = Settings()

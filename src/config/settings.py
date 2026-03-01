"""
Application configuration settings
"""
from typing import List, Generator
from pydantic_settings import BaseSettings
from pydantic import Field
from sqlalchemy.orm import Session


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application
    app_name: str = Field(default="KrishiMitra", env="APP_NAME")
    app_version: str = Field(default="0.1.0", env="APP_VERSION")
    environment: str = Field(default="development", env="ENVIRONMENT")
    debug: bool = Field(default=False, env="DEBUG")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    
    # API
    api_host: str = Field(default="0.0.0.0", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")
    api_prefix: str = Field(default="/api/v1", env="API_PREFIX")
    
    # Database
    database_url: str = Field(..., env="DATABASE_URL")
    database_pool_size: int = Field(default=20, env="DATABASE_POOL_SIZE")
    database_max_overflow: int = Field(default=10, env="DATABASE_MAX_OVERFLOW")
    
    # Redis
    redis_url: str = Field(default="redis://localhost:6379/0", env="REDIS_URL")
    redis_cache_ttl: int = Field(default=3600, env="REDIS_CACHE_TTL")
    
    # Kafka
    kafka_bootstrap_servers: str = Field(default="localhost:9092", env="KAFKA_BOOTSTRAP_SERVERS")
    kafka_consumer_group: str = Field(default="krishimitra-consumers", env="KAFKA_CONSUMER_GROUP")
    
    # AWS
    aws_region: str = Field(default="us-east-1", env="AWS_REGION")
    aws_access_key_id: str = Field(..., env="AWS_ACCESS_KEY_ID")
    aws_secret_access_key: str = Field(..., env="AWS_SECRET_ACCESS_KEY")
    s3_bucket_satellite: str = Field(..., env="S3_BUCKET_SATELLITE")
    s3_bucket_audio: str = Field(..., env="S3_BUCKET_AUDIO")
    
    # Satellite Data
    sentinel_hub_client_id: str = Field(..., env="SENTINEL_HUB_CLIENT_ID")
    sentinel_hub_client_secret: str = Field(..., env="SENTINEL_HUB_CLIENT_SECRET")
    google_earth_engine_key: str = Field(default="", env="GOOGLE_EARTH_ENGINE_KEY")
    
    # Weather Data
    openweathermap_api_key: str = Field(..., env="OPENWEATHERMAP_API_KEY")
    noaa_api_key: str = Field(default="", env="NOAA_API_KEY")
    
    # Voice Services
    twilio_account_sid: str = Field(..., env="TWILIO_ACCOUNT_SID")
    twilio_auth_token: str = Field(..., env="TWILIO_AUTH_TOKEN")
    twilio_phone_number: str = Field(..., env="TWILIO_PHONE_NUMBER")
    exotel_api_key: str = Field(default="", env="EXOTEL_API_KEY")
    exotel_api_token: str = Field(default="", env="EXOTEL_API_TOKEN")
    
    # LLM Services
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    anthropic_api_key: str = Field(default="", env="ANTHROPIC_API_KEY")
    elevenlabs_api_key: str = Field(..., env="ELEVENLABS_API_KEY")
    
    # LLM Provider Selection
    llm_provider: str = Field(default="openai", env="LLM_PROVIDER")  # openai, bedrock, anthropic
    use_aws_services: bool = Field(default=False, env="USE_AWS_SERVICES")  # Use AWS Bedrock, Transcribe, Polly
    
    # Vector Database
    chromadb_host: str = Field(default="localhost", env="CHROMADB_HOST")
    chromadb_port: int = Field(default=8001, env="CHROMADB_PORT")
    
    # Security
    jwt_secret_key: str = Field(..., env="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", env="JWT_ALGORITHM")
    jwt_access_token_expire_minutes: int = Field(default=60, env="JWT_ACCESS_TOKEN_EXPIRE_MINUTES")
    jwt_refresh_token_expire_days: int = Field(default=7, env="JWT_REFRESH_TOKEN_EXPIRE_DAYS")
    encryption_key: str = Field(..., env="ENCRYPTION_KEY")
    
    # Monitoring
    prometheus_port: int = Field(default=9090, env="PROMETHEUS_PORT")
    grafana_port: int = Field(default=3000, env="GRAFANA_PORT")
    
    # Feature Flags
    enable_agentic_ai: bool = Field(default=True, env="ENABLE_AGENTIC_AI")
    enable_voice_chatbot: bool = Field(default=True, env="ENABLE_VOICE_CHATBOT")
    enable_continuous_learning: bool = Field(default=True, env="ENABLE_CONTINUOUS_LEARNING")
    
    # Rate Limiting
    rate_limit_per_minute: int = Field(default=100, env="RATE_LIMIT_PER_MINUTE")
    rate_limit_per_hour: int = Field(default=1000, env="RATE_LIMIT_PER_HOUR")
    rate_limit_per_day: int = Field(default=10000, env="RATE_LIMIT_PER_DAY")
    
    # Cost Optimization
    use_regional_tiles: bool = Field(default=True, env="USE_REGIONAL_TILES")
    enable_caching: bool = Field(default=True, env="ENABLE_CACHING")
    cache_hit_rate_target: float = Field(default=0.85, env="CACHE_HIT_RATE_TARGET")
    
    # Supported Languages
    supported_languages: str = Field(default="hi,bn,te,mr,ta,gu,kn,ml,pa,or", env="SUPPORTED_LANGUAGES")
    
    @property
    def supported_languages_list(self) -> List[str]:
        """Get list of supported language codes"""
        return [lang.strip() for lang in self.supported_languages.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()

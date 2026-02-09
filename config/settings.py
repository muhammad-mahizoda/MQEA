"""
Современная система конфигурации MQEA с использованием Pydantic.

Автор: Мухаммад Махизода
Таджикский национальный университет
"""

from typing import List, Optional, Dict, Any
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from pathlib import Path


class DatabaseSettings(BaseSettings):
    """Настройки базы данных."""
    
    url: str = Field(default="sqlite:///./mqea.db", env="DATABASE_URL")
    echo: bool = Field(default=False, env="DATABASE_ECHO")
    pool_size: int = Field(default=5, env="DATABASE_POOL_SIZE")
    max_overflow: int = Field(default=10, env="DATABASE_MAX_OVERFLOW")
    
    class Config:
        env_prefix = "DB_"


class RedisSettings(BaseSettings):
    """Настройки Redis для кэширования."""
    
    host: str = Field(default="localhost", env="REDIS_HOST")
    port: int = Field(default=6379, env="REDIS_PORT")
    db: int = Field(default=0, env="REDIS_DB")
    password: Optional[str] = Field(default=None, env="REDIS_PASSWORD")
    
    class Config:
        env_prefix = "REDIS_"


class QuantumSettings(BaseSettings):
    """Настройки квантового движка."""
    
    hbar: float = Field(default=1.0, env="QUANTUM_HBAR")
    max_iterations: int = Field(default=100, env="QUANTUM_MAX_ITERATIONS")
    convergence_threshold: float = Field(default=1e-6, env="QUANTUM_CONVERGENCE_THRESHOLD")
    entanglement_threshold: float = Field(default=0.5, env="QUANTUM_ENTANGLEMENT_THRESHOLD")
    
    class Config:
        env_prefix = "QUANTUM_"


class APISettings(BaseSettings):
    """Настройки API."""
    
    title: str = Field(default="MQEA API", env="API_TITLE")
    description: str = Field(default="Medical Quantum Entanglement Analysis API", env="API_DESCRIPTION")
    version: str = Field(default="1.0.0", env="API_VERSION")
    host: str = Field(default="127.0.0.1", env="API_HOST")
    port: int = Field(default=8000, env="API_PORT")
    debug: bool = Field(default=False, env="API_DEBUG")
    cors_origins: List[str] = Field(default=["*"], env="API_CORS_ORIGINS")
    
    class Config:
        env_prefix = "API_"


class LoggingSettings(BaseSettings):
    """Настройки логирования."""
    
    level: str = Field(default="INFO", env="LOG_LEVEL")
    format: str = Field(default="json", env="LOG_FORMAT")
    file: Optional[str] = Field(default=None, env="LOG_FILE")
    max_size: int = Field(default=10485760, env="LOG_MAX_SIZE")  # 10MB
    backup_count: int = Field(default=5, env="LOG_BACKUP_COUNT")
    
    @field_validator('level')
    @classmethod
    def validate_log_level(cls, v):
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if v.upper() not in valid_levels:
            raise ValueError(f'Log level must be one of {valid_levels}')
        return v.upper()
    
    class Config:
        env_prefix = "LOG_"


class SecuritySettings(BaseSettings):
    """Настройки безопасности."""
    
    secret_key: str = Field(default="mqea-secret-key-change-in-production", env="SECRET_KEY")
    algorithm: str = Field(default="HS256", env="SECURITY_ALGORITHM")
    access_token_expire_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_days: int = Field(default=7, env="REFRESH_TOKEN_EXPIRE_DAYS")
    
    class Config:
        env_prefix = "SECURITY_"


class MonitoringSettings(BaseSettings):
    """Настройки мониторинга."""
    
    enabled: bool = Field(default=True, env="MONITORING_ENABLED")
    prometheus_port: int = Field(default=9090, env="PROMETHEUS_PORT")
    sentry_dsn: Optional[str] = Field(default=None, env="SENTRY_DSN")
    health_check_interval: int = Field(default=30, env="HEALTH_CHECK_INTERVAL")
    
    class Config:
        env_prefix = "MONITORING_"


class MQEASettings(BaseSettings):
    """Основные настройки MQEA."""
    
    # Подсистемы
    database: DatabaseSettings = DatabaseSettings()
    redis: RedisSettings = RedisSettings()
    quantum: QuantumSettings = QuantumSettings()
    api: APISettings = APISettings()
    logging: LoggingSettings = LoggingSettings()
    security: SecuritySettings = SecuritySettings()
    monitoring: MonitoringSettings = MonitoringSettings()
    
    # Общие настройки
    app_name: str = Field(default="MQEA", env="APP_NAME")
    environment: str = Field(default="development", env="ENVIRONMENT")
    debug: bool = Field(default=False, env="DEBUG")
    
    # Пути
    base_dir: Path = Field(default=Path(__file__).parent.parent)
    data_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent / "data")
    logs_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent / "logs")
    temp_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent / "temp")
    
    # Медицинские показатели
    supported_indicators: List[str] = Field(default=[
        "heart_rate", "blood_pressure_systolic", "blood_pressure_diastolic",
        "temperature", "oxygen_saturation", "respiratory_rate",
        "glucose", "cholesterol"
    ])
    
    # Ограничения
    max_file_size: int = Field(default=104857600, env="MAX_FILE_SIZE")  # 100MB
    max_analysis_duration: int = Field(default=3600, env="MAX_ANALYSIS_DURATION")  # 1 hour
    
    @field_validator('environment')
    @classmethod
    def validate_environment(cls, v):
        valid_envs = ['development', 'testing', 'staging', 'production']
        if v.lower() not in valid_envs:
            raise ValueError(f'Environment must be one of {valid_envs}')
        return v.lower()
    
    @field_validator('data_dir', 'logs_dir', 'temp_dir')
    @classmethod
    def create_directories(cls, v):
        v.mkdir(parents=True, exist_ok=True)
        return v
    
    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8",
        case_sensitive = False,
        extra = "ignore",  # Игнорировать лишние переменные окружения (они могут быть для вложенных настроек)
        env_ignore_empty = True
    )


# Глобальный экземпляр настроек
settings = MQEASettings()


def get_settings() -> MQEASettings:
    """Получить настройки приложения."""
    return settings


def get_database_url() -> str:
    """Получить URL базы данных."""
    return settings.database.url


def get_redis_url() -> str:
    """Получить URL Redis."""
    redis = settings.redis
    if redis.password:
        return f"redis://:{redis.password}@{redis.host}:{redis.port}/{redis.db}"
    return f"redis://{redis.host}:{redis.port}/{redis.db}"


def is_production() -> bool:
    """Проверить, является ли среда production."""
    return settings.environment == "production"


def is_development() -> bool:
    """Проверить, является ли среда development."""
    return settings.environment == "development"

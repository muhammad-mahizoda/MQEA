"""
Конфигурация MQEA.

Автор: Мухаммад Махизода
Таджикский национальный университет
"""

from .settings import (
    MQEASettings,
    get_settings,
    get_database_url,
    get_redis_url,
    is_production,
    is_development,
    settings
)

__all__ = [
    "MQEASettings",
    "get_settings", 
    "get_database_url",
    "get_redis_url",
    "is_production",
    "is_development",
    "settings"
]

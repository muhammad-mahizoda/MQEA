"""
Современная система логирования MQEA.

Автор: Мухаммад Махизода
Таджикский национальный университет
"""

import logging
import sys
from typing import Optional
from pathlib import Path
import structlog
from config import get_settings

# Получение настроек
settings = get_settings()


def setup_logging():
    """Настройка системы логирования."""
    
    # Настройка structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer() if settings.logging.format == "json" 
            else structlog.dev.ConsoleRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    # Настройка стандартного логгера
    logging.basicConfig(
        level=getattr(logging, settings.logging.level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=get_log_handlers()
    )


def get_log_handlers():
    """Получить обработчики логов."""
    handlers = []
    
    # Консольный обработчик
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, settings.logging.level))
    handlers.append(console_handler)
    
    # Файловый обработчик
    if settings.logging.file:
        log_file = Path(settings.logging.file)
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        from logging.handlers import RotatingFileHandler
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=settings.logging.max_size,
            backupCount=settings.logging.backup_count
        )
        file_handler.setLevel(getattr(logging, settings.logging.level))
        handlers.append(file_handler)
    
    return handlers


def get_logger(name: str) -> structlog.BoundLogger:
    """Получить логгер с именем."""
    return structlog.get_logger(name)


class MQEALogger:
    """Специальный логгер для MQEA."""
    
    def __init__(self, name: str):
        self.logger = get_logger(name)
        self.name = name
    
    def info(self, message: str, **kwargs):
        """Информационное сообщение."""
        self.logger.info(message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Предупреждение."""
        self.logger.warning(message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """Ошибка."""
        self.logger.error(message, **kwargs)
    
    def debug(self, message: str, **kwargs):
        """Отладочное сообщение."""
        self.logger.debug(message, **kwargs)
    
    def critical(self, message: str, **kwargs):
        """Критическая ошибка."""
        self.logger.critical(message, **kwargs)
    
    def quantum_analysis_start(self, time_series_id: str, **kwargs):
        """Начало квантового анализа."""
        self.logger.info(
            "Квантовый анализ запущен",
            event="quantum_analysis_start",
            time_series_id=time_series_id,
            **kwargs
        )
    
    def quantum_analysis_complete(self, time_series_id: str, duration: float, **kwargs):
        """Завершение квантового анализа."""
        self.logger.info(
            "Квантовый анализ завершен",
            event="quantum_analysis_complete",
            time_series_id=time_series_id,
            duration=duration,
            **kwargs
        )
    
    def pattern_detected(self, pattern_type: str, confidence: float, **kwargs):
        """Обнаружен паттерн."""
        self.logger.info(
            "Паттерн обнаружен",
            event="pattern_detected",
            pattern_type=pattern_type,
            confidence=confidence,
            **kwargs
        )
    
    def imputation_start(self, method: str, missing_count: int, **kwargs):
        """Начало заполнения пропусков."""
        self.logger.info(
            "Заполнение пропусков запущено",
            event="imputation_start",
            method=method,
            missing_count=missing_count,
            **kwargs
        )
    
    def imputation_complete(self, method: str, iterations: int, **kwargs):
        """Завершение заполнения пропусков."""
        self.logger.info(
            "Заполнение пропусков завершено",
            event="imputation_complete",
            method=method,
            iterations=iterations,
            **kwargs
        )
    
    def api_request(self, method: str, endpoint: str, status_code: int, **kwargs):
        """API запрос."""
        self.logger.info(
            "API запрос",
            event="api_request",
            method=method,
            endpoint=endpoint,
            status_code=status_code,
            **kwargs
        )
    
    def error_occurred(self, error_type: str, error_message: str, **kwargs):
        """Произошла ошибка."""
        self.logger.error(
            "Ошибка произошла",
            event="error_occurred",
            error_type=error_type,
            error_message=error_message,
            **kwargs
        )


# Инициализация логирования при импорте модуля
setup_logging()

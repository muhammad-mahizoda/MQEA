"""
Система мониторинга MQEA.

Автор: Мухаммад Махизода
Таджикский национальный университет
"""

import time
import psutil
from typing import Dict, Any
from prometheus_client import Counter, Histogram, Gauge, start_http_server
from config import get_settings
from utils.logging import get_logger

logger = get_logger(__name__)
settings = get_settings()

# Метрики Prometheus
quantum_analysis_requests = Counter(
    'mqea_quantum_analysis_requests_total',
    'Total number of quantum analysis requests'
)

quantum_analysis_duration = Histogram(
    'mqea_quantum_analysis_duration_seconds',
    'Duration of quantum analysis in seconds'
)

pattern_detection_requests = Counter(
    'mqea_pattern_detection_requests_total',
    'Total number of pattern detection requests'
)

pattern_detection_duration = Histogram(
    'mqea_pattern_detection_duration_seconds',
    'Duration of pattern detection in seconds'
)

imputation_requests = Counter(
    'mqea_imputation_requests_total',
    'Total number of imputation requests'
)

imputation_duration = Histogram(
    'mqea_imputation_duration_seconds',
    'Duration of imputation in seconds'
)

active_connections = Gauge(
    'mqea_active_connections',
    'Number of active connections'
)

memory_usage = Gauge(
    'mqea_memory_usage_bytes',
    'Memory usage in bytes'
)

cpu_usage = Gauge(
    'mqea_cpu_usage_percent',
    'CPU usage percentage'
)

patterns_detected = Counter(
    'mqea_patterns_detected_total',
    'Total number of patterns detected',
    ['pattern_type']
)

quantum_entanglements = Counter(
    'mqea_quantum_entanglements_total',
    'Total number of quantum entanglements found'
)

api_requests = Counter(
    'mqea_api_requests_total',
    'Total number of API requests',
    ['method', 'endpoint', 'status_code']
)


def setup_monitoring():
    """Настройка системы мониторинга."""
    if not settings.monitoring.enabled:
        logger.info("Мониторинг отключен")
        return
    
    try:
        # Запуск Prometheus сервера
        start_http_server(settings.monitoring.prometheus_port)
        logger.info(f"Prometheus сервер запущен на порту {settings.monitoring.prometheus_port}")
        
        # Настройка Sentry для отслеживания ошибок
        if settings.monitoring.sentry_dsn:
            import sentry_sdk
            from sentry_sdk.integrations.fastapi import FastApiIntegration
            from sentry_sdk.integrations.starlette import StarletteIntegration
            
            sentry_sdk.init(
                dsn=settings.monitoring.sentry_dsn,
                integrations=[
                    FastApiIntegration(auto_enabling_instrumentations=True),
                    StarletteIntegration(auto_enabling_instrumentations=True),
                ],
                traces_sample_rate=0.1,
                environment=settings.environment
            )
            logger.info("Sentry интегрирован для отслеживания ошибок")
        
        # Запуск фонового обновления метрик
        import threading
        metrics_thread = threading.Thread(target=update_system_metrics, daemon=True)
        metrics_thread.start()
        
        logger.info("Система мониторинга настроена успешно")
        
    except Exception as e:
        logger.error(f"Ошибка при настройке мониторинга: {str(e)}")


def update_system_metrics():
    """Обновление системных метрик."""
    while True:
        try:
            # Обновление метрик памяти
            memory_info = psutil.virtual_memory()
            memory_usage.set(memory_info.used)
            
            # Обновление метрик CPU
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_usage.set(cpu_percent)
            
            # Пауза между обновлениями
            time.sleep(settings.monitoring.health_check_interval)
            
        except Exception as e:
            logger.error(f"Ошибка при обновлении метрик: {str(e)}")
            time.sleep(60)  # Пауза при ошибке


def record_quantum_analysis(duration: float):
    """Записать метрику квантового анализа."""
    quantum_analysis_requests.inc()
    quantum_analysis_duration.observe(duration)


def record_pattern_detection(duration: float, pattern_count: int, pattern_types: list):
    """Записать метрику обнаружения паттернов."""
    pattern_detection_requests.inc()
    pattern_detection_duration.observe(duration)
    
    for pattern_type in pattern_types:
        patterns_detected.labels(pattern_type=pattern_type).inc(pattern_count)


def record_imputation(duration: float, method: str):
    """Записать метрику заполнения пропусков."""
    imputation_requests.inc()
    imputation_duration.observe(duration)


def record_api_request(method: str, endpoint: str, status_code: int):
    """Записать метрику API запроса."""
    api_requests.labels(
        method=method,
        endpoint=endpoint,
        status_code=status_code
    ).inc()


def record_quantum_entanglements(count: int):
    """Записать метрику квантовых запутанностей."""
    quantum_entanglements.inc(count)


def get_system_metrics() -> Dict[str, Any]:
    """Получить текущие системные метрики."""
    try:
        memory_info = psutil.virtual_memory()
        cpu_percent = psutil.cpu_percent()
        disk_usage = psutil.disk_usage('/')
        
        return {
            "memory": {
                "total": memory_info.total,
                "available": memory_info.available,
                "used": memory_info.used,
                "percent": memory_info.percent
            },
            "cpu": {
                "percent": cpu_percent,
                "count": psutil.cpu_count()
            },
            "disk": {
                "total": disk_usage.total,
                "used": disk_usage.used,
                "free": disk_usage.free,
                "percent": (disk_usage.used / disk_usage.total) * 100
            },
            "process": {
                "pid": psutil.Process().pid,
                "create_time": psutil.Process().create_time(),
                "num_threads": psutil.Process().num_threads()
            }
        }
    except Exception as e:
        logger.error(f"Ошибка при получении системных метрик: {str(e)}")
        return {}


class HealthChecker:
    """Проверка здоровья системы."""
    
    def __init__(self):
        self.start_time = time.time()
    
    def check_health(self) -> Dict[str, Any]:
        """Проверить здоровье системы."""
        try:
            uptime = time.time() - self.start_time
            metrics = get_system_metrics()
            
            # Проверка критических ресурсов
            memory_ok = metrics.get("memory", {}).get("percent", 0) < 90
            cpu_ok = metrics.get("cpu", {}).get("percent", 0) < 90
            disk_ok = metrics.get("disk", {}).get("percent", 0) < 90
            
            overall_status = "healthy" if all([memory_ok, cpu_ok, disk_ok]) else "unhealthy"
            
            return {
                "status": overall_status,
                "uptime": uptime,
                "checks": {
                    "memory": "ok" if memory_ok else "critical",
                    "cpu": "ok" if cpu_ok else "critical", 
                    "disk": "ok" if disk_ok else "critical"
                },
                "metrics": metrics
            }
            
        except Exception as e:
            logger.error(f"Ошибка при проверке здоровья: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }


# Глобальный экземпляр проверки здоровья
health_checker = HealthChecker()

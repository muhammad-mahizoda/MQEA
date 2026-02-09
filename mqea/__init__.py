"""
Medical Quantum Entanglement Analysis (MQEA)

Революционный алгоритм для анализа многомерных медицинских временных рядов
на основе принципов квантовой запутанности.

Основатель и разработчик: Мухаммад Махизода
Администратор сети Таджикского национального университета
"""

from .core import MQEAAnalyzer
from .quantum_entanglement import QuantumEntanglementEngine
from .data_processor import MedicalDataProcessor
from .visualizer import MQEAVisualizer
from .data_sources import DataSourceManager, create_default_sources, CSVDataLoader, DatabaseDataLoader, APIDataLoader, SyntheticDataGenerator
from .question_generator import QuestionGenerator, MedicalQuestion
from .data_question_integration import MedicalDataQuestionSystem
from .ai_assistant import MQEAAssistant
from .recommendation_engine import MedicalRecommendationEngine, MedicalRecommendation, RecommendationType, RiskLevel
from .patient_profile import PatientProfile, Gender, ActivityLevel, MedicalHistory, create_sample_patient_profiles

# Новые модули системы мониторинга в реальном времени
from .iot_sensors import (
    IoTMedicalSensor, IoTMedicalSensorManager, SensorConfig, 
    SensorReading, AlertLevel, SensorStatus, create_sensor_manager
)
from .realtime_monitoring import (
    RealtimeMonitoringSystem, PatientMonitoringSession, 
    MonitoringAlert, create_monitoring_system
)
from .notification_system import (
    NotificationSystem, NotificationTemplate, NotificationChannel,
    NotificationPriority, NotificationRule, create_notification_system
)
from .realtime_charts import (
    RealtimeChart, RealtimeChartManager, ChartConfig, 
    ChartDataPoint, create_chart_manager
)
from .disease_pattern_analyzer import (
    DiseasePatternAnalyzer,
    DiseasePattern,
    DiseaseAnalysisResult,
    DiseaseCategory
)

__version__ = "1.0.0"
__author__ = "Мухаммад Махизода"
__founder__ = "Мухаммад Махизода"
__institution__ = "Таджикский национальный университет"
__position__ = "Администратор сети"

__all__ = [
    # Основные компоненты MQEA
    "MQEAAnalyzer",
    "QuantumEntanglementEngine",
    "MedicalDataProcessor",
    "MQEAVisualizer",
    "DataSourceManager",
    "create_default_sources",
    "CSVDataLoader",
    "DatabaseDataLoader",
    "APIDataLoader",
    "SyntheticDataGenerator",
    "QuestionGenerator",
    "MedicalQuestion",
    "MedicalDataQuestionSystem",
    "MQEAAssistant",
    "MedicalRecommendationEngine",
    "MedicalRecommendation",
    "RecommendationType",
    "RiskLevel",
    "PatientProfile",
    "Gender",
    "ActivityLevel",
    "MedicalHistory",
    "create_sample_patient_profiles",
    
    # Система мониторинга в реальном времени
    "IoTMedicalSensor",
    "IoTMedicalSensorManager", 
    "SensorConfig",
    "SensorReading",
    "AlertLevel",
    "SensorStatus",
    "create_sensor_manager",
    "RealtimeMonitoringSystem",
    "PatientMonitoringSession",
    "MonitoringAlert",
    "create_monitoring_system",
    "NotificationSystem",
    "NotificationTemplate",
    "NotificationChannel",
    "NotificationPriority",
    "NotificationRule",
    "create_notification_system",
    "RealtimeChart",
    "RealtimeChartManager",
    "ChartConfig",
    "ChartDataPoint",
    "create_chart_manager",
    
    # Анализатор признаков заболеваний
    "DiseasePatternAnalyzer",
    "DiseasePattern",
    "DiseaseAnalysisResult",
    "DiseaseCategory"
]


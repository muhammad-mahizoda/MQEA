"""
Pydantic схемы для MQEA API.

Автор: Мухаммад Махизода
Таджикский национальный университет
"""

from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from pydantic import BaseModel, Field, validator
import numpy as np


class QuantumStateSchema(BaseModel):
    """Схема квантового состояния."""
    
    amplitude: complex = Field(..., description="Амплитуда квантового состояния")
    phase: float = Field(..., description="Фаза квантового состояния")
    energy: float = Field(..., description="Энергия квантового состояния")
    uncertainty: float = Field(..., description="Неопределенность измерения")
    
    class Config:
        json_encoders = {
            complex: lambda v: {"real": v.real, "imag": v.imag}
        }


class EntangledPairSchema(BaseModel):
    """Схема запутанной пары."""
    
    indicator1: str = Field(..., description="Первый показатель")
    indicator2: str = Field(..., description="Второй показатель")
    entanglement_strength: float = Field(..., description="Сила запутанности")
    correlation_phase: float = Field(..., description="Фаза корреляции")
    bell_state: str = Field(..., description="Состояние Белла")


class TemporalPatternSchema(BaseModel):
    """Схема временного паттерна."""
    
    pattern_type: str = Field(..., description="Тип паттерна")
    indicators: List[str] = Field(..., description="Затронутые показатели")
    start_time: datetime = Field(..., description="Время начала")
    end_time: datetime = Field(..., description="Время окончания")
    confidence: float = Field(..., ge=0, le=1, description="Уверенность в паттерне")
    quantum_signature: Optional[Dict[str, Any]] = Field(None, description="Квантовая подпись")


class MedicalDataPointSchema(BaseModel):
    """Схема точки медицинских данных."""
    
    timestamp: datetime = Field(..., description="Временная метка")
    heart_rate: Optional[float] = Field(None, ge=40, le=200, description="Частота сердечных сокращений")
    blood_pressure_systolic: Optional[float] = Field(None, ge=70, le=200, description="Систолическое давление")
    blood_pressure_diastolic: Optional[float] = Field(None, ge=40, le=120, description="Диастолическое давление")
    temperature: Optional[float] = Field(None, ge=35, le=42, description="Температура тела")
    oxygen_saturation: Optional[float] = Field(None, ge=70, le=100, description="Насыщение кислородом")
    respiratory_rate: Optional[float] = Field(None, ge=8, le=30, description="Частота дыхания")
    glucose: Optional[float] = Field(None, ge=50, le=400, description="Уровень глюкозы")
    cholesterol: Optional[float] = Field(None, ge=100, le=300, description="Уровень холестерина")


class MedicalTimeSeriesSchema(BaseModel):
    """Схема медицинского временного ряда."""
    
    data_points: List[MedicalDataPointSchema] = Field(..., description="Точки данных")
    indicators: List[str] = Field(..., description="Список показателей")
    duration_hours: float = Field(..., description="Продолжительность в часах")
    sampling_rate_minutes: int = Field(..., description="Частота дискретизации в минутах")
    missing_percentage: float = Field(..., ge=0, le=100, description="Процент пропущенных данных")
    
    @validator('data_points')
    def validate_data_points(cls, v):
        if not v:
            raise ValueError("Должна быть хотя бы одна точка данных")
        return v


class QuantumAnalysisRequestSchema(BaseModel):
    """Схема запроса квантового анализа."""
    
    time_series: MedicalTimeSeriesSchema = Field(..., description="Временной ряд для анализа")
    quantum_threshold: float = Field(0.5, ge=0, le=1, description="Порог квантовой запутанности")
    time_windows: Optional[List[int]] = Field(None, description="Временные окна для анализа")
    enable_pattern_detection: bool = Field(True, description="Включить обнаружение паттернов")
    enable_quantum_imputation: bool = Field(True, description="Включить квантовое заполнение")


class QuantumAnalysisResultSchema(BaseModel):
    """Схема результата квантового анализа."""
    
    quantum_entanglements: List[Dict[str, Any]] = Field(..., description="Результаты запутанности")
    entanglement_network: Dict[str, List[str]] = Field(..., description="Сеть запутанности")
    quantum_patterns: List[Dict[str, Any]] = Field(..., description="Квантовые паттерны")
    temporal_analysis: Dict[str, Any] = Field(..., description="Временной анализ")
    quantum_signatures: Dict[str, Any] = Field(..., description="Квантовые подписи")
    analysis_duration: float = Field(..., description="Длительность анализа в секундах")
    created_at: datetime = Field(default_factory=datetime.now, description="Время создания")


class ImputationRequestSchema(BaseModel):
    """Схема запроса заполнения пропусков."""
    
    time_series: MedicalTimeSeriesSchema = Field(..., description="Временной ряд с пропусками")
    method: str = Field("quantum", description="Метод заполнения")
    max_iterations: int = Field(100, ge=1, le=1000, description="Максимальное количество итераций")
    
    @validator('method')
    def validate_method(cls, v):
        valid_methods = ['quantum', 'linear', 'mean']
        if v not in valid_methods:
            raise ValueError(f"Метод должен быть одним из {valid_methods}")
        return v


class ImputationResultSchema(BaseModel):
    """Схема результата заполнения пропусков."""
    
    filled_time_series: MedicalTimeSeriesSchema = Field(..., description="Заполненный временной ряд")
    iterations_used: int = Field(..., description="Использованные итерации")
    convergence_achieved: bool = Field(..., description="Достигнута ли сходимость")
    final_convergence: float = Field(..., description="Финальная сходимость")
    processing_time: float = Field(..., description="Время обработки в секундах")


class PatternDetectionRequestSchema(BaseModel):
    """Схема запроса обнаружения паттернов."""
    
    time_series: MedicalTimeSeriesSchema = Field(..., description="Временной ряд для анализа")
    pattern_types: Optional[List[str]] = Field(None, description="Типы паттернов для поиска")
    min_pattern_length: int = Field(10, ge=1, description="Минимальная длина паттерна")
    quantum_threshold: float = Field(0.5, ge=0, le=1, description="Порог квантовой запутанности")


class PatternDetectionResultSchema(BaseModel):
    """Схема результата обнаружения паттернов."""
    
    patterns: List[TemporalPatternSchema] = Field(..., description="Обнаруженные паттерны")
    total_patterns: int = Field(..., description="Общее количество паттернов")
    pattern_types_found: List[str] = Field(..., description="Найденные типы паттернов")
    quantum_patterns_count: int = Field(..., description="Количество квантовых паттернов")
    processing_time: float = Field(..., description="Время обработки в секундах")


class HealthCheckSchema(BaseModel):
    """Схема проверки здоровья системы."""
    
    status: str = Field(..., description="Статус системы")
    version: str = Field(..., description="Версия MQEA")
    uptime: float = Field(..., description="Время работы в секундах")
    quantum_engine_status: str = Field(..., description="Статус квантового движка")
    database_status: str = Field(..., description="Статус базы данных")
    redis_status: str = Field(..., description="Статус Redis")
    memory_usage: Dict[str, Any] = Field(..., description="Использование памяти")
    cpu_usage: float = Field(..., description="Использование CPU")
    timestamp: datetime = Field(default_factory=datetime.now, description="Время проверки")


class ErrorResponseSchema(BaseModel):
    """Схема ответа об ошибке."""
    
    error: str = Field(..., description="Тип ошибки")
    message: str = Field(..., description="Сообщение об ошибке")
    details: Optional[Dict[str, Any]] = Field(None, description="Детали ошибки")
    timestamp: datetime = Field(default_factory=datetime.now, description="Время ошибки")
    request_id: Optional[str] = Field(None, description="ID запроса")


class SuccessResponseSchema(BaseModel):
    """Схема успешного ответа."""
    
    success: bool = Field(True, description="Статус успеха")
    message: str = Field(..., description="Сообщение")
    data: Optional[Dict[str, Any]] = Field(None, description="Данные ответа")
    timestamp: datetime = Field(default_factory=datetime.now, description="Время ответа")


class FileUploadSchema(BaseModel):
    """Схема загрузки файла."""
    
    filename: str = Field(..., description="Имя файла")
    content_type: str = Field(..., description="Тип содержимого")
    size: int = Field(..., description="Размер файла в байтах")
    uploaded_at: datetime = Field(default_factory=datetime.now, description="Время загрузки")


class AnalysisJobSchema(BaseModel):
    """Схема задачи анализа."""
    
    job_id: str = Field(..., description="ID задачи")
    status: str = Field(..., description="Статус задачи")
    progress: float = Field(0, ge=0, le=100, description="Прогресс в процентах")
    created_at: datetime = Field(default_factory=datetime.now, description="Время создания")
    started_at: Optional[datetime] = Field(None, description="Время начала")
    completed_at: Optional[datetime] = Field(None, description="Время завершения")
    result: Optional[Dict[str, Any]] = Field(None, description="Результат анализа")
    error: Optional[str] = Field(None, description="Ошибка выполнения")

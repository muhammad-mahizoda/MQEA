"""
Сервис обнаружения паттернов MQEA.

Автор: Мухаммад Махизода
Таджикский национальный университет
"""

import asyncio
from typing import Dict, List, Any, Optional
from models.schemas import MedicalTimeSeriesSchema, TemporalPatternSchema
from utils.logging import get_logger

logger = get_logger(__name__)


class PatternDetectionService:
    """Сервис для обнаружения паттернов в медицинских данных."""
    
    def __init__(self):
        """Инициализация сервиса."""
        from mqea import MQEAAnalyzer
        self.analyzer = MQEAAnalyzer()
        logger.info("PatternDetectionService инициализирован")
    
    async def detect_patterns(
        self,
        time_series: MedicalTimeSeriesSchema,
        pattern_types: Optional[List[str]] = None,
        min_pattern_length: int = 10,
        quantum_threshold: float = 0.5
    ) -> Dict[str, Any]:
        """
        Обнаружить паттерны в данных.
        
        Args:
            time_series: Медицинский временной ряд
            pattern_types: Типы паттернов для поиска
            min_pattern_length: Минимальная длина паттерна
            quantum_threshold: Порог квантовой запутанности
            
        Returns:
            Результат обнаружения паттернов
        """
        try:
            logger.info("Начало обнаружения паттернов")
            
            # Конвертация схемы в объект MQEA
            mqea_time_series = await self._convert_to_mqea_timeseries(time_series)
            
            # Выполнение обнаружения в отдельном потоке
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                self._run_pattern_detection,
                mqea_time_series,
                pattern_types,
                min_pattern_length,
                quantum_threshold
            )
            
            logger.info("Обнаружение паттернов завершено успешно")
            return result
            
        except Exception as e:
            logger.error(f"Ошибка при обнаружении паттернов: {str(e)}")
            raise
    
    def _run_pattern_detection(
        self,
        time_series,
        pattern_types: Optional[List[str]],
        min_pattern_length: int,
        quantum_threshold: float
    ) -> Dict[str, Any]:
        """Выполнить обнаружение паттернов в синхронном режиме."""
        
        # Обнаружение паттернов
        patterns = self.analyzer.detect_patterns(time_series=time_series)
        
        # Фильтрация по типам паттернов
        if pattern_types:
            patterns = [p for p in patterns if p.pattern_type in pattern_types]
        
        # Конвертация в схемы
        pattern_schemas = [
            TemporalPatternSchema(
                pattern_type=pattern.pattern_type,
                indicators=pattern.indicators,
                start_time=pattern.start_time,
                end_time=pattern.end_time,
                confidence=pattern.confidence,
                quantum_signature=pattern.quantum_signature
            )
            for pattern in patterns
        ]
        
        # Подсчет статистики
        total_patterns = len(patterns)
        pattern_types_found = list(set([p.pattern_type for p in patterns]))
        quantum_patterns_count = len([p for p in patterns if p.pattern_type == 'quantum_entangled'])
        
        # Формирование результата
        result = {
            "patterns": pattern_schemas,
            "total_patterns": total_patterns,
            "pattern_types_found": pattern_types_found,
            "quantum_patterns_count": quantum_patterns_count
        }
        
        return result
    
    async def _convert_to_mqea_timeseries(
        self, 
        time_series: MedicalTimeSeriesSchema
    ):
        """Конвертировать схему в объект MQEA временного ряда."""
        import pandas as pd
        from mqea.data_processor import MedicalTimeSeries
        
        # Создание DataFrame
        data_dict = {}
        for indicator in time_series.indicators:
            data_dict[indicator] = [
                getattr(point, indicator) for point in time_series.data_points
            ]
        
        df = pd.DataFrame(data_dict)
        
        # Создание временных меток
        timestamps = pd.to_datetime([
            point.timestamp for point in time_series.data_points
        ])
        df.index = timestamps
        
        # Создание маски пропущенных данных
        missing_mask = df.isnull()
        
        # Создание объекта MedicalTimeSeries
        mqea_time_series = MedicalTimeSeries(
            data=df,
            indicators=time_series.indicators,
            timestamps=timestamps,
            missing_data_mask=missing_mask,
            quantum_states={indicator: [0.0] * len(df) for indicator in time_series.indicators},
            metadata={
                "duration_hours": time_series.duration_hours,
                "sampling_rate_minutes": time_series.sampling_rate_minutes,
                "missing_percentage": time_series.missing_percentage
            }
        )
        
        return mqea_time_series
    
    async def get_pattern_statistics(self) -> Dict[str, Any]:
        """Получить статистику обнаруженных паттернов."""
        try:
            # Здесь можно добавить логику для получения статистики
            # из базы данных или кэша
            return {
                "total_patterns_detected": 0,
                "pattern_types_available": [
                    "periodic", "trend_increasing", "trend_decreasing", 
                    "anomaly", "quantum_entangled"
                ],
                "last_analysis_time": None
            }
        except Exception as e:
            logger.error(f"Ошибка при получении статистики: {str(e)}")
            raise

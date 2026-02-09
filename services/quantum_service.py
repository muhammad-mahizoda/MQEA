"""
Сервис квантового анализа MQEA.

Автор: Мухаммад Махизода
Таджикский национальный университет
"""

import asyncio
import time
from typing import Dict, List, Any, Optional
from datetime import datetime

from mqea import MQEAAnalyzer
from models.schemas import MedicalTimeSeriesSchema, QuantumAnalysisResultSchema
from utils.logging import get_logger

logger = get_logger(__name__)


class QuantumAnalysisService:
    """Сервис для выполнения квантового анализа."""
    
    def __init__(self):
        """Инициализация сервиса."""
        self.analyzer = MQEAAnalyzer(
            quantum_hbar=1.0,
            enable_quantum_imputation=True,
            enable_pattern_detection=True
        )
        logger.info("QuantumAnalysisService инициализирован")
    
    async def analyze_entanglement(
        self,
        time_series: MedicalTimeSeriesSchema,
        quantum_threshold: float = 0.5,
        time_windows: Optional[List[int]] = None,
        enable_pattern_detection: bool = True,
        enable_quantum_imputation: bool = True
    ) -> Dict[str, Any]:
        """
        Выполнить квантовый анализ запутанности.
        
        Args:
            time_series: Медицинский временной ряд
            quantum_threshold: Порог квантовой запутанности
            time_windows: Временные окна для анализа
            enable_pattern_detection: Включить обнаружение паттернов
            enable_quantum_imputation: Включить квантовое заполнение
            
        Returns:
            Результаты квантового анализа
        """
        try:
            logger.info("Начало квантового анализа запутанности")
            
            # Конвертация схемы в объект MQEA
            mqea_time_series = await self._convert_to_mqea_timeseries(time_series)
            
            # Выполнение анализа в отдельном потоке
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                self._run_quantum_analysis,
                mqea_time_series,
                quantum_threshold,
                time_windows,
                enable_pattern_detection,
                enable_quantum_imputation
            )
            
            logger.info("Квантовый анализ запутанности завершен успешно")
            return result
            
        except Exception as e:
            logger.error(f"Ошибка при квантовом анализе: {str(e)}")
            raise
    
    def _run_quantum_analysis(
        self,
        time_series,
        quantum_threshold: float,
        time_windows: Optional[List[int]],
        enable_pattern_detection: bool,
        enable_quantum_imputation: bool
    ) -> Dict[str, Any]:
        """Выполнить квантовый анализ в синхронном режиме."""
        
        # Квантовый анализ запутанности
        quantum_results = self.analyzer.quantum_entanglement_analysis(
            time_series=time_series,
            quantum_threshold=quantum_threshold,
            time_windows=time_windows
        )
        
        # Обнаружение паттернов
        patterns = []
        if enable_pattern_detection:
            patterns = self.analyzer.detect_patterns(time_series=time_series)
        
        # Заполнение пропущенных данных
        filled_data = time_series
        if enable_quantum_imputation:
            filled_data = self.analyzer.fill_missing_data(
                time_series=time_series,
                method='quantum'
            )
        
        # Формирование результата
        result = {
            "quantum_entanglements": quantum_results.get('quantum_entanglements', []),
            "entanglement_network": quantum_results.get('entanglement_network', {}),
            "quantum_patterns": [
                {
                    "type": pattern.pattern_type,
                    "indicators": pattern.indicators,
                    "start_time": pattern.start_time.isoformat(),
                    "end_time": pattern.end_time.isoformat(),
                    "confidence": pattern.confidence,
                    "quantum_signature": pattern.quantum_signature
                }
                for pattern in patterns
            ],
            "temporal_analysis": quantum_results.get('temporal_analysis', {}),
            "quantum_signatures": quantum_results.get('quantum_signatures', {})
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
    
    async def get_analysis_summary(self) -> Dict[str, Any]:
        """Получить сводку анализа."""
        try:
            summary = self.analyzer.get_analysis_summary()
            return summary
        except Exception as e:
            logger.error(f"Ошибка при получении сводки: {str(e)}")
            raise
    
    async def reset_analyzer(self):
        """Сбросить анализатор."""
        try:
            self.analyzer.reset()
            logger.info("Анализатор сброшен")
        except Exception as e:
            logger.error(f"Ошибка при сбросе анализатора: {str(e)}")
            raise

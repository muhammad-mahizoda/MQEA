"""
Сервис заполнения пропущенных данных MQEA.

Автор: Мухаммад Махизода
Таджикский национальный университет
"""

import asyncio
from typing import Dict, Any
from models.schemas import MedicalTimeSeriesSchema, ImputationResultSchema
from utils.logging import get_logger

logger = get_logger(__name__)


class ImputationService:
    """Сервис для заполнения пропущенных данных."""
    
    def __init__(self):
        """Инициализация сервиса."""
        from mqea import MQEAAnalyzer
        self.analyzer = MQEAAnalyzer()
        logger.info("ImputationService инициализирован")
    
    async def fill_missing_data(
        self,
        time_series: MedicalTimeSeriesSchema,
        method: str = "quantum",
        max_iterations: int = 100
    ) -> Dict[str, Any]:
        """
        Заполнить пропущенные данные.
        
        Args:
            time_series: Медицинский временной ряд с пропусками
            method: Метод заполнения ('quantum', 'linear', 'mean')
            max_iterations: Максимальное количество итераций
            
        Returns:
            Результат заполнения данных
        """
        try:
            logger.info(f"Начало заполнения данных методом {method}")
            
            # Конвертация схемы в объект MQEA
            mqea_time_series = await self._convert_to_mqea_timeseries(time_series)
            
            # Выполнение заполнения в отдельном потоке
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                self._run_imputation,
                mqea_time_series,
                method,
                max_iterations
            )
            
            logger.info("Заполнение данных завершено успешно")
            return result
            
        except Exception as e:
            logger.error(f"Ошибка при заполнении данных: {str(e)}")
            raise
    
    def _run_imputation(
        self,
        time_series,
        method: str,
        max_iterations: int
    ) -> Dict[str, Any]:
        """Выполнить заполнение в синхронном режиме."""
        
        # Заполнение пропущенных данных
        filled_data = self.analyzer.fill_missing_data(
            time_series=time_series,
            method=method,
            max_iterations=max_iterations
        )
        
        # Конвертация обратно в схему
        filled_schema = self._convert_to_schema(filled_data)
        
        # Формирование результата
        result = {
            "filled_time_series": filled_schema,
            "iterations_used": filled_data.metadata.get('quantum_imputation_iterations', 1),
            "convergence_achieved": filled_data.metadata.get('final_convergence', 0) < 1e-6,
            "final_convergence": filled_data.metadata.get('final_convergence', 0)
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
    
    def _convert_to_schema(self, mqea_time_series) -> MedicalTimeSeriesSchema:
        """Конвертировать объект MQEA в схему."""
        from models.schemas import MedicalDataPointSchema
        
        # Создание точек данных
        data_points = []
        for i, timestamp in enumerate(mqea_time_series.timestamps):
            point_data = {
                "timestamp": timestamp,
            }
            
            for indicator in mqea_time_series.indicators:
                value = mqea_time_series.data.loc[timestamp, indicator]
                point_data[indicator] = value if not pd.isna(value) else None
            
            data_points.append(MedicalDataPointSchema(**point_data))
        
        # Вычисление статистики
        total_points = len(mqea_time_series.timestamps)
        missing_count = mqea_time_series.missing_data_mask.sum().sum()
        missing_percentage = (missing_count / (total_points * len(mqea_time_series.indicators))) * 100
        
        duration_hours = (mqea_time_series.timestamps[-1] - mqea_time_series.timestamps[0]).total_seconds() / 3600
        sampling_rate_minutes = (mqea_time_series.timestamps[1] - mqea_time_series.timestamps[0]).total_seconds() / 60
        
        return MedicalTimeSeriesSchema(
            data_points=data_points,
            indicators=mqea_time_series.indicators,
            duration_hours=duration_hours,
            sampling_rate_minutes=int(sampling_rate_minutes),
            missing_percentage=missing_percentage
        )

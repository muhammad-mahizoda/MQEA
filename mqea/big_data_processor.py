"""
Система обработки больших медицинских данных для MQEA
с поддержкой распределенной обработки и масштабирования.

Автор: Мухаммад Махизода
Таджикский национальный университет
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any, Union, Iterator
from datetime import datetime, timedelta
from dataclasses import dataclass
import warnings
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
import multiprocessing as mp
from pathlib import Path
import json
import pickle
import logging
import sqlite3
import h5py
import dask.dataframe as dd
from dask.distributed import Client, as_completed as dask_completed
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
import gc

from .core import MQEAAnalyzer
from .quantum_entanglement import QuantumEntanglementEngine
from .data_processor import MedicalTimeSeries, TemporalPattern
from .medical_diagnostic_system import MedicalDiagnosticSystem, PatientProfile, DiagnosticResult


@dataclass
class DataChunk:
    """Чанк данных для обработки."""
    chunk_id: str
    patient_ids: List[str]
    time_range: Tuple[datetime, datetime]
    indicators: List[str]
    data: pd.DataFrame
    metadata: Dict[str, Any]


@dataclass
class ProcessingResult:
    """Результат обработки чанка данных."""
    chunk_id: str
    success: bool
    quantum_entanglements: Dict[str, Any]
    patterns: List[TemporalPattern]
    diagnostics: List[DiagnosticResult]
    processing_time: float
    memory_usage: float
    error_message: Optional[str] = None


class BigDataProcessor:
    """
    Процессор больших медицинских данных для MQEA.
    
    Обеспечивает:
    - Обработку терабайтов медицинских данных
    - Распределенную обработку на кластере
    - Потоковую обработку в реальном времени
    - Оптимизацию памяти и производительности
    - Автоматическое масштабирование
    """
    
    def __init__(self, 
                 chunk_size: int = 10000,
                 max_workers: Optional[int] = None,
                 enable_dask: bool = True,
                 enable_streaming: bool = True,
                 memory_limit_gb: float = 8.0,
                 enable_compression: bool = True):
        """
        Инициализация процессора больших данных.
        
        Args:
            chunk_size: Размер чанка данных
            max_workers: Максимальное количество рабочих процессов
            enable_dask: Включить Dask для распределенной обработки
            enable_streaming: Включить потоковую обработку
            memory_limit_gb: Лимит памяти в ГБ
            enable_compression: Включить сжатие данных
        """
        self.chunk_size = chunk_size
        self.max_workers = max_workers or min(mp.cpu_count(), 16)
        self.enable_dask = enable_dask
        self.enable_streaming = enable_streaming
        self.memory_limit_gb = memory_limit_gb
        self.enable_compression = enable_compression
        
        # Инициализация компонентов
        self.mqea_analyzer = MQEAAnalyzer()
        self.medical_system = MedicalDiagnosticSystem()
        
        # Настройка Dask
        if self.enable_dask:
            self.dask_client = Client(
                n_workers=self.max_workers,
                memory_limit=f"{memory_limit_gb}GB",
                threads_per_worker=2
            )
        else:
            self.dask_client = None
        
        # Настройка логирования
        self.logger = logging.getLogger(__name__)
        
        # Кэш для оптимизации
        self._quantum_cache = {}
        self._pattern_cache = {}
        
        # Статистика обработки
        self.processing_stats = {
            'total_chunks_processed': 0,
            'total_patients_analyzed': 0,
            'total_processing_time': 0.0,
            'average_memory_usage': 0.0,
            'error_count': 0
        }
        
        print(f"🚀 Процессор больших данных MQEA инициализирован")
        print(f"   - Размер чанка: {chunk_size:,} записей")
        print(f"   - Рабочих процессов: {self.max_workers}")
        print(f"   - Dask: {'включен' if enable_dask else 'отключен'}")
        print(f"   - Потоковая обработка: {'включена' if enable_streaming else 'отключена'}")
        print(f"   - Лимит памяти: {memory_limit_gb} ГБ")
    
    def process_large_dataset(self, 
                            data_source: Union[str, pd.DataFrame, Iterator[pd.DataFrame]],
                            output_format: str = "parquet",
                            output_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Обработка большого набора медицинских данных.
        
        Args:
            data_source: Источник данных (файл, DataFrame, итератор)
            output_format: Формат выходных данных
            output_path: Путь для сохранения результатов
            
        Returns:
            Dict[str, Any]: Результаты обработки
        """
        print(f"📊 Начинаем обработку большого набора данных...")
        
        start_time = datetime.now()
        results = {
            'total_chunks': 0,
            'successful_chunks': 0,
            'failed_chunks': 0,
            'total_patients': 0,
            'processing_time': 0.0,
            'quantum_entanglements': [],
            'patterns': [],
            'diagnostics': [],
            'statistics': {}
        }
        
        try:
            # Загрузка данных
            if isinstance(data_source, str):
                data_iterator = self._load_data_from_file(data_source)
            elif isinstance(data_source, pd.DataFrame):
                data_iterator = self._chunk_dataframe(data_source)
            else:
                data_iterator = data_source
            
            # Обработка чанков
            if self.enable_dask and self.dask_client:
                chunk_results = self._process_chunks_distributed(data_iterator)
            else:
                chunk_results = self._process_chunks_parallel(data_iterator)
            
            # Агрегация результатов
            for result in chunk_results:
                results['total_chunks'] += 1
                if result.success:
                    results['successful_chunks'] += 1
                    results['quantum_entanglements'].extend(
                        result.quantum_entanglements.get('quantum_entanglements', [])
                    )
                    results['patterns'].extend(result.patterns)
                    results['diagnostics'].extend(result.diagnostics)
                    results['total_patients'] += len(result.diagnostics)
                else:
                    results['failed_chunks'] += 1
                    self.logger.error(f"Ошибка обработки чанка {result.chunk_id}: {result.error_message}")
            
            # Сохранение результатов
            if output_path:
                self._save_results(results, output_path, output_format)
            
            # Обновление статистики
            processing_time = (datetime.now() - start_time).total_seconds()
            results['processing_time'] = processing_time
            
            self.processing_stats['total_chunks_processed'] += results['total_chunks']
            self.processing_stats['total_patients_analyzed'] += results['total_patients']
            self.processing_stats['total_processing_time'] += processing_time
            
            print(f"✅ Обработка завершена:")
            print(f"   - Чанков обработано: {results['successful_chunks']}/{results['total_chunks']}")
            print(f"   - Пациентов проанализировано: {results['total_patients']}")
            print(f"   - Время обработки: {processing_time:.2f} секунд")
            print(f"   - Скорость: {results['total_patients']/processing_time:.1f} пациентов/сек")
            
        except Exception as e:
            self.logger.error(f"Критическая ошибка обработки: {e}")
            results['error'] = str(e)
        
        return results
    
    def _load_data_from_file(self, file_path: str) -> Iterator[pd.DataFrame]:
        """Загрузка данных из файла по чанкам."""
        file_path = Path(file_path)
        
        if file_path.suffix == '.csv':
            # Чтение CSV по чанкам
            for chunk in pd.read_csv(file_path, chunksize=self.chunk_size):
                yield chunk
        elif file_path.suffix == '.parquet':
            # Чтение Parquet
            df = pd.read_parquet(file_path)
            for chunk in self._chunk_dataframe(df):
                yield chunk
        elif file_path.suffix == '.h5':
            # Чтение HDF5
            with h5py.File(file_path, 'r') as f:
                for i in range(0, len(f['data']), self.chunk_size):
                    chunk_data = f['data'][i:i+self.chunk_size]
                    chunk_df = pd.DataFrame(chunk_data)
                    yield chunk_df
        else:
            raise ValueError(f"Неподдерживаемый формат файла: {file_path.suffix}")
    
    def _chunk_dataframe(self, df: pd.DataFrame) -> Iterator[pd.DataFrame]:
        """Разбиение DataFrame на чанки."""
        for i in range(0, len(df), self.chunk_size):
            yield df.iloc[i:i+self.chunk_size].copy()
    
    def _process_chunks_distributed(self, data_iterator: Iterator[pd.DataFrame]) -> List[ProcessingResult]:
        """Распределенная обработка чанков с использованием Dask."""
        print("🔄 Запуск распределенной обработки с Dask...")
        
        # Создание задач Dask
        futures = []
        chunk_id = 0
        
        for chunk_df in data_iterator:
            future = self.dask_client.submit(
                self._process_single_chunk,
                chunk_df,
                f"chunk_{chunk_id}",
                self.mqea_analyzer,
                self.medical_system
            )
            futures.append(future)
            chunk_id += 1
        
        # Сбор результатов
        results = []
        for future in dask_completed(futures):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                self.logger.error(f"Ошибка получения результата: {e}")
                results.append(ProcessingResult(
                    chunk_id="unknown",
                    success=False,
                    quantum_entanglements={},
                    patterns=[],
                    diagnostics=[],
                    processing_time=0.0,
                    memory_usage=0.0,
                    error_message=str(e)
                ))
        
        return results
    
    def _process_chunks_parallel(self, data_iterator: Iterator[pd.DataFrame]) -> List[ProcessingResult]:
        """Параллельная обработка чанков."""
        print("🔄 Запуск параллельной обработки...")
        
        results = []
        chunk_id = 0
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = []
            
            for chunk_df in data_iterator:
                future = executor.submit(
                    self._process_single_chunk,
                    chunk_df,
                    f"chunk_{chunk_id}",
                    self.mqea_analyzer,
                    self.medical_system
                )
                futures.append(future)
                chunk_id += 1
            
            # Сбор результатов
            for future in as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    self.logger.error(f"Ошибка обработки чанка: {e}")
                    results.append(ProcessingResult(
                        chunk_id="unknown",
                        success=False,
                        quantum_entanglements={},
                        patterns=[],
                        diagnostics=[],
                        processing_time=0.0,
                        memory_usage=0.0,
                        error_message=str(e)
                    ))
        
        return results
    
    @staticmethod
    def _process_single_chunk(chunk_df: pd.DataFrame, 
                            chunk_id: str,
                            mqea_analyzer: MQEAAnalyzer,
                            medical_system: MedicalDiagnosticSystem) -> ProcessingResult:
        """Обработка одного чанка данных."""
        start_time = datetime.now()
        start_memory = _get_memory_usage()
        
        try:
            # Создание временного анализатора для изоляции
            temp_analyzer = MQEAAnalyzer()
            
            # Подготовка данных
            if 'timestamp' not in chunk_df.columns:
                chunk_df['timestamp'] = pd.date_range(
                    start=datetime.now() - timedelta(hours=len(chunk_df)),
                    periods=len(chunk_df),
                    freq='H'
                )
            
            # Создание MedicalTimeSeries
            indicators = [col for col in chunk_df.columns if col != 'timestamp']
            time_series = MedicalTimeSeries(
                data=chunk_df.set_index('timestamp'),
                indicators=indicators,
                timestamps=chunk_df['timestamp'].tolist(),
                missing_data_mask=chunk_df[indicators].isnull(),
                quantum_states={},
                metadata={
                    'chunk_id': chunk_id,
                    'total_records': len(chunk_df),
                    'missing_percentage': chunk_df[indicators].isnull().sum().sum() / (len(chunk_df) * len(indicators)) * 100
                }
            )
            
            # Квантовый анализ
            quantum_results = temp_analyzer.quantum_entanglement_analysis(
                time_series=time_series,
                quantum_threshold=0.3
            )
            
            # Обнаружение паттернов
            patterns = temp_analyzer.detect_patterns(time_series=time_series)
            
            # Медицинская диагностика (если есть профили пациентов)
            diagnostics = []
            if 'patient_id' in chunk_df.columns:
                for patient_id in chunk_df['patient_id'].unique():
                    patient_data = chunk_df[chunk_df['patient_id'] == patient_id]
                    patient_time_series = MedicalTimeSeries(
                        data=patient_data.set_index('timestamp'),
                        indicators=indicators,
                        timestamps=patient_data['timestamp'].tolist(),
                        missing_data_mask=patient_data[indicators].isnull(),
                        quantum_states={},
                        metadata={'patient_id': patient_id}
                    )
                    
                    try:
                        diagnostic = medical_system.analyze_patient_data(
                            patient_id=str(patient_id),
                            medical_data=patient_time_series
                        )
                        diagnostics.append(diagnostic)
                    except Exception as e:
                        # Если профиль пациента не найден, пропускаем
                        pass
            
            processing_time = (datetime.now() - start_time).total_seconds()
            memory_usage = _get_memory_usage() - start_memory
            
            return ProcessingResult(
                chunk_id=chunk_id,
                success=True,
                quantum_entanglements=quantum_results,
                patterns=patterns,
                diagnostics=diagnostics,
                processing_time=processing_time,
                memory_usage=memory_usage
            )
            
        except Exception as e:
            processing_time = (datetime.now() - start_time).total_seconds()
            memory_usage = _get_memory_usage() - start_memory
            
            return ProcessingResult(
                chunk_id=chunk_id,
                success=False,
                quantum_entanglements={},
                patterns=[],
                diagnostics=[],
                processing_time=processing_time,
                memory_usage=memory_usage,
                error_message=str(e)
            )
    
    def stream_process_data(self, 
                          data_stream: Iterator[pd.DataFrame],
                          window_size: int = 1000,
                          slide_size: int = 500) -> Iterator[ProcessingResult]:
        """
        Потоковая обработка данных в реальном времени.
        
        Args:
            data_stream: Поток данных
            window_size: Размер окна для анализа
            slide_size: Размер сдвига окна
            
        Yields:
            ProcessingResult: Результаты обработки
        """
        print(f"🌊 Запуск потоковой обработки (окно: {window_size}, сдвиг: {slide_size})...")
        
        window_buffer = []
        result_id = 0
        
        for data_chunk in data_stream:
            window_buffer.append(data_chunk)
            
            # Если буфер заполнен, обрабатываем окно
            if len(window_buffer) >= window_size:
                # Объединяем данные в окне
                window_data = pd.concat(window_buffer, ignore_index=True)
                
                # Обрабатываем окно
                result = self._process_single_chunk(
                    window_data,
                    f"stream_window_{result_id}",
                    self.mqea_analyzer,
                    self.medical_system
                )
                
                yield result
                result_id += 1
                
                # Сдвигаем окно
                window_buffer = window_buffer[slide_size:]
                
                # Очистка памяти
                del window_data
                gc.collect()
    
    def _save_results(self, 
                     results: Dict[str, Any], 
                     output_path: str, 
                     format: str) -> None:
        """Сохранение результатов обработки."""
        output_path = Path(output_path)
        output_path.mkdir(parents=True, exist_ok=True)
        
        if format == "parquet":
            # Сохранение в Parquet
            if results['quantum_entanglements']:
                qe_df = pd.DataFrame(results['quantum_entanglements'])
                qe_df.to_parquet(output_path / "quantum_entanglements.parquet")
            
            if results['patterns']:
                patterns_data = []
                for pattern in results['patterns']:
                    patterns_data.append({
                        'pattern_type': pattern.pattern_type,
                        'indicators': pattern.indicators,
                        'start_time': pattern.start_time,
                        'end_time': pattern.end_time,
                        'confidence': pattern.confidence
                    })
                patterns_df = pd.DataFrame(patterns_data)
                patterns_df.to_parquet(output_path / "patterns.parquet")
        
        elif format == "json":
            # Сохранение в JSON
            with open(output_path / "results.json", 'w', encoding='utf-8') as f:
                json.dump(results, f, default=str, indent=2, ensure_ascii=False)
        
        elif format == "hdf5":
            # Сохранение в HDF5
            with h5py.File(output_path / "results.h5", 'w') as f:
                f.create_dataset('quantum_entanglements', 
                               data=json.dumps(results['quantum_entanglements']).encode())
                f.create_dataset('patterns', 
                               data=json.dumps([p.__dict__ for p in results['patterns']]).encode())
        
        print(f"💾 Результаты сохранены в {output_path}")
    
    def optimize_memory_usage(self) -> Dict[str, Any]:
        """Оптимизация использования памяти."""
        print("🧹 Оптимизация использования памяти...")
        
        # Очистка кэшей
        self._quantum_cache.clear()
        self._pattern_cache.clear()
        
        # Принудительная сборка мусора
        gc.collect()
        
        # Статистика памяти
        memory_stats = {
            'quantum_cache_size': len(self._quantum_cache),
            'pattern_cache_size': len(self._pattern_cache),
            'memory_usage_mb': _get_memory_usage(),
            'gc_objects': len(gc.get_objects())
        }
        
        print(f"✅ Оптимизация завершена:")
        print(f"   - Использование памяти: {memory_stats['memory_usage_mb']:.1f} МБ")
        print(f"   - Объектов в памяти: {memory_stats['gc_objects']:,}")
        
        return memory_stats
    
    def get_processing_statistics(self) -> Dict[str, Any]:
        """Получить статистику обработки."""
        if self.processing_stats['total_chunks_processed'] > 0:
            avg_processing_time = (self.processing_stats['total_processing_time'] / 
                                 self.processing_stats['total_chunks_processed'])
            avg_patients_per_second = (self.processing_stats['total_patients_analyzed'] / 
                                     self.processing_stats['total_processing_time'])
        else:
            avg_processing_time = 0.0
            avg_patients_per_second = 0.0
        
        return {
            **self.processing_stats,
            'average_processing_time_per_chunk': avg_processing_time,
            'average_patients_per_second': avg_patients_per_second,
            'success_rate': (self.processing_stats['total_chunks_processed'] - 
                           self.processing_stats['error_count']) / 
                          max(1, self.processing_stats['total_chunks_processed']),
            'current_memory_usage_mb': _get_memory_usage()
        }
    
    def close(self):
        """Закрытие процессора и освобождение ресурсов."""
        if self.dask_client:
            self.dask_client.close()
        
        # Очистка кэшей
        self._quantum_cache.clear()
        self._pattern_cache.clear()
        
        # Принудительная сборка мусора
        gc.collect()
        
        print("🔒 Процессор больших данных закрыт")


def _get_memory_usage() -> float:
    """Получить текущее использование памяти в МБ."""
    import psutil
    process = psutil.Process()
    return process.memory_info().rss / 1024 / 1024


# Пример использования
if __name__ == "__main__":
    # Создание процессора больших данных
    processor = BigDataProcessor(
        chunk_size=5000,
        max_workers=8,
        enable_dask=True,
        memory_limit_gb=16.0
    )
    
    # Генерация тестовых данных
    print("📊 Генерация тестовых данных...")
    n_patients = 1000
    n_records_per_patient = 100
    
    test_data = []
    for patient_id in range(n_patients):
        for record_id in range(n_records_per_patient):
            test_data.append({
                'patient_id': f"P{patient_id:04d}",
                'timestamp': datetime.now() - timedelta(hours=record_id),
                'heart_rate': np.random.normal(75, 10),
                'blood_pressure_systolic': np.random.normal(120, 15),
                'blood_pressure_diastolic': np.random.normal(80, 10),
                'temperature': np.random.normal(36.6, 0.5),
                'oxygen_saturation': np.random.normal(98, 2)
            })
    
    test_df = pd.DataFrame(test_data)
    
    # Обработка данных
    results = processor.process_large_dataset(
        data_source=test_df,
        output_format="parquet",
        output_path="output/big_data_results"
    )
    
    # Статистика
    stats = processor.get_processing_statistics()
    print(f"\n📈 Статистика обработки:")
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # Закрытие процессора
    processor.close()
    
    print("🏁 Обработка больших данных завершена!")

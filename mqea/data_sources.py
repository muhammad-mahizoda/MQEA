"""
Модуль для работы с различными источниками медицинских данных.

Автор: Мухаммад Махизода
Таджикский национальный университет
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union, Tuple
import requests
import json
from datetime import datetime, timedelta
import sqlite3
import os
from pathlib import Path
import warnings

from .data_processor import MedicalTimeSeries


class MedicalDataSource:
    """Базовый класс для источников медицинских данных."""
    
    def __init__(self, name: str):
        self.name = name
        self.data_cache = {}
    
    def get_data(self, **kwargs) -> MedicalTimeSeries:
        """Получает данные из источника."""
        raise NotImplementedError
    
    def validate_data(self, data: pd.DataFrame) -> bool:
        """Проверяет валидность данных."""
        required_columns = [
            'heart_rate', 'blood_pressure_systolic', 'blood_pressure_diastolic',
            'temperature', 'oxygen_saturation', 'respiratory_rate'
        ]
        return all(col in data.columns for col in required_columns)


class SyntheticDataGenerator(MedicalDataSource):
    """Генератор синтетических медицинских данных."""
    
    def __init__(self):
        super().__init__("Synthetic Generator")
        self.medical_indicators = {
            'heart_rate': {'unit': 'уд/мин', 'normal_range': (60, 100), 'name': 'Частота пульса'},
            'blood_pressure_systolic': {'unit': 'мм рт.ст.', 'normal_range': (90, 140), 'name': 'Систолическое давление'},
            'blood_pressure_diastolic': {'unit': 'мм рт.ст.', 'normal_range': (60, 90), 'name': 'Диастолическое давление'},
            'temperature': {'unit': '°C', 'normal_range': (36.1, 37.2), 'name': 'Температура тела'},
            'oxygen_saturation': {'unit': '%', 'normal_range': (95, 100), 'name': 'Насыщение кислородом'},
            'respiratory_rate': {'unit': 'дых/мин', 'normal_range': (12, 20), 'name': 'Частота дыхания'},
            'glucose': {'unit': 'ммоль/л', 'normal_range': (3.9, 5.6), 'name': 'Уровень глюкозы'},
            'cholesterol': {'unit': 'мг/дл', 'normal_range': (0, 200), 'name': 'Уровень холестерина'}
        }
    
    def get_data(self, 
                 duration_hours: int = 24,
                 sampling_rate_minutes: int = 15,
                 add_noise: bool = True,
                 add_missing_data: bool = True,
                 patient_profile: Optional[Dict] = None) -> MedicalTimeSeries:
        """Генерирует синтетические медицинские данные."""
        
        # Создание временного ряда
        timestamps = pd.date_range(
            start=datetime.now() - timedelta(hours=duration_hours),
            periods=duration_hours * 60 // sampling_rate_minutes,
            freq=f'{sampling_rate_minutes}min'
        )
        
        data = {}
        missing_mask = pd.DataFrame(False, index=timestamps, columns=list(self.medical_indicators.keys()))
        
        for indicator, config in self.medical_indicators.items():
            # Базовые значения с учетом профиля пациента
            if patient_profile and indicator in patient_profile:
                base_value = patient_profile[indicator]
            else:
                base_value = np.mean(config['normal_range'])
            
            # Генерация данных с трендом и сезонностью
            trend = np.linspace(0, 0.1, len(timestamps))
            seasonal = 0.05 * np.sin(2 * np.pi * np.arange(len(timestamps)) / (24 * 60 // sampling_rate_minutes))
            noise = np.random.normal(0, 0.02, len(timestamps)) if add_noise else 0
            
            values = base_value * (1 + trend + seasonal + noise)
            
            # Ограничение значений с учетом профиля пациента
            min_val, max_val = config['normal_range']
            
            # Если значение из профиля пациента выходит за нормальный диапазон,
            # расширяем допустимый диапазон для этого показателя
            if patient_profile and indicator in patient_profile:
                profile_value = patient_profile[indicator]
                if profile_value < min_val:
                    # Значение ниже нормы - расширяем диапазон вниз
                    min_val = max(profile_value * 0.8, min_val * 0.5)
                elif profile_value > max_val:
                    # Значение выше нормы - расширяем диапазон вверх
                    max_val = min(profile_value * 1.2, max_val * 2.0)
            
            values = np.clip(values, min_val, max_val)
            
            data[indicator] = values
            
            # Добавление пропущенных данных
            if add_missing_data:
                missing_indices = np.random.choice(
                    len(timestamps), 
                    size=int(len(timestamps) * 0.05), 
                    replace=False
                )
                missing_mask.loc[timestamps[missing_indices], indicator] = True
                data[indicator] = np.where(missing_mask[indicator], np.nan, data[indicator])
        
        df = pd.DataFrame(data, index=timestamps)
        
        return MedicalTimeSeries(
            data=df,
            indicators=list(self.medical_indicators.keys()),
            timestamps=timestamps,
            missing_data_mask=missing_mask,
            quantum_states={},
            metadata={
                'source': self.name,
                'generation_time': datetime.now(),
                'duration_hours': duration_hours,
                'sampling_rate_minutes': sampling_rate_minutes,
                'missing_percentage': missing_mask.sum().sum() / (len(self.medical_indicators) * len(timestamps)) * 100,
                'patient_profile': patient_profile or {}
            }
        )


class CSVDataLoader(MedicalDataSource):
    """Загрузчик данных из CSV файлов."""
    
    def __init__(self, file_path: str):
        super().__init__("CSV Loader")
        self.file_path = Path(file_path)
    
    def get_data(self, 
                 timestamp_column: str = 'timestamp',
                 date_format: str = '%Y-%m-%d %H:%M:%S') -> MedicalTimeSeries:
        """Загружает данные из CSV файла."""
        
        if not self.file_path.exists():
            raise FileNotFoundError(f"Файл {self.file_path} не найден")
        
        # Загрузка данных
        df = pd.read_csv(self.file_path)
        
        # Преобразование временных меток
        if timestamp_column in df.columns:
            df[timestamp_column] = pd.to_datetime(df[timestamp_column], format=date_format)
            df.set_index(timestamp_column, inplace=True)
        
        # Создание маски пропущенных данных
        missing_mask = df.isnull()
        
        # Определение медицинских показателей
        medical_columns = [col for col in df.columns if col in [
            'heart_rate', 'blood_pressure_systolic', 'blood_pressure_diastolic',
            'temperature', 'oxygen_saturation', 'respiratory_rate', 'glucose', 'cholesterol'
        ]]
        
        return MedicalTimeSeries(
            data=df[medical_columns],
            indicators=medical_columns,
            timestamps=df.index,
            missing_data_mask=missing_mask[medical_columns],
            quantum_states={},
            metadata={
                'source': self.name,
                'file_path': str(self.file_path),
                'load_time': datetime.now(),
                'missing_percentage': missing_mask[medical_columns].sum().sum() / (len(medical_columns) * len(df)) * 100
            }
        )


class DatabaseDataLoader(MedicalDataSource):
    """Загрузчик данных из базы данных."""
    
    def __init__(self, db_path: str, table_name: str = 'medical_data'):
        super().__init__("Database Loader")
        self.db_path = db_path
        self.table_name = table_name
    
    def get_data(self, 
                 patient_id: Optional[str] = None,
                 start_date: Optional[datetime] = None,
                 end_date: Optional[datetime] = None) -> MedicalTimeSeries:
        """Загружает данные из базы данных."""
        
        conn = sqlite3.connect(self.db_path)
        
        # Построение запроса
        query = f"SELECT * FROM {self.table_name}"
        conditions = []
        
        if patient_id:
            conditions.append(f"patient_id = '{patient_id}'")
        if start_date:
            conditions.append(f"timestamp >= '{start_date}'")
        if end_date:
            conditions.append(f"timestamp <= '{end_date}'")
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY timestamp"
        
        # Выполнение запроса
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if df.empty:
            raise ValueError("Данные не найдены в базе данных")
        
        # Преобразование временных меток
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
        
        # Создание маски пропущенных данных
        missing_mask = df.isnull()
        
        # Определение медицинских показателей
        medical_columns = [col for col in df.columns if col in [
            'heart_rate', 'blood_pressure_systolic', 'blood_pressure_diastolic',
            'temperature', 'oxygen_saturation', 'respiratory_rate', 'glucose', 'cholesterol'
        ]]
        
        return MedicalTimeSeries(
            data=df[medical_columns],
            indicators=medical_columns,
            timestamps=df.index,
            missing_data_mask=missing_mask[medical_columns],
            quantum_states={},
            metadata={
                'source': self.name,
                'db_path': self.db_path,
                'table_name': self.table_name,
                'patient_id': patient_id,
                'load_time': datetime.now(),
                'missing_percentage': missing_mask[medical_columns].sum().sum() / (len(medical_columns) * len(df)) * 100
            }
        )


class APIDataLoader(MedicalDataSource):
    """Загрузчик данных из внешних API."""
    
    def __init__(self, api_url: str, api_key: Optional[str] = None):
        super().__init__("API Loader")
        self.api_url = api_url
        self.api_key = api_key
        self.headers = {}
        
        if api_key:
            self.headers['Authorization'] = f'Bearer {api_key}'
    
    def get_data(self, 
                 patient_id: str,
                 start_date: Optional[datetime] = None,
                 end_date: Optional[datetime] = None) -> MedicalTimeSeries:
        """Загружает данные из API."""
        
        params = {'patient_id': patient_id}
        
        if start_date:
            params['start_date'] = start_date.isoformat()
        if end_date:
            params['end_date'] = end_date.isoformat()
        
        try:
            response = requests.get(
                self.api_url,
                headers=self.headers,
                params=params,
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            
            # Преобразование в DataFrame
            df = pd.DataFrame(data['measurements'])
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df.set_index('timestamp', inplace=True)
            
            # Создание маски пропущенных данных
            missing_mask = df.isnull()
            
            # Определение медицинских показателей
            medical_columns = [col for col in df.columns if col in [
                'heart_rate', 'blood_pressure_systolic', 'blood_pressure_diastolic',
                'temperature', 'oxygen_saturation', 'respiratory_rate', 'glucose', 'cholesterol'
            ]]
            
            return MedicalTimeSeries(
                data=df[medical_columns],
                indicators=medical_columns,
                timestamps=df.index,
                missing_data_mask=missing_mask[medical_columns],
                quantum_states={},
                metadata={
                    'source': self.name,
                    'api_url': self.api_url,
                    'patient_id': patient_id,
                    'load_time': datetime.now(),
                    'missing_percentage': missing_mask[medical_columns].sum().sum() / (len(medical_columns) * len(df)) * 100
                }
            )
            
        except requests.RequestException as e:
            raise ConnectionError(f"Ошибка подключения к API: {e}")


class DataSourceManager:
    """Менеджер источников данных."""
    
    def __init__(self):
        self.sources = {}
        self.current_source = None
    
    def add_source(self, name: str, source: MedicalDataSource):
        """Добавляет источник данных."""
        self.sources[name] = source
    
    def set_current_source(self, name: str):
        """Устанавливает текущий источник данных."""
        if name not in self.sources:
            raise ValueError(f"Источник {name} не найден")
        self.current_source = name
    
    def get_data(self, **kwargs) -> MedicalTimeSeries:
        """Получает данные из текущего источника."""
        if not self.current_source:
            raise ValueError("Текущий источник не установлен")
        
        source = self.sources[self.current_source]
        return source.get_data(**kwargs)
    
    def list_sources(self) -> List[str]:
        """Возвращает список доступных источников."""
        return list(self.sources.keys())
    
    def get_source_info(self, name: str) -> Dict:
        """Возвращает информацию об источнике."""
        if name not in self.sources:
            raise ValueError(f"Источник {name} не найден")
        
        source = self.sources[name]
        return {
            'name': source.name,
            'type': type(source).__name__,
            'cached': len(source.data_cache) > 0
        }


# Предустановленные источники данных
def create_default_sources() -> DataSourceManager:
    """Создает менеджер с предустановленными источниками."""
    manager = DataSourceManager()
    
    # Синтетический генератор
    manager.add_source("synthetic", SyntheticDataGenerator())
    
    # Примеры других источников (если файлы существуют)
    if os.path.exists("data/medical_data.csv"):
        manager.add_source("csv", CSVDataLoader("data/medical_data.csv"))
    
    if os.path.exists("data/medical.db"):
        manager.add_source("database", DatabaseDataLoader("data/medical.db"))
    
    return manager

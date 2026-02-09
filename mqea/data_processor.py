"""
Модуль обработки многомерных медицинских временных рядов.

Реализует уникальные алгоритмы для работы с медицинскими данными,
включая квантовое заполнение пропусков и анализ временных паттернов.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Union
from dataclasses import dataclass
from datetime import datetime, timedelta
import warnings
from .quantum_entanglement import QuantumEntanglementEngine


@dataclass
class MedicalTimeSeries:
    """Структура данных для многомерного медицинского временного ряда."""
    data: pd.DataFrame
    indicators: List[str]
    timestamps: pd.DatetimeIndex
    missing_data_mask: pd.DataFrame
    quantum_states: Dict[str, np.ndarray]
    metadata: Dict[str, any]


@dataclass
class TemporalPattern:
    """Обнаруженный временной паттерн в медицинских данных."""
    pattern_type: str  # 'periodic', 'trend', 'anomaly', 'quantum_entangled'
    indicators: List[str]
    start_time: datetime
    end_time: datetime
    confidence: float
    quantum_signature: Optional[Dict[str, float]]


class MedicalDataProcessor:
    """
    Процессор многомерных медицинских временных рядов.
    
    Уникальные возможности:
    - Квантовое заполнение пропущенных данных
    - Обнаружение паттернов через квантовую запутанность
    - Анализ временной неопределенности
    """
    
    def __init__(self, quantum_engine: Optional[QuantumEntanglementEngine] = None):
        """
        Инициализация процессора данных.
        
        Args:
            quantum_engine: Движок квантовой запутанности
        """
        self.quantum_engine = quantum_engine or QuantumEntanglementEngine()
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
    
    def load_medical_data(self, 
                         file_path: str, 
                         time_column: str = 'timestamp',
                         indicator_columns: Optional[List[str]] = None) -> MedicalTimeSeries:
        """
        Загружает медицинские данные из файла.
        
        Args:
            file_path: Путь к файлу с данными
            time_column: Название колонки с временными метками
            indicator_columns: Список колонок с медицинскими показателями
            
        Returns:
            MedicalTimeSeries: Обработанные медицинские данные
        """
        # Загрузка данных
        df = pd.read_csv(file_path)
        
        # Преобразование временных меток
        df[time_column] = pd.to_datetime(df[time_column])
        df = df.set_index(time_column)
        
        # Определение колонок с показателями
        if indicator_columns is None:
            indicator_columns = [col for col in df.columns 
                               if col in self.medical_indicators]
        
        # Создание маски пропущенных данных
        missing_mask = df[indicator_columns].isnull()
        
        # Инициализация квантовых состояний
        quantum_states = {}
        for indicator in indicator_columns:
            quantum_states[indicator] = np.zeros(len(df))
        
        # Создание объекта временного ряда
        time_series = MedicalTimeSeries(
            data=df[indicator_columns],
            indicators=indicator_columns,
            timestamps=df.index,
            missing_data_mask=missing_mask,
            quantum_states=quantum_states,
            metadata={
                'file_path': file_path,
                'total_points': len(df),
                'missing_percentage': missing_mask.sum().sum() / (len(df) * len(indicator_columns)) * 100
            }
        )
        
        return time_series
    
    def quantum_imputation(self, 
                          time_series: MedicalTimeSeries,
                          max_iterations: int = 100,
                          convergence_threshold: float = 1e-6) -> MedicalTimeSeries:
        """
        Заполняет пропущенные данные с использованием квантовых принципов.
        
        Уникальный алгоритм:
        1. Создает квантовые состояния для всех показателей
        2. Вычисляет запутанности между показателями
        3. Использует квантовую интерференцию для восстановления пропусков
        4. Итеративно уточняет значения до сходимости
        
        Args:
            time_series: Временной ряд с пропущенными данными
            max_iterations: Максимальное количество итераций
            convergence_threshold: Порог сходимости
            
        Returns:
            MedicalTimeSeries: Временной ряд с заполненными пропусками
        """
        print("Начинаем квантовое заполнение пропущенных данных...")
        
        # Создаем копию для заполнения
        filled_data = time_series.data.copy()
        missing_mask = time_series.missing_data_mask.copy()
        
        # Инициализация пропущенных значений средними
        for indicator in time_series.indicators:
            if missing_mask[indicator].any():
                mean_val = filled_data[indicator].mean()
                filled_data.loc[missing_mask[indicator], indicator] = mean_val
        
        # Итеративное заполнение
        for iteration in range(max_iterations):
            print(f"Итерация {iteration + 1}/{max_iterations}")
            
            # Сброс квантовых состояний
            self.quantum_engine.reset()
            
            # Создание квантовых состояний для текущих значений
            for i, timestamp in enumerate(time_series.timestamps):
                for indicator in time_series.indicators:
                    if not missing_mask.loc[timestamp, indicator]:
                        value = filled_data.loc[timestamp, indicator]
                        uncertainty = self._calculate_uncertainty(indicator, value)
                        self.quantum_engine.create_quantum_state(
                            f"{indicator}_{i}", value, uncertainty
                        )
            
            # Вычисление запутанностей между показателями
            entanglement_matrix = self._compute_entanglement_matrix(
                time_series.indicators, len(time_series.timestamps)
            )
            
            # Обновление пропущенных значений
            old_values = filled_data[missing_mask].copy()
            
            for i, timestamp in enumerate(time_series.timestamps):
                for indicator in time_series.indicators:
                    if missing_mask.loc[timestamp, indicator]:
                        # Квантовое восстановление значения
                        new_value = self._quantum_reconstruction(
                            indicator, i, filled_data, entanglement_matrix
                        )
                        filled_data.loc[timestamp, indicator] = new_value
            
            # Проверка сходимости
            if missing_mask.any().any():
                new_values = filled_data[missing_mask]
                max_change = np.abs((new_values - old_values) / (old_values + 1e-10)).max().max()
                
                if max_change < convergence_threshold:
                    print(f"Сходимость достигнута на итерации {iteration + 1}")
                    break
        
        # Создание нового временного ряда с заполненными данными
        filled_time_series = MedicalTimeSeries(
            data=filled_data,
            indicators=time_series.indicators,
            timestamps=time_series.timestamps,
            missing_data_mask=pd.DataFrame(False, 
                                         index=time_series.timestamps,
                                         columns=time_series.indicators),
            quantum_states=time_series.quantum_states,
            metadata=time_series.metadata.copy()
        )
        
        filled_time_series.metadata['quantum_imputation_iterations'] = iteration + 1
        filled_time_series.metadata['final_convergence'] = max_change if 'max_change' in locals() else 0
        
        return filled_time_series
    
    def _calculate_uncertainty(self, indicator: str, value: float) -> float:
        """Вычисляет неопределенность измерения для медицинского показателя."""
        if indicator in self.medical_indicators:
            normal_range = self.medical_indicators[indicator]['normal_range']
            min_val, max_val = normal_range
            
            # Неопределенность зависит от отклонения от нормального диапазона
            if min_val <= value <= max_val:
                return 0.1  # Низкая неопределенность для нормальных значений
            else:
                # Высокая неопределенность для аномальных значений
                deviation = min(abs(value - min_val), abs(value - max_val))
                return min(0.5, 0.1 + deviation / (max_val - min_val))
        else:
            return 0.2  # Средняя неопределенность для неизвестных показателей
    
    def _compute_entanglement_matrix(self, 
                                   indicators: List[str], 
                                   time_points: int) -> np.ndarray:
        """Вычисляет матрицу запутанности между всеми показателями."""
        n_indicators = len(indicators)
        entanglement_matrix = np.zeros((n_indicators, n_indicators))
        
        for i, indicator1 in enumerate(indicators):
            for j, indicator2 in enumerate(indicators):
                if i != j:
                    # Вычисляем среднюю запутанность по времени
                    entanglement_values = []
                    for t in range(time_points):
                        state1_name = f"{indicator1}_{t}"
                        state2_name = f"{indicator2}_{t}"
                        
                        if (state1_name in self.quantum_engine.quantum_states and 
                            state2_name in self.quantum_engine.quantum_states):
                            
                            try:
                                entangled_pair = self.quantum_engine.calculate_entanglement(
                                    state1_name, state2_name
                                )
                                entanglement_values.append(entangled_pair.entanglement_strength)
                            except:
                                entanglement_values.append(0.0)
                    
                    if entanglement_values:
                        entanglement_matrix[i, j] = np.mean(entanglement_values)
        
        return entanglement_matrix
    
    def _quantum_reconstruction(self, 
                              indicator: str, 
                              time_index: int,
                              filled_data: pd.DataFrame,
                              entanglement_matrix: np.ndarray) -> float:
        """
        Восстанавливает пропущенное значение с использованием квантовых принципов.
        
        Уникальный алгоритм, основанный на квантовой интерференции.
        """
        indicator_index = filled_data.columns.get_loc(indicator)
        
        # Находим связанные показатели (высокая запутанность)
        related_indicators = []
        for i, other_indicator in enumerate(filled_data.columns):
            if i != indicator_index and entanglement_matrix[indicator_index, i] > 0.3:
                related_indicators.append((other_indicator, i))
        
        if not related_indicators:
            # Если нет связанных показателей, используем простое среднее
            return filled_data[indicator].mean()
        
        # Квантовая реконструкция на основе связанных показателей
        weighted_sum = 0.0
        total_weight = 0.0
        
        for other_indicator, other_index in related_indicators:
            # Получаем значение связанного показателя в тот же момент времени
            timestamp = filled_data.index[time_index]
            related_value = filled_data.loc[timestamp, other_indicator]
            
            # Вес основан на силе запутанности
            weight = entanglement_matrix[indicator_index, other_index]
            
            # Квантовая интерференция между показателями
            interference_factor = self.quantum_engine.quantum_interference(
                f"{indicator}_{time_index}",
                f"{other_indicator}_{time_index}",
                time_delay=0.0
            )
            
            # Корректируем вес с учетом интерференции
            adjusted_weight = weight * (1 + interference_factor)
            
            # Предсказываем значение на основе связанного показателя
            predicted_value = self._predict_value_from_related(
                indicator, other_indicator, related_value
            )
            
            weighted_sum += predicted_value * adjusted_weight
            total_weight += adjusted_weight
        
        if total_weight > 0:
            return weighted_sum / total_weight
        else:
            return filled_data[indicator].mean()
    
    def _predict_value_from_related(self, 
                                  target_indicator: str, 
                                  source_indicator: str, 
                                  source_value: float) -> float:
        """
        Предсказывает значение целевого показателя на основе связанного.
        
        Использует медицинские корреляции и квантовые принципы.
        """
        # Медицинские корреляции между показателями
        correlations = {
            ('heart_rate', 'blood_pressure_systolic'): 0.7,
            ('heart_rate', 'blood_pressure_diastolic'): 0.5,
            ('temperature', 'heart_rate'): 0.6,
            ('oxygen_saturation', 'respiratory_rate'): -0.8,
            ('glucose', 'cholesterol'): 0.4,
        }
        
        # Получаем корреляцию
        correlation = correlations.get((source_indicator, target_indicator), 0.0)
        if correlation == 0.0:
            correlation = correlations.get((target_indicator, source_indicator), 0.0)
        
        if correlation == 0.0:
            # Если нет известной корреляции, используем среднее
            if target_indicator in self.medical_indicators:
                normal_range = self.medical_indicators[target_indicator]['normal_range']
                return np.mean(normal_range)
            else:
                return 0.0
        
        # Нормализуем исходное значение
        if source_indicator in self.medical_indicators:
            source_range = self.medical_indicators[source_indicator]['normal_range']
            normalized_source = (source_value - source_range[0]) / (source_range[1] - source_range[0])
        else:
            normalized_source = 0.5
        
        # Применяем корреляцию
        normalized_target = 0.5 + correlation * (normalized_source - 0.5)
        
        # Денормализуем в целевой показатель
        if target_indicator in self.medical_indicators:
            target_range = self.medical_indicators[target_indicator]['normal_range']
            return target_range[0] + normalized_target * (target_range[1] - target_range[0])
        else:
            return normalized_target * 100  # Простая денормализация
    
    def detect_temporal_patterns(self, 
                               time_series: MedicalTimeSeries,
                               min_pattern_length: int = 10,
                               quantum_threshold: float = 0.5) -> List[TemporalPattern]:
        """
        Обнаруживает временные паттерны в медицинских данных.
        
        Уникальные возможности:
        - Обнаружение квантово-запутанных паттернов
        - Анализ временной неопределенности
        - Выявление скрытых корреляций
        
        Args:
            time_series: Временной ряд для анализа
            min_pattern_length: Минимальная длина паттерна
            quantum_threshold: Порог для квантовых паттернов
            
        Returns:
            List[TemporalPattern]: Список обнаруженных паттернов
        """
        patterns = []
        
        # 1. Обнаружение периодических паттернов
        periodic_patterns = self._detect_periodic_patterns(
            time_series, min_pattern_length
        )
        patterns.extend(periodic_patterns)
        
        # 2. Обнаружение трендов
        trend_patterns = self._detect_trend_patterns(
            time_series, min_pattern_length
        )
        patterns.extend(trend_patterns)
        
        # 3. Обнаружение аномалий
        anomaly_patterns = self._detect_anomaly_patterns(
            time_series, min_pattern_length
        )
        patterns.extend(anomaly_patterns)
        
        # 4. Обнаружение квантово-запутанных паттернов (уникальная особенность)
        quantum_patterns = self._detect_quantum_entangled_patterns(
            time_series, min_pattern_length, quantum_threshold
        )
        patterns.extend(quantum_patterns)
        
        return patterns
    
    def _detect_periodic_patterns(self, 
                                time_series: MedicalTimeSeries,
                                min_length: int) -> List[TemporalPattern]:
        """Обнаруживает периодические паттерны в данных."""
        patterns = []
        
        for indicator in time_series.indicators:
            data = time_series.data[indicator].dropna()
            
            if len(data) < min_length * 2:
                continue
            
            # Используем FFT для обнаружения периодичности
            fft = np.fft.fft(data.values)
            freqs = np.fft.fftfreq(len(data))
            
            # Находим доминирующие частоты
            power_spectrum = np.abs(fft) ** 2
            dominant_freqs = np.argsort(power_spectrum)[-3:]  # Топ-3 частоты
            
            for freq_idx in dominant_freqs:
                if freqs[freq_idx] > 0:  # Только положительные частоты
                    period = 1 / freqs[freq_idx]
                    
                    if period >= min_length:
                        # Создаем паттерн
                        pattern = TemporalPattern(
                            pattern_type='periodic',
                            indicators=[indicator],
                            start_time=data.index[0],
                            end_time=data.index[-1],
                            confidence=power_spectrum[freq_idx] / np.max(power_spectrum),
                            quantum_signature=None
                        )
                        patterns.append(pattern)
        
        return patterns
    
    def _detect_trend_patterns(self, 
                             time_series: MedicalTimeSeries,
                             min_length: int) -> List[TemporalPattern]:
        """Обнаруживает трендовые паттерны в данных."""
        patterns = []
        
        for indicator in time_series.indicators:
            data = time_series.data[indicator].dropna()
            
            if len(data) < min_length:
                continue
            
            # Вычисляем тренд с помощью линейной регрессии
            x = np.arange(len(data))
            y = data.values
            
            # Простая линейная регрессия
            coeffs = np.polyfit(x, y, 1)
            slope = coeffs[0]
            
            # Определяем тип тренда
            if abs(slope) > np.std(y) * 0.1:  # Значимый тренд
                trend_type = 'increasing' if slope > 0 else 'decreasing'
                
                pattern = TemporalPattern(
                    pattern_type=f'trend_{trend_type}',
                    indicators=[indicator],
                    start_time=data.index[0],
                    end_time=data.index[-1],
                    confidence=abs(slope) / (np.std(y) + 1e-10),
                    quantum_signature=None
                )
                patterns.append(pattern)
        
        return patterns
    
    def _detect_anomaly_patterns(self, 
                               time_series: MedicalTimeSeries,
                               min_length: int) -> List[TemporalPattern]:
        """Обнаруживает аномальные паттерны в данных."""
        patterns = []
        
        for indicator in time_series.indicators:
            data = time_series.data[indicator].dropna()
            
            if len(data) < min_length:
                continue
            
            # Вычисляем статистические границы
            mean_val = data.mean()
            std_val = data.std()
            
            # Находим аномалии (значения за пределами 2 стандартных отклонений)
            anomaly_mask = np.abs(data - mean_val) > 2 * std_val
            
            if anomaly_mask.any():
                # Группируем соседние аномалии
                anomaly_indices = data.index[anomaly_mask]
                
                # Простая группировка по времени
                groups = []
                current_group = [anomaly_indices[0]]
                
                for i in range(1, len(anomaly_indices)):
                    time_diff = (anomaly_indices[i] - anomaly_indices[i-1]).total_seconds() / 3600  # часы
                    
                    if time_diff < 24:  # В пределах 24 часов
                        current_group.append(anomaly_indices[i])
                    else:
                        if len(current_group) >= min_length:
                            groups.append(current_group)
                        current_group = [anomaly_indices[i]]
                
                if len(current_group) >= min_length:
                    groups.append(current_group)
                
                # Создаем паттерны для каждой группы
                for group in groups:
                    pattern = TemporalPattern(
                        pattern_type='anomaly',
                        indicators=[indicator],
                        start_time=group[0],
                        end_time=group[-1],
                        confidence=len(group) / len(data),
                        quantum_signature=None
                    )
                    patterns.append(pattern)
        
        return patterns
    
    def _detect_quantum_entangled_patterns(self, 
                                         time_series: MedicalTimeSeries,
                                         min_length: int,
                                         threshold: float) -> List[TemporalPattern]:
        """
        Обнаруживает квантово-запутанные паттерны (уникальная особенность MQEA).
        
        Ищет периоды, когда показатели демонстрируют квантовую запутанность.
        """
        patterns = []
        
        # Создаем скользящее окно для анализа
        window_size = min_length
        
        for start_idx in range(len(time_series.timestamps) - window_size + 1):
            end_idx = start_idx + window_size
            
            # Извлекаем данные для окна
            window_data = time_series.data.iloc[start_idx:end_idx]
            window_timestamps = time_series.timestamps[start_idx:end_idx]
            
            # Сбрасываем квантовые состояния
            self.quantum_engine.reset()
            
            # Создаем квантовые состояния для всех показателей в окне
            quantum_entanglements = []
            
            for i, timestamp in enumerate(window_timestamps):
                for indicator in time_series.indicators:
                    if not pd.isna(window_data.loc[timestamp, indicator]):
                        value = window_data.loc[timestamp, indicator]
                        uncertainty = self._calculate_uncertainty(indicator, value)
                        self.quantum_engine.create_quantum_state(
                            f"{indicator}_{i}", value, uncertainty
                        )
            
            # Вычисляем запутанности между всеми парами показателей
            for i, indicator1 in enumerate(time_series.indicators):
                for j, indicator2 in enumerate(time_series.indicators):
                    if i < j:  # Избегаем дублирования
                        try:
                            entangled_pair = self.quantum_engine.calculate_entanglement(
                                f"{indicator1}_{0}", f"{indicator2}_{0}"
                            )
                            
                            if entangled_pair.entanglement_strength > threshold:
                                quantum_entanglements.append({
                                    'indicators': [indicator1, indicator2],
                                    'strength': entangled_pair.entanglement_strength,
                                    'phase': entangled_pair.correlation_phase
                                })
                        except:
                            continue
            
            # Если найдены значимые запутанности, создаем паттерн
            if quantum_entanglements:
                # Вычисляем общую силу квантовой запутанности
                total_strength = np.mean([qe['strength'] for qe in quantum_entanglements])
                
                if total_strength > threshold:
                    # Создаем квантовую подпись
                    quantum_signature = {
                        'total_entanglement_strength': total_strength,
                        'entangled_pairs': len(quantum_entanglements),
                        'average_phase': np.mean([qe['phase'] for qe in quantum_entanglements])
                    }
                    
                    pattern = TemporalPattern(
                        pattern_type='quantum_entangled',
                        indicators=list(set([ind for qe in quantum_entanglements 
                                           for ind in qe['indicators']])),
                        start_time=window_timestamps[0],
                        end_time=window_timestamps[-1],
                        confidence=total_strength,
                        quantum_signature=quantum_signature
                    )
                    patterns.append(pattern)
        
        return patterns
    
    def generate_synthetic_medical_data(self, 
                                      duration_hours: int = 24,
                                      sampling_rate_minutes: int = 5,
                                      add_noise: bool = True,
                                      add_missing_data: bool = True,
                                      patient_profile: Optional[Dict] = None) -> MedicalTimeSeries:
        """
        Генерирует синтетические медицинские данные для тестирования.
        
        Args:
            duration_hours: Продолжительность данных в часах
            sampling_rate_minutes: Частота дискретизации в минутах
            add_noise: Добавлять ли шум к данным
            add_missing_data: Добавлять ли пропущенные данные
            patient_profile: Профиль пациента с базовыми значениями показателей
            
        Returns:
            MedicalTimeSeries: Сгенерированные данные
        """
        # Создаем временные метки
        start_time = datetime.now()
        timestamps = pd.date_range(
            start=start_time,
            periods=duration_hours * 60 // sampling_rate_minutes,
            freq=f'{sampling_rate_minutes}min'
        )
        
        # Генерируем данные для каждого показателя
        data = {}
        
        for indicator, info in self.medical_indicators.items():
            normal_range = info['normal_range']
            
            # Используем patient_profile если предоставлен, иначе среднее нормального диапазона
            if patient_profile and indicator in patient_profile:
                mean_val = patient_profile[indicator]
            else:
                mean_val = np.mean(normal_range)
            
            std_val = (normal_range[1] - normal_range[0]) / 6  # 99.7% в пределах 3σ
            
            # Базовый сигнал с трендом и периодичностью
            t = np.arange(len(timestamps))
            
            # Тренд
            trend = 0.1 * np.sin(2 * np.pi * t / (len(timestamps) * 0.1))
            
            # Периодические компоненты
            periodic1 = 0.2 * np.sin(2 * np.pi * t / (24 * 60 // sampling_rate_minutes))  # Суточный цикл
            periodic2 = 0.1 * np.sin(2 * np.pi * t / (12 * 60 // sampling_rate_minutes))  # 12-часовой цикл
            
            # Случайный шум
            noise = np.random.normal(0, std_val * 0.1, len(timestamps))
            
            # Комбинируем компоненты
            values = mean_val + trend + periodic1 + periodic2 + noise
            
            # Ограничиваем значения с учетом профиля пациента
            min_val, max_val = normal_range[0], normal_range[1]
            
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
        
        # Создаем DataFrame
        df = pd.DataFrame(data, index=timestamps)
        
        # Добавляем пропущенные данные
        if add_missing_data:
            missing_percentage = 0.05  # 5% пропущенных данных
            for indicator in df.columns:
                missing_indices = np.random.choice(
                    len(df), 
                    size=int(len(df) * missing_percentage), 
                    replace=False
                )
                df.loc[df.index[missing_indices], indicator] = np.nan
        
        # Создаем маску пропущенных данных
        missing_mask = df.isnull()
        
        # Создаем объект временного ряда
        time_series = MedicalTimeSeries(
            data=df,
            indicators=list(self.medical_indicators.keys()),
            timestamps=timestamps,
            missing_data_mask=missing_mask,
            quantum_states={indicator: np.zeros(len(timestamps)) 
                          for indicator in self.medical_indicators.keys()},
            metadata={
                'synthetic': True,
                'duration_hours': duration_hours,
                'sampling_rate_minutes': sampling_rate_minutes,
                'missing_percentage': missing_mask.sum().sum() / (len(df) * len(df.columns)) * 100
            }
        )
        
        return time_series

"""
Основной модуль MQEA - Medical Quantum Entanglement Analysis.

Объединяет все компоненты системы для комплексного анализа
многомерных медицинских временных рядов.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Union
import warnings
from datetime import datetime

from .quantum_entanglement import QuantumEntanglementEngine
from .data_processor import MedicalDataProcessor, MedicalTimeSeries, TemporalPattern


class MQEAAnalyzer:
    """
    Главный класс системы MQEA.
    
    Предоставляет единый интерфейс для:
    - Загрузки и обработки медицинских данных
    - Квантового анализа временных рядов
    - Заполнения пропущенных данных
    - Обнаружения паттернов и аномалий
    - Визуализации результатов
    """
    
    def __init__(self, 
                 quantum_hbar: float = 1.0,
                 enable_quantum_imputation: bool = True,
                 enable_pattern_detection: bool = True):
        """
        Инициализация анализатора MQEA.
        
        Args:
            quantum_hbar: Постоянная Планка для квантовых вычислений
            enable_quantum_imputation: Включить квантовое заполнение пропусков
            enable_pattern_detection: Включить обнаружение паттернов
        """
        self.quantum_engine = QuantumEntanglementEngine(hbar=quantum_hbar)
        self.data_processor = MedicalDataProcessor(quantum_engine=self.quantum_engine)
        
        self.enable_quantum_imputation = enable_quantum_imputation
        self.enable_pattern_detection = enable_pattern_detection
        
        self.current_data: Optional[MedicalTimeSeries] = None
        self.analysis_results: Dict[str, any] = {}
        self.detected_patterns: List[TemporalPattern] = []
        
        print("MQEA Analyzer инициализирован")
        print(f"Квантовое заполнение пропусков: {'включено' if enable_quantum_imputation else 'отключено'}")
        print(f"Обнаружение паттернов: {'включено' if enable_pattern_detection else 'отключено'}")
    
    def load_medical_data(self, 
                         file_path: str, 
                         time_column: str = 'timestamp',
                         indicator_columns: Optional[List[str]] = None) -> MedicalTimeSeries:
        """
        Загружает медицинские данные из файла.
        
        Args:
            file_path: Путь к файлу с данными (CSV)
            time_column: Название колонки с временными метками
            indicator_columns: Список колонок с медицинскими показателями
            
        Returns:
            MedicalTimeSeries: Загруженные данные
        """
        print(f"Загружаем медицинские данные из {file_path}...")
        
        try:
            self.current_data = self.data_processor.load_medical_data(
                file_path, time_column, indicator_columns
            )
            
            print(f"Данные успешно загружены:")
            print(f"  - Показателей: {len(self.current_data.indicators)}")
            print(f"  - Временных точек: {len(self.current_data.timestamps)}")
            print(f"  - Пропущенных данных: {self.current_data.metadata['missing_percentage']:.1f}%")
            
            return self.current_data
            
        except Exception as e:
            print(f"Ошибка при загрузке данных: {e}")
            raise
    
    def generate_synthetic_data(self, 
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
        print(f"Генерируем синтетические данные на {duration_hours} часов...")
        
        self.current_data = self.data_processor.generate_synthetic_medical_data(
            duration_hours, sampling_rate_minutes, add_noise, add_missing_data, patient_profile
        )
        
        print(f"Синтетические данные созданы:")
        print(f"  - Показателей: {len(self.current_data.indicators)}")
        print(f"  - Временных точек: {len(self.current_data.timestamps)}")
        print(f"  - Пропущенных данных: {self.current_data.metadata['missing_percentage']:.1f}%")
        
        return self.current_data
    
    def quantum_entanglement_analysis(self, 
                                    time_series: Optional[MedicalTimeSeries] = None,
                                    quantum_threshold: float = 0.5,
                                    time_windows: Optional[List[int]] = None) -> Dict[str, any]:
        """
        Выполняет квантовый анализ запутанности медицинских данных.
        
        Уникальная особенность MQEA - анализ медицинских показателей
        как квантово-запутанной системы.
        
        Args:
            time_series: Временной ряд для анализа (если None, используется текущий)
            quantum_threshold: Порог для определения значимой запутанности
            time_windows: Список размеров временных окон для анализа
            
        Returns:
            Dict[str, any]: Результаты квантового анализа
        """
        if time_series is None:
            if self.current_data is None:
                raise ValueError("Нет данных для анализа. Сначала загрузите данные.")
            time_series = self.current_data
        
        print("Начинаем квантовый анализ запутанности...")
        print(f"  - Показателей: {len(time_series.indicators)}")
        print(f"  - Временных точек: {len(time_series.timestamps)}")
        print(f"  - Порог запутанности: {quantum_threshold}")
        
        # Сброс предыдущих результатов перед новым анализом
        self.quantum_engine.reset()
        
        # Определяем временные окна для анализа
        if time_windows is None:
            data_length = len(time_series.timestamps)
            time_windows = [
                min(24, data_length // 4),  # 25% данных
                min(48, data_length // 2),  # 50% данных
                data_length  # Все данные
            ]
        
        results = {
            'quantum_entanglements': [],
            'entanglement_network': {},
            'quantum_patterns': [],
            'temporal_analysis': {},
            'quantum_signatures': {}
        }
        
        # Анализ для каждого временного окна
        for window_size in time_windows:
            if window_size > len(time_series.timestamps):
                continue
                
            print(f"Анализируем окно размером {window_size} точек...")
            
            # Выбираем данные для окна
            window_data = time_series.data.iloc[:window_size]
            window_timestamps = time_series.timestamps[:window_size]
            
            # Создаем квантовые состояния для всех показателей
            quantum_states_created = 0
            for i, timestamp in enumerate(window_timestamps):
                for indicator in time_series.indicators:
                    if not pd.isna(window_data.loc[timestamp, indicator]):
                        value = window_data.loc[timestamp, indicator]
                        uncertainty = self.data_processor._calculate_uncertainty(indicator, value)
                        
                        self.quantum_engine.create_quantum_state(
                            f"{indicator}_{i}", value, uncertainty
                        )
                        quantum_states_created += 1
            
            print(f"  Создано {quantum_states_created} квантовых состояний")
            
            # Вычисляем запутанности между всеми парами показателей
            entanglement_matrix = np.zeros((len(time_series.indicators), len(time_series.indicators)))
            entanglement_pairs = []
            
            for i, indicator1 in enumerate(time_series.indicators):
                for j, indicator2 in enumerate(time_series.indicators):
                    if i < j:  # Избегаем дублирования
                        try:
                            # Вычисляем запутанность на основе реальных данных
                            # Используем корреляцию между показателями для более точной оценки
                            indicator1_data = window_data[indicator1].dropna()
                            indicator2_data = window_data[indicator2].dropna()
                            
                            if len(indicator1_data) > 1 and len(indicator2_data) > 1:
                                # Находим общие временные точки
                                common_indices = indicator1_data.index.intersection(indicator2_data.index)
                                
                                if len(common_indices) > 1:
                                    # Вычисляем корреляцию Пирсона
                                    corr = np.corrcoef(
                                        indicator1_data.loc[common_indices].values,
                                        indicator2_data.loc[common_indices].values
                                    )[0, 1]
                                    
                                    # Преобразуем корреляцию в силу запутанности (0-1)
                                    # Используем абсолютное значение корреляции
                                    base_entanglement = abs(corr) if not np.isnan(corr) else 0.0
                                    
                                    # Вычисляем среднюю запутанность по времени через квантовые состояния
                                    entanglement_values = []
                                    sample_size = min(20, len(common_indices))  # Увеличиваем выборку
                                    sample_indices = np.linspace(0, len(common_indices) - 1, sample_size, dtype=int)
                                    
                                    for idx in sample_indices:
                                        timestamp = common_indices[idx]
                                        t = list(window_timestamps).index(timestamp) if timestamp in window_timestamps else idx
                                        
                                        state1_name = f"{indicator1}_{t}"
                                        state2_name = f"{indicator2}_{t}"
                                        
                                        if (state1_name in self.quantum_engine.quantum_states and 
                                            state2_name in self.quantum_engine.quantum_states):
                                            
                                            try:
                                                entangled_pair = self.quantum_engine.calculate_entanglement(
                                                    state1_name, state2_name
                                                )
                                                # Комбинируем квантовую запутанность с корреляцией данных
                                                combined_strength = (base_entanglement * 0.4 + entangled_pair.entanglement_strength * 0.6)
                                                entanglement_values.append(combined_strength)
                                            except Exception:
                                                # Если не удалось вычислить, используем только корреляцию
                                                entanglement_values.append(base_entanglement)
                                    
                                    if entanglement_values:
                                        avg_entanglement = np.mean(entanglement_values)
                                        # Убеждаемся, что значение в допустимом диапазоне
                                        avg_entanglement = max(0.0, min(1.0, avg_entanglement))
                                        
                                        entanglement_matrix[i, j] = avg_entanglement
                                        entanglement_matrix[j, i] = avg_entanglement
                                        
                                        if avg_entanglement > quantum_threshold:
                                            entanglement_pairs.append({
                                                'indicators': [indicator1, indicator2],
                                                'strength': avg_entanglement,
                                                'window_size': window_size,
                                                'significance': 'high' if avg_entanglement > 0.7 else 'medium'
                                            })
                        except Exception as e:
                            print(f"    Ошибка при вычислении запутанности {indicator1}-{indicator2}: {e}")
                            continue
            
            # Сохраняем результаты для окна
            window_results = {
                'window_size': window_size,
                'entanglement_matrix': entanglement_matrix.tolist(),
                'significant_pairs': [pair for pair in entanglement_pairs 
                                    if pair['strength'] > quantum_threshold],
                'max_entanglement': float(np.max(entanglement_matrix)),
                'avg_entanglement': float(np.mean(entanglement_matrix[entanglement_matrix > 0]))
            }
            
            results['quantum_entanglements'].append(window_results)
            
            print(f"  Найдено {len(window_results['significant_pairs'])} значимых запутанностей")
            print(f"  Максимальная запутанность: {window_results['max_entanglement']:.3f}")
        
        # Строим сеть запутанности
        results['entanglement_network'] = self.quantum_engine.get_entanglement_network()
        
        # Создаем общую матрицу запутанности (используем последнее окно)
        if results['quantum_entanglements']:
            latest_entanglement = results['quantum_entanglements'][-1]
            if 'entanglement_matrix' in latest_entanglement:
                results['entanglement_matrix'] = np.array(latest_entanglement['entanglement_matrix'])
            else:
                # Создаем матрицу из сети запутанности
                n_indicators = len(time_series.indicators)
                results['entanglement_matrix'] = np.zeros((n_indicators, n_indicators))
                
                # Заполняем матрицу из сети запутанности
                for i, indicator1 in enumerate(time_series.indicators):
                    for j, indicator2 in enumerate(time_series.indicators):
                        if i != j:
                            pair_key = f"{indicator1}_{indicator2}"
                            if pair_key in self.quantum_engine.entangled_pairs:
                                results['entanglement_matrix'][i, j] = self.quantum_engine.entangled_pairs[pair_key].entanglement_strength
        else:
            # Если нет результатов запутанности, создаем пустую матрицу
            n_indicators = len(time_series.indicators)
            results['entanglement_matrix'] = np.zeros((n_indicators, n_indicators))
        
        # Анализ квантовых паттернов
        if self.enable_pattern_detection:
            print("Обнаружение квантовых паттернов...")
            quantum_patterns = self.data_processor._detect_quantum_entangled_patterns(
                time_series, min_length=10, threshold=quantum_threshold
            )
            results['quantum_patterns'] = [
                {
                    'type': pattern.pattern_type,
                    'indicators': pattern.indicators,
                    'start_time': pattern.start_time.isoformat(),
                    'end_time': pattern.end_time.isoformat(),
                    'confidence': pattern.confidence,
                    'quantum_signature': pattern.quantum_signature
                }
                for pattern in quantum_patterns
            ]
        
        # Временной анализ
        results['temporal_analysis'] = {
            'total_duration_hours': (time_series.timestamps[-1] - time_series.timestamps[0]).total_seconds() / 3600,
            'sampling_rate_minutes': (time_series.timestamps[1] - time_series.timestamps[0]).total_seconds() / 60,
            'data_completeness': 1 - time_series.metadata.get('missing_percentage', 0) / 100
        }
        
        # Вычисляем статистику запутанности из результатов
        max_entanglement = 0.0
        total_entangled_pairs = 0
        if results['quantum_entanglements']:
            for window_result in results['quantum_entanglements']:
                if 'max_entanglement' in window_result:
                    max_entanglement = max(max_entanglement, window_result['max_entanglement'])
                if 'significant_pairs' in window_result:
                    total_entangled_pairs += len(window_result['significant_pairs'])
        
        # Если нет результатов в окнах, используем данные из quantum_engine
        if total_entangled_pairs == 0:
            total_entangled_pairs = len(self.quantum_engine.entangled_pairs)
            if self.quantum_engine.entangled_pairs:
                max_entanglement = max(pair.entanglement_strength 
                                     for pair in self.quantum_engine.entangled_pairs.values())
        
        # Квантовые подписи
        results['quantum_signatures'] = {
            'total_quantum_states': len(self.quantum_engine.quantum_states),
            'entangled_pairs_count': total_entangled_pairs,
            'quantum_coherence': self._calculate_quantum_coherence(time_series),
            'entanglement_entropy': self._calculate_entanglement_entropy(entanglement_matrix),
            'average_entanglement': self._calculate_average_entanglement(results['quantum_entanglements'])
        }
        
        # Статистика запутанности (для совместимости)
        results['entanglement_statistics'] = {
            'entangled_pairs': total_entangled_pairs,
            'max_entanglement': max_entanglement,
            'average_entanglement': results['quantum_signatures']['average_entanglement'],
            'total_pairs': len(self.quantum_engine.entangled_pairs)
        }
        
        self.analysis_results = results
        
        print("Квантовый анализ завершен!")
        print(f"  - Всего квантовых состояний: {results['quantum_signatures']['total_quantum_states']}")
        print(f"  - Запутанных пар: {results['quantum_signatures']['entangled_pairs_count']}")
        print(f"  - Квантовая когерентность: {results['quantum_signatures']['quantum_coherence']:.3f}")
        
        return results
    
    def _calculate_quantum_coherence(self, time_series: MedicalTimeSeries) -> float:
        """Вычисляет квантовую когерентность системы."""
        if not self.quantum_engine.quantum_states:
            return 0.0
        
        # Когерентность основана на фазовых соотношениях между состояниями
        phases = [state.phase for state in self.quantum_engine.quantum_states.values()]
        
        if len(phases) < 2:
            return 0.0
        
        # Вычисляем дисперсию фаз как меру когерентности
        phase_variance = np.var(phases)
        coherence = 1.0 / (1.0 + phase_variance)
        
        return float(coherence)
    
    def _calculate_entanglement_entropy(self, entanglement_matrix: np.ndarray) -> float:
        """Вычисляет энтропию запутанности системы."""
        if np.all(entanglement_matrix == 0):
            return 0.0
        
        # Используем энтропию фон Неймана для матрицы запутанности
        eigenvals = np.linalg.eigvals(entanglement_matrix)
        eigenvals = eigenvals[eigenvals > 1e-10]  # Убираем нулевые значения
        
        if len(eigenvals) == 0:
            return 0.0
        
        # Нормализуем собственные значения
        eigenvals = eigenvals / np.sum(eigenvals)
        
        # Энтропия фон Неймана
        entropy = -np.sum(eigenvals * np.log2(eigenvals + 1e-10))
        
        return float(entropy)
    
    def _calculate_average_entanglement(self, quantum_entanglements: list) -> float:
        """Вычисляет среднюю силу запутанности."""
        if not quantum_entanglements:
            return 0.0
        
        strengths = []
        for window in quantum_entanglements:
            if isinstance(window, list):
                for qe in window:
                    if isinstance(qe, dict) and 'strength' in qe:
                        strengths.append(qe['strength'])
            elif isinstance(window, dict) and 'strength' in window:
                strengths.append(window['strength'])
        
        return float(np.mean(strengths)) if strengths else 0.0
    
    def fill_missing_data(self, 
                         time_series: Optional[MedicalTimeSeries] = None,
                         method: str = 'quantum',
                         max_iterations: int = 100) -> MedicalTimeSeries:
        """
        Заполняет пропущенные данные в временном ряду.
        
        Args:
            time_series: Временной ряд для заполнения
            method: Метод заполнения ('quantum', 'linear', 'mean')
            max_iterations: Максимальное количество итераций для квантового метода
            
        Returns:
            MedicalTimeSeries: Временной ряд с заполненными пропусками
        """
        if time_series is None:
            if self.current_data is None:
                raise ValueError("Нет данных для заполнения. Сначала загрузите данные.")
            time_series = self.current_data
        
        print(f"Заполняем пропущенные данные методом '{method}'...")
        
        if method == 'quantum' and self.enable_quantum_imputation:
            filled_data = self.data_processor.quantum_imputation(
                time_series, max_iterations
            )
        elif method == 'linear':
            filled_data = self._linear_imputation(time_series)
        elif method == 'mean':
            filled_data = self._mean_imputation(time_series)
        else:
            raise ValueError(f"Неизвестный метод заполнения: {method}")
        
        print(f"Заполнение завершено. Пропущенных данных: {filled_data.missing_data_mask.sum().sum()}")
        
        return filled_data
    
    def _linear_imputation(self, time_series: MedicalTimeSeries) -> MedicalTimeSeries:
        """Простое линейное заполнение пропущенных данных."""
        filled_data = time_series.data.copy()
        
        for indicator in time_series.indicators:
            filled_data[indicator] = filled_data[indicator].interpolate(method='linear')
        
        # Создаем новый временной ряд
        return MedicalTimeSeries(
            data=filled_data,
            indicators=time_series.indicators,
            timestamps=time_series.timestamps,
            missing_data_mask=pd.DataFrame(False, 
                                         index=time_series.timestamps,
                                         columns=time_series.indicators),
            quantum_states=time_series.quantum_states,
            metadata=time_series.metadata.copy()
        )
    
    def _mean_imputation(self, time_series: MedicalTimeSeries) -> MedicalTimeSeries:
        """Заполнение пропущенных данных средними значениями."""
        filled_data = time_series.data.copy()
        
        for indicator in time_series.indicators:
            mean_val = filled_data[indicator].mean()
            filled_data[indicator] = filled_data[indicator].fillna(mean_val)
        
        # Создаем новый временной ряд
        return MedicalTimeSeries(
            data=filled_data,
            indicators=time_series.indicators,
            timestamps=time_series.timestamps,
            missing_data_mask=pd.DataFrame(False, 
                                         index=time_series.timestamps,
                                         columns=time_series.indicators),
            quantum_states=time_series.quantum_states,
            metadata=time_series.metadata.copy()
        )
    
    def detect_patterns(self, 
                       time_series: Optional[MedicalTimeSeries] = None,
                       pattern_types: Optional[List[str]] = None) -> List[TemporalPattern]:
        """
        Обнаруживает различные типы паттернов в данных.
        
        Args:
            time_series: Временной ряд для анализа
            pattern_types: Типы паттернов для поиска
            
        Returns:
            List[TemporalPattern]: Список обнаруженных паттернов
        """
        if time_series is None:
            if self.current_data is None:
                raise ValueError("Нет данных для анализа. Сначала загрузите данные.")
            time_series = self.current_data
        
        if not self.enable_pattern_detection:
            print("Обнаружение паттернов отключено")
            return []
        
        print("Обнаружение паттернов в данных...")
        
        patterns = self.data_processor.detect_temporal_patterns(time_series)
        self.detected_patterns = patterns
        
        print(f"Найдено {len(patterns)} паттернов:")
        for pattern in patterns:
            print(f"  - {pattern.pattern_type}: {pattern.indicators} "
                  f"({pattern.start_time} - {pattern.end_time}, "
                  f"уверенность: {pattern.confidence:.3f})")
        
        return patterns
    
    def get_analysis_summary(self) -> Dict[str, any]:
        """
        Возвращает сводку результатов анализа.
        
        Returns:
            Dict[str, any]: Сводка анализа
        """
        if not self.analysis_results:
            return {"error": "Анализ не выполнен"}
        
        summary = {
            "data_info": {
                "indicators": self.current_data.indicators if self.current_data else [],
                "data_points": len(self.current_data.timestamps) if self.current_data else 0,
                "missing_percentage": self.current_data.metadata.get('missing_percentage', 0) if self.current_data else 0
            },
            "quantum_analysis": {
                "total_entanglements": len(self.analysis_results.get('quantum_entanglements', [])),
                "quantum_coherence": self.analysis_results.get('quantum_signatures', {}).get('quantum_coherence', 0),
                "entanglement_entropy": self.analysis_results.get('quantum_signatures', {}).get('entanglement_entropy', 0)
            },
            "patterns_detected": {
                "total_patterns": len(self.detected_patterns),
                "pattern_types": list(set([p.pattern_type for p in self.detected_patterns])),
                "quantum_patterns": len([p for p in self.detected_patterns if p.pattern_type == 'quantum_entangled'])
            }
        }
        
        return summary
    
    def reset(self):
        """Сбрасывает все данные и результаты анализа."""
        self.quantum_engine.reset()
        self.current_data = None
        self.analysis_results = {}
        self.detected_patterns = []
        print("MQEA Analyzer сброшен")

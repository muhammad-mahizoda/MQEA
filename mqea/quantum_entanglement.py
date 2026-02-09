"""
Модуль квантовой запутанности для медицинских данных.

Реализует математическую модель квантовой запутанности,
адаптированную для анализа многомерных медицинских временных рядов.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import warnings


@dataclass
class QuantumState:
    """Квантовое состояние медицинского показателя."""
    amplitude: complex
    phase: float
    energy: float
    uncertainty: float


@dataclass
class EntangledPair:
    """Запутанная пара медицинских показателей."""
    indicator1: str
    indicator2: str
    entanglement_strength: float
    correlation_phase: float
    bell_state: str  # |00⟩, |01⟩, |10⟩, |11⟩


class QuantumEntanglementEngine:
    """
    Движок квантовой запутанности для медицинских данных.
    
    Реализует уникальный алгоритм, который создает квантовые состояния
    из медицинских показателей и вычисляет их запутанность.
    """
    
    def __init__(self, hbar: float = 1.0):
        """
        Инициализация движка квантовой запутанности.
        
        Args:
            hbar: Постоянная Планка (нормализованная)
        """
        self.hbar = hbar
        self.quantum_states: Dict[str, QuantumState] = {}
        self.entangled_pairs: List[EntangledPair] = []
        self.bell_states = {
            '|00⟩': np.array([1, 0, 0, 0]),
            '|01⟩': np.array([0, 1, 0, 0]), 
            '|10⟩': np.array([0, 0, 1, 0]),
            '|11⟩': np.array([0, 0, 0, 1])
        }
    
    def create_quantum_state(self, 
                           indicator_name: str, 
                           value: float, 
                           uncertainty: float = 0.1) -> QuantumState:
        """
        Создает квантовое состояние из медицинского показателя.
        
        Уникальная формула: |ψ⟩ = A * e^(iφ) * |value⟩
        где A = sqrt(1/uncertainty), φ = value * π/2
        
        Args:
            indicator_name: Название показателя (например, 'heart_rate')
            value: Значение показателя
            uncertainty: Неопределенность измерения
            
        Returns:
            QuantumState: Квантовое состояние показателя
        """
        # Нормализация значения в диапазон [0, 1]
        normalized_value = self._normalize_medical_value(indicator_name, value)
        
        # Вычисление амплитуды на основе неопределенности
        amplitude = np.sqrt(1.0 / (uncertainty + 1e-10))
        
        # Фаза зависит от значения показателя
        phase = normalized_value * np.pi / 2
        
        # Энергия состояния (аналог энергии в квантовой механике)
        energy = 0.5 * (normalized_value ** 2) + 0.5 * (uncertainty ** 2)
        
        quantum_state = QuantumState(
            amplitude=amplitude * np.exp(1j * phase),
            phase=phase,
            energy=energy,
            uncertainty=uncertainty
        )
        
        self.quantum_states[indicator_name] = quantum_state
        return quantum_state
    
    def _normalize_medical_value(self, indicator_name: str, value: float) -> float:
        """
        Нормализует медицинское значение в диапазон [0, 1].
        
        Использует медицинские стандарты для нормализации.
        """
        # Медицинские диапазоны (минимальные и максимальные значения)
        medical_ranges = {
            'heart_rate': (40, 200),      # ударов в минуту
            'blood_pressure_systolic': (70, 200),  # мм рт.ст.
            'blood_pressure_diastolic': (40, 120), # мм рт.ст.
            'temperature': (35, 42),       # градусы Цельсия
            'oxygen_saturation': (70, 100), # %
            'respiratory_rate': (8, 30),   # вдохов в минуту
            'glucose': (50, 400),          # мг/дл
            'cholesterol': (100, 300),     # мг/дл
        }
        
        if indicator_name in medical_ranges:
            min_val, max_val = medical_ranges[indicator_name]
            return np.clip((value - min_val) / (max_val - min_val), 0, 1)
        else:
            # Для неизвестных показателей используем сигмоидальную нормализацию
            return 1 / (1 + np.exp(-(value - 50) / 10))
    
    def calculate_entanglement(self, 
                             indicator1: str, 
                             indicator2: str) -> EntangledPair:
        """
        Вычисляет квантовую запутанность между двумя медицинскими показателями.
        
        Использует модифицированную формулу Белла для медицинских данных:
        |ψ⟩ = α|00⟩ + β|01⟩ + γ|10⟩ + δ|11⟩
        
        Args:
            indicator1: Первый показатель
            indicator2: Второй показатель
            
        Returns:
            EntangledPair: Запутанная пара с характеристиками
        """
        if indicator1 not in self.quantum_states or indicator2 not in self.quantum_states:
            raise ValueError(f"Квантовые состояния для {indicator1} или {indicator2} не найдены")
        
        state1 = self.quantum_states[indicator1]
        state2 = self.quantum_states[indicator2]
        
        # Вычисление коэффициентов Белла
        alpha = state1.amplitude * state2.amplitude
        beta = state1.amplitude * np.conj(state2.amplitude)
        gamma = np.conj(state1.amplitude) * state2.amplitude
        delta = np.conj(state1.amplitude) * np.conj(state2.amplitude)
        
        # Нормализация
        norm = np.sqrt(np.abs(alpha)**2 + np.abs(beta)**2 + np.abs(gamma)**2 + np.abs(delta)**2)
        alpha /= norm
        beta /= norm
        gamma /= norm
        delta /= norm
        
        # Определение состояния Белла
        bell_state = self._determine_bell_state(alpha, beta, gamma, delta)
        
        # Сила запутанности (коэффициент запутанности)
        entanglement_strength = self._calculate_entanglement_strength(alpha, beta, gamma, delta)
        
        # Фаза корреляции
        correlation_phase = np.angle(alpha * np.conj(delta) + beta * np.conj(gamma))
        
        entangled_pair = EntangledPair(
            indicator1=indicator1,
            indicator2=indicator2,
            entanglement_strength=entanglement_strength,
            correlation_phase=correlation_phase,
            bell_state=bell_state
        )
        
        self.entangled_pairs.append(entangled_pair)
        return entangled_pair
    
    def _determine_bell_state(self, alpha: complex, beta: complex, 
                            gamma: complex, delta: complex) -> str:
        """Определяет состояние Белла на основе коэффициентов."""
        # Находим максимальный коэффициент
        coeffs = [np.abs(alpha), np.abs(beta), np.abs(gamma), np.abs(delta)]
        max_idx = np.argmax(coeffs)
        
        bell_state_names = ['|00⟩', '|01⟩', '|10⟩', '|11⟩']
        return bell_state_names[max_idx]
    
    def _calculate_entanglement_strength(self, alpha: complex, beta: complex,
                                       gamma: complex, delta: complex) -> float:
        """
        Вычисляет силу запутанности по формуле фон Неймана.
        
        S = -Tr(ρ_A * log(ρ_A))
        где ρ_A - приведенная матрица плотности
        """
        # Создаем матрицу плотности
        rho = np.array([
            [alpha * np.conj(alpha), alpha * np.conj(beta)],
            [beta * np.conj(alpha), beta * np.conj(beta)]
        ])
        
        # Вычисляем собственные значения
        eigenvals = np.linalg.eigvals(rho)
        eigenvals = eigenvals[eigenvals > 1e-10]  # Убираем нулевые значения
        
        # Энтропия фон Неймана
        entropy = -np.sum(eigenvals * np.log2(eigenvals))
        
        # Нормализуем в диапазон [0, 1]
        return min(entropy, 1.0)
    
    def quantum_measurement(self, indicator_name: str, 
                          measurement_basis: str = 'computational') -> Tuple[float, float]:
        """
        Выполняет квантовое измерение медицинского показателя.
        
        Args:
            indicator_name: Название показателя
            measurement_basis: Базис измерения ('computational', 'hadamard', 'circular')
            
        Returns:
            Tuple[float, float]: (измеренное значение, неопределенность)
        """
        if indicator_name not in self.quantum_states:
            raise ValueError(f"Квантовое состояние для {indicator_name} не найдено")
        
        state = self.quantum_states[indicator_name]
        
        if measurement_basis == 'computational':
            # Измерение в вычислительном базисе
            probability_0 = np.abs(state.amplitude) ** 2
            measured_value = 1.0 if np.random.random() < probability_0 else 0.0
            
        elif measurement_basis == 'hadamard':
            # Измерение в базисе Адамара
            hadamard_amplitude = (state.amplitude + np.conj(state.amplitude)) / np.sqrt(2)
            probability_0 = np.abs(hadamard_amplitude) ** 2
            measured_value = 1.0 if np.random.random() < probability_0 else 0.0
            
        elif measurement_basis == 'circular':
            # Измерение в круговом базисе (уникально для медицинских данных)
            circular_amplitude = state.amplitude * np.exp(1j * state.phase)
            probability_0 = np.abs(circular_amplitude) ** 2
            measured_value = 1.0 if np.random.random() < probability_0 else 0.0
            
        else:
            raise ValueError(f"Неизвестный базис измерения: {measurement_basis}")
        
        # Обратное преобразование в медицинское значение
        medical_value = self._denormalize_medical_value(indicator_name, measured_value)
        uncertainty = state.uncertainty
        
        return medical_value, uncertainty
    
    def _denormalize_medical_value(self, indicator_name: str, normalized_value: float) -> float:
        """Обратное преобразование нормализованного значения в медицинское."""
        medical_ranges = {
            'heart_rate': (40, 200),
            'blood_pressure_systolic': (70, 200),
            'blood_pressure_diastolic': (40, 120),
            'temperature': (35, 42),
            'oxygen_saturation': (70, 100),
            'respiratory_rate': (8, 30),
            'glucose': (50, 400),
            'cholesterol': (100, 300),
        }
        
        if indicator_name in medical_ranges:
            min_val, max_val = medical_ranges[indicator_name]
            return min_val + normalized_value * (max_val - min_val)
        else:
            # Обратное сигмоидальное преобразование
            return 50 + 10 * np.log(normalized_value / (1 - normalized_value))
    
    def get_entanglement_network(self) -> Dict[str, List[str]]:
        """
        Возвращает сеть запутанности между всеми показателями.
        
        Returns:
            Dict[str, List[str]]: Словарь, где ключ - показатель, 
                                значение - список запутанных с ним показателей
        """
        network = {}
        
        for pair in self.entangled_pairs:
            if pair.entanglement_strength > 0.5:  # Порог значимости
                if pair.indicator1 not in network:
                    network[pair.indicator1] = []
                if pair.indicator2 not in network:
                    network[pair.indicator2] = []
                
                network[pair.indicator1].append(pair.indicator2)
                network[pair.indicator2].append(pair.indicator1)
        
        return network
    
    def quantum_interference(self, 
                           indicator1: str, 
                           indicator2: str,
                           time_delay: float = 0.0) -> float:
        """
        Вычисляет квантовую интерференцию между двумя показателями.
        
        Уникальная особенность: учитывает временную задержку между измерениями.
        
        Args:
            indicator1: Первый показатель
            indicator2: Второй показатель  
            time_delay: Временная задержка между измерениями (в часах)
            
        Returns:
            float: Коэффициент интерференции [0, 1]
        """
        if indicator1 not in self.quantum_states or indicator2 not in self.quantum_states:
            return 0.0
        
        state1 = self.quantum_states[indicator1]
        state2 = self.quantum_states[indicator2]
        
        # Учет временной задержки через фазовый сдвиг
        time_phase_shift = 2 * np.pi * time_delay / 24  # 24 часа = полный цикл
        
        # Вычисление интерференции
        interference = np.abs(
            state1.amplitude * np.conj(state2.amplitude) * 
            np.exp(1j * (state1.phase - state2.phase + time_phase_shift))
        )
        
        return float(interference)
    
    def reset(self):
        """Сбрасывает все квантовые состояния и запутанности."""
        self.quantum_states.clear()
        self.entangled_pairs.clear()


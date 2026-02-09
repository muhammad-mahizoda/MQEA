"""
Детская квантовая диагностическая система MQEA-Pediatric.
Специализированная система для детей от рождения до 10 лет.

Особенности:
- Возрастные нормы и диапазоны показателей
- Квантовые алгоритмы для детской диагностики
- Раннее выявление врожденных патологий
- Адаптивные квантовые состояния для растущего организма
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Union, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
import warnings
from enum import Enum

from .quantum_entanglement import QuantumEntanglementEngine, QuantumState, EntangledPair
from .data_processor import MedicalTimeSeries


class AgeGroup(Enum):
    """Возрастные группы для детей."""
    NEWBORN = (0, 1)      # 0-1 месяц
    INFANT = (1, 12)      # 1-12 месяцев  
    TODDLER = (1, 3)      # 1-3 года
    PRESCHOOL = (3, 6)    # 3-6 лет
    SCHOOL = (6, 10)      # 6-10 лет


class PediatricCondition(Enum):
    """Детские заболевания и состояния."""
    # Врожденные патологии
    CONGENITAL_HEART_DEFECT = "врожденный порок сердца"
    CONGENITAL_HYPOTHYROIDISM = "врожденный гипотиреоз"
    CONGENITAL_ADRENAL_HYPERPLASIA = "врожденная гиперплазия надпочечников"
    
    # Инфекционные заболевания
    RESPIRATORY_SYNCYTIAL_VIRUS = "респираторно-синцитиальный вирус"
    ROTAVIRUS_INFECTION = "ротавирусная инфекция"
    HAND_FOOT_MOUTH = "болезнь рук-ног-рта"
    
    # Метаболические нарушения
    PEDIATRIC_DIABETES = "детский диабет"
    FAILURE_TO_THRIVE = "задержка развития"
    METABOLIC_DISORDER = "метаболическое расстройство"
    
    # Неврологические состояния
    DEVELOPMENTAL_DELAY = "задержка развития"
    AUTISM_SPECTRUM = "расстройство аутистического спектра"
    CEREBRAL_PALSY = "детский церебральный паралич"


@dataclass
class DetailedAnthropometry:
    """Детальные антропометрические измерения для точного анализа развития."""
    # Основные измерения (см)
    weight_kg: float
    height_cm: float
    head_circumference_cm: float
    chest_circumference_cm: float
    abdominal_circumference_cm: float
    
    # Размеры конечностей (см)
    arm_span_cm: float
    leg_length_cm: float
    foot_length_cm: float
    foot_width_cm: float
    
    # Размеры пальцев рук (мм)
    thumb_length_mm: float
    index_finger_length_mm: float
    middle_finger_length_mm: float
    ring_finger_length_mm: float
    little_finger_length_mm: float
    
    # Размеры пальцев ног (мм)
    big_toe_length_mm: float
    second_toe_length_mm: float
    third_toe_length_mm: float
    fourth_toe_length_mm: float
    little_toe_length_mm: float
    
    # Размеры головы (см)
    head_length_cm: float  # длина головы
    head_width_cm: float   # ширина головы
    face_height_cm: float  # высота лица
    face_width_cm: float   # ширина лица
    
    # Размеры носа (мм)
    nose_length_mm: float
    nose_width_mm: float
    nose_height_mm: float
    
    # Размеры глаз (мм)
    eye_width_mm: float
    eye_height_mm: float
    inter_eye_distance_mm: float
    
    # Размеры рта (мм)
    mouth_width_mm: float
    lip_thickness_mm: float
    
    # Размеры ушей (мм)
    ear_length_mm: float
    ear_width_mm: float
    
    # Дополнительные пропорции
    waist_to_hip_ratio: float
    shoulder_width_cm: float
    hip_width_cm: float
    
    # Кожные складки (мм)
    triceps_skinfold_mm: float
    subscapular_skinfold_mm: float
    suprailiac_skinfold_mm: float
    
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class PediatricVitalSigns:
    """Детские жизненные показатели с возрастными нормами."""
    age_months: int
    heart_rate: float
    respiratory_rate: float
    blood_pressure_systolic: float
    blood_pressure_diastolic: float
    temperature: float
    oxygen_saturation: float
    weight_kg: float
    height_cm: float
    head_circumference_cm: Optional[float] = None
    # Детальные антропометрические измерения
    detailed_anthropometry: Optional[DetailedAnthropometry] = None
    
    def get_age_group(self) -> AgeGroup:
        """Определяет возрастную группу."""
        age_years = self.age_months / 12
        if self.age_months < 1:
            return AgeGroup.NEWBORN
        elif self.age_months < 12:
            return AgeGroup.INFANT
        elif age_years < 3:
            return AgeGroup.TODDLER
        elif age_years < 6:
            return AgeGroup.PRESCHOOL
        else:
            return AgeGroup.SCHOOL


@dataclass
class PediatricQuantumState(QuantumState):
    """Квантовое состояние для детского показателя."""
    age_group: AgeGroup
    growth_factor: float  # Фактор роста для данного возраста
    developmental_stage: str  # Стадия развития


class PediatricQuantumEngine(QuantumEntanglementEngine):
    """
    Квантовый движок для детской диагностики.
    
    Адаптирует квантовые алгоритмы для особенностей детского организма:
    - Возрастные нормы показателей
    - Факторы роста и развития
    - Специфические детские заболевания
    """
    
    def __init__(self, hbar: float = 1.0):
        super().__init__(hbar)
        
        # Детские медицинские диапазоны по возрастным группам
        self.pediatric_ranges = self._initialize_pediatric_ranges()
        
        # Квантовые паттерны детских заболеваний
        self.pediatric_quantum_patterns = self._initialize_pediatric_patterns()
        
        # Факторы роста и развития
        self.growth_factors = self._initialize_growth_factors()
    
    def _initialize_pediatric_ranges(self) -> Dict[AgeGroup, Dict[str, Tuple[float, float]]]:
        """Инициализация возрастных диапазонов для детей."""
        return {
            AgeGroup.NEWBORN: {
                'heart_rate': (70, 190),      # Новорожденные: 70-190 уд/мин
                'respiratory_rate': (30, 60),  # 30-60 дых/мин
                'blood_pressure_systolic': (60, 90),   # 60-90 мм рт.ст.
                'blood_pressure_diastolic': (35, 60),  # 35-60 мм рт.ст.
                'temperature': (36.5, 37.5),   # 36.5-37.5°C
                'oxygen_saturation': (95, 100), # 95-100%
                'weight': (2.5, 4.5),         # 2.5-4.5 кг
                'height': (45, 55),           # 45-55 см
                'head_circumference': (32, 38) # 32-38 см
            },
            AgeGroup.INFANT: {
                'heart_rate': (80, 160),      # 80-160 уд/мин
                'respiratory_rate': (24, 40),  # 24-40 дых/мин
                'blood_pressure_systolic': (70, 100),   # 70-100 мм рт.ст.
                'blood_pressure_diastolic': (40, 70),   # 40-70 мм рт.ст.
                'temperature': (36.1, 37.3),   # 36.1-37.3°C
                'oxygen_saturation': (95, 100), # 95-100%
                'weight': (4.0, 12.0),        # 4.0-12.0 кг
                'height': (55, 85),           # 55-85 см
                'head_circumference': (38, 48) # 38-48 см
            },
            AgeGroup.TODDLER: {
                'heart_rate': (80, 130),      # 80-130 уд/мин
                'respiratory_rate': (20, 30),  # 20-30 дых/мин
                'blood_pressure_systolic': (80, 110),   # 80-110 мм рт.ст.
                'blood_pressure_diastolic': (50, 80),   # 50-80 мм рт.ст.
                'temperature': (36.1, 37.2),   # 36.1-37.2°C
                'oxygen_saturation': (95, 100), # 95-100%
                'weight': (10.0, 18.0),       # 10.0-18.0 кг
                'height': (80, 110),          # 80-110 см
                'head_circumference': (46, 52) # 46-52 см
            },
            AgeGroup.PRESCHOOL: {
                'heart_rate': (70, 120),      # 70-120 уд/мин
                'respiratory_rate': (18, 26),  # 18-26 дых/мин
                'blood_pressure_systolic': (85, 115),   # 85-115 мм рт.ст.
                'blood_pressure_diastolic': (55, 85),   # 55-85 мм рт.ст.
                'temperature': (36.1, 37.2),   # 36.1-37.2°C
                'oxygen_saturation': (95, 100), # 95-100%
                'weight': (15.0, 25.0),       # 15.0-25.0 кг
                'height': (100, 125),         # 100-125 см
                'head_circumference': (48, 54) # 48-54 см
            },
            AgeGroup.SCHOOL: {
                'heart_rate': (60, 110),      # 60-110 уд/мин
                'respiratory_rate': (16, 24),  # 16-24 дых/мин
                'blood_pressure_systolic': (90, 120),   # 90-120 мм рт.ст.
                'blood_pressure_diastolic': (60, 90),   # 60-90 мм рт.ст.
                'temperature': (36.1, 37.2),   # 36.1-37.2°C
                'oxygen_saturation': (95, 100), # 95-100%
                'weight': (20.0, 40.0),       # 20.0-40.0 кг
                'height': (115, 150),         # 115-150 см
                'head_circumference': (50, 56) # 50-56 см
            }
        }
    
    def _initialize_pediatric_patterns(self) -> Dict[PediatricCondition, Dict[str, float]]:
        """Инициализация квантовых паттернов детских заболеваний."""
        return {
            PediatricCondition.CONGENITAL_HEART_DEFECT: {
                'heart_rate_entanglement': 0.95,  # Высокая корреляция с сердечным ритмом
                'oxygen_saturation_correlation': -0.85,  # Снижение сатурации
                'respiratory_rate_increase': 0.75,  # Учащение дыхания
                'weight_gain_slowing': -0.60,  # Замедление прибавки веса
                'quantum_signature': 'cardiac_anomaly'
            },
            PediatricCondition.RESPIRATORY_SYNCYTIAL_VIRUS: {
                'respiratory_rate_entanglement': 0.90,
                'oxygen_saturation_decrease': -0.80,
                'temperature_increase': 0.70,
                'heart_rate_increase': 0.65,
                'quantum_signature': 'respiratory_infection'
            },
            PediatricCondition.FAILURE_TO_THRIVE: {
                'weight_entanglement': 0.95,
                'height_correlation': 0.80,
                'head_circumference_slowing': -0.70,
                'metabolic_slowdown': -0.75,
                'quantum_signature': 'growth_retardation'
            },
            PediatricCondition.DEVELOPMENTAL_DELAY: {
                'developmental_milestones': -0.85,
                'neurological_indicators': -0.75,
                'social_interaction': -0.80,
                'motor_skills': -0.70,
                'quantum_signature': 'developmental_disorder'
            }
        }
    
    def _initialize_growth_factors(self) -> Dict[AgeGroup, Dict[str, float]]:
        """Инициализация факторов роста для каждого возраста."""
        return {
            AgeGroup.NEWBORN: {
                'weight_growth_rate': 30.0,    # г/день
                'height_growth_rate': 0.1,     # см/день
                'head_growth_rate': 0.05,      # см/день
                'metabolic_rate': 1.5          # Высокий метаболизм
            },
            AgeGroup.INFANT: {
                'weight_growth_rate': 20.0,    # г/день
                'height_growth_rate': 0.08,    # см/день
                'head_growth_rate': 0.03,      # см/день
                'metabolic_rate': 1.3
            },
            AgeGroup.TODDLER: {
                'weight_growth_rate': 8.0,     # г/день
                'height_growth_rate': 0.05,    # см/день
                'head_growth_rate': 0.01,      # см/день
                'metabolic_rate': 1.2
            },
            AgeGroup.PRESCHOOL: {
                'weight_growth_rate': 5.0,     # г/день
                'height_growth_rate': 0.04,    # см/день
                'head_growth_rate': 0.005,     # см/день
                'metabolic_rate': 1.1
            },
            AgeGroup.SCHOOL: {
                'weight_growth_rate': 3.0,     # г/день
                'height_growth_rate': 0.03,    # см/день
                'head_growth_rate': 0.002,     # см/день
                'metabolic_rate': 1.0
            }
        }
    
    def create_pediatric_quantum_state(self, 
                                     indicator_name: str, 
                                     value: float, 
                                     age_months: int,
                                     uncertainty: float = 0.1) -> PediatricQuantumState:
        """
        Создает квантовое состояние для детского показателя.
        
        Args:
            indicator_name: Название показателя
            value: Значение показателя
            age_months: Возраст в месяцах
            uncertainty: Неопределенность измерения
            
        Returns:
            PediatricQuantumState: Квантовое состояние с учетом возраста
        """
        # Определяем возрастную группу
        age_group = self._determine_age_group(age_months)
        
        # Получаем нормальный диапазон для данного возраста
        normal_range = self.pediatric_ranges[age_group].get(indicator_name, (0, 100))
        
        # Нормализация с учетом возрастных особенностей
        normalized_value = self._normalize_pediatric_value(value, normal_range)
        
        # Вычисление фактора роста
        growth_factor = self.growth_factors[age_group].get('metabolic_rate', 1.0)
        
        # Амплитуда с учетом роста и развития
        amplitude = np.sqrt(1.0 / (uncertainty + 1e-10)) * growth_factor
        
        # Фаза с учетом возраста (дети развиваются циклически)
        age_phase = (age_months / 12.0) * np.pi / 2
        value_phase = normalized_value * np.pi / 2
        phase = age_phase + value_phase
        
        # Энергия состояния с учетом метаболизма
        energy = 0.5 * (normalized_value ** 2) + 0.5 * (uncertainty ** 2) * growth_factor
        
        # Определение стадии развития
        developmental_stage = self._determine_developmental_stage(age_months, indicator_name, value)
        
        quantum_state = PediatricQuantumState(
            amplitude=amplitude * np.exp(1j * phase),
            phase=phase,
            energy=energy,
            uncertainty=uncertainty,
            age_group=age_group,
            growth_factor=growth_factor,
            developmental_stage=developmental_stage
        )
        
        self.quantum_states[indicator_name] = quantum_state
        return quantum_state
    
    def _determine_age_group(self, age_months: int) -> AgeGroup:
        """Определяет возрастную группу по возрасту в месяцах."""
        if age_months < 1:
            return AgeGroup.NEWBORN
        elif age_months < 12:
            return AgeGroup.INFANT
        elif age_months < 36:
            return AgeGroup.TODDLER
        elif age_months < 72:
            return AgeGroup.PRESCHOOL
        else:
            return AgeGroup.SCHOOL
    
    def _normalize_pediatric_value(self, value: float, normal_range: Tuple[float, float]) -> float:
        """Нормализация детского показателя с учетом возрастного диапазона."""
        min_val, max_val = normal_range
        return np.clip((value - min_val) / (max_val - min_val), 0, 1)
    
    def _determine_developmental_stage(self, age_months: int, indicator: str, value: float) -> str:
        """Определяет стадию развития на основе возраста и показателей."""
        if age_months < 6:
            return "early_infant"
        elif age_months < 12:
            return "late_infant"
        elif age_months < 24:
            return "early_toddler"
        elif age_months < 36:
            return "late_toddler"
        elif age_months < 48:
            return "early_preschool"
        elif age_months < 72:
            return "late_preschool"
        else:
            return "school_age"
    
    def calculate_pediatric_entanglement(self, 
                                       indicator1: str, 
                                       indicator2: str,
                                       age_months: int) -> EntangledPair:
        """
        Вычисляет квантовую запутанность между детскими показателями.
        
        Учитывает возрастные особенности и факторы развития.
        """
        if indicator1 not in self.quantum_states or indicator2 not in self.quantum_states:
            raise ValueError(f"Квантовые состояния для {indicator1} или {indicator2} не найдены")
        
        state1 = self.quantum_states[indicator1]
        state2 = self.quantum_states[indicator2]
        
        # Проверяем, что это детские квантовые состояния
        if not isinstance(state1, PediatricQuantumState) or not isinstance(state2, PediatricQuantumState):
            raise ValueError("Состояния должны быть PediatricQuantumState")
        
        # Возрастной фактор корреляции (дети развиваются быстрее)
        age_factor = min(2.0, 1.0 + (age_months / 120.0))  # До 10 лет
        
        # Вычисление коэффициентов Белла с учетом возраста
        alpha = state1.amplitude * state2.amplitude * age_factor
        beta = state1.amplitude * np.conj(state2.amplitude) * age_factor
        gamma = np.conj(state1.amplitude) * state2.amplitude * age_factor
        delta = np.conj(state1.amplitude) * np.conj(state2.amplitude) * age_factor
        
        # Нормализация
        norm = np.sqrt(np.abs(alpha)**2 + np.abs(beta)**2 + np.abs(gamma)**2 + np.abs(delta)**2)
        alpha /= norm
        beta /= norm
        gamma /= norm
        delta /= norm
        
        # Определение состояния Белла
        bell_state = self._determine_bell_state(alpha, beta, gamma, delta)
        
        # Сила запутанности с учетом развития
        base_entanglement = self._calculate_entanglement_strength(alpha, beta, gamma, delta)
        developmental_boost = (state1.growth_factor + state2.growth_factor) / 2.0
        entanglement_strength = min(1.0, base_entanglement * developmental_boost)
        
        # Фаза корреляции с учетом стадии развития
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
    
    def analyze_detailed_anthropometry(self, 
                                     anthropometry: DetailedAnthropometry,
                                     age_months: int) -> Dict[str, Any]:
        """
        Анализирует детальные антропометрические измерения с квантовой точностью.
        
        Args:
            anthropometry: Детальные антропометрические измерения
            age_months: Возраст в месяцах
            
        Returns:
            Dict: Результаты анализа с квантовыми оценками
        """
        analysis_results = {
            'age_months': age_months,
            'age_group': self._get_age_group_from_months(age_months),
            'quantum_assessment': {},
            'developmental_indicators': {},
            'proportional_analysis': {},
            'growth_patterns': {},
            'anomaly_detection': {}
        }
        
        # Создаем квантовые состояния для всех антропометрических показателей
        anthropometric_indicators = {
            # Основные измерения
            'weight': anthropometry.weight_kg,
            'height': anthropometry.height_cm,
            'head_circumference': anthropometry.head_circumference_cm,
            'chest_circumference': anthropometry.chest_circumference_cm,
            'abdominal_circumference': anthropometry.abdominal_circumference_cm,
            
            # Размеры конечностей
            'arm_span': anthropometry.arm_span_cm,
            'leg_length': anthropometry.leg_length_cm,
            'foot_length': anthropometry.foot_length_cm,
            'foot_width': anthropometry.foot_width_cm,
            
            # Размеры пальцев рук
            'thumb_length': anthropometry.thumb_length_mm,
            'index_finger_length': anthropometry.index_finger_length_mm,
            'middle_finger_length': anthropometry.middle_finger_length_mm,
            'ring_finger_length': anthropometry.ring_finger_length_mm,
            'little_finger_length': anthropometry.little_finger_length_mm,
            
            # Размеры пальцев ног
            'big_toe_length': anthropometry.big_toe_length_mm,
            'second_toe_length': anthropometry.second_toe_length_mm,
            'third_toe_length': anthropometry.third_toe_length_mm,
            'fourth_toe_length': anthropometry.fourth_toe_length_mm,
            'little_toe_length': anthropometry.little_toe_length_mm,
            
            # Размеры головы и лица
            'head_length': anthropometry.head_length_cm,
            'head_width': anthropometry.head_width_cm,
            'face_height': anthropometry.face_height_cm,
            'face_width': anthropometry.face_width_cm,
            
            # Размеры носа
            'nose_length': anthropometry.nose_length_mm,
            'nose_width': anthropometry.nose_width_mm,
            'nose_height': anthropometry.nose_height_mm,
            
            # Размеры глаз
            'eye_width': anthropometry.eye_width_mm,
            'eye_height': anthropometry.eye_height_mm,
            'inter_eye_distance': anthropometry.inter_eye_distance_mm,
            
            # Размеры рта
            'mouth_width': anthropometry.mouth_width_mm,
            'lip_thickness': anthropometry.lip_thickness_mm,
            
            # Размеры ушей
            'ear_length': anthropometry.ear_length_mm,
            'ear_width': anthropometry.ear_width_mm,
            
            # Пропорции
            'waist_to_hip_ratio': anthropometry.waist_to_hip_ratio,
            'shoulder_width': anthropometry.shoulder_width_cm,
            'hip_width': anthropometry.hip_width_cm,
            
            # Кожные складки
            'triceps_skinfold': anthropometry.triceps_skinfold_mm,
            'subscapular_skinfold': anthropometry.subscapular_skinfold_mm,
            'suprailiac_skinfold': anthropometry.suprailiac_skinfold_mm
        }
        
        # Создаем квантовые состояния для каждого показателя
        quantum_states = {}
        for indicator, value in anthropometric_indicators.items():
            if value is not None and value > 0:
                quantum_states[indicator] = self.create_pediatric_quantum_state(
                    indicator, value, age_months
                )
        
        # Анализ пропорций и симметрии
        analysis_results['proportional_analysis'] = self._analyze_body_proportions(anthropometry, age_months)
        
        # Анализ паттернов роста
        analysis_results['growth_patterns'] = self._analyze_growth_patterns(anthropometry, age_months)
        
        # Квантовый анализ запутанности между показателями
        analysis_results['quantum_assessment'] = self._quantum_anthropometry_assessment(quantum_states, age_months)
        
        # Обнаружение аномалий развития
        analysis_results['anomaly_detection'] = self._detect_developmental_anomalies(anthropometry, age_months)
        
        # Индикаторы развития
        analysis_results['developmental_indicators'] = self._assess_developmental_indicators(anthropometry, age_months)
        
        return analysis_results

    def detect_pediatric_conditions(self, 
                                  vital_signs: PediatricVitalSigns,
                                  quantum_threshold: float = 0.7) -> List[Dict[str, Any]]:
        """
        Обнаруживает детские заболевания на основе квантового анализа.
        
        Args:
            vital_signs: Детские жизненные показатели
            quantum_threshold: Порог для определения значимой запутанности
            
        Returns:
            List[Dict]: Список обнаруженных состояний с вероятностями
        """
        detected_conditions = []
        age_group = vital_signs.get_age_group()
        
        # Создаем квантовые состояния для всех показателей
        indicators = {
            'heart_rate': vital_signs.heart_rate,
            'respiratory_rate': vital_signs.respiratory_rate,
            'blood_pressure_systolic': vital_signs.blood_pressure_systolic,
            'blood_pressure_diastolic': vital_signs.blood_pressure_diastolic,
            'temperature': vital_signs.temperature,
            'oxygen_saturation': vital_signs.oxygen_saturation,
            'weight': vital_signs.weight_kg,
            'height': vital_signs.height_cm
        }
        
        if vital_signs.head_circumference_cm:
            indicators['head_circumference'] = vital_signs.head_circumference_cm
        
        # Создаем квантовые состояния
        quantum_states = {}
        for indicator, value in indicators.items():
            if value is not None:
                quantum_states[indicator] = self.create_pediatric_quantum_state(
                    indicator, value, vital_signs.age_months
                )
        
        # Анализируем каждое заболевание
        for condition, pattern in self.pediatric_quantum_patterns.items():
            condition_score = 0.0
            matched_indicators = []
            
            # Проверяем соответствие паттернам
            for indicator_pattern, expected_correlation in pattern.items():
                if indicator_pattern == 'quantum_signature':
                    continue
                
                # Извлекаем название показателя из паттерна
                indicator_name = indicator_pattern.replace('_entanglement', '').replace('_correlation', '').replace('_increase', '').replace('_decrease', '').replace('_slowing', '')
                
                if indicator_name in quantum_states:
                    # Вычисляем фактическую корреляцию с другими показателями
                    actual_correlation = self._calculate_indicator_correlation(
                        indicator_name, quantum_states, vital_signs.age_months
                    )
                    
                    # Сравниваем с ожидаемой корреляцией
                    correlation_match = 1.0 - abs(actual_correlation - expected_correlation)
                    condition_score += correlation_match
                    matched_indicators.append({
                        'indicator': indicator_name,
                        'expected': expected_correlation,
                        'actual': actual_correlation,
                        'match': correlation_match
                    })
            
            # Нормализуем оценку
            if matched_indicators:
                condition_score /= len(matched_indicators)
                
                if condition_score > quantum_threshold:
                    detected_conditions.append({
                        'condition': condition.value,
                        'probability': condition_score,
                        'age_group': age_group.value,
                        'quantum_signature': pattern.get('quantum_signature', 'unknown'),
                        'matched_indicators': matched_indicators,
                        'recommendations': self._generate_pediatric_recommendations(condition, condition_score)
                    })
        
        # Сортируем по вероятности
        detected_conditions.sort(key=lambda x: x['probability'], reverse=True)
        
        return detected_conditions
    
    def _calculate_indicator_correlation(self, 
                                       indicator_name: str, 
                                       quantum_states: Dict[str, PediatricQuantumState],
                                       age_months: int) -> float:
        """Вычисляет корреляцию показателя с другими показателями."""
        if indicator_name not in quantum_states:
            return 0.0
        
        correlations = []
        target_state = quantum_states[indicator_name]
        
        for other_indicator, other_state in quantum_states.items():
            if other_indicator != indicator_name:
                # Вычисляем запутанность
                try:
                    entangled_pair = self.calculate_pediatric_entanglement(
                        indicator_name, other_indicator, age_months
                    )
                    correlations.append(entangled_pair.entanglement_strength)
                except:
                    # Если не удается вычислить запутанность, используем простую корреляцию
                    phase_diff = abs(target_state.phase - other_state.phase)
                    simple_correlation = np.cos(phase_diff)
                    correlations.append(simple_correlation)
        
        return np.mean(correlations) if correlations else 0.0
    
    def _generate_pediatric_recommendations(self, 
                                          condition: PediatricCondition, 
                                          probability: float) -> List[str]:
        """Генерирует рекомендации для детского состояния."""
        recommendations = []
        
        if condition == PediatricCondition.CONGENITAL_HEART_DEFECT:
            recommendations.extend([
                "Немедленная консультация детского кардиолога",
                "Эхокардиография для подтверждения диагноза",
                "Мониторинг насыщения кислородом",
                "Ограничение физической активности"
            ])
        
        elif condition == PediatricCondition.RESPIRATORY_SYNCYTIAL_VIRUS:
            recommendations.extend([
                "Консультация педиатра",
                "Поддерживающая терапия (увлажнение, покой)",
                "Мониторинг дыхания и сатурации",
                "При необходимости - госпитализация"
            ])
        
        elif condition == PediatricCondition.FAILURE_TO_THRIVE:
            recommendations.extend([
                "Консультация педиатра и диетолога",
                "Анализ питания и режима кормления",
                "Исследование на метаболические нарушения",
                "Регулярный мониторинг веса и роста"
            ])
        
        elif condition == PediatricCondition.DEVELOPMENTAL_DELAY:
            recommendations.extend([
                "Консультация детского невролога",
                "Оценка развития по стандартным шкалам",
                "Раннее вмешательство и терапия",
                "Мониторинг прогресса развития"
            ])
        
        # Добавляем общие рекомендации
        if probability > 0.9:
            recommendations.append("🚨 КРИТИЧЕСКИ ВАЖНО: Немедленное медицинское вмешательство")
        elif probability > 0.8:
            recommendations.append("⚠️ ВЫСОКИЙ ПРИОРИТЕТ: Срочная консультация специалиста")
        elif probability > 0.7:
            recommendations.append("📋 РЕКОМЕНДУЕТСЯ: Плановый осмотр специалиста")
        
        return recommendations
    
    def generate_pediatric_quantum_report(self, 
                                        vital_signs: PediatricVitalSigns,
                                        detected_conditions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Генерирует детский квантовый отчет."""
        age_group = vital_signs.get_age_group()
        
        report = {
            'patient_info': {
                'age_months': vital_signs.age_months,
                'age_group': age_group.value,
                'developmental_stage': self._determine_developmental_stage(vital_signs.age_months, 'general', 0)
            },
            'vital_signs': {
                'heart_rate': vital_signs.heart_rate,
                'respiratory_rate': vital_signs.respiratory_rate,
                'blood_pressure': f"{vital_signs.blood_pressure_systolic}/{vital_signs.blood_pressure_diastolic}",
                'temperature': vital_signs.temperature,
                'oxygen_saturation': vital_signs.oxygen_saturation,
                'weight_kg': vital_signs.weight_kg,
                'height_cm': vital_signs.height_cm,
                'head_circumference_cm': vital_signs.head_circumference_cm
            },
            'quantum_analysis': {
                'total_quantum_states': len(self.quantum_states),
                'entangled_pairs': len(self.entangled_pairs),
                'quantum_coherence': self._calculate_pediatric_quantum_coherence(age_group),
                'developmental_quantum_factor': self.growth_factors[age_group]['metabolic_rate']
            },
            'detected_conditions': detected_conditions,
            'overall_assessment': self._generate_overall_assessment(detected_conditions),
            'recommendations': self._generate_overall_recommendations(detected_conditions),
            'timestamp': datetime.now().isoformat()
        }
        
        return report
    
    def _get_age_group_from_months(self, age_months: int) -> str:
        """Получает возрастную группу из месяцев."""
        if age_months < 1:
            return "newborn"
        elif age_months < 12:
            return "infant"
        elif age_months < 36:
            return "toddler"
        elif age_months < 72:
            return "preschool"
        else:
            return "school_age"
    
    def _analyze_body_proportions(self, anthropometry: DetailedAnthropometry, age_months: int) -> Dict[str, Any]:
        """Анализирует пропорции тела для выявления аномалий развития."""
        proportions = {}
        
        # Анализ пропорций головы
        if anthropometry.head_length_cm > 0 and anthropometry.head_width_cm > 0:
            cephalic_index = (anthropometry.head_width_cm / anthropometry.head_length_cm) * 100
            proportions['cephalic_index'] = cephalic_index
            
            # Классификация формы головы
            if cephalic_index < 75:
                proportions['head_shape'] = "долихоцефалия (длинная голова)"
            elif cephalic_index > 85:
                proportions['head_shape'] = "брахицефалия (широкая голова)"
            else:
                proportions['head_shape'] = "мезоцефалия (нормальная форма)"
        
        # Анализ пропорций лица
        if anthropometry.face_height_cm > 0 and anthropometry.face_width_cm > 0:
            facial_index = (anthropometry.face_height_cm / anthropometry.face_width_cm) * 100
            proportions['facial_index'] = facial_index
        
        # Анализ пропорций конечностей
        if anthropometry.height_cm > 0:
            if anthropometry.arm_span_cm > 0:
                arm_span_ratio = anthropometry.arm_span_cm / anthropometry.height_cm
                proportions['arm_span_ratio'] = arm_span_ratio
                
                if arm_span_ratio > 1.05:
                    proportions['limb_assessment'] = "возможная марафаноподобная конституция"
                elif arm_span_ratio < 0.95:
                    proportions['limb_assessment'] = "возможная задержка роста конечностей"
                else:
                    proportions['limb_assessment'] = "нормальные пропорции конечностей"
        
        # Анализ симметрии пальцев
        finger_lengths = [
            anthropometry.thumb_length_mm,
            anthropometry.index_finger_length_mm,
            anthropometry.middle_finger_length_mm,
            anthropometry.ring_finger_length_mm,
            anthropometry.little_finger_length_mm
        ]
        
        if all(length > 0 for length in finger_lengths):
            finger_ratios = []
            for i in range(1, len(finger_lengths)):
                if finger_lengths[i] > 0:
                    finger_ratios.append(finger_lengths[i] / finger_lengths[0])
            
            proportions['finger_ratios'] = finger_ratios
            
            # Анализ паттернов пальцев для генетических синдромов
            if finger_ratios[1] > 1.5:  # Указательный палец значительно длиннее большого
                proportions['genetic_assessment'] = "возможные генетические особенности"
        
        return proportions
    
    def _analyze_growth_patterns(self, anthropometry: DetailedAnthropometry, age_months: int) -> Dict[str, Any]:
        """Анализирует паттерны роста и развития."""
        growth_patterns = {}
        
        # Анализ соответствия веса и роста
        if anthropometry.weight_kg > 0 and anthropometry.height_cm > 0:
            bmi = anthropometry.weight_kg / ((anthropometry.height_cm / 100) ** 2)
            growth_patterns['bmi'] = bmi
            
            # Возрастные нормы BMI для детей
            if age_months < 12:
                if bmi < 13:
                    growth_patterns['weight_assessment'] = "недостаточный вес"
                elif bmi > 20:
                    growth_patterns['weight_assessment'] = "избыточный вес"
                else:
                    growth_patterns['weight_assessment'] = "нормальный вес"
            elif age_months < 36:
                if bmi < 14:
                    growth_patterns['weight_assessment'] = "недостаточный вес"
                elif bmi > 18:
                    growth_patterns['weight_assessment'] = "избыточный вес"
                else:
                    growth_patterns['weight_assessment'] = "нормальный вес"
            else:
                if bmi < 15:
                    growth_patterns['weight_assessment'] = "недостаточный вес"
                elif bmi > 20:
                    growth_patterns['weight_assessment'] = "избыточный вес"
                else:
                    growth_patterns['weight_assessment'] = "нормальный вес"
        
        # Анализ пропорций головы к телу
        if anthropometry.head_circumference_cm > 0 and anthropometry.height_cm > 0:
            head_to_height_ratio = anthropometry.head_circumference_cm / anthropometry.height_cm
            growth_patterns['head_to_height_ratio'] = head_to_height_ratio
            
            if head_to_height_ratio > 0.35:
                growth_patterns['head_assessment'] = "возможная макроцефалия"
            elif head_to_height_ratio < 0.25:
                growth_patterns['head_assessment'] = "возможная микроцефалия"
            else:
                growth_patterns['head_assessment'] = "нормальные пропорции головы"
        
        return growth_patterns
    
    def _quantum_anthropometry_assessment(self, quantum_states: Dict[str, PediatricQuantumState], age_months: int) -> Dict[str, Any]:
        """Квантовый анализ антропометрических показателей."""
        quantum_assessment = {
            'total_indicators': len(quantum_states),
            'entanglement_analysis': {},
            'quantum_coherence': {},
            'developmental_quantum_score': 0.0
        }
        
        # Анализ квантовой запутанности между показателями
        entanglement_pairs = []
        indicators = list(quantum_states.keys())
        
        for i in range(len(indicators)):
            for j in range(i + 1, len(indicators)):
                try:
                    entangled_pair = self.calculate_pediatric_entanglement(
                        indicators[i], indicators[j], age_months
                    )
                    entanglement_pairs.append(entangled_pair)
                except:
                    continue
        
        # Оценка общей квантовой когерентности
        if entanglement_pairs:
            avg_entanglement = sum(pair.entanglement_strength for pair in entanglement_pairs) / len(entanglement_pairs)
            quantum_assessment['quantum_coherence']['average_entanglement'] = avg_entanglement
            quantum_assessment['quantum_coherence']['total_pairs'] = len(entanglement_pairs)
            
            # Квантовый балл развития
            quantum_assessment['developmental_quantum_score'] = avg_entanglement * (len(quantum_states) / 10.0)
        
        return quantum_assessment
    
    def _detect_developmental_anomalies(self, anthropometry: DetailedAnthropometry, age_months: int) -> Dict[str, Any]:
        """Обнаруживает аномалии развития на основе антропометрических данных."""
        anomalies = {
            'detected_anomalies': [],
            'risk_factors': [],
            'recommendations': []
        }
        
        # Проверка на синдромальные признаки
        # Синдром Дауна - короткие пальцы, широкие ладони
        if (anthropometry.little_finger_length_mm > 0 and 
            anthropometry.middle_finger_length_mm > 0 and
            anthropometry.little_finger_length_mm / anthropometry.middle_finger_length_mm < 0.6):
            anomalies['detected_anomalies'].append({
                'condition': 'возможные признаки синдрома Дауна',
                'probability': 0.3,
                'indicators': ['короткий мизинец относительно среднего пальца']
            })
        
        # Синдром Марфана - длинные конечности
        if (anthropometry.arm_span_cm > 0 and anthropometry.height_cm > 0 and
            anthropometry.arm_span_cm / anthropometry.height_cm > 1.05):
            anomalies['detected_anomalies'].append({
                'condition': 'возможные признаки синдрома Марфана',
                'probability': 0.4,
                'indicators': ['увеличенное соотношение размаха рук к росту']
            })
        
        # Микроцефалия
        if anthropometry.head_circumference_cm > 0:
            expected_head_circumference = self._get_expected_head_circumference(age_months)
            if anthropometry.head_circumference_cm < expected_head_circumference * 0.9:
                anomalies['detected_anomalies'].append({
                    'condition': 'возможная микроцефалия',
                    'probability': 0.7,
                    'indicators': ['малый размер окружности головы']
                })
        
        # Макроцефалия
        if anthropometry.head_circumference_cm > expected_head_circumference * 1.1:
            anomalies['detected_anomalies'].append({
                'condition': 'возможная макроцефалия',
                'probability': 0.6,
                'indicators': ['большой размер окружности головы']
            })
        
        return anomalies
    
    def _assess_developmental_indicators(self, anthropometry: DetailedAnthropometry, age_months: int) -> Dict[str, Any]:
        """Оценивает индикаторы развития ребенка."""
        developmental_indicators = {
            'physical_development': {},
            'proportional_development': {},
            'overall_assessment': 'нормальное развитие'
        }
        
        # Оценка физического развития
        if anthropometry.weight_kg > 0 and anthropometry.height_cm > 0:
            developmental_indicators['physical_development']['weight_height_ratio'] = (
                anthropometry.weight_kg / anthropometry.height_cm
            )
        
        # Оценка пропорционального развития
        if (anthropometry.arm_span_cm > 0 and anthropometry.leg_length_cm > 0 and 
            anthropometry.height_cm > 0):
            
            limb_balance = (anthropometry.arm_span_cm + anthropometry.leg_length_cm) / (2 * anthropometry.height_cm)
            developmental_indicators['proportional_development']['limb_balance'] = limb_balance
            
            if limb_balance > 0.9 and limb_balance < 1.1:
                developmental_indicators['overall_assessment'] = 'гармоничное развитие'
            elif limb_balance < 0.9:
                developmental_indicators['overall_assessment'] = 'возможная задержка роста конечностей'
            else:
                developmental_indicators['overall_assessment'] = 'возможное ускорение роста конечностей'
        
        return developmental_indicators
    
    def _get_expected_head_circumference(self, age_months: int) -> float:
        """Возвращает ожидаемую окружность головы для возраста."""
        if age_months < 1:
            return 35.0  # Новорожденные
        elif age_months < 12:
            return 35.0 + (age_months * 1.0)  # Быстрый рост в первый год
        elif age_months < 36:
            return 47.0 + ((age_months - 12) * 0.3)  # Медленный рост
        else:
            return 52.0  # Стабилизация после 3 лет
    
    def generate_comprehensive_development_report(self, 
                                                 anthropometry: DetailedAnthropometry,
                                                 age_months: int,
                                                 detailed_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Генерирует комплексный отчет о развитии ребенка с рекомендациями.
        
        Включает:
        - Стадию развития
        - Оценку физического и психического развития
        - Рекомендации по витаминам
        - Рекомендации по массажу
        - План дальнейших осмотров
        - Превентивные меры
        """
        
        report = {
            'child_info': {
                'age_months': age_months,
                'age_group': self._get_age_group_from_months(age_months),
                'developmental_stage': self._determine_developmental_stage_detailed(age_months)
            },
            'physical_development': {},
            'proportional_assessment': {},
            'vitamin_recommendations': [],
            'massage_recommendations': [],
            'follow_up_plan': [],
            'preventive_measures': [],
            'specialist_consultations': [],
            'overall_conclusion': ''
        }
        
        # Оценка физического развития
        report['physical_development'] = self._assess_physical_development_status(
            anthropometry, age_months, detailed_analysis
        )
        
        # Оценка пропорций
        report['proportional_assessment'] = detailed_analysis.get('proportional_analysis', {})
        
        # Генерация рекомендаций по витаминам
        report['vitamin_recommendations'] = self._generate_vitamin_recommendations(
            age_months, detailed_analysis, anthropometry
        )
        
        # Генерация рекомендаций по массажу
        report['massage_recommendations'] = self._generate_massage_recommendations(
            age_months, detailed_analysis
        )
        
        # План дальнейших осмотров
        report['follow_up_plan'] = self._generate_follow_up_plan(
            age_months, detailed_analysis
        )
        
        # Превентивные меры
        report['preventive_measures'] = self._generate_preventive_measures(
            age_months, detailed_analysis
        )
        
        # Консультации специалистов
        report['specialist_consultations'] = self._generate_specialist_recommendations(
            detailed_analysis
        )
        
        # Общее заключение
        report['overall_conclusion'] = self._generate_overall_conclusion(
            report, detailed_analysis
        )
        
        return report
    
    def _determine_developmental_stage_detailed(self, age_months: int) -> Dict[str, Any]:
        """Определяет детальную стадию развития ребенка."""
        if age_months < 1:
            return {
                'stage': 'Неонатальный период',
                'description': 'Адаптация к внеутробной жизни',
                'key_milestones': [
                    'Рефлексы новорожденного',
                    'Начало грудного вскармливания',
                    'Фокусировка взгляда',
                    'Реакция на звуки'
                ]
            }
        elif age_months < 3:
            return {
                'stage': 'Ранний младенческий период',
                'description': 'Быстрый рост и развитие',
                'key_milestones': [
                    'Удержание головы',
                    'Социальная улыбка',
                    'Гуление',
                    'Слежение за объектами'
                ]
            }
        elif age_months < 6:
            return {
                'stage': 'Средний младенческий период',
                'description': 'Развитие моторики и коммуникации',
                'key_milestones': [
                    'Переворачивание',
                    'Захват предметов',
                    'Лепет',
                    'Узнавание близких'
                ]
            }
        elif age_months < 12:
            return {
                'stage': 'Поздний младенческий период',
                'description': 'Подготовка к ходьбе и речи',
                'key_milestones': [
                    'Ползание',
                    'Сидение без поддержки',
                    'Первые слова',
                    'Понимание простых команд'
                ]
            }
        elif age_months < 18:
            return {
                'stage': 'Ранний ясельный возраст',
                'description': 'Освоение ходьбы и речи',
                'key_milestones': [
                    'Самостоятельная ходьба',
                    'Простые фразы',
                    'Игра с предметами',
                    'Проявление эмоций'
                ]
            }
        elif age_months < 36:
            return {
                'stage': 'Поздний ясельный возраст',
                'description': 'Активное познание мира',
                'key_milestones': [
                    'Бег и прыжки',
                    'Связная речь',
                    'Игра с другими детьми',
                    'Самостоятельность в еде'
                ]
            }
        elif age_months < 72:
            return {
                'stage': 'Дошкольный возраст',
                'description': 'Подготовка к школе',
                'key_milestones': [
                    'Сложная координация',
                    'Развернутая речь',
                    'Социальные навыки',
                    'Подготовка к обучению'
                ]
            }
        else:
            return {
                'stage': 'Младший школьный возраст',
                'description': 'Развитие когнитивных способностей',
                'key_milestones': [
                    'Академические навыки',
                    'Абстрактное мышление',
                    'Дружеские отношения',
                    'Самоконтроль'
                ]
            }
    
    def _assess_physical_development_status(self, 
                                          anthropometry: DetailedAnthropometry,
                                          age_months: int,
                                          detailed_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Оценивает статус физического развития."""
        growth_patterns = detailed_analysis.get('growth_patterns', {})
        
        status = {
            'weight_status': 'нормальный',
            'height_status': 'нормальный',
            'head_status': 'нормальный',
            'overall_status': 'соответствует возрасту',
            'percentile_estimates': {}
        }
        
        # Оценка веса
        weight_assessment = growth_patterns.get('weight_assessment', 'нормальный вес')
        if 'недостаточный' in weight_assessment:
            status['weight_status'] = 'ниже нормы'
        elif 'избыточный' in weight_assessment:
            status['weight_status'] = 'выше нормы'
        
        # Оценка головы
        head_assessment = growth_patterns.get('head_assessment', 'нормальные пропорции головы')
        if 'микроцефалия' in head_assessment:
            status['head_status'] = 'малый размер'
        elif 'макроцефалия' in head_assessment:
            status['head_status'] = 'большой размер'
        
        # Общий статус
        if status['weight_status'] != 'нормальный' or status['head_status'] != 'нормальный':
            status['overall_status'] = 'требует внимания'
        
        return status
    
    def _generate_vitamin_recommendations(self, 
                                        age_months: int,
                                        detailed_analysis: Dict[str, Any],
                                        anthropometry: DetailedAnthropometry) -> List[Dict[str, str]]:
        """Генерирует рекомендации по витаминам."""
        recommendations = []
        
        # Базовые витамины для возраста
        if age_months < 12:
            recommendations.append({
                'vitamin': 'Витамин D3',
                'dosage': '400-500 МЕ в день',
                'reason': 'Профилактика рахита и укрепление костей',
                'duration': 'Ежедневно, особенно в зимний период'
            })
            recommendations.append({
                'vitamin': 'Витамин К',
                'dosage': 'По назначению педиатра',
                'reason': 'Профилактика кровотечений',
                'duration': 'По показаниям'
            })
        elif age_months < 36:
            recommendations.append({
                'vitamin': 'Витамин D3',
                'dosage': '600 МЕ в день',
                'reason': 'Поддержка роста костей и зубов',
                'duration': 'Ежедневно'
            })
            recommendations.append({
                'vitamin': 'Поливитамины для детей',
                'dosage': 'По инструкции',
                'reason': 'Общее укрепление организма',
                'duration': 'Курсами по 1-2 месяца'
            })
        else:
            recommendations.append({
                'vitamin': 'Витамин D3',
                'dosage': '600-800 МЕ в день',
                'reason': 'Поддержка иммунитета и костной системы',
                'duration': 'Ежедневно'
            })
            recommendations.append({
                'vitamin': 'Омега-3',
                'dosage': '250-500 мг в день',
                'reason': 'Развитие мозга и когнитивных функций',
                'duration': 'Курсами по 2-3 месяца'
            })
        
        # Дополнительные витамины на основе анализа
        anomalies = detailed_analysis.get('anomaly_detection', {}).get('detected_anomalies', [])
        growth_patterns = detailed_analysis.get('growth_patterns', {})
        
        # При задержке роста
        if 'недостаточный вес' in growth_patterns.get('weight_assessment', ''):
            recommendations.append({
                'vitamin': 'Витамин А',
                'dosage': 'По назначению врача',
                'reason': 'Стимуляция роста и развития',
                'duration': 'Курсами'
            })
            recommendations.append({
                'vitamin': 'Цинк',
                'dosage': '5-10 мг в день',
                'reason': 'Улучшение аппетита и роста',
                'duration': '2-3 месяца'
            })
        
        # При проблемах с костной системой
        for anomaly in anomalies:
            if 'микроцефалия' in anomaly.get('condition', '').lower():
                recommendations.append({
                    'vitamin': 'Кальций + Витамин D',
                    'dosage': 'По назначению врача',
                    'reason': 'Поддержка развития костей черепа',
                    'duration': 'Длительно'
                })
        
        return recommendations
    
    def _generate_massage_recommendations(self,
                                        age_months: int,
                                        detailed_analysis: Dict[str, Any]) -> List[Dict[str, str]]:
        """Генерирует рекомендации по массажу."""
        recommendations = []
        
        # Базовые рекомендации по возрасту
        if age_months < 6:
            recommendations.append({
                'type': 'Общеукрепляющий массаж',
                'frequency': '2-3 раза в день',
                'duration': '10-15 минут',
                'description': 'Легкие поглаживания, способствующие развитию мышечного тонуса',
                'focus_areas': ['спина', 'ножки', 'ручки', 'животик']
            })
            recommendations.append({
                'type': 'Массаж стоп',
                'frequency': 'Ежедневно',
                'duration': '5 минут',
                'description': 'Стимуляция рефлексогенных зон для общего развития',
                'focus_areas': ['стопы']
            })
        elif age_months < 12:
            recommendations.append({
                'type': 'Развивающий массаж',
                'frequency': '1-2 раза в день',
                'duration': '15-20 минут',
                'description': 'Массаж для подготовки к ползанию и сидению',
                'focus_areas': ['спина', 'мышцы кора', 'ножки']
            })
        elif age_months < 36:
            recommendations.append({
                'type': 'Массаж для формирования осанки',
                'frequency': '3-4 раза в неделю',
                'duration': '20-30 минут',
                'description': 'Укрепление мышц спины и правильной осанки',
                'focus_areas': ['спина', 'плечи', 'шея']
            })
        else:
            recommendations.append({
                'type': 'Профилактический массаж',
                'frequency': '2-3 раза в неделю',
                'duration': '30 минут',
                'description': 'Общеукрепляющий массаж для поддержания здоровья',
                'focus_areas': ['все тело']
            })
        
        # Специальные рекомендации на основе анализа
        anomalies = detailed_analysis.get('anomaly_detection', {}).get('detected_anomalies', [])
        proportional_analysis = detailed_analysis.get('proportional_analysis', {})
        
        # При проблемах с конечностями
        if 'задержка роста конечностей' in proportional_analysis.get('limb_assessment', ''):
            recommendations.append({
                'type': 'Массаж конечностей',
                'frequency': 'Ежедневно',
                'duration': '15 минут',
                'description': 'Стимулирующий массаж для улучшения кровообращения',
                'focus_areas': ['руки', 'ноги']
            })
        
        # При проблемах с головой
        for anomaly in anomalies:
            if 'микроцефалия' in anomaly.get('condition', '').lower():
                recommendations.append({
                    'type': 'Массаж головы и шеи',
                    'frequency': 'Ежедневно',
                    'duration': '10 минут',
                    'description': 'Легкий массаж для улучшения кровообращения головного мозга',
                    'focus_areas': ['голова', 'шея', 'воротниковая зона']
                })
        
        return recommendations
    
    def _generate_follow_up_plan(self,
                               age_months: int,
                               detailed_analysis: Dict[str, Any]) -> List[Dict[str, str]]:
        """Генерирует план дальнейших осмотров."""
        plan = []
        
        # Базовый план по возрасту
        if age_months < 12:
            plan.append({
                'specialist': 'Педиатр',
                'frequency': 'Ежемесячно',
                'purpose': 'Контроль развития и вакцинация',
                'priority': 'Высокий'
            })
            plan.append({
                'specialist': 'Невролог',
                'frequency': 'В 3, 6 и 12 месяцев',
                'purpose': 'Оценка нервно-психического развития',
                'priority': 'Средний'
            })
        elif age_months < 36:
            plan.append({
                'specialist': 'Педиатр',
                'frequency': 'Каждые 3 месяца',
                'purpose': 'Контроль роста и развития',
                'priority': 'Высокий'
            })
            plan.append({
                'specialist': 'Стоматолог',
                'frequency': 'Каждые 6 месяцев',
                'purpose': 'Контроль развития зубов',
                'priority': 'Средний'
            })
        else:
            plan.append({
                'specialist': 'Педиатр',
                'frequency': 'Раз в полгода',
                'purpose': 'Профилактический осмотр',
                'priority': 'Средний'
            })
            plan.append({
                'specialist': 'Офтальмолог',
                'frequency': 'Ежегодно',
                'purpose': 'Проверка зрения',
                'priority': 'Средний'
            })
        
        # Дополнительные осмотры на основе анализа
        anomalies = detailed_analysis.get('anomaly_detection', {}).get('detected_anomalies', [])
        
        for anomaly in anomalies:
            condition = anomaly.get('condition', '').lower()
            probability = anomaly.get('probability', 0)
            
            if probability > 0.5:
                if 'марфан' in condition:
                    plan.append({
                        'specialist': 'Генетик',
                        'frequency': 'В ближайшее время',
                        'purpose': 'Исключение синдрома Марфана',
                        'priority': 'Высокий'
                    })
                    plan.append({
                        'specialist': 'Кардиолог',
                        'frequency': 'Каждые 6 месяцев',
                        'purpose': 'Контроль сердечно-сосудистой системы',
                        'priority': 'Высокий'
                    })
                
                if 'дауна' in condition:
                    plan.append({
                        'specialist': 'Генетик',
                        'frequency': 'Срочно',
                        'purpose': 'Генетическое обследование',
                        'priority': 'Критический'
                    })
                
                if 'микроцефалия' in condition or 'макроцефалия' in condition:
                    plan.append({
                        'specialist': 'Невролог',
                        'frequency': 'Каждый месяц',
                        'purpose': 'Контроль развития головного мозга',
                        'priority': 'Высокий'
                    })
                    plan.append({
                        'specialist': 'УЗИ головного мозга',
                        'frequency': 'По назначению',
                        'purpose': 'Оценка структуры мозга',
                        'priority': 'Высокий'
                    })
        
        return plan
    
    def _generate_preventive_measures(self,
                                     age_months: int,
                                     detailed_analysis: Dict[str, Any]) -> List[str]:
        """Генерирует превентивные меры."""
        measures = []
        
        # Базовые меры по возрасту
        if age_months < 12:
            measures.extend([
                '✓ Грудное вскармливание или адаптированная смесь',
                '✓ Соблюдение режима сна (14-17 часов в сутки)',
                '✓ Ежедневные прогулки на свежем воздухе (2-3 часа)',
                '✓ Гимнастика и массаж',
                '✓ Развивающие игры по возрасту',
                '✓ Соблюдение графика вакцинации'
            ])
        elif age_months < 36:
            measures.extend([
                '✓ Сбалансированное питание с разнообразными продуктами',
                '✓ Режим сна (12-14 часов в сутки)',
                '✓ Активные игры и физическая активность',
                '✓ Развитие речи через общение и игры',
                '✓ Социализация с другими детьми',
                '✓ Ограничение экранного времени'
            ])
        else:
            measures.extend([
                '✓ Здоровое разнообразное питание',
                '✓ Режим дня с достаточным сном (10-12 часов)',
                '✓ Регулярная физическая активность',
                '✓ Интеллектуальное развитие (чтение, игры, подготовка к школе)',
                '✓ Социальные навыки и общение',
                '✓ Ограничение гаджетов (не более 1 часа в день)'
            ])
        
        # Специфические меры на основе анализа
        growth_patterns = detailed_analysis.get('growth_patterns', {})
        
        if 'недостаточный вес' in growth_patterns.get('weight_assessment', ''):
            measures.extend([
                '⚠ Консультация диетолога для коррекции питания',
                '⚠ Увеличение калорийности рациона',
                '⚠ Контроль набора веса еженедельно'
            ])
        
        if 'избыточный вес' in growth_patterns.get('weight_assessment', ''):
            measures.extend([
                '⚠ Коррекция рациона - снижение быстрых углеводов',
                '⚠ Увеличение физической активности',
                '⚠ Контроль веса ежемесячно'
            ])
        
        return measures
    
    def _generate_specialist_recommendations(self,
                                           detailed_analysis: Dict[str, Any]) -> List[str]:
        """Генерирует рекомендации по консультациям специалистов."""
        specialists = []
        
        anomalies = detailed_analysis.get('anomaly_detection', {}).get('detected_anomalies', [])
        
        for anomaly in anomalies:
            condition = anomaly.get('condition', '').lower()
            probability = anomaly.get('probability', 0)
            
            if probability > 0.4:
                if 'синдром' in condition or 'генетические' in condition:
                    if 'Генетик - для исключения наследственных заболеваний' not in specialists:
                        specialists.append('🔬 Генетик - для исключения наследственных заболеваний')
                
                if 'марфан' in condition or 'сердца' in condition:
                    if 'Кардиолог - для обследования сердечно-сосудистой системы' not in specialists:
                        specialists.append('❤️ Кардиолог - для обследования сердечно-сосудистой системы')
                
                if 'микроцефалия' in condition or 'макроцефалия' in condition or 'мозг' in condition:
                    if 'Невролог - для оценки развития нервной системы' not in specialists:
                        specialists.append('🧠 Невролог - для оценки развития нервной системы')
                
                if 'конечност' in condition:
                    if 'Ортопед - для оценки костно-мышечной системы' not in specialists:
                        specialists.append('🦴 Ортопед - для оценки костно-мышечной системы')
        
        if not specialists:
            specialists.append('✅ По результатам анализа дополнительные консультации не требуются')
        
        return specialists
    
    def _generate_overall_conclusion(self,
                                    report: Dict[str, Any],
                                    detailed_analysis: Dict[str, Any]) -> str:
        """Генерирует общее заключение о развитии ребенка."""
        age_months = report['child_info']['age_months']
        stage = report['child_info']['developmental_stage']['stage']
        
        physical_status = report['physical_development'].get('overall_status', 'соответствует возрасту')
        quantum_score = detailed_analysis.get('quantum_assessment', {}).get('developmental_quantum_score', 0)
        
        anomalies = detailed_analysis.get('anomaly_detection', {}).get('detected_anomalies', [])
        high_risk_anomalies = [a for a in anomalies if a.get('probability', 0) > 0.6]
        
        conclusion = f"**Ребенок {age_months} месяцев, {stage}.**\n\n"
        
        if quantum_score > 0.8 and not high_risk_anomalies and physical_status == 'соответствует возрасту':
            conclusion += "✅ **ЗАКЛЮЧЕНИЕ: Развитие соответствует возрастной норме.**\n\n"
            conclusion += "Ребенок развивается гармонично, все показатели в пределах нормы. "
            conclusion += "Квантовый анализ показывает высокий уровень согласованности всех систем организма. "
            conclusion += "Рекомендуется продолжать текущий режим питания, ухода и развивающих занятий. "
            conclusion += "Профилактические осмотры согласно возрастному графику."
        
        elif quantum_score > 0.6 and not high_risk_anomalies:
            conclusion += "📋 **ЗАКЛЮЧЕНИЕ: Развитие в целом соответствует норме с незначительными особенностями.**\n\n"
            conclusion += "Ребенок развивается согласно возрасту, выявлены минимальные отклонения, "
            conclusion += "которые могут быть вариантом нормы или требуют наблюдения. "
            conclusion += "Рекомендуется выполнение всех назначений и повторный осмотр через указанный срок."
        
        elif high_risk_anomalies:
            conclusion += "⚠️ **ЗАКЛЮЧЕНИЕ: Выявлены отклонения, требующие внимания специалистов.**\n\n"
            conclusion += "Обнаружены следующие особенности развития:\n"
            for anomaly in high_risk_anomalies:
                conclusion += f"• {anomaly['condition']} (вероятность: {anomaly['probability']:.0%})\n"
            conclusion += "\nНеобходима консультация специалистов для уточнения диагноза и назначения лечения. "
            conclusion += "Важно своевременное обращение для максимально эффективной коррекции."
        
        else:
            conclusion += "📊 **ЗАКЛЮЧЕНИЕ: Развитие требует дополнительного наблюдения.**\n\n"
            conclusion += "Некоторые показатели отличаются от возрастной нормы. "
            conclusion += "Рекомендуется усиленный контроль развития, выполнение всех назначенных мероприятий "
            conclusion += "и консультации специалистов согласно плану."
        
        return conclusion
    
    def _calculate_pediatric_quantum_coherence(self, age_group: AgeGroup) -> float:
        """Вычисляет квантовую когерентность для детского возраста."""
        if not self.quantum_states:
            return 0.0
        
        # Дети имеют более высокую квантовую когерентность из-за быстрого развития
        base_coherence = 0.8
        age_factor = self.growth_factors[age_group]['metabolic_rate']
        
        return min(1.0, base_coherence * age_factor)
    
    def _generate_overall_assessment(self, detected_conditions: List[Dict[str, Any]]) -> str:
        """Генерирует общую оценку состояния."""
        if not detected_conditions:
            return "✅ Все показатели в пределах нормы для данного возраста"
        
        high_risk_conditions = [c for c in detected_conditions if c['probability'] > 0.8]
        if high_risk_conditions:
            return f"🚨 Обнаружено {len(high_risk_conditions)} состояний высокого риска, требующих немедленного внимания"
        
        medium_risk_conditions = [c for c in detected_conditions if 0.6 <= c['probability'] <= 0.8]
        if medium_risk_conditions:
            return f"⚠️ Обнаружено {len(medium_risk_conditions)} состояний средней степени риска, рекомендуется наблюдение"
        
        return "📋 Обнаружены незначительные отклонения, рекомендуется плановое наблюдение"
    
    def _generate_overall_recommendations(self, detected_conditions: List[Dict[str, Any]]) -> List[str]:
        """Генерирует общие рекомендации."""
        recommendations = []
        
        if not detected_conditions:
            recommendations.append("Продолжать плановое наблюдение у педиатра")
            recommendations.append("Соблюдать режим питания и сна")
            recommendations.append("Отслеживать этапы развития")
            return recommendations
        
        # Собираем все рекомендации
        all_recommendations = []
        for condition in detected_conditions:
            all_recommendations.extend(condition['recommendations'])
        
        # Удаляем дубликаты и сортируем по приоритету
        unique_recommendations = list(set(all_recommendations))
        recommendations.extend(unique_recommendations)
        
        return recommendations

"""
Расширенная медицинская диагностическая система MQEA
для работы с большими объемами данных, персонализации лечения
и прогнозирования рисков заболеваний.

Автор: Мухаммад Махизода
Таджикский национальный университет
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any, Union
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import warnings
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import multiprocessing as mp
from pathlib import Path
import json
import pickle
import logging

from .core import MQEAAnalyzer
from .quantum_entanglement import QuantumEntanglementEngine
from .data_processor import MedicalTimeSeries, TemporalPattern


class RiskLevel(Enum):
    """Уровни медицинского риска."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class DiagnosticCategory(Enum):
    """Категории диагностики."""
    CARDIOVASCULAR = "cardiovascular"
    RESPIRATORY = "respiratory"
    METABOLIC = "metabolic"
    NEUROLOGICAL = "neurological"
    INFECTIOUS = "infectious"
    ONCOLOGICAL = "oncological"


@dataclass
class PatientProfile:
    """Профиль пациента для персонализированного анализа."""
    patient_id: str
    age: int
    gender: str
    weight: float
    height: float
    medical_history: List[str]
    current_medications: List[str]
    allergies: List[str]
    lifestyle_factors: Dict[str, Any]
    genetic_factors: Optional[Dict[str, Any]] = None
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
    
    @property
    def bmi(self) -> float:
        """Индекс массы тела."""
        return self.weight / ((self.height / 100) ** 2)
    
    @property
    def age_group(self) -> str:
        """Возрастная группа."""
        if self.age < 18:
            return "pediatric"
        elif self.age < 65:
            return "adult"
        else:
            return "elderly"


@dataclass
class DiagnosticResult:
    """Результат диагностики."""
    patient_id: str
    timestamp: datetime
    category: DiagnosticCategory
    risk_level: RiskLevel
    confidence: float
    indicators: List[str]
    quantum_signature: Dict[str, float]
    recommendations: List[str]
    urgency_score: float
    follow_up_required: bool
    follow_up_timeframe: Optional[timedelta] = None


@dataclass
class TreatmentRecommendation:
    """Рекомендация по лечению."""
    patient_id: str
    recommendation_type: str
    description: str
    priority: int
    expected_effectiveness: float
    side_effects: List[str]
    contraindications: List[str]
    monitoring_required: List[str]
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


class MedicalDiagnosticSystem:
    """
    Расширенная медицинская диагностическая система MQEA.
    
    Обеспечивает:
    - Анализ больших объемов медицинских данных
    - Персонализированную диагностику
    - Прогнозирование рисков заболеваний
    - Рекомендации по лечению
    - Мониторинг в реальном времени
    """
    
    def __init__(self, 
                 max_workers: Optional[int] = None,
                 enable_parallel_processing: bool = True,
                 enable_ml_models: bool = True,
                 enable_real_time_monitoring: bool = True):
        """
        Инициализация медицинской диагностической системы.
        
        Args:
            max_workers: Максимальное количество рабочих процессов
            enable_parallel_processing: Включить параллельную обработку
            enable_ml_models: Включить машинное обучение
            enable_real_time_monitoring: Включить мониторинг в реальном времени
        """
        self.max_workers = max_workers or min(mp.cpu_count(), 8)
        self.enable_parallel_processing = enable_parallel_processing
        self.enable_ml_models = enable_ml_models
        self.enable_real_time_monitoring = enable_real_time_monitoring
        
        # Инициализация компонентов
        self.mqea_analyzer = MQEAAnalyzer()
        self.quantum_engine = QuantumEntanglementEngine()
        
        # Медицинские базы данных
        self.patient_profiles: Dict[str, PatientProfile] = {}
        self.diagnostic_history: Dict[str, List[DiagnosticResult]] = {}
        self.treatment_recommendations: Dict[str, List[TreatmentRecommendation]] = {}
        
        # Модели машинного обучения
        self.risk_prediction_models: Dict[str, Any] = {}
        self.diagnostic_models: Dict[DiagnosticCategory, Any] = {}
        
        # Настройки логирования
        self.logger = logging.getLogger(__name__)
        
        # Инициализация медицинских стандартов
        self._initialize_medical_standards()
        
        print(f"🏥 Медицинская диагностическая система MQEA инициализирована")
        print(f"   - Параллельная обработка: {'включена' if enable_parallel_processing else 'отключена'}")
        print(f"   - ML модели: {'включены' if enable_ml_models else 'отключены'}")
        print(f"   - Реальное время: {'включено' if enable_real_time_monitoring else 'отключено'}")
        print(f"   - Рабочих процессов: {self.max_workers}")
    
    def _initialize_medical_standards(self):
        """Инициализация медицинских стандартов и нормативов."""
        self.medical_standards = {
            'heart_rate': {
                'normal': (60, 100),
                'bradycardia': (0, 59),
                'tachycardia': (101, 200)
            },
            'blood_pressure_systolic': {
                'normal': (90, 120),
                'elevated': (121, 129),
                'hypertension_stage1': (130, 139),
                'hypertension_stage2': (140, 180),
                'hypertensive_crisis': (181, 300)
            },
            'blood_pressure_diastolic': {
                'normal': (60, 80),
                'elevated': (81, 89),
                'hypertension_stage1': (90, 99),
                'hypertension_stage2': (100, 120),
                'hypertensive_crisis': (121, 200)
            },
            'temperature': {
                'normal': (36.1, 37.2),
                'fever': (37.3, 40.0),
                'hypothermia': (35.0, 36.0)
            },
            'oxygen_saturation': {
                'normal': (95, 100),
                'mild_hypoxemia': (90, 94),
                'moderate_hypoxemia': (85, 89),
                'severe_hypoxemia': (0, 84)
            },
            'respiratory_rate': {
                'normal': (12, 20),
                'bradypnea': (0, 11),
                'tachypnea': (21, 30)
            },
            'glucose': {
                'normal': (3.9, 5.6),
                'prediabetes': (5.7, 6.9),
                'diabetes': (7.0, 20.0),
                'hypoglycemia': (0, 3.8)
            },
            'cholesterol': {
                'normal': (0, 200),
                'borderline_high': (201, 239),
                'high': (240, 500)
            }
        }
        
        # Веса рисков для различных состояний
        self.risk_weights = {
            'cardiovascular': {
                'heart_rate': 0.15,
                'blood_pressure_systolic': 0.25,
                'blood_pressure_diastolic': 0.25,
                'cholesterol': 0.20,
                'glucose': 0.15
            },
            'respiratory': {
                'respiratory_rate': 0.30,
                'oxygen_saturation': 0.40,
                'temperature': 0.30
            },
            'metabolic': {
                'glucose': 0.40,
                'cholesterol': 0.30,
                'weight': 0.30
            }
        }
    
    def add_patient_profile(self, profile: PatientProfile) -> bool:
        """
        Добавить профиль пациента.
        
        Args:
            profile: Профиль пациента
            
        Returns:
            bool: True если профиль добавлен успешно
        """
        try:
            self.patient_profiles[profile.patient_id] = profile
            self.diagnostic_history[profile.patient_id] = []
            self.treatment_recommendations[profile.patient_id] = []
            
            self.logger.info(f"Профиль пациента {profile.patient_id} добавлен")
            return True
        except Exception as e:
            self.logger.error(f"Ошибка добавления профиля пациента: {e}")
            return False
    
    def analyze_patient_data(self, 
                           patient_id: str,
                           medical_data: MedicalTimeSeries,
                           analysis_depth: str = "comprehensive") -> DiagnosticResult:
        """
        Анализ медицинских данных пациента.
        
        Args:
            patient_id: ID пациента
            medical_data: Медицинские данные
            analysis_depth: Глубина анализа ("basic", "standard", "comprehensive")
            
        Returns:
            DiagnosticResult: Результат диагностики
        """
        if patient_id not in self.patient_profiles:
            raise ValueError(f"Профиль пациента {patient_id} не найден")
        
        profile = self.patient_profiles[patient_id]
        
        print(f"🔍 Анализ данных пациента {patient_id}...")
        
        # 1. Квантовый анализ запутанности
        quantum_results = self.mqea_analyzer.quantum_entanglement_analysis(
            time_series=medical_data,
            quantum_threshold=0.3
        )
        
        # 2. Анализ рисков по категориям
        risk_analysis = self._analyze_medical_risks(profile, medical_data)
        
        # 3. Определение наиболее критичной категории
        primary_category = max(risk_analysis.keys(), 
                             key=lambda k: risk_analysis[k]['risk_score'])
        
        # 4. Расчет уровня риска
        risk_level = self._calculate_risk_level(risk_analysis[primary_category]['risk_score'])
        
        # 5. Генерация рекомендаций
        recommendations = self._generate_recommendations(
            profile, medical_data, risk_analysis, primary_category
        )
        
        # 6. Расчет срочности
        urgency_score = self._calculate_urgency_score(
            risk_analysis, quantum_results, profile
        )
        
        # 7. Создание результата диагностики
        diagnostic_result = DiagnosticResult(
            patient_id=patient_id,
            timestamp=datetime.now(),
            category=DiagnosticCategory(primary_category),
            risk_level=risk_level,
            confidence=risk_analysis[primary_category]['confidence'],
            indicators=risk_analysis[primary_category]['indicators'],
            quantum_signature=quantum_results['quantum_signatures'],
            recommendations=recommendations,
            urgency_score=urgency_score,
            follow_up_required=risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL],
            follow_up_timeframe=self._calculate_follow_up_timeframe(risk_level)
        )
        
        # 8. Сохранение результата
        self.diagnostic_history[patient_id].append(diagnostic_result)
        
        print(f"✅ Диагностика завершена:")
        print(f"   - Категория: {diagnostic_result.category.value}")
        print(f"   - Уровень риска: {diagnostic_result.risk_level.value}")
        print(f"   - Уверенность: {diagnostic_result.confidence:.3f}")
        print(f"   - Срочность: {diagnostic_result.urgency_score:.3f}")
        
        return diagnostic_result
    
    def _analyze_medical_risks(self, 
                             profile: PatientProfile, 
                             medical_data: MedicalTimeSeries) -> Dict[str, Dict[str, Any]]:
        """Анализ медицинских рисков по категориям."""
        risk_analysis = {}
        
        for category, weights in self.risk_weights.items():
            category_risks = []
            indicators = []
            
            for indicator, weight in weights.items():
                if indicator in medical_data.indicators:
                    # Получаем последние значения показателя
                    values = medical_data.data[indicator].dropna().tail(10)
                    
                    if len(values) > 0:
                        avg_value = values.mean()
                        risk_score = self._calculate_indicator_risk(
                            indicator, avg_value, profile
                        )
                        category_risks.append(risk_score * weight)
                        indicators.append(indicator)
            
            if category_risks:
                risk_analysis[category] = {
                    'risk_score': sum(category_risks),
                    'confidence': min(0.95, len(category_risks) / len(weights)),
                    'indicators': indicators,
                    'individual_risks': dict(zip(indicators, category_risks))
                }
        
        return risk_analysis
    
    def _calculate_indicator_risk(self, 
                                indicator: str, 
                                value: float, 
                                profile: PatientProfile) -> float:
        """Расчет риска для отдельного показателя."""
        if indicator not in self.medical_standards:
            return 0.0
        
        standards = self.medical_standards[indicator]
        
        # Определяем категорию риска
        for category, (min_val, max_val) in standards.items():
            if min_val <= value <= max_val:
                if category == 'normal':
                    return 0.0
                elif category in ['elevated', 'mild_hypoxemia']:
                    return 0.3
                elif category in ['hypertension_stage1', 'prediabetes', 'borderline_high']:
                    return 0.6
                elif category in ['hypertension_stage2', 'diabetes', 'high']:
                    return 0.8
                elif category in ['hypertensive_crisis', 'severe_hypoxemia']:
                    return 1.0
                else:
                    return 0.5
        
        # Значение вне нормальных диапазонов
        return 0.9
    
    def _calculate_risk_level(self, risk_score: float) -> RiskLevel:
        """Расчет уровня риска."""
        if risk_score < 0.3:
            return RiskLevel.LOW
        elif risk_score < 0.6:
            return RiskLevel.MEDIUM
        elif risk_score < 0.8:
            return RiskLevel.HIGH
        else:
            return RiskLevel.CRITICAL
    
    def _generate_recommendations(self, 
                                profile: PatientProfile,
                                medical_data: MedicalTimeSeries,
                                risk_analysis: Dict[str, Dict[str, Any]],
                                primary_category: str) -> List[str]:
        """Генерация персонализированных рекомендаций."""
        recommendations = []
        
        # Базовые рекомендации на основе категории риска
        if primary_category == 'cardiovascular':
            recommendations.extend([
                "Регулярный мониторинг артериального давления",
                "Контроль уровня холестерина",
                "Физическая активность 30 минут в день",
                "Ограничение соли в рационе"
            ])
        elif primary_category == 'respiratory':
            recommendations.extend([
                "Мониторинг насыщения кислородом",
                "Дыхательные упражнения",
                "Избегание курения и загрязненного воздуха"
            ])
        elif primary_category == 'metabolic':
            recommendations.extend([
                "Контроль уровня глюкозы",
                "Сбалансированное питание",
                "Регулярные физические упражнения",
                "Контроль веса"
            ])
        
        # Персонализированные рекомендации
        if profile.age > 65:
            recommendations.append("Усиленный мониторинг из-за возраста")
        
        if profile.bmi > 30:
            recommendations.append("Программа снижения веса")
        
        if 'diabetes' in profile.medical_history:
            recommendations.append("Строгий контроль глюкозы")
        
        return recommendations
    
    def _calculate_urgency_score(self, 
                               risk_analysis: Dict[str, Dict[str, Any]],
                               quantum_results: Dict[str, Any],
                               profile: PatientProfile) -> float:
        """Расчет срочности медицинского вмешательства."""
        urgency_factors = []
        
        # Фактор риска
        max_risk = max([analysis['risk_score'] for analysis in risk_analysis.values()])
        urgency_factors.append(max_risk)
        
        # Фактор квантовой когерентности (низкая когерентность = высокая срочность)
        quantum_coherence = quantum_results['quantum_signatures'].get('quantum_coherence', 0.5)
        urgency_factors.append(1.0 - quantum_coherence)
        
        # Фактор возраста
        if profile.age > 75:
            urgency_factors.append(0.8)
        elif profile.age > 65:
            urgency_factors.append(0.5)
        else:
            urgency_factors.append(0.2)
        
        # Фактор медицинской истории
        critical_conditions = ['diabetes', 'hypertension', 'heart_disease', 'cancer']
        if any(condition in profile.medical_history for condition in critical_conditions):
            urgency_factors.append(0.7)
        
        return min(1.0, sum(urgency_factors) / len(urgency_factors))
    
    def _calculate_follow_up_timeframe(self, risk_level: RiskLevel) -> timedelta:
        """Расчет времени до следующего наблюдения."""
        timeframes = {
            RiskLevel.LOW: timedelta(days=90),
            RiskLevel.MEDIUM: timedelta(days=30),
            RiskLevel.HIGH: timedelta(days=7),
            RiskLevel.CRITICAL: timedelta(hours=24)
        }
        return timeframes[risk_level]
    
    def predict_disease_risk(self, 
                           patient_id: str,
                           time_horizon_days: int = 30) -> Dict[str, float]:
        """
        Прогнозирование риска заболеваний.
        
        Args:
            patient_id: ID пациента
            time_horizon_days: Временной горизонт прогноза в днях
            
        Returns:
            Dict[str, float]: Риски различных заболеваний
        """
        if patient_id not in self.patient_profiles:
            raise ValueError(f"Профиль пациента {patient_id} не найден")
        
        profile = self.patient_profiles[patient_id]
        diagnostic_history = self.diagnostic_history.get(patient_id, [])
        
        print(f"🔮 Прогнозирование рисков для пациента {patient_id}...")
        
        # Базовые риски на основе профиля
        base_risks = self._calculate_base_risks(profile)
        
        # Корректировка на основе истории диагностики
        if diagnostic_history:
            recent_diagnostics = [d for d in diagnostic_history 
                                if d.timestamp > datetime.now() - timedelta(days=30)]
            
            for diagnostic in recent_diagnostics:
                category = diagnostic.category.value
                if category in base_risks:
                    # Увеличиваем риск на основе недавних диагнозов
                    base_risks[category] *= (1 + diagnostic.urgency_score * 0.5)
        
        # Временная корректировка
        time_factor = min(1.0, time_horizon_days / 30)
        for category in base_risks:
            base_risks[category] *= time_factor
        
        # Нормализация рисков
        max_risk = max(base_risks.values()) if base_risks else 0
        if max_risk > 0:
            for category in base_risks:
                base_risks[category] = min(1.0, base_risks[category] / max_risk)
        
        print(f"✅ Прогноз рисков на {time_horizon_days} дней:")
        for category, risk in base_risks.items():
            print(f"   - {category}: {risk:.3f}")
        
        return base_risks
    
    def _calculate_base_risks(self, profile: PatientProfile) -> Dict[str, float]:
        """Расчет базовых рисков на основе профиля пациента."""
        risks = {}
        
        # Возрастные риски
        if profile.age > 65:
            risks['cardiovascular'] = 0.6
            risks['metabolic'] = 0.5
        elif profile.age > 45:
            risks['cardiovascular'] = 0.4
            risks['metabolic'] = 0.3
        else:
            risks['cardiovascular'] = 0.2
            risks['metabolic'] = 0.1
        
        # Риски на основе ИМТ
        if profile.bmi > 30:
            risks['metabolic'] = max(risks.get('metabolic', 0), 0.8)
            risks['cardiovascular'] = max(risks.get('cardiovascular', 0), 0.6)
        elif profile.bmi > 25:
            risks['metabolic'] = max(risks.get('metabolic', 0), 0.4)
        
        # Риски на основе медицинской истории
        if 'diabetes' in profile.medical_history:
            risks['metabolic'] = 0.9
        if 'hypertension' in profile.medical_history:
            risks['cardiovascular'] = max(risks.get('cardiovascular', 0), 0.7)
        if 'heart_disease' in profile.medical_history:
            risks['cardiovascular'] = 0.9
        
        # Риски на основе образа жизни
        if profile.lifestyle_factors.get('smoking', False):
            risks['respiratory'] = 0.8
            risks['cardiovascular'] = max(risks.get('cardiovascular', 0), 0.6)
        
        if profile.lifestyle_factors.get('sedentary', False):
            risks['metabolic'] = max(risks.get('metabolic', 0), 0.5)
            risks['cardiovascular'] = max(risks.get('cardiovascular', 0), 0.4)
        
        return risks
    
    def generate_treatment_plan(self, 
                              patient_id: str,
                              diagnostic_result: DiagnosticResult) -> List[TreatmentRecommendation]:
        """
        Генерация плана лечения на основе диагностики.
        
        Args:
            patient_id: ID пациента
            diagnostic_result: Результат диагностики
            
        Returns:
            List[TreatmentRecommendation]: Рекомендации по лечению
        """
        profile = self.patient_profiles[patient_id]
        recommendations = []
        
        print(f"💊 Генерация плана лечения для пациента {patient_id}...")
        
        # Рекомендации на основе категории и уровня риска
        if diagnostic_result.category == DiagnosticCategory.CARDIOVASCULAR:
            if diagnostic_result.risk_level == RiskLevel.CRITICAL:
                recommendations.append(TreatmentRecommendation(
                    patient_id=patient_id,
                    recommendation_type="medication",
                    description="Немедленная консультация кардиолога",
                    priority=1,
                    expected_effectiveness=0.9,
                    side_effects=["Возможны побочные эффекты лекарств"],
                    contraindications=["Аллергия на сердечные препараты"],
                    monitoring_required=["ЭКГ", "АД", "Пульс"]
                ))
            elif diagnostic_result.risk_level == RiskLevel.HIGH:
                recommendations.append(TreatmentRecommendation(
                    patient_id=patient_id,
                    recommendation_type="lifestyle",
                    description="Строгая диета и физические упражнения",
                    priority=2,
                    expected_effectiveness=0.7,
                    side_effects=[],
                    contraindications=[],
                    monitoring_required=["АД", "Вес", "Холестерин"]
                ))
        
        elif diagnostic_result.category == DiagnosticCategory.METABOLIC:
            if diagnostic_result.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
                recommendations.append(TreatmentRecommendation(
                    patient_id=patient_id,
                    recommendation_type="medication",
                    description="Контроль уровня глюкозы",
                    priority=1,
                    expected_effectiveness=0.8,
                    side_effects=["Гипогликемия"],
                    contraindications=["Почечная недостаточность"],
                    monitoring_required=["Глюкоза", "HbA1c", "Функция почек"]
                ))
        
        # Персонализированные рекомендации
        if profile.age > 65:
            recommendations.append(TreatmentRecommendation(
                patient_id=patient_id,
                recommendation_type="monitoring",
                description="Усиленный мониторинг из-за возраста",
                priority=3,
                expected_effectiveness=0.6,
                side_effects=[],
                contraindications=[],
                monitoring_required=["Общий анализ крови", "Биохимия"]
            ))
        
        # Сохранение рекомендаций
        self.treatment_recommendations[patient_id].extend(recommendations)
        
        print(f"✅ Создано {len(recommendations)} рекомендаций по лечению")
        
        return recommendations
    
    def batch_analyze_patients(self, 
                             patient_data: Dict[str, MedicalTimeSeries],
                             analysis_depth: str = "standard") -> Dict[str, DiagnosticResult]:
        """
        Пакетный анализ нескольких пациентов.
        
        Args:
            patient_data: Словарь {patient_id: medical_data}
            analysis_depth: Глубина анализа
            
        Returns:
            Dict[str, DiagnosticResult]: Результаты диагностики
        """
        print(f"🔄 Пакетный анализ {len(patient_data)} пациентов...")
        
        results = {}
        
        if self.enable_parallel_processing and len(patient_data) > 1:
            # Параллельная обработка
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = {}
                
                for patient_id, medical_data in patient_data.items():
                    future = executor.submit(
                        self.analyze_patient_data, 
                        patient_id, 
                        medical_data, 
                        analysis_depth
                    )
                    futures[future] = patient_id
                
                for future in futures:
                    try:
                        patient_id = futures[future]
                        result = future.result(timeout=300)  # 5 минут таймаут
                        results[patient_id] = result
                    except Exception as e:
                        self.logger.error(f"Ошибка анализа пациента {futures[future]}: {e}")
        else:
            # Последовательная обработка
            for patient_id, medical_data in patient_data.items():
                try:
                    result = self.analyze_patient_data(patient_id, medical_data, analysis_depth)
                    results[patient_id] = result
                except Exception as e:
                    self.logger.error(f"Ошибка анализа пациента {patient_id}: {e}")
        
        print(f"✅ Пакетный анализ завершен: {len(results)} из {len(patient_data)} успешно")
        
        return results
    
    def get_patient_summary(self, patient_id: str) -> Dict[str, Any]:
        """Получить сводку по пациенту."""
        if patient_id not in self.patient_profiles:
            raise ValueError(f"Профиль пациента {patient_id} не найден")
        
        profile = self.patient_profiles[patient_id]
        diagnostics = self.diagnostic_history.get(patient_id, [])
        treatments = self.treatment_recommendations.get(patient_id, [])
        
        return {
            'patient_profile': profile,
            'total_diagnostics': len(diagnostics),
            'recent_diagnostics': diagnostics[-5:] if diagnostics else [],
            'active_treatments': [t for t in treatments if t.created_at > datetime.now() - timedelta(days=30)],
            'risk_level': diagnostics[-1].risk_level if diagnostics else RiskLevel.LOW,
            'last_analysis': diagnostics[-1].timestamp if diagnostics else None
        }
    
    def export_patient_data(self, patient_id: str, format: str = "json") -> str:
        """Экспорт данных пациента."""
        if patient_id not in self.patient_profiles:
            raise ValueError(f"Профиль пациента {patient_id} не найден")
        
        data = self.get_patient_summary(patient_id)
        
        if format == "json":
            # Конвертируем datetime в строки для JSON
            def datetime_converter(obj):
                if isinstance(obj, datetime):
                    return obj.isoformat()
                elif isinstance(obj, timedelta):
                    return str(obj)
                raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
            
            json_str = json.dumps(data, default=datetime_converter, indent=2, ensure_ascii=False)
            
            # Сохраняем в файл
            filename = f"patient_{patient_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(json_str)
            
            return filename
        
        elif format == "pickle":
            filename = f"patient_{patient_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pkl"
            with open(filename, 'wb') as f:
                pickle.dump(data, f)
            return filename
        
        else:
            raise ValueError(f"Неподдерживаемый формат: {format}")


# Пример использования
if __name__ == "__main__":
    # Создание системы
    medical_system = MedicalDiagnosticSystem()
    
    # Создание профиля пациента
    patient_profile = PatientProfile(
        patient_id="P001",
        age=65,
        gender="male",
        weight=80.0,
        height=175.0,
        medical_history=["hypertension", "diabetes"],
        current_medications=["metformin", "lisinopril"],
        allergies=["penicillin"],
        lifestyle_factors={
            "smoking": False,
            "sedentary": True,
            "alcohol": "moderate"
        }
    )
    
    # Добавление профиля
    medical_system.add_patient_profile(patient_profile)
    
    print("🏥 Медицинская диагностическая система MQEA готова к работе!")

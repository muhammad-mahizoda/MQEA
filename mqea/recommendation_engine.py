"""
Движок медицинских рекомендаций на основе анализа MQEA.

Автор: Мухаммад Махизода
Таджикский национальный университет
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
from .patient_profile import PatientProfile


class RecommendationType(Enum):
    """Типы медицинских рекомендаций."""
    URGENT = "urgent"  # Срочные
    WARNING = "warning"  # Предупреждения
    CAUTION = "caution"  # Осторожность
    MONITORING = "monitoring"  # Мониторинг
    LIFESTYLE = "lifestyle"  # Образ жизни
    MEDICATION = "medication"  # Лекарства
    FOLLOW_UP = "follow_up"  # Контроль


class RiskLevel(Enum):
    """Уровни риска."""
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class MedicalRecommendation:
    """Медицинская рекомендация."""
    type: RecommendationType
    risk_level: RiskLevel
    title: str
    description: str
    indicators: List[str]
    confidence: float
    priority: int  # 1-10, где 10 - наивысший приоритет
    action_required: str
    timeframe: str  # "immediate", "within_hours", "within_days", "within_weeks"
    medical_justification: str


class MedicalRecommendationEngine:
    """Движок медицинских рекомендаций."""
    
    def __init__(self, patient_profile: Optional[PatientProfile] = None):
        """Инициализация движка рекомендаций."""
        self.patient_profile = patient_profile
        
        # Базовые нормы (будут скорректированы на основе профиля пациента)
        self.medical_ranges = {
            'heart_rate': {'normal': (60, 100), 'warning': (50, 120), 'critical': (40, 150)},
            'blood_pressure_systolic': {'normal': (90, 140), 'warning': (80, 160), 'critical': (70, 180)},
            'blood_pressure_diastolic': {'normal': (60, 90), 'warning': (50, 100), 'critical': (40, 110)},
            'temperature': {'normal': (36.1, 37.2), 'warning': (35.5, 38.0), 'critical': (35.0, 40.0)},
            'oxygen_saturation': {'normal': (95, 100), 'warning': (90, 95), 'critical': (85, 90)},
            'respiratory_rate': {'normal': (12, 20), 'warning': (10, 25), 'critical': (8, 30)},
            'glucose': {'normal': (3.9, 5.6), 'warning': (3.0, 7.8), 'critical': (2.5, 11.1)},
            'cholesterol': {'normal': (0, 200), 'warning': (200, 240), 'critical': (240, 300)}
        }
        
        # Обновляем нормы на основе профиля пациента
        if self.patient_profile:
            self._update_ranges_for_patient()
        
        self.indicator_names = {
            'heart_rate': 'Частота пульса',
            'blood_pressure_systolic': 'Систолическое давление',
            'blood_pressure_diastolic': 'Диастолическое давление',
            'temperature': 'Температура тела',
            'oxygen_saturation': 'Насыщение кислородом',
            'respiratory_rate': 'Частота дыхания',
            'glucose': 'Уровень глюкозы',
            'cholesterol': 'Уровень холестерина'
        }
    
    def _update_ranges_for_patient(self):
        """Обновляет нормы на основе профиля пациента."""
        if not self.patient_profile:
            return
        
        for indicator in self.medical_ranges.keys():
            age_adjusted_ranges = self.patient_profile.get_age_adjusted_ranges(indicator)
            self.medical_ranges[indicator] = age_adjusted_ranges
    
    def analyze_patient_data(self, 
                           current_data: Any, 
                           analysis_results: Dict[str, Any]) -> List[MedicalRecommendation]:
        """
        Анализирует данные пациента и генерирует рекомендации.
        
        Args:
            current_data: Текущие данные пациента
            analysis_results: Результаты анализа MQEA
            
        Returns:
            Список медицинских рекомендаций
        """
        recommendations = []
        
        # Анализ индивидуальных показателей
        recommendations.extend(self._analyze_individual_indicators(current_data))
        
        # Анализ квантовой запутанности
        recommendations.extend(self._analyze_quantum_entanglement(analysis_results))
        
        # Анализ паттернов
        recommendations.extend(self._analyze_patterns(analysis_results))
        
        # Анализ трендов
        recommendations.extend(self._analyze_trends(current_data))
        
        # Персонализированные рекомендации на основе профиля
        if self.patient_profile:
            recommendations.extend(self._analyze_patient_profile())
        
        # Сортировка по приоритету
        recommendations.sort(key=lambda x: x.priority, reverse=True)
        
        return recommendations
    
    def _analyze_individual_indicators(self, current_data: Any) -> List[MedicalRecommendation]:
        """Анализирует индивидуальные показатели."""
        recommendations = []
        
        if not hasattr(current_data, 'data') or current_data.data is None:
            return recommendations
        
        # Получаем последние значения
        latest_values = current_data.data.iloc[-1] if len(current_data.data) > 0 else {}
        
        for indicator, value in latest_values.items():
            if indicator not in self.medical_ranges:
                continue
                
            ranges = self.medical_ranges[indicator]
            indicator_name = self.indicator_names.get(indicator, indicator)
            
            # Определяем уровень риска
            if value < ranges['critical'][0] or value > ranges['critical'][1]:
                # Критические значения - за пределами критического диапазона
                risk_level = RiskLevel.CRITICAL
                rec_type = RecommendationType.URGENT
                priority = 10
                timeframe = "immediate"
            elif value < ranges['warning'][0] or value > ranges['warning'][1]:
                # Предупреждающие значения - за пределами предупреждающего диапазона
                risk_level = RiskLevel.HIGH
                rec_type = RecommendationType.WARNING
                priority = 8
                timeframe = "within_hours"
            elif value < ranges['normal'][0] or value > ranges['normal'][1]:
                # Осторожность - за пределами нормального диапазона
                risk_level = RiskLevel.MODERATE
                rec_type = RecommendationType.CAUTION
                priority = 6
                timeframe = "within_days"
            else:
                # Нормальные значения
                risk_level = RiskLevel.LOW
                rec_type = RecommendationType.MONITORING
                priority = 3
                timeframe = "within_weeks"
            
            # Создаем рекомендацию
            recommendation = self._create_indicator_recommendation(
                indicator, indicator_name, value, ranges, 
                risk_level, rec_type, priority, timeframe
            )
            
            if recommendation:
                recommendations.append(recommendation)
        
        return recommendations
    
    def _create_indicator_recommendation(self, 
                                       indicator: str, 
                                       indicator_name: str, 
                                       value: float,
                                       ranges: Dict[str, tuple],
                                       risk_level: RiskLevel,
                                       rec_type: RecommendationType,
                                       priority: int,
                                       timeframe: str) -> Optional[MedicalRecommendation]:
        """Создает рекомендацию для конкретного показателя."""
        
        if indicator == 'heart_rate':
            if value < 60:
                return MedicalRecommendation(
                    type=rec_type,
                    risk_level=risk_level,
                    title=f"Брадикардия: {indicator_name} {value:.0f} уд/мин",
                    description=f"Частота пульса ниже нормы. Рекомендуется консультация кардиолога.",
                    indicators=[indicator],
                    confidence=0.9,
                    priority=priority,
                    action_required="Консультация кардиолога, ЭКГ",
                    timeframe=timeframe,
                    medical_justification=f"Норма: 60-100 уд/мин, текущее значение: {value:.0f} уд/мин"
                )
            elif value > 100:
                return MedicalRecommendation(
                    type=rec_type,
                    risk_level=risk_level,
                    title=f"Тахикардия: {indicator_name} {value:.0f} уд/мин",
                    description=f"Частота пульса выше нормы. Возможны стресс, обезвоживание или сердечные проблемы.",
                    indicators=[indicator],
                    confidence=0.9,
                    priority=priority,
                    action_required="Консультация кардиолога, анализ причин",
                    timeframe=timeframe,
                    medical_justification=f"Норма: 60-100 уд/мин, текущее значение: {value:.0f} уд/мин"
                )
        
        elif indicator == 'blood_pressure_systolic':
            if value < 90:
                return MedicalRecommendation(
                    type=rec_type,
                    risk_level=risk_level,
                    title=f"Гипотония: Систолическое давление {value:.0f} мм рт.ст.",
                    description=f"Систолическое давление ниже нормы. Возможны головокружения, слабость.",
                    indicators=[indicator],
                    confidence=0.9,
                    priority=priority,
                    action_required="Консультация терапевта, контроль давления",
                    timeframe=timeframe,
                    medical_justification=f"Норма: 90-140 мм рт.ст., текущее значение: {value:.0f} мм рт.ст."
                )
            elif value > 140:
                return MedicalRecommendation(
                    type=rec_type,
                    risk_level=risk_level,
                    title=f"Гипертония: Систолическое давление {value:.0f} мм рт.ст.",
                    description=f"Систолическое давление выше нормы. Требуется контроль и возможное лечение.",
                    indicators=[indicator],
                    confidence=0.9,
                    priority=priority,
                    action_required="Консультация кардиолога, антигипертензивная терапия",
                    timeframe=timeframe,
                    medical_justification=f"Норма: 90-140 мм рт.ст., текущее значение: {value:.0f} мм рт.ст."
                )
        
        elif indicator == 'temperature':
            if value < 36.1:
                return MedicalRecommendation(
                    type=rec_type,
                    risk_level=risk_level,
                    title=f"Гипотермия: Температура {value:.1f}°C",
                    description=f"Температура тела ниже нормы. Возможны нарушения терморегуляции.",
                    indicators=[indicator],
                    confidence=0.9,
                    priority=priority,
                    action_required="Консультация терапевта, контроль температуры",
                    timeframe=timeframe,
                    medical_justification=f"Норма: 36.1-37.2°C, текущее значение: {value:.1f}°C"
                )
            elif value > 37.2:
                return MedicalRecommendation(
                    type=rec_type,
                    risk_level=risk_level,
                    title=f"Гипертермия: Температура {value:.1f}°C",
                    description=f"Температура тела выше нормы. Возможен воспалительный процесс.",
                    indicators=[indicator],
                    confidence=0.9,
                    priority=priority,
                    action_required="Консультация терапевта, анализ причин лихорадки",
                    timeframe=timeframe,
                    medical_justification=f"Норма: 36.1-37.2°C, текущее значение: {value:.1f}°C"
                )
        
        elif indicator == 'oxygen_saturation':
            if value < 95:
                return MedicalRecommendation(
                    type=rec_type,
                    risk_level=risk_level,
                    title=f"Гипоксемия: Насыщение кислородом {value:.0f}%",
                    description=f"Насыщение кислородом ниже нормы. Возможны проблемы с дыханием.",
                    indicators=[indicator],
                    confidence=0.9,
                    priority=priority,
                    action_required="Консультация пульмонолога, оксигенотерапия",
                    timeframe=timeframe,
                    medical_justification=f"Норма: 95-100%, текущее значение: {value:.0f}%"
                )
        
        elif indicator == 'glucose':
            if value < 3.9:
                return MedicalRecommendation(
                    type=rec_type,
                    risk_level=risk_level,
                    title=f"Гипогликемия: Глюкоза {value:.1f} ммоль/л",
                    description=f"Уровень глюкозы ниже нормы. Возможны головокружения, слабость.",
                    indicators=[indicator],
                    confidence=0.9,
                    priority=priority,
                    action_required="Консультация эндокринолога, контроль глюкозы",
                    timeframe=timeframe,
                    medical_justification=f"Норма: 3.9-5.6 ммоль/л, текущее значение: {value:.1f} ммоль/л"
                )
            elif value > 5.6:
                return MedicalRecommendation(
                    type=rec_type,
                    risk_level=risk_level,
                    title=f"Гипергликемия: Глюкоза {value:.1f} ммоль/л",
                    description=f"Уровень глюкозы выше нормы. Возможен преддиабет или диабет.",
                    indicators=[indicator],
                    confidence=0.9,
                    priority=priority,
                    action_required="Консультация эндокринолога, глюкозотолерантный тест",
                    timeframe=timeframe,
                    medical_justification=f"Норма: 3.9-5.6 ммоль/л, текущее значение: {value:.1f} ммоль/л"
                )
        
        elif indicator == 'cholesterol':
            if value > 200:
                return MedicalRecommendation(
                    type=rec_type,
                    risk_level=risk_level,
                    title=f"Гиперхолестеринемия: Холестерин {value:.0f} мг/дл",
                    description=f"Уровень холестерина выше нормы. Повышен риск сердечно-сосудистых заболеваний.",
                    indicators=[indicator],
                    confidence=0.9,
                    priority=priority,
                    action_required="Консультация кардиолога, диета, статины",
                    timeframe=timeframe,
                    medical_justification=f"Норма: <200 мг/дл, текущее значение: {value:.0f} мг/дл"
                )
        
        return None
    
    def _analyze_quantum_entanglement(self, analysis_results: Dict[str, Any]) -> List[MedicalRecommendation]:
        """Анализирует квантовую запутанность для рекомендаций."""
        recommendations = []
        
        if 'quantum_entanglements' not in analysis_results:
            return recommendations
        
        entanglements = analysis_results['quantum_entanglements']
        if not entanglements:
            return recommendations
        
        # Анализируем последнее окно запутанности
        latest_entanglement = entanglements[-1]
        if isinstance(latest_entanglement, dict) and 'entanglement_matrix' in latest_entanglement:
            matrix = latest_entanglement['entanglement_matrix']
            
            # Находим сильные корреляции
            strong_correlations = []
            for i in range(len(matrix)):
                for j in range(i+1, len(matrix)):
                    if matrix[i][j] > 0.7:  # Высокая корреляция
                        strong_correlations.append((i, j, matrix[i][j]))
            
            if strong_correlations:
                # Создаем рекомендацию о сильных корреляциях
                indicators = analysis_results.get('indicators', [])
                if indicators:
                    correlated_pairs = []
                    for i, j, strength in strong_correlations[:3]:  # Топ-3 корреляции
                        if i < len(indicators) and j < len(indicators):
                            pair = f"{self.indicator_names.get(indicators[i], indicators[i])} ↔ {self.indicator_names.get(indicators[j], indicators[j])}"
                            correlated_pairs.append(pair)
                    
                    if correlated_pairs:
                        recommendation = MedicalRecommendation(
                            type=RecommendationType.MONITORING,
                            risk_level=RiskLevel.MODERATE,
                            title="Обнаружены сильные корреляции между показателями",
                            description=f"Найдены тесные связи между медицинскими показателями: {', '.join(correlated_pairs)}. Это может указывать на системные изменения в организме.",
                            indicators=[indicators[i] for i, j, _ in strong_correlations[:3] if i < len(indicators)],
                            confidence=0.8,
                            priority=5,
                            action_required="Мониторинг связанных показателей, консультация специалиста",
                            timeframe="within_days",
                            medical_justification=f"Квантовая запутанность показывает сильные корреляции (сила > 0.7) между показателями"
                        )
                        recommendations.append(recommendation)
        
        return recommendations
    
    def _analyze_patterns(self, analysis_results: Dict[str, Any]) -> List[MedicalRecommendation]:
        """Анализирует паттерны для рекомендаций."""
        recommendations = []
        
        # Здесь можно добавить анализ паттернов из analysis_results
        # Пока что возвращаем пустой список
        return recommendations
    
    def _analyze_trends(self, current_data: Any) -> List[MedicalRecommendation]:
        """Анализирует тренды для рекомендаций."""
        recommendations = []
        
        if not hasattr(current_data, 'data') or current_data.data is None:
            return recommendations
        
        # Анализируем тренды за последние 6 часов
        if len(current_data.data) < 2:
            return recommendations
        
        # Берем последние 24 точки (6 часов при интервале 15 минут)
        recent_data = current_data.data.tail(24)
        
        for indicator in current_data.indicators:
            if indicator not in recent_data.columns:
                continue
            
            values = recent_data[indicator].dropna()
            if len(values) < 3:
                continue
            
            # Вычисляем тренд
            x = np.arange(len(values))
            y = values.values
            trend = np.polyfit(x, y, 1)[0]  # Наклон линии тренда
            
            indicator_name = self.indicator_names.get(indicator, indicator)
            
            # Определяем направление тренда
            if abs(trend) < 0.1:  # Стабильный
                continue
            elif trend > 0.1:  # Растущий
                trend_direction = "растущий"
                risk_level = RiskLevel.MODERATE
                priority = 6
            else:  # Убывающий
                trend_direction = "убывающий"
                risk_level = RiskLevel.MODERATE
                priority = 6
            
            # Создаем рекомендацию о тренде
            recommendation = MedicalRecommendation(
                type=RecommendationType.MONITORING,
                risk_level=risk_level,
                title=f"{trend_direction.title()} тренд: {indicator_name}",
                description=f"Обнаружен {trend_direction} тренд в показателе {indicator_name}. Рекомендуется усиленный мониторинг.",
                indicators=[indicator],
                confidence=0.7,
                priority=priority,
                action_required="Усиленный мониторинг показателя",
                timeframe="within_days",
                medical_justification=f"Тренд показывает {trend_direction} изменение показателя за последние 6 часов"
            )
            recommendations.append(recommendation)
        
        return recommendations
    
    def _analyze_patient_profile(self) -> List[MedicalRecommendation]:
        """Анализирует профиль пациента для персонализированных рекомендаций."""
        recommendations = []
        
        if not self.patient_profile:
            return recommendations
        
        # Рекомендации на основе возраста
        age = self.patient_profile.age
        if age >= 65:
            recommendations.append(MedicalRecommendation(
                type=RecommendationType.MONITORING,
                risk_level=RiskLevel.MODERATE,
                title=f"Пожилой возраст: {age} лет",
                description=f"Пациент в возрасте {age} лет требует особого внимания к здоровью.",
                indicators=[],
                confidence=1.0,
                priority=5,
                action_required="Регулярные медицинские осмотры каждые 6 месяцев",
                timeframe="within_weeks",
                medical_justification=f"Возраст {age} лет является фактором риска для многих заболеваний"
            ))
        elif age < 18:
            recommendations.append(MedicalRecommendation(
                type=RecommendationType.MONITORING,
                risk_level=RiskLevel.LOW,
                title=f"Детский возраст: {age} лет",
                description=f"Пациент в возрасте {age} лет требует педиатрического наблюдения.",
                indicators=[],
                confidence=1.0,
                priority=4,
                action_required="Регулярные педиатрические осмотры",
                timeframe="within_weeks",
                medical_justification=f"Возраст {age} лет требует специального подхода к медицинскому наблюдению"
            ))
        
        # Рекомендации на основе BMI
        bmi = self.patient_profile.bmi
        bmi_category = self.patient_profile.bmi_category
        if bmi >= 30:
            recommendations.append(MedicalRecommendation(
                type=RecommendationType.WARNING,
                risk_level=RiskLevel.HIGH,
                title=f"Ожирение: BMI {bmi:.1f}",
                description=f"Индекс массы тела {bmi:.1f} указывает на ожирение. Требуется снижение веса.",
                indicators=[],
                confidence=1.0,
                priority=8,
                action_required="Консультация диетолога, программа снижения веса",
                timeframe="within_days",
                medical_justification=f"BMI {bmi:.1f} значительно превышает норму (18.5-24.9)"
            ))
        elif bmi >= 25:
            recommendations.append(MedicalRecommendation(
                type=RecommendationType.CAUTION,
                risk_level=RiskLevel.MODERATE,
                title=f"Избыточный вес: BMI {bmi:.1f}",
                description=f"Индекс массы тела {bmi:.1f} указывает на избыточный вес.",
                indicators=[],
                confidence=1.0,
                priority=6,
                action_required="Контроль питания, увеличение физической активности",
                timeframe="within_weeks",
                medical_justification=f"BMI {bmi:.1f} превышает норму (18.5-24.9)"
            ))
        elif bmi < 18.5:
            recommendations.append(MedicalRecommendation(
                type=RecommendationType.CAUTION,
                risk_level=RiskLevel.MODERATE,
                title=f"Недостаточный вес: BMI {bmi:.1f}",
                description=f"Индекс массы тела {bmi:.1f} указывает на недостаточный вес.",
                indicators=[],
                confidence=1.0,
                priority=6,
                action_required="Консультация диетолога, проверка на возможные заболевания",
                timeframe="within_weeks",
                medical_justification=f"BMI {bmi:.1f} ниже нормы (18.5-24.9)"
            ))
        
        # Рекомендации на основе медицинской истории
        for condition in self.patient_profile.medical_history:
            if condition.value != "none":
                recommendations.append(MedicalRecommendation(
                    type=RecommendationType.MONITORING,
                    risk_level=RiskLevel.MODERATE,
                    title=f"Медицинская история: {condition.value}",
                    description=f"Пациент имеет в анамнезе {condition.value}. Требуется регулярный мониторинг.",
                    indicators=[],
                    confidence=1.0,
                    priority=5,
                    action_required="Регулярные консультации специалиста",
                    timeframe="within_weeks",
                    medical_justification=f"Наличие {condition.value} в медицинской истории требует особого внимания"
                ))
        
        # Рекомендации на основе образа жизни
        if self.patient_profile.smoking:
            recommendations.append(MedicalRecommendation(
                type=RecommendationType.URGENT,
                risk_level=RiskLevel.CRITICAL,
                title="Курение - критический фактор риска",
                description="Курение значительно повышает риск сердечно-сосудистых и онкологических заболеваний.",
                indicators=[],
                confidence=1.0,
                priority=10,
                action_required="Немедленный отказ от курения, консультация специалиста",
                timeframe="immediate",
                medical_justification="Курение является одним из основных факторов риска для здоровья"
            ))
        
        if self.patient_profile.activity_level.value == "sedentary":
            recommendations.append(MedicalRecommendation(
                type=RecommendationType.CAUTION,
                risk_level=RiskLevel.MODERATE,
                title="Малоподвижный образ жизни",
                description="Недостаточная физическая активность повышает риск многих заболеваний.",
                indicators=[],
                confidence=1.0,
                priority=6,
                action_required="Увеличение физической активности, консультация тренера",
                timeframe="within_weeks",
                medical_justification="Регулярная физическая активность необходима для поддержания здоровья"
            ))
        
        return recommendations
    
    def generate_summary_report(self, recommendations: List[MedicalRecommendation]) -> str:
        """Генерирует сводный отчет по рекомендациям."""
        if not recommendations:
            return "✅ Все показатели в пределах нормы. Рекомендуется регулярный мониторинг."
        
        # Группируем по типам
        urgent = [r for r in recommendations if r.type == RecommendationType.URGENT]
        warnings = [r for r in recommendations if r.type == RecommendationType.WARNING]
        cautions = [r for r in recommendations if r.type == RecommendationType.CAUTION]
        monitoring = [r for r in recommendations if r.type == RecommendationType.MONITORING]
        
        report = "📋 **МЕДИЦИНСКИЕ РЕКОМЕНДАЦИИ**\n\n"
        
        if urgent:
            report += "🚨 **СРОЧНЫЕ РЕКОМЕНДАЦИИ:**\n"
            for rec in urgent:
                report += f"• {rec.title}\n"
                report += f"  {rec.description}\n"
                report += f"  Действие: {rec.action_required}\n\n"
        
        if warnings:
            report += "⚠️ **ПРЕДУПРЕЖДЕНИЯ:**\n"
            for rec in warnings:
                report += f"• {rec.title}\n"
                report += f"  {rec.description}\n"
                report += f"  Действие: {rec.action_required}\n\n"
        
        if cautions:
            report += "🔶 **ОСТОРОЖНОСТЬ:**\n"
            for rec in cautions:
                report += f"• {rec.title}\n"
                report += f"  {rec.description}\n"
                report += f"  Действие: {rec.action_required}\n\n"
        
        if monitoring:
            report += "👁️ **МОНИТОРИНГ:**\n"
            for rec in monitoring:
                report += f"• {rec.title}\n"
                report += f"  {rec.description}\n"
                report += f"  Действие: {rec.action_required}\n\n"
        
        return report

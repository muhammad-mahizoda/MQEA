"""
Модуль для генерации важных вопросов для медицинского анализа.

Автор: Мухаммад Махизода
Таджикский национальный университет
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
import random
from dataclasses import dataclass

from .data_processor import MedicalTimeSeries


@dataclass
class MedicalQuestion:
    """Класс для представления медицинского вопроса."""
    question: str
    question_type: str
    priority: int  # 1-5, где 5 - высший приоритет
    indicators: List[str]
    time_range: Optional[Tuple[datetime, datetime]] = None
    expected_insights: List[str] = None
    analysis_method: str = "quantum_entanglement"


class QuestionGenerator:
    """Генератор важных вопросов для медицинского анализа."""
    
    def __init__(self):
        self.question_templates = {
            'correlation': [
                "Какие медицинские показатели показывают сильную корреляцию в период {time_range}?",
                "Есть ли скрытые связи между {indicators} в течение последних {hours} часов?",
                "Какие показатели демонстрируют квантовую запутанность в {time_range}?"
            ],
            'anomaly': [
                "Обнаружены ли аномальные значения в {indicators} за последние {hours} часов?",
                "Есть ли подозрительные паттерны в данных за {time_range}?",
                "Какие показатели выходят за нормальные пределы в период {time_range}?"
            ],
            'trend': [
                "Какие тренды наблюдаются в {indicators} за последние {hours} часов?",
                "Есть ли признаки ухудшения состояния по показателям {indicators}?",
                "Какие показатели показывают улучшение в {time_range}?"
            ],
            'prediction': [
                "Можно ли предсказать изменения в {indicators} на основе текущих данных?",
                "Какие показатели могут ухудшиться в ближайшие {hours} часов?",
                "Есть ли ранние признаки проблем в {indicators}?"
            ],
            'treatment': [
                "Какие показатели требуют немедленного внимания?",
                "Есть ли признаки эффективности лечения по {indicators}?",
                "Какие показатели стабилизировались после вмешательства?"
            ]
        }
        
        self.insight_templates = {
            'correlation': [
                "Обнаружена сильная квантовая запутанность между показателями",
                "Показатели демонстрируют синхронные изменения",
                "Выявлена скрытая корреляция, невидимая в классическом анализе"
            ],
            'anomaly': [
                "Обнаружены аномальные значения, требующие внимания",
                "Показатели выходят за нормальные пределы",
                "Выявлены подозрительные паттерны в данных"
            ],
            'trend': [
                "Наблюдается устойчивый тренд изменения показателей",
                "Показатели демонстрируют улучшение/ухудшение",
                "Выявлены циклические изменения в данных"
            ],
            'prediction': [
                "Данные позволяют предсказать будущие изменения",
                "Обнаружены ранние признаки проблем",
                "Показатели демонстрируют предсказуемые паттерны"
            ],
            'treatment': [
                "Показатели требуют медицинского вмешательства",
                "Наблюдается положительная динамика лечения",
                "Необходимо скорректировать план лечения"
            ]
        }
    
    def generate_questions(self, 
                          time_series: MedicalTimeSeries,
                          analysis_results: Optional[Dict] = None,
                          max_questions: int = 10) -> List[MedicalQuestion]:
        """Генерирует важные вопросы на основе данных и результатов анализа."""
        
        questions = []
        
        # Анализ данных для определения приоритетов
        data_analysis = self._analyze_data_patterns(time_series)
        
        # Генерация вопросов по типам
        question_types = ['correlation', 'anomaly', 'trend', 'prediction', 'treatment']
        
        for question_type in question_types:
            type_questions = self._generate_questions_by_type(
                time_series, question_type, data_analysis, analysis_results
            )
            questions.extend(type_questions)
        
        # Сортировка по приоритету и ограничение количества
        questions.sort(key=lambda x: x.priority, reverse=True)
        return questions[:max_questions]
    
    def _analyze_data_patterns(self, time_series: MedicalTimeSeries) -> Dict[str, Any]:
        """Анализирует паттерны в данных для определения приоритетов."""
        
        analysis = {
            'missing_data_percentage': time_series.missing_data_mask.sum().sum() / 
                                    (len(time_series.indicators) * len(time_series.timestamps)) * 100,
            'data_quality': 'good',
            'anomaly_indicators': [],
            'trend_indicators': [],
            'correlation_indicators': [],
            'critical_indicators': []
        }
        
        # Анализ качества данных
        if analysis['missing_data_percentage'] > 20:
            analysis['data_quality'] = 'poor'
        elif analysis['missing_data_percentage'] > 10:
            analysis['data_quality'] = 'fair'
        
        # Анализ аномалий
        for indicator in time_series.indicators:
            data = time_series.data[indicator].dropna()
            if len(data) > 0:
                # Проверка на аномальные значения
                q1, q3 = data.quantile([0.25, 0.75])
                iqr = q3 - q1
                lower_bound = q1 - 1.5 * iqr
                upper_bound = q3 + 1.5 * iqr
                
                anomalies = data[(data < lower_bound) | (data > upper_bound)]
                if len(anomalies) > len(data) * 0.05:  # Более 5% аномалий
                    analysis['anomaly_indicators'].append(indicator)
                
                # Анализ трендов
                if len(data) > 10:
                    correlation = data.corr(pd.Series(range(len(data))))
                    if abs(correlation) > 0.3:
                        analysis['trend_indicators'].append(indicator)
        
        # Определение критических показателей
        critical_indicators = ['heart_rate', 'blood_pressure_systolic', 'oxygen_saturation']
        analysis['critical_indicators'] = [ind for ind in critical_indicators 
                                         if ind in time_series.indicators]
        
        return analysis
    
    def _generate_questions_by_type(self, 
                                   time_series: MedicalTimeSeries,
                                   question_type: str,
                                   data_analysis: Dict,
                                   analysis_results: Optional[Dict]) -> List[MedicalQuestion]:
        """Генерирует вопросы определенного типа."""
        
        questions = []
        
        if question_type == 'correlation':
            questions.extend(self._generate_correlation_questions(time_series, data_analysis, analysis_results))
        elif question_type == 'anomaly':
            questions.extend(self._generate_anomaly_questions(time_series, data_analysis))
        elif question_type == 'trend':
            questions.extend(self._generate_trend_questions(time_series, data_analysis))
        elif question_type == 'prediction':
            questions.extend(self._generate_prediction_questions(time_series, data_analysis))
        elif question_type == 'treatment':
            questions.extend(self._generate_treatment_questions(time_series, data_analysis))
        
        return questions
    
    def _generate_correlation_questions(self, 
                                       time_series: MedicalTimeSeries,
                                       data_analysis: Dict,
                                       analysis_results: Optional[Dict]) -> List[MedicalQuestion]:
        """Генерирует вопросы о корреляциях."""
        
        questions = []
        
        # Вопросы о квантовой запутанности
        if analysis_results and 'quantum_entanglements' in analysis_results:
            entanglements = analysis_results['quantum_entanglements']
            if entanglements:
                latest_entanglement = entanglements[-1]
                if isinstance(latest_entanglement, dict) and 'entangled_pairs' in latest_entanglement:
                    pairs = latest_entanglement['entangled_pairs']
                    if pairs:
                        indicators = list(set([pair[0] for pair in pairs] + [pair[1] for pair in pairs]))
                        
                        question = MedicalQuestion(
                            question=f"Какие медицинские показатели показывают квантовую запутанность?",
                            question_type="correlation",
                            priority=5,
                            indicators=indicators,
                            expected_insights=self.insight_templates['correlation'],
                            analysis_method="quantum_entanglement"
                        )
                        questions.append(question)
        
        # Вопросы о скрытых связях
        if len(time_series.indicators) >= 2:
            indicators = random.sample(time_series.indicators, min(3, len(time_series.indicators)))
            
            question = MedicalQuestion(
                question=f"Есть ли скрытые связи между {', '.join(indicators)}?",
                question_type="correlation",
                priority=4,
                indicators=indicators,
                expected_insights=self.insight_templates['correlation'],
                analysis_method="quantum_entanglement"
            )
            questions.append(question)
        
        return questions
    
    def _generate_anomaly_questions(self, 
                                   time_series: MedicalTimeSeries,
                                   data_analysis: Dict) -> List[MedicalQuestion]:
        """Генерирует вопросы об аномалиях."""
        
        questions = []
        
        # Вопросы об аномальных показателях
        if data_analysis['anomaly_indicators']:
            indicators = data_analysis['anomaly_indicators']
            
            question = MedicalQuestion(
                question=f"Обнаружены ли аномальные значения в {', '.join(indicators)}?",
                question_type="anomaly",
                priority=5,
                indicators=indicators,
                expected_insights=self.insight_templates['anomaly'],
                analysis_method="anomaly_detection"
            )
            questions.append(question)
        
        # Вопросы о качестве данных
        if data_analysis['data_quality'] == 'poor':
            question = MedicalQuestion(
                question="Качество данных низкое. Какие показатели требуют дополнительного внимания?",
                question_type="anomaly",
                priority=4,
                indicators=time_series.indicators,
                expected_insights=["Необходимо улучшить качество данных", "Требуется дополнительная проверка"],
                analysis_method="data_quality"
            )
            questions.append(question)
        
        return questions
    
    def _generate_trend_questions(self, 
                                 time_series: MedicalTimeSeries,
                                 data_analysis: Dict) -> List[MedicalQuestion]:
        """Генерирует вопросы о трендах."""
        
        questions = []
        
        # Вопросы о трендовых показателях
        if data_analysis['trend_indicators']:
            indicators = data_analysis['trend_indicators']
            
            question = MedicalQuestion(
                question=f"Какие тренды наблюдаются в {', '.join(indicators)}?",
                question_type="trend",
                priority=3,
                indicators=indicators,
                expected_insights=self.insight_templates['trend'],
                analysis_method="trend_analysis"
            )
            questions.append(question)
        
        # Вопросы о критических показателях
        if data_analysis['critical_indicators']:
            indicators = data_analysis['critical_indicators']
            
            question = MedicalQuestion(
                question=f"Есть ли признаки ухудшения в критических показателях {', '.join(indicators)}?",
                question_type="trend",
                priority=5,
                indicators=indicators,
                expected_insights=self.insight_templates['trend'],
                analysis_method="critical_analysis"
            )
            questions.append(question)
        
        return questions
    
    def _generate_prediction_questions(self, 
                                      time_series: MedicalTimeSeries,
                                      data_analysis: Dict) -> List[MedicalQuestion]:
        """Генерирует вопросы о предсказаниях."""
        
        questions = []
        
        # Вопросы о предсказании для критических показателей
        if data_analysis['critical_indicators']:
            indicators = data_analysis['critical_indicators']
            
            question = MedicalQuestion(
                question=f"Можно ли предсказать изменения в критических показателях {', '.join(indicators)}?",
                question_type="prediction",
                priority=4,
                indicators=indicators,
                expected_insights=self.insight_templates['prediction'],
                analysis_method="quantum_prediction"
            )
            questions.append(question)
        
        # Общие вопросы о предсказании
        if len(time_series.indicators) >= 2:
            indicators = random.sample(time_series.indicators, min(3, len(time_series.indicators)))
            
            question = MedicalQuestion(
                question=f"Какие показатели могут измениться в ближайшие часы?",
                question_type="prediction",
                priority=3,
                indicators=indicators,
                expected_insights=self.insight_templates['prediction'],
                analysis_method="quantum_prediction"
            )
            questions.append(question)
        
        return questions
    
    def _generate_treatment_questions(self, 
                                     time_series: MedicalTimeSeries,
                                     data_analysis: Dict) -> List[MedicalQuestion]:
        """Генерирует вопросы о лечении."""
        
        questions = []
        
        # Вопросы о критических показателях
        if data_analysis['critical_indicators']:
            indicators = data_analysis['critical_indicators']
            
            question = MedicalQuestion(
                question=f"Какие из критических показателей {', '.join(indicators)} требуют немедленного внимания?",
                question_type="treatment",
                priority=5,
                indicators=indicators,
                expected_insights=self.insight_templates['treatment'],
                analysis_method="critical_assessment"
            )
            questions.append(question)
        
        # Вопросы об эффективности лечения
        question = MedicalQuestion(
            question="Есть ли признаки эффективности текущего лечения?",
            question_type="treatment",
            priority=4,
            indicators=time_series.indicators,
            expected_insights=self.insight_templates['treatment'],
            analysis_method="treatment_effectiveness"
        )
        questions.append(question)
        
        return questions
    
    def get_question_insights(self, 
                             question: MedicalQuestion,
                             analysis_results: Dict) -> List[str]:
        """Генерирует инсайты для конкретного вопроса."""
        
        insights = []
        
        if question.analysis_method == "quantum_entanglement":
            if 'quantum_entanglements' in analysis_results:
                entanglements = analysis_results['quantum_entanglements']
                if entanglements:
                    insights.append(f"Обнаружено {len(entanglements)} окон квантовой запутанности")
                    
                    # Анализ силы запутанности
                    if 'quantum_signatures' in analysis_results:
                        coherence = analysis_results['quantum_signatures'].get('quantum_coherence', 0)
                        insights.append(f"Квантовая когерентность: {coherence:.3f}")
        
        elif question.analysis_method == "anomaly_detection":
            insights.extend(question.expected_insights or [])
        
        elif question.analysis_method == "trend_analysis":
            insights.extend(question.expected_insights or [])
        
        elif question.analysis_method == "quantum_prediction":
            insights.extend(question.expected_insights or [])
        
        elif question.analysis_method == "critical_assessment":
            insights.extend(question.expected_insights or [])
        
        elif question.analysis_method == "treatment_effectiveness":
            insights.extend(question.expected_insights or [])
        
        return insights

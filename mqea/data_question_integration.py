"""
Интегрированный модуль для работы с данными и генерации вопросов.

Автор: Мухаммад Махизода
Таджикский национальный университет
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
import json
import os
from pathlib import Path

from .data_sources import DataSourceManager, create_default_sources
from .question_generator import QuestionGenerator, MedicalQuestion
from .data_processor import MedicalTimeSeries
from .core import MQEAAnalyzer


class MedicalDataQuestionSystem:
    """Интегрированная система для работы с медицинскими данными и генерации вопросов."""
    
    def __init__(self):
        self.data_manager = create_default_sources()
        self.question_generator = QuestionGenerator()
        self.mqea_analyzer = MQEAAnalyzer()
        
        # Установка синтетического источника по умолчанию
        self.data_manager.set_current_source("synthetic")
        
        self.current_data: Optional[MedicalTimeSeries] = None
        self.current_questions: List[MedicalQuestion] = []
        self.analysis_results: Dict[str, Any] = {}
    
    def load_data(self, 
                  source_name: str = "synthetic",
                  **kwargs) -> MedicalTimeSeries:
        """Загружает данные из указанного источника."""
        
        self.data_manager.set_current_source(source_name)
        self.current_data = self.data_manager.get_data(**kwargs)
        
        print(f"✅ Данные загружены из источника: {source_name}")
        print(f"   - Показателей: {len(self.current_data.indicators)}")
        print(f"   - Точек данных: {len(self.current_data.timestamps)}")
        print(f"   - Пропущенных данных: {self.current_data.missing_data_mask.sum().sum()}")
        
        return self.current_data
    
    def generate_questions(self, 
                          max_questions: int = 10,
                          question_types: Optional[List[str]] = None) -> List[MedicalQuestion]:
        """Генерирует важные вопросы на основе текущих данных."""
        
        if self.current_data is None:
            raise ValueError("Сначала загрузите данные")
        
        # Фильтрация типов вопросов
        if question_types:
            original_templates = self.question_generator.question_templates
            filtered_templates = {k: v for k, v in original_templates.items() if k in question_types}
            self.question_generator.question_templates = filtered_templates
        
        self.current_questions = self.question_generator.generate_questions(
            self.current_data, 
            self.analysis_results, 
            max_questions
        )
        
        print(f"✅ Сгенерировано {len(self.current_questions)} важных вопросов")
        
        return self.current_questions
    
    def analyze_data(self, 
                    quantum_threshold: float = 0.3,
                    fill_missing: bool = True) -> Dict[str, Any]:
        """Выполняет полный анализ данных с помощью MQEA."""
        
        if self.current_data is None:
            raise ValueError("Сначала загрузите данные")
        
        print("🔬 Начинаем квантовый анализ данных...")
        
        # Заполнение пропущенных данных
        if fill_missing and self.current_data.missing_data_mask.sum().sum() > 0:
            print("📊 Заполняем пропущенные данные...")
            filled_data = self.mqea_analyzer.fill_missing_data(
                self.current_data, 
                method='quantum'
            )
            self.current_data = filled_data
        
        # Квантовый анализ запутанности
        print("⚛️ Анализируем квантовую запутанность...")
        self.analysis_results = self.mqea_analyzer.quantum_entanglement_analysis(
            self.current_data, 
            quantum_threshold
        )
        
        # Обнаружение паттернов
        print("🔍 Обнаруживаем паттерны...")
        patterns = self.mqea_analyzer.detect_patterns(self.current_data)
        self.analysis_results['patterns'] = patterns
        
        print("✅ Анализ завершен!")
        print(f"   - Квантовая когерентность: {self.analysis_results.get('quantum_signatures', {}).get('quantum_coherence', 0):.3f}")
        print(f"   - Обнаружено паттернов: {len(patterns)}")
        
        return self.analysis_results
    
    def answer_questions(self) -> Dict[str, Any]:
        """Отвечает на сгенерированные вопросы."""
        
        if not self.current_questions:
            raise ValueError("Сначала сгенерируйте вопросы")
        
        if not self.analysis_results:
            raise ValueError("Сначала выполните анализ данных")
        
        answers = {}
        
        for i, question in enumerate(self.current_questions):
            print(f"❓ Вопрос {i+1}: {question.question}")
            
            # Генерация ответа
            answer = self._generate_answer(question)
            answers[f"question_{i+1}"] = {
                'question': question.question,
                'question_type': question.question_type,
                'priority': question.priority,
                'indicators': question.indicators,
                'answer': answer,
                'insights': self.question_generator.get_question_insights(question, self.analysis_results)
            }
            
            print(f"✅ Ответ: {answer}")
            print()
        
        return answers
    
    def _generate_answer(self, question: MedicalQuestion) -> str:
        """Генерирует ответ на конкретный вопрос."""
        
        if question.analysis_method == "quantum_entanglement":
            return self._answer_quantum_entanglement_question(question)
        elif question.analysis_method == "anomaly_detection":
            return self._answer_anomaly_question(question)
        elif question.analysis_method == "trend_analysis":
            return self._answer_trend_question(question)
        elif question.analysis_method == "quantum_prediction":
            return self._answer_prediction_question(question)
        elif question.analysis_method == "critical_assessment":
            return self._answer_critical_question(question)
        elif question.analysis_method == "treatment_effectiveness":
            return self._answer_treatment_question(question)
        else:
            return "Анализ не выполнен для данного типа вопроса."
    
    def _answer_quantum_entanglement_question(self, question: MedicalQuestion) -> str:
        """Отвечает на вопросы о квантовой запутанности."""
        
        if 'quantum_entanglements' not in self.analysis_results:
            return "Данные о квантовой запутанности недоступны."
        
        entanglements = self.analysis_results['quantum_entanglements']
        if not entanglements:
            return "Квантовая запутанность не обнаружена."
        
        # Анализ запутанных пар
        entangled_pairs = []
        for window in entanglements:
            if isinstance(window, dict) and 'entangled_pairs' in window:
                entangled_pairs.extend(window['entangled_pairs'])
        
        if not entangled_pairs:
            return "Запутанные пары не найдены."
        
        # Подсчет запутанности по показателям
        indicator_entanglement = {}
        for pair in entangled_pairs:
            for indicator in pair:
                indicator_entanglement[indicator] = indicator_entanglement.get(indicator, 0) + 1
        
        # Сортировка по количеству запутанностей
        sorted_indicators = sorted(indicator_entanglement.items(), key=lambda x: x[1], reverse=True)
        
        answer = f"Обнаружена квантовая запутанность между показателями. "
        answer += f"Наиболее запутанные показатели: {', '.join([ind[0] for ind in sorted_indicators[:3]])}. "
        
        # Добавление информации о когерентности
        if 'quantum_signatures' in self.analysis_results:
            coherence = self.analysis_results['quantum_signatures'].get('quantum_coherence', 0)
            answer += f"Квантовая когерентность: {coherence:.3f}."
        
        return answer
    
    def _answer_anomaly_question(self, question: MedicalQuestion) -> str:
        """Отвечает на вопросы об аномалиях."""
        
        if not question.indicators:
            return "Показатели для анализа не указаны."
        
        anomalies_found = []
        
        for indicator in question.indicators:
            if indicator in self.current_data.indicators:
                data = self.current_data.data[indicator].dropna()
                if len(data) > 0:
                    # Проверка на аномальные значения
                    q1, q3 = data.quantile([0.25, 0.75])
                    iqr = q3 - q1
                    lower_bound = q1 - 1.5 * iqr
                    upper_bound = q3 + 1.5 * iqr
                    
                    anomalies = data[(data < lower_bound) | (data > upper_bound)]
                    if len(anomalies) > 0:
                        anomalies_found.append(f"{indicator}: {len(anomalies)} аномалий")
        
        if anomalies_found:
            return f"Обнаружены аномалии: {', '.join(anomalies_found)}."
        else:
            return "Аномалии не обнаружены."
    
    def _answer_trend_question(self, question: MedicalQuestion) -> str:
        """Отвечает на вопросы о трендах."""
        
        if not question.indicators:
            return "Показатели для анализа не указаны."
        
        trends = []
        
        for indicator in question.indicators:
            if indicator in self.current_data.indicators:
                data = self.current_data.data[indicator].dropna()
                if len(data) > 10:
                    # Простой анализ тренда
                    correlation = data.corr(pd.Series(range(len(data))))
                    if correlation > 0.3:
                        trends.append(f"{indicator}: восходящий тренд")
                    elif correlation < -0.3:
                        trends.append(f"{indicator}: нисходящий тренд")
                    else:
                        trends.append(f"{indicator}: стабильный")
        
        if trends:
            return f"Тренды: {', '.join(trends)}."
        else:
            return "Тренды не обнаружены."
    
    def _answer_prediction_question(self, question: MedicalQuestion) -> str:
        """Отвечает на вопросы о предсказаниях."""
        
        # Простое предсказание на основе последних значений
        if not question.indicators:
            return "Показатели для анализа не указаны."
        
        predictions = []
        
        for indicator in question.indicators:
            if indicator in self.current_data.indicators:
                data = self.current_data.data[indicator].dropna()
                if len(data) > 5:
                    # Простое предсказание на основе среднего изменения
                    recent_values = data.tail(5)
                    if len(recent_values) > 1:
                        avg_change = recent_values.diff().mean()
                        last_value = recent_values.iloc[-1]
                        predicted_value = last_value + avg_change
                        predictions.append(f"{indicator}: {predicted_value:.2f}")
        
        if predictions:
            return f"Предсказания: {', '.join(predictions)}."
        else:
            return "Предсказания недоступны."
    
    def _answer_critical_question(self, question: MedicalQuestion) -> str:
        """Отвечает на вопросы о критических показателях."""
        
        if not question.indicators:
            return "Критические показатели не указаны."
        
        critical_issues = []
        
        for indicator in question.indicators:
            if indicator in self.current_data.indicators:
                data = self.current_data.data[indicator].dropna()
                if len(data) > 0:
                    # Проверка на критические значения
                    if indicator == 'heart_rate':
                        critical_low, critical_high = 40, 120
                    elif indicator == 'blood_pressure_systolic':
                        critical_low, critical_high = 70, 180
                    elif indicator == 'oxygen_saturation':
                        critical_low, critical_high = 90, 100
                    else:
                        continue
                    
                    critical_values = data[(data < critical_low) | (data > critical_high)]
                    if len(critical_values) > 0:
                        critical_issues.append(f"{indicator}: {len(critical_values)} критических значений")
        
        if critical_issues:
            return f"Критические проблемы: {', '.join(critical_issues)}."
        else:
            return "Критические проблемы не обнаружены."
    
    def _answer_treatment_question(self, question: MedicalQuestion) -> str:
        """Отвечает на вопросы об эффективности лечения."""
        
        # Анализ стабильности показателей
        if not question.indicators:
            return "Показатели для анализа не указаны."
        
        stability_analysis = []
        
        for indicator in question.indicators:
            if indicator in self.current_data.indicators:
                data = self.current_data.data[indicator].dropna()
                if len(data) > 10:
                    # Анализ стабильности
                    std_dev = data.std()
                    mean_val = data.mean()
                    cv = std_dev / mean_val if mean_val != 0 else 0
                    
                    if cv < 0.1:
                        stability_analysis.append(f"{indicator}: стабильный")
                    elif cv < 0.2:
                        stability_analysis.append(f"{indicator}: умеренно стабильный")
                    else:
                        stability_analysis.append(f"{indicator}: нестабильный")
        
        if stability_analysis:
            return f"Стабильность показателей: {', '.join(stability_analysis)}."
        else:
            return "Анализ стабильности недоступен."
    
    def get_summary_report(self) -> Dict[str, Any]:
        """Возвращает сводный отчет по анализу."""
        
        if self.current_data is None:
            return {"error": "Данные не загружены"}
        
        report = {
            "data_info": {
                "indicators": self.current_data.indicators,
                "data_points": len(self.current_data.timestamps),
                "missing_percentage": self.current_data.missing_data_mask.sum().sum() / 
                                   (len(self.current_data.indicators) * len(self.current_data.timestamps)) * 100,
                "time_range": {
                    "start": self.current_data.timestamps[0].isoformat(),
                    "end": self.current_data.timestamps[-1].isoformat()
                }
            },
            "analysis_results": self.analysis_results,
            "questions_generated": len(self.current_questions),
            "questions": [
                {
                    "question": q.question,
                    "type": q.question_type,
                    "priority": q.priority,
                    "indicators": q.indicators
                } for q in self.current_questions
            ]
        }
        
        return report
    
    def save_report(self, file_path: str):
        """Сохраняет отчет в файл."""
        
        report = self.get_summary_report()
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2, default=str)
        
        print(f"✅ Отчет сохранен в файл: {file_path}")
    
    def reset(self):
        """Сбрасывает состояние системы."""
        
        self.current_data = None
        self.current_questions = []
        self.analysis_results = {}
        
        print("🔄 Система сброшена")

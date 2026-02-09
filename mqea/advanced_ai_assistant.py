#!/usr/bin/env python3
"""
Продвинутый AI-помощник MQEA с возможностью самообучения.

Автор: Мухаммад Махизода
Таджикский национальный университет
"""

import json
import pickle
import numpy as np
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import re
import os

class AdvancedAIAssistant:
    """Продвинутый AI-помощник с возможностью самообучения."""
    
    def __init__(self, knowledge_base_path: str = "mqea_ai_knowledge.json"):
        """Инициализация AI-помощника."""
        self.knowledge_base_path = knowledge_base_path
        self.knowledge_base = self._load_knowledge_base()
        self.conversation_history = []
        self.learning_data = []
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.knowledge_vectors = None
        self._build_knowledge_vectors()
        
        # Статистика обучения
        self.learning_stats = {
            'total_queries': 0,
            'successful_answers': 0,
            'learning_events': 0,
            'knowledge_updates': 0,
            'last_learning': None
        }
    
    def _load_knowledge_base(self) -> Dict[str, Any]:
        """Загрузка базы знаний."""
        if os.path.exists(self.knowledge_base_path):
            try:
                with open(self.knowledge_base_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Ошибка загрузки базы знаний: {e}")
                return self._create_default_knowledge_base()
        else:
            return self._create_default_knowledge_base()
    
    def _create_default_knowledge_base(self) -> Dict[str, Any]:
        """Создание базовой базы знаний."""
        return {
            'mqea_concepts': {
                'quantum_entanglement': {
                    'definition': 'Квантовая запутанность - это квантовомеханическое явление, при котором квантовые состояния двух или более объектов оказываются взаимосвязанными',
                    'medical_application': 'В MQEA используется для анализа корреляций между медицинскими показателями',
                    'examples': ['Связь между пульсом и давлением', 'Корреляция температуры и частоты дыхания'],
                    'quantum_formula': '|ψ⟩ = α|00⟩ + β|11⟩',
                    'medical_significance': 'Помогает выявить скрытые связи между симптомами и заболеваниями'
                },
                'quantum_coherence': {
                    'definition': 'Квантовая когерентность - это свойство квантовых систем сохранять фазу волновой функции',
                    'medical_application': 'Помогает анализировать стабильность медицинских показателей',
                    'examples': ['Стабильность сердечного ритма', 'Регулярность дыхания'],
                    'quantum_formula': 'ρ = |ψ⟩⟨ψ|',
                    'medical_significance': 'Оценивает стабильность жизненных функций'
                },
                'quantum_superposition': {
                    'definition': 'Квантовая суперпозиция - это способность квантовой системы находиться в нескольких состояниях одновременно',
                    'medical_application': 'Моделирует множественные диагнозы и состояния пациента',
                    'examples': ['Дифференциальная диагностика', 'Множественные симптомы'],
                    'quantum_formula': '|ψ⟩ = Σᵢ cᵢ|i⟩',
                    'medical_significance': 'Помогает в сложных случаях диагностики'
                }
            },
            'medical_indicators': {
                'heart_rate': {
                    'normal_range': '60-100 уд/мин',
                    'description': 'Частота сердечных сокращений',
                    'critical_values': {'low': 40, 'high': 120},
                    'related_indicators': ['blood_pressure', 'oxygen_saturation'],
                    'quantum_analysis': 'Анализируется через квантовую запутанность с другими показателями',
                    'medical_conditions': {
                        'bradycardia': 'Пульс < 60 уд/мин - возможна брадикардия',
                        'tachycardia': 'Пульс > 100 уд/мин - возможна тахикардия'
                    }
                },
                'blood_pressure': {
                    'normal_range': '90-140/60-90 мм рт.ст.',
                    'description': 'Артериальное давление',
                    'critical_values': {'systolic_low': 80, 'systolic_high': 160, 'diastolic_low': 50, 'diastolic_high': 100},
                    'related_indicators': ['heart_rate', 'cholesterol'],
                    'quantum_analysis': 'Квантовая корреляция с пульсом и кислородом',
                    'medical_conditions': {
                        'hypertension': 'АД > 140/90 - артериальная гипертензия',
                        'hypotension': 'АД < 90/60 - артериальная гипотензия'
                    }
                },
                'temperature': {
                    'normal_range': '36.1-37.2°C',
                    'description': 'Температура тела',
                    'critical_values': {'low': 35.0, 'high': 38.0},
                    'related_indicators': ['heart_rate', 'respiratory_rate'],
                    'quantum_analysis': 'Квантовая когерентность с метаболическими процессами',
                    'medical_conditions': {
                        'fever': 'Температура > 37.2°C - лихорадка',
                        'hypothermia': 'Температура < 36.0°C - переохлаждение'
                    }
                },
                'oxygen_saturation': {
                    'normal_range': '95-100%',
                    'description': 'Насыщение крови кислородом',
                    'critical_values': {'low': 90, 'high': 100},
                    'related_indicators': ['respiratory_rate', 'heart_rate'],
                    'quantum_analysis': 'Квантовая запутанность с дыхательной системой',
                    'medical_conditions': {
                        'hypoxemia': 'SpO2 < 95% - гипоксемия',
                        'severe_hypoxemia': 'SpO2 < 90% - тяжелая гипоксемия'
                    }
                }
            },
            'quantum_medical_diagnosis': {
                'quantum_symptom_analysis': {
                    'description': 'Квантовый анализ симптомов для диагностики',
                    'method': 'Использование квантовой суперпозиции для множественных диагнозов',
                    'formula': '|diagnosis⟩ = Σᵢ pᵢ|disease_i⟩',
                    'applications': ['Дифференциальная диагностика', 'Раннее выявление заболеваний']
                },
                'quantum_risk_assessment': {
                    'description': 'Квантовая оценка рисков для здоровья',
                    'method': 'Анализ квантовой запутанности между факторами риска',
                    'formula': 'P(risk) = |⟨risk_factors|quantum_state⟩|²',
                    'applications': ['Профилактика заболеваний', 'Персонализированная медицина']
                },
                'quantum_treatment_optimization': {
                    'description': 'Квантовая оптимизация лечения',
                    'method': 'Поиск оптимального лечения через квантовые алгоритмы',
                    'formula': '|treatment⟩ = argmax(⟨patient|treatment|patient⟩)',
                    'applications': ['Персонализированное лечение', 'Минимизация побочных эффектов']
                }
            },
            'analysis_patterns': {
                'anomaly_detection': {
                    'description': 'Обнаружение аномальных значений в медицинских данных',
                    'methods': ['statistical_outliers', 'quantum_entanglement_analysis', 'pattern_deviation'],
                    'thresholds': {'statistical': 2.0, 'quantum': 0.8, 'pattern': 0.7},
                    'quantum_approach': 'Использование квантовых состояний для выявления аномалий'
                },
                'correlation_analysis': {
                    'description': 'Анализ корреляций между медицинскими показателями',
                    'methods': ['pearson_correlation', 'quantum_entanglement', 'mutual_information'],
                    'significance_threshold': 0.05,
                    'quantum_approach': 'Квантовая запутанность для выявления скрытых связей'
                }
            },
            'user_queries': [],
            'learning_patterns': {},
            'successful_responses': []
        }
    
    def _build_knowledge_vectors(self):
        """Построение векторного представления базы знаний."""
        try:
            # Собираем все текстовые данные для векторизации
            texts = []
            for category, data in self.knowledge_base.items():
                if isinstance(data, dict):
                    for key, value in data.items():
                        if isinstance(value, dict):
                            for sub_key, sub_value in value.items():
                                if isinstance(sub_value, str):
                                    texts.append(sub_value)
                                elif isinstance(sub_value, list):
                                    texts.extend([str(item) for item in sub_value])
            
            if texts:
                self.knowledge_vectors = self.vectorizer.fit_transform(texts)
            else:
                self.knowledge_vectors = None
        except Exception as e:
            print(f"Ошибка построения векторов: {e}")
            self.knowledge_vectors = None
    
    def process_query(self, query: str) -> str:
        """Обработка запроса пользователя."""
        self.learning_stats['total_queries'] += 1
        
        # Сохраняем запрос в историю
        self.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'type': 'user'
        })
        
        try:
            # Анализируем запрос
            query_analysis = self._analyze_query(query)
            
            # Ищем ответ в базе знаний
            response = self._find_best_response(query, query_analysis)
            
            # Если ответ не найден, пытаемся сгенерировать
            if not response or response == "Не знаю":
                response = self._generate_response(query, query_analysis)
            
            # Сохраняем ответ в историю
            self.conversation_history.append({
                'timestamp': datetime.now().isoformat(),
                'response': response,
                'type': 'assistant'
            })
            
            # Обновляем статистику
            if response and response != "Не знаю":
                self.learning_stats['successful_answers'] += 1
            
            # Сохраняем данные для обучения
            self._save_learning_data(query, response, query_analysis)
            
            return response
            
        except Exception as e:
            error_response = f"❌ Ошибка обработки запроса: {str(e)}"
            self.conversation_history.append({
                'timestamp': datetime.now().isoformat(),
                'error': str(e),
                'type': 'error'
            })
            return error_response
    
    def _analyze_query(self, query: str) -> Dict[str, Any]:
        """Анализ запроса пользователя."""
        analysis = {
            'intent': 'unknown',
            'entities': [],
            'keywords': [],
            'complexity': 'low',
            'category': 'general'
        }
        
        query_lower = query.lower()
        
        # Определяем намерение
        if any(word in query_lower for word in ['привет', 'здравствуй', 'добро', 'добрый', 'hi', 'hello', 'hey']):
            analysis['intent'] = 'greeting'
        elif any(word in query_lower for word in ['спасибо', 'благодарю', 'thanks', 'thank you']):
            analysis['intent'] = 'thanks'
        elif any(word in query_lower for word in ['пока', 'до свидания', 'bye', 'goodbye', 'увидимся']):
            analysis['intent'] = 'goodbye'
        elif any(word in query_lower for word in ['как дела', 'как поживаешь', 'how are you', 'что нового']):
            analysis['intent'] = 'how_are_you'
        elif any(word in query_lower for word in ['объясни', 'что такое', 'как работает', 'расскажи', 'опиши']):
            analysis['intent'] = 'explanation'
        elif any(word in query_lower for word in ['анализ', 'результат', 'график', 'интерпретировать', 'покажи']):
            analysis['intent'] = 'analysis'
        elif any(word in query_lower for word in ['рекомендация', 'совет', 'что делать', 'рекомендуй', 'помоги']):
            analysis['intent'] = 'recommendation'
        elif any(word in query_lower for word in ['диагностика', 'болезнь', 'симптом', 'диагноз', 'лечение']):
            analysis['intent'] = 'diagnosis'
        elif any(word in query_lower for word in ['квант', 'запутанность', 'когерентность', 'физика', 'механика']):
            analysis['intent'] = 'quantum_physics'
        
        # Извлекаем ключевые слова
        keywords = re.findall(r'\b\w+\b', query_lower)
        analysis['keywords'] = [word for word in keywords if len(word) > 3]
        
        # Определяем сложность
        if len(query.split()) > 10 or any(word in query_lower for word in ['сложный', 'детально', 'подробно']):
            analysis['complexity'] = 'high'
        elif len(query.split()) > 5:
            analysis['complexity'] = 'medium'
        
        # Определяем категорию
        if any(word in query_lower for word in ['mqea', 'квант', 'запутанность']):
            analysis['category'] = 'mqea'
        elif any(word in query_lower for word in ['медицин', 'здоровье', 'диагностика']):
            analysis['category'] = 'medical'
        elif any(word in query_lower for word in ['данные', 'анализ', 'статистика']):
            analysis['category'] = 'data_analysis'
        
        return analysis
    
    def _find_best_response(self, query: str, analysis: Dict[str, Any]) -> str:
        """Поиск лучшего ответа в базе знаний."""
        try:
            # Простой поиск по ключевым словам
            query_lower = query.lower()
            
            # Проверяем намерения и возвращаем соответствующие ответы
            if analysis['intent'] == 'greeting':
                return self._handle_greeting(analysis)
            
            elif analysis['intent'] == 'thanks':
                return self._handle_thanks(analysis)
            
            elif analysis['intent'] == 'goodbye':
                return self._handle_goodbye(analysis)
            
            elif analysis['intent'] == 'how_are_you':
                return self._handle_how_are_you(analysis)
            
            elif analysis['intent'] == 'explanation':
                if any(word in query_lower for word in ['квант', 'запутанность', 'entanglement']):
                    return self._explain_quantum_concepts(analysis)
                elif any(word in query_lower for word in ['когерентность', 'coherence']):
                    return self._explain_quantum_concepts(analysis)
                elif any(word in query_lower for word in ['суперпозиция', 'superposition']):
                    return self._explain_quantum_concepts(analysis)
                elif any(word in query_lower for word in ['mqea', 'система', 'алгоритм']):
                    return self._explain_mqea_concepts(analysis)
                else:
                    return self._explain_mqea_concepts(analysis)
            
            elif analysis['intent'] == 'analysis':
                return self._provide_analysis_help(analysis)
            
            elif analysis['intent'] == 'recommendation':
                return self._provide_recommendations(analysis)
            
            elif analysis['intent'] == 'diagnosis':
                return self._provide_diagnostic_help(analysis)
            
            elif analysis['intent'] == 'quantum_physics':
                return self._explain_quantum_concepts(analysis)
            
            # Если намерение не определено, пробуем по ключевым словам
            if any(word in query_lower for word in ['квант', 'запутанность', 'когерентность', 'суперпозиция']):
                return self._explain_quantum_concepts(analysis)
            elif any(word in query_lower for word in ['mqea', 'система', 'алгоритм']):
                return self._explain_mqea_concepts(analysis)
            elif any(word in query_lower for word in ['анализ', 'результат', 'график', 'показатель']):
                return self._provide_analysis_help(analysis)
            elif any(word in query_lower for word in ['рекомендация', 'совет', 'медицин', 'лечение']):
                return self._provide_recommendations(analysis)
            elif any(word in query_lower for word in ['диагностика', 'болезнь', 'симптом', 'диагноз']):
                return self._provide_diagnostic_help(analysis)
            elif any(word in query_lower for word in ['пульс', 'давление', 'температура', 'кислород']):
                return self._provide_medical_indicators_help(analysis)
            
            return "Не знаю"
            
        except Exception as e:
            print(f"Ошибка поиска ответа: {e}")
            return "Не знаю"
    
    def _get_response_by_index(self, index: int, analysis: Dict[str, Any]) -> str:
        """Получение ответа по индексу."""
        # Простая логика для демонстрации
        if analysis['intent'] == 'explanation':
            if 'квант' in analysis['keywords']:
                return self._explain_quantum_concepts(analysis)
            elif 'mqea' in analysis['keywords']:
                return self._explain_mqea_concepts(analysis)
        elif analysis['intent'] == 'analysis':
            return self._provide_analysis_help(analysis)
        elif analysis['intent'] == 'recommendation':
            return self._provide_recommendations(analysis)
        elif analysis['intent'] == 'diagnosis':
            return self._provide_diagnostic_help(analysis)
        
        return "Не знаю"
    
    def _explain_quantum_concepts(self, analysis: Dict[str, Any]) -> str:
        """Объяснение квантовых концепций."""
        concepts = self.knowledge_base.get('mqea_concepts', {})
        
        if 'запутанность' in analysis['keywords']:
            concept = concepts.get('quantum_entanglement', {})
            return f"""🔬 **Квантовая запутанность в медицине**

**Определение:** {concept.get('definition', '')}

**Квантовая формула:** {concept.get('quantum_formula', '')}

**Медицинское применение:** {concept.get('medical_application', '')}

**Медицинское значение:** {concept.get('medical_significance', '')}

**Примеры в медицине:**
{chr(10).join(['- ' + ex for ex in concept.get('examples', [])])}

**Квантовый анализ:**
- Выявление скрытых связей между симптомами
- Анализ корреляций между показателями
- Раннее выявление заболеваний"""
        
        elif 'когерентность' in analysis['keywords']:
            concept = concepts.get('quantum_coherence', {})
            return f"""🌊 **Квантовая когерентность в медицине**

**Определение:** {concept.get('definition', '')}

**Квантовая формула:** {concept.get('quantum_formula', '')}

**Медицинское применение:** {concept.get('medical_application', '')}

**Медицинское значение:** {concept.get('medical_significance', '')}

**Примеры в медицине:**
{chr(10).join(['- ' + ex for ex in concept.get('examples', [])])}

**Квантовый анализ:**
- Оценка стабильности жизненных функций
- Анализ регулярности ритмов
- Выявление нарушений когерентности"""
        
        elif 'суперпозиция' in analysis['keywords']:
            concept = concepts.get('quantum_superposition', {})
            return f"""🔬 **Квантовая суперпозиция в медицине**

**Определение:** {concept.get('definition', '')}

**Квантовая формула:** {concept.get('quantum_formula', '')}

**Медицинское применение:** {concept.get('medical_application', '')}

**Медицинское значение:** {concept.get('medical_significance', '')}

**Примеры в медицине:**
{chr(10).join(['- ' + ex for ex in concept.get('examples', [])])}

**Квантовый анализ:**
- Моделирование множественных диагнозов
- Дифференциальная диагностика
- Анализ неопределенности состояний"""
        
        return """🔬 **Квантовые концепции в MQEA**

**Основные квантовые принципы:**
- ⚛️ **Квантовая запутанность:** |ψ⟩ = α|00⟩ + β|11⟩
- 🌊 **Квантовая когерентность:** ρ = |ψ⟩⟨ψ|
- 🔬 **Квантовая суперпозиция:** |ψ⟩ = Σᵢ cᵢ|i⟩

**Медицинские применения:**
- Анализ корреляций между показателями
- Выявление скрытых связей между симптомами
- Дифференциальная диагностика
- Персонализированное лечение

**Квантовые методы:**
- Квантовая запутанность для выявления связей
- Квантовая когерентность для анализа стабильности
- Квантовая суперпозиция для множественных состояний"""
    
    def _explain_mqea_concepts(self, analysis: Dict[str, Any]) -> str:
        """Объяснение концепций MQEA."""
        return """🧠 **MQEA (Medical Quantum Entanglement Analysis)**

**Описание:** Революционный квантовый алгоритм для анализа многомерных медицинских временных рядов на основе принципов квантовой механики.

**Квантовые возможности:**
- ⚛️ **Квантовая запутанность:** |ψ⟩ = α|00⟩ + β|11⟩
  - Анализ корреляций между медицинскими показателями
  - Выявление скрытых связей между симптомами
  - Раннее выявление заболеваний

- 🌊 **Квантовая когерентность:** ρ = |ψ⟩⟨ψ|
  - Анализ стабильности жизненных функций
  - Оценка регулярности ритмов организма
  - Выявление нарушений когерентности

- 🔬 **Квантовая суперпозиция:** |ψ⟩ = Σᵢ cᵢ|i⟩
  - Моделирование множественных диагнозов
  - Дифференциальная диагностика
  - Анализ неопределенности состояний

**Медицинские показатели:**
- ❤️ **heart_rate:** 60-100 уд/мин (квантовая корреляция с давлением)
- 🩸 **blood_pressure:** 90-140/60-90 мм рт.ст. (квантовая запутанность)
- 🌡️ **temperature:** 36.1-37.2°C (квантовая когерентность)
- 💨 **oxygen_saturation:** 95-100% (квантовая корреляция с дыханием)
- 🫁 **respiratory_rate:** 12-20 дых/мин (квантовая суперпозиция)
- 🍯 **glucose:** 3.9-5.6 ммоль/л (квантовая когерентность)
- 🧈 **cholesterol:** <200 мг/дл (квантовая запутанность)

**Квантовые методы:**
- Заполнение пропущенных данных квантовым методом
- Обнаружение скрытых паттернов через квантовую запутанность
- Генерация вопросов для анализа через квантовую суперпозицию
- Предсказание изменений через квантовую когерентность
- Выявление аномалий через квантовые нарушения"""
    
    def _provide_analysis_help(self, analysis: Dict[str, Any]) -> str:
        """Помощь с анализом данных."""
        return """📊 **Квантовый анализ медицинских данных MQEA**

**Квантовые методы анализа:**
1. **⚛️ Квантовая запутанность** - |ψ⟩ = α|00⟩ + β|11⟩
   - Показывает силу связи между показателями
   - Порог значимости: > 0.7
   - Выявляет скрытые корреляции

2. **🌊 Квантовая когерентность** - ρ = |ψ⟩⟨ψ|
   - Анализирует стабильность показателей
   - Оценивает регулярность функций
   - Выявляет нарушения ритма

3. **🔬 Квантовая суперпозиция** - |ψ⟩ = Σᵢ cᵢ|i⟩
   - Моделирует множественные состояния
   - Дифференциальная диагностика
   - Анализ неопределенности

**Медицинские показатели:**
- ❤️ **Пульс:** Квантовая корреляция с давлением и кислородом
- 🩸 **Давление:** Квантовая запутанность с сердечным ритмом
- 🌡️ **Температура:** Квантовая когерентность с метаболизмом
- 💨 **Дыхание:** Квантовая суперпозиция с кислородом

**Квантовые аномалии:**
- Статистические выбросы (σ > 2.0)
- Квантовые нарушения (entanglement < 0.3)
- Паттерн-отклонения (coherence < 0.7)

**Рекомендации:**
- Анализируйте квантовые состояния комплексно
- Обращайте внимание на нарушения когерентности
- Используйте суперпозицию для сложных случаев"""
    
    def _provide_recommendations(self, analysis: Dict[str, Any]) -> str:
        """Предоставление рекомендаций."""
        return """💊 **Квантовые медицинские рекомендации MQEA**

**Квантовые принципы лечения:**
1. **⚛️ Квантовая суперпозиция терапии:** |treatment⟩ = Σᵢ pᵢ|therapy_i⟩
   - Персонализированное лечение
   - Минимизация побочных эффектов
   - Оптимизация дозировок

2. **🔬 Квантовая запутанность мониторинга:**
   - Отслеживание корреляций между показателями
   - Раннее выявление изменений
   - Предсказание осложнений

3. **🌊 Квантовая когерентность стабилизации:**
   - Поддержание стабильности функций
   - Регуляция ритмов организма
   - Восстановление баланса

**Медицинские рекомендации:**
- ❤️ **Сердечно-сосудистая система:** Мониторинг квантовой корреляции пульса и давления
- 🫁 **Дыхательная система:** Анализ квантовой запутанности кислорода и дыхания
- 🧠 **Нервная система:** Оценка квантовой когерентности функций
- 🩸 **Кровеносная система:** Квантовый анализ циркуляции и свертывания

**Квантовые методы профилактики:**
- Регулярный квантовый анализ показателей
- Раннее выявление через квантовые аномалии
- Персонализированная профилактика через суперпозицию

**Консультация специалиста** рекомендуется при квантовых нарушениях когерентности."""
    
    def _provide_diagnostic_help(self, analysis: Dict[str, Any]) -> str:
        """Помощь с диагностикой."""
        return """🏥 **Квантовая медицинская диагностика MQEA**

**Квантовые возможности диагностики:**
- 🔬 **Квантовая суперпозиция диагнозов:** |diagnosis⟩ = Σᵢ pᵢ|disease_i⟩
- ⚛️ **Квантовая запутанность симптомов:** Выявление скрытых связей между симптомами
- 🌊 **Квантовая когерентность:** Анализ стабильности жизненных функций
- 📊 **Квантовая оценка рисков:** P(risk) = |⟨risk_factors|quantum_state⟩|²

**Медицинские показатели:**
- ❤️ **Пульс:** 60-100 уд/мин (квантовая корреляция с давлением)
- 🩸 **Давление:** 90-140/60-90 мм рт.ст. (квантовая запутанность)
- 🌡️ **Температура:** 36.1-37.2°C (квантовая когерентность)
- 💨 **Кислород:** 95-100% (квантовая корреляция с дыханием)

**Квантовые методы:**
- Дифференциальная диагностика через суперпозицию
- Раннее выявление через квантовые аномалии
- Персонализированное лечение через квантовую оптимизацию

**Важно:** MQEA - это квантовый инструмент поддержки, не заменяет консультацию врача."""
    
    def _handle_greeting(self, analysis: Dict[str, Any]) -> str:
        """Обработка приветствий."""
        greetings = [
            "👋 Привет! Я ваш квантовый медицинский AI-помощник MQEA!",
            "🤖 Здравствуйте! Готов помочь с квантовым анализом медицинских данных!",
            "⚛️ Привет! Я специализируюсь на квантовой медицине и MQEA!",
            "🏥 Добро пожаловать! Я ваш квантовый помощник по здоровью!",
            "🔬 Привет! Готов объяснить квантовые принципы в медицине!"
        ]
        import random
        return random.choice(greetings)
    
    def _handle_thanks(self, analysis: Dict[str, Any]) -> str:
        """Обработка благодарностей."""
        thanks_responses = [
            "😊 Пожалуйста! Рад помочь с квантовым анализом!",
            "🤖 Не за что! Всегда готов помочь с MQEA!",
            "⚛️ Пожалуйста! Квантовая медицина - моя страсть!",
            "🏥 Рад помочь! Обращайтесь за квантовыми советами!",
            "🔬 Пожалуйста! Готов к новым квантовым вопросам!"
        ]
        import random
        return random.choice(thanks_responses)
    
    def _handle_goodbye(self, analysis: Dict[str, Any]) -> str:
        """Обработка прощаний."""
        goodbye_responses = [
            "👋 До свидания! Удачи с квантовым анализом!",
            "🤖 Пока! Обращайтесь за помощью с MQEA!",
            "⚛️ До встречи! Изучайте квантовую медицину!",
            "🏥 Пока! Берегите здоровье!",
            "🔬 До свидания! Успехов в квантовых исследованиях!"
        ]
        import random
        return random.choice(goodbye_responses)
    
    def _handle_how_are_you(self, analysis: Dict[str, Any]) -> str:
        """Обработка вопроса 'Как дела?'."""
        how_are_you_responses = [
            "🤖 Отлично! Готов помочь с квантовым анализом медицинских данных!",
            "⚛️ Прекрасно! Изучаю новые квантовые методы в медицине!",
            "🏥 Хорошо! Готов к новым медицинским вопросам!",
            "🔬 Отлично! Квантовая медицина развивается!",
            "💡 Хорошо! Готов объяснить принципы MQEA!"
        ]
        import random
        return random.choice(how_are_you_responses)
    
    def _provide_medical_indicators_help(self, analysis: Dict[str, Any]) -> str:
        """Помощь с медицинскими показателями."""
        query_lower = analysis.get('keywords', [])
        indicators = self.knowledge_base.get('medical_indicators', {})
        
        # Ищем конкретный показатель
        for indicator_name, indicator_data in indicators.items():
            if any(word in query_lower for word in indicator_data.get('related_indicators', [])):
                return f"""🏥 **Квантовый анализ {indicator_data.get('description', '')}**

**Нормальные значения:** {indicator_data.get('normal_range', '')}

**Квантовый анализ:** {indicator_data.get('quantum_analysis', '')}

**Критические значения:**
{chr(10).join([f"- {key}: {value}" for key, value in indicator_data.get('critical_values', {}).items()])}

**Медицинские состояния:**
{chr(10).join([f"- **{key}:** {value}" for key, value in indicator_data.get('medical_conditions', {}).items()])}

**Связанные показатели:** {', '.join(indicator_data.get('related_indicators', []))}

**Квантовые рекомендации:**
- Анализируйте квантовую корреляцию с связанными показателями
- Обращайте внимание на нарушения квантовой когерентности
- Используйте квантовую суперпозицию для сложных случаев"""
        
        # Если конкретный показатель не найден, показываем общую информацию
        return """🏥 **Квантовый анализ медицинских показателей MQEA**

**Основные показатели:**
- ❤️ **Пульс (heart_rate):** 60-100 уд/мин
  - Квантовая корреляция с давлением и кислородом
  - Анализ через квантовую запутанность

- 🩸 **Давление (blood_pressure):** 90-140/60-90 мм рт.ст.
  - Квантовая запутанность с сердечным ритмом
  - Анализ через квантовую когерентность

- 🌡️ **Температура (temperature):** 36.1-37.2°C
  - Квантовая когерентность с метаболизмом
  - Анализ через квантовую суперпозицию

- 💨 **Кислород (oxygen_saturation):** 95-100%
  - Квантовая корреляция с дыханием
  - Анализ через квантовую запутанность

**Квантовые методы анализа:**
- Квантовая запутанность для выявления связей
- Квантовая когерентность для анализа стабильности
- Квантовая суперпозиция для множественных состояний

**Рекомендации:**
- Анализируйте показатели комплексно через квантовые состояния
- Обращайте внимание на нарушения квантовой когерентности
- Используйте квантовую суперпозицию для сложных случаев"""
    
    def _generate_response(self, query: str, analysis: Dict[str, Any]) -> str:
        """Генерация ответа на основе анализа."""
        query_lower = query.lower()
        
        if analysis['intent'] == 'greeting':
            return self._handle_greeting(analysis)
        elif analysis['intent'] == 'thanks':
            return self._handle_thanks(analysis)
        elif analysis['intent'] == 'goodbye':
            return self._handle_goodbye(analysis)
        elif analysis['intent'] == 'how_are_you':
            return self._handle_how_are_you(analysis)
        elif analysis['intent'] == 'explanation':
            if any(word in query_lower for word in ['квант', 'запутанность', 'когерентность']):
                return self._explain_quantum_concepts(analysis)
            elif any(word in query_lower for word in ['mqea', 'система', 'алгоритм']):
                return self._explain_mqea_concepts(analysis)
            else:
                return self._explain_mqea_concepts(analysis)
        elif analysis['intent'] == 'analysis':
            return self._provide_analysis_help(analysis)
        elif analysis['intent'] == 'recommendation':
            return self._provide_recommendations(analysis)
        elif analysis['intent'] == 'diagnosis':
            return self._provide_diagnostic_help(analysis)
        elif analysis['intent'] == 'quantum_physics':
            return self._explain_quantum_concepts(analysis)
        else:
            # Пробуем определить по ключевым словам
            if any(word in query_lower for word in ['квант', 'запутанность', 'когерентность']):
                return self._explain_quantum_concepts(analysis)
            elif any(word in query_lower for word in ['mqea', 'система', 'алгоритм']):
                return self._explain_mqea_concepts(analysis)
            elif any(word in query_lower for word in ['анализ', 'результат', 'график']):
                return self._provide_analysis_help(analysis)
            elif any(word in query_lower for word in ['рекомендация', 'совет', 'медицин']):
                return self._provide_recommendations(analysis)
            elif any(word in query_lower for word in ['диагностика', 'болезнь', 'симптом']):
                return self._provide_diagnostic_help(analysis)
            else:
                return "Интересный вопрос! Я изучаю эту тему и постараюсь дать более подробный ответ в будущем."
    
    def _save_learning_data(self, query: str, response: str, analysis: Dict[str, Any]):
        """Сохранение данных для обучения."""
        learning_event = {
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'response': response,
            'analysis': analysis,
            'success': response != "Не знаю"
        }
        
        self.learning_data.append(learning_event)
        self.learning_stats['learning_events'] += 1
        self.learning_stats['last_learning'] = datetime.now().isoformat()
        
        # Сохраняем каждые 10 событий
        if len(self.learning_data) % 10 == 0:
            self._update_knowledge_base()
    
    def _update_knowledge_base(self):
        """Обновление базы знаний на основе обучения."""
        try:
            # Анализируем паттерны в данных обучения
            successful_responses = [event for event in self.learning_data if event['success']]
            
            if successful_responses:
                # Обновляем статистику
                self.learning_stats['knowledge_updates'] += 1
                
                # Добавляем успешные ответы в базу знаний
                if 'successful_responses' not in self.knowledge_base:
                    self.knowledge_base['successful_responses'] = []
                
                for event in successful_responses[-5:]:  # Последние 5 успешных ответов
                    self.knowledge_base['successful_responses'].append({
                        'query': event['query'],
                        'response': event['response'],
                        'timestamp': event['timestamp']
                    })
                
                # Сохраняем обновленную базу знаний
                self._save_knowledge_base()
                
                # Перестраиваем векторы
                self._build_knowledge_vectors()
                
        except Exception as e:
            print(f"Ошибка обновления базы знаний: {e}")
    
    def _save_knowledge_base(self):
        """Сохранение базы знаний."""
        try:
            with open(self.knowledge_base_path, 'w', encoding='utf-8') as f:
                json.dump(self.knowledge_base, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения базы знаний: {e}")
    
    def get_learning_stats(self) -> Dict[str, Any]:
        """Получение статистики обучения."""
        return {
            **self.learning_stats,
            'conversation_length': len(self.conversation_history),
            'learning_data_size': len(self.learning_data),
            'knowledge_base_size': len(self.knowledge_base)
        }
    
    def learn_from_feedback(self, query: str, response: str, feedback: str):
        """Обучение на основе обратной связи."""
        learning_event = {
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'response': response,
            'feedback': feedback,
            'type': 'feedback'
        }
        
        self.learning_data.append(learning_event)
        
        # Если обратная связь положительная, добавляем в базу знаний
        if feedback.lower() in ['хорошо', 'отлично', 'правильно', 'спасибо']:
            if 'successful_responses' not in self.knowledge_base:
                self.knowledge_base['successful_responses'] = []
            
            self.knowledge_base['successful_responses'].append({
                'query': query,
                'response': response,
                'feedback': feedback,
                'timestamp': learning_event['timestamp']
            })
            
            self._save_knowledge_base()
            self.learning_stats['knowledge_updates'] += 1
    
    def export_knowledge(self, filepath: str):
        """Экспорт базы знаний."""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.knowledge_base, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Ошибка экспорта: {e}")
            return False
    
    def import_knowledge(self, filepath: str):
        """Импорт базы знаний."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                imported_knowledge = json.load(f)
            
            # Объединяем с существующей базой знаний
            for key, value in imported_knowledge.items():
                if key in self.knowledge_base:
                    if isinstance(value, list) and isinstance(self.knowledge_base[key], list):
                        self.knowledge_base[key].extend(value)
                    elif isinstance(value, dict) and isinstance(self.knowledge_base[key], dict):
                        self.knowledge_base[key].update(value)
                else:
                    self.knowledge_base[key] = value
            
            self._save_knowledge_base()
            self._build_knowledge_vectors()
            return True
        except Exception as e:
            print(f"Ошибка импорта: {e}")
            return False


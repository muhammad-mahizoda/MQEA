#!/usr/bin/env python3
"""
Улучшенный AI-помощник MQEA с возможностью обучения
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import json
import re
import random

from .core import MQEAAnalyzer
from .data_processor import MedicalTimeSeries
from .question_generator import QuestionGenerator, MedicalQuestion
from .data_sources import DataSourceManager, create_default_sources
from .recommendation_engine import MedicalRecommendationEngine
from .patient_profile import PatientProfile, create_sample_patient_profiles

class EnhancedMQEAAssistant:
    """Улучшенный AI-помощник MQEA с возможностью обучения и ответов на любые вопросы."""
    
    def __init__(self, analyzer: MQEAAnalyzer):
        self.analyzer = analyzer
        self.data_system = MedicalDataQuestionSystem(analyzer)
        self.knowledge_base = self._initialize_knowledge_base()
        self.learning_data = self._load_learning_data()
        self.current_data: Optional[MedicalTimeSeries] = None
        self.current_questions: List[MedicalQuestion] = []
        self.analysis_results: Dict[str, Any] = {}
        self.conversation_history: List[Dict[str, str]] = []
        
    def _initialize_knowledge_base(self) -> Dict[str, Any]:
        """Инициализирует базу знаний с расширенной информацией."""
        return {
            "mqea_description": """🧬⚛️ **Medical Quantum Entanglement Analysis (MQEA)**

**Описание:** Революционный алгоритм для анализа многомерных медицинских временных рядов на основе принципов квантовой запутанности

**Основатель:** Мухаммад Махизода
**Учреждение:** Таджикский национальный университет
**Версия:** 1.0.0

**Основные возможности:**
• Анализ квантовой запутанности между медицинскими показателями
• Заполнение пропущенных данных квантовым методом
• Обнаружение скрытых паттернов и корреляций
• Генерация важных вопросов для анализа
• Предсказание изменений в показателях
• Выявление аномалий и критических состояний

**Медицинские показатели:**
• heart_rate: Частота пульса (уд/мин)
• blood_pressure_systolic: Систолическое давление (мм рт.ст.)
• blood_pressure_diastolic: Диастолическое давление (мм рт.ст.)
• temperature: Температура тела (°C)
• oxygen_saturation: Насыщение кислородом (%)
• respiratory_rate: Частота дыхания (дых/мин)
• glucose: Уровень глюкозы (ммоль/л)
• cholesterol: Уровень холестерина (мг/дл)
""",
            "help_commands": """🆘 **Помощь по MQEA**

**Основные команды:**
• `загрузить данные` - загрузить данные для анализа
• `создать пример` - создать пример данных
• `выполнить анализ` - запустить квантовый анализ
• `сгенерировать вопросы` - создать важные вопросы
• `найти паттерны` - показать обнаруженные паттерны
• `найти аномалии` - проверить на аномалии
• `предсказать` - сделать предсказания
• `помочь` - показать эту справку

**Что умеет MQEA:**
• Анализ квантовой запутанности между показателями
• Заполнение пропущенных данных
• Обнаружение скрытых паттернов
• Генерация важных вопросов
• Предсказание изменений
• Выявление аномалий

**Примеры вопросов:**
• "Что такое MQEA?"
• "Как загрузить данные?"
• "Выполни анализ"
• "Какие паттерны найдены?"
• "Есть ли аномалии в данных?"

Просто задайте вопрос, и я помогу! 😊
""",
            "about_me": """🤖 **О себе**

Привет! Я ваш AI-помощник по системе MQEA (Medical Quantum Entanglement Analysis).

**Кто я:**
• Интеллектуальный помощник для анализа медицинских данных
• Специализируюсь на квантовом анализе запутанности
• Могу отвечать на любые вопросы о здоровье и медицине
• Постоянно обучаюсь и улучшаю свои ответы

**Что я умею:**
• Анализировать медицинские данные
• Генерировать рекомендации
• Отвечать на вопросы о здоровье
• Объяснять медицинские термины
• Помогать с интерпретацией результатов

**Мой создатель:** Мухаммад Махизода
**Университет:** Таджикский национальный университет

Задавайте любые вопросы - я постараюсь помочь! 😊
""",
            "medical_terms": {
                "пульс": "Частота сердечных сокращений, измеряется в ударах в минуту",
                "давление": "Артериальное давление, состоит из систолического и диастолического",
                "температура": "Температура тела, нормальная 36.1-37.2°C",
                "сахар": "Уровень глюкозы в крови, нормальный 3.9-5.6 ммоль/л",
                "холестерин": "Жировое вещество в крови, нормальный <200 мг/дл",
                "кислород": "Насыщение крови кислородом, нормальное 95-100%",
                "дыхание": "Частота дыхания, нормальная 12-20 вдохов в минуту",
                "bmi": "Индекс массы тела, рассчитывается как вес(кг)/рост(м)²",
                "гипертония": "Повышенное артериальное давление",
                "гипотония": "Пониженное артериальное давление",
                "тахикардия": "Учащенное сердцебиение",
                "брадикардия": "Замедленное сердцебиение",
                "гипергликемия": "Повышенный уровень глюкозы",
                "гипогликемия": "Пониженный уровень глюкозы"
            },
            "common_questions": {
                "как дела": "Спасибо, у меня все хорошо! Готов помочь с анализом медицинских данных. Как дела у вас?",
                "как поживаешь": "Отлично! Работаю над анализом данных и готов ответить на ваши вопросы. Как у вас дела?",
                "что нового": "Много интересного! Система MQEA постоянно развивается, добавляются новые функции анализа. А что нового у вас?",
                "спасибо": "Пожалуйста! Рад был помочь. Если есть еще вопросы - обращайтесь!",
                "пока": "До свидания! Увидимся в следующий раз. Берегите себя!",
                "до свидания": "До свидания! Увидимся в следующий раз. Берегите себя!",
                "привет": "Привет! Рад вас видеть! Чем могу помочь с анализом медицинских данных?",
                "здравствуйте": "Здравствуйте! Добро пожаловать в систему MQEA! Чем могу помочь?"
            }
        }
    
    def _load_learning_data(self) -> Dict[str, Any]:
        """Загружает данные для обучения из файла."""
        try:
            with open('mqea_learning_data.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "learned_responses": {},
                "conversation_patterns": {},
                "user_preferences": {},
                "medical_knowledge": {}
            }
    
    def _save_learning_data(self):
        """Сохраняет данные обучения в файл."""
        try:
            with open('mqea_learning_data.json', 'w', encoding='utf-8') as f:
                json.dump(self.learning_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения данных обучения: {e}")
    
    def _learn_from_conversation(self, question: str, response: str, user_feedback: Optional[str] = None):
        """Обучается на основе разговора."""
        # Сохраняем вопрос и ответ
        if "learned_responses" not in self.learning_data:
            self.learning_data["learned_responses"] = {}
        
        self.learning_data["learned_responses"][question.lower()] = {
            "response": response,
            "timestamp": datetime.now().isoformat(),
            "feedback": user_feedback
        }
        
        # Анализируем паттерны в вопросе
        words = question.lower().split()
        for word in words:
            if word not in self.learning_data["conversation_patterns"]:
                self.learning_data["conversation_patterns"][word] = 0
            self.learning_data["conversation_patterns"][word] += 1
        
        # Сохраняем данные
        self._save_learning_data()
    
    def _generate_contextual_response(self, question: str) -> str:
        """Генерирует контекстуальный ответ на основе текущего состояния системы."""
        context_info = []
        
        if self.current_data:
            context_info.append(f"📊 **Текущие данные:** {len(self.current_data.indicators)} показателей, {len(self.current_data.timestamps)} точек")
        
        if self.analysis_results:
            coherence = self.analysis_results.get('quantum_signatures', {}).get('quantum_coherence', 0)
            context_info.append(f"🔬 **Анализ:** когерентность {coherence:.3f}")
        
        if self.current_questions:
            context_info.append(f"❓ **Вопросы:** {len(self.current_questions)} сгенерировано")
        
        if context_info:
            return f"{' '.join(context_info)}\n\n"
        return ""
    
    def _analyze_question_intent(self, question: str) -> str:
        """Анализирует намерение пользователя в вопросе."""
        question_lower = question.lower()
        
        # Проверяем на приветствие
        greetings = ["привет", "здравствуйте", "добро пожаловать", "hi", "hello"]
        if any(greeting in question_lower for greeting in greetings):
            return "greeting"
        
        # Проверяем на вопросы о системе
        system_questions = ["что такое", "как работает", "что умеет", "возможности"]
        if any(sq in question_lower for sq in system_questions):
            return "system_info"
        
        # Проверяем на медицинские вопросы
        medical_terms = ["пульс", "давление", "температура", "сахар", "холестерин", "кислород", "дыхание"]
        if any(term in question_lower for term in medical_terms):
            return "medical_question"
        
        # Проверяем на команды
        commands = ["загрузить", "создать", "выполнить", "анализ", "паттерны", "аномалии", "предсказать"]
        if any(cmd in question_lower for cmd in commands):
            return "command"
        
        # Проверяем на вопросы о себе
        about_me = ["кто ты", "что ты", "расскажи о себе", "о себе"]
        if any(am in question_lower for am in about_me):
            return "about_me"
        
        # Проверяем на помощь
        help_requests = ["помощь", "помоги", "как", "что делать", "справка"]
        if any(help_word in question_lower for help_word in help_requests):
            return "help"
        
        return "general"
    
    def _generate_medical_response(self, question: str) -> str:
        """Генерирует ответ на медицинский вопрос."""
        question_lower = question.lower()
        
        # Ищем медицинские термины в вопросе
        found_terms = []
        for term, definition in self.knowledge_base["medical_terms"].items():
            if term in question_lower:
                found_terms.append(f"**{term.title()}:** {definition}")
        
        if found_terms:
            response = "🏥 **Медицинская информация:**\n\n"
            response += "\n".join(found_terms)
            
            # Добавляем контекстную информацию
            if self.current_data:
                response += f"\n\n📊 **В ваших данных:**\n"
                for indicator in self.current_data.indicators:
                    if any(term in indicator.lower() for term in self.knowledge_base["medical_terms"].keys()):
                        value = self.current_data.data[indicator].iloc[-1]
                        response += f"• {indicator}: {value:.2f}\n"
            
            return response
        
        # Если не найдены конкретные термины, даем общую медицинскую информацию
        return "🏥 **Медицинская справка:**\n\nЕсли у вас есть вопросы о конкретных медицинских показателях, я могу объяснить их значения и нормальные диапазоны. Также могу проанализировать ваши данные и дать рекомендации."
    
    def _generate_system_response(self, question: str) -> str:
        """Генерирует ответ о системе MQEA."""
        question_lower = question.lower()
        
        if "что такое mqea" in question_lower or "mqea" in question_lower:
            return self.knowledge_base["mqea_description"]
        elif "как работает" in question_lower:
            return "🔬 **Как работает MQEA:**\n\n1. Загружаете медицинские данные\n2. Система анализирует квантовую запутанность между показателями\n3. Заполняет пропущенные данные квантовым методом\n4. Обнаруживает скрытые паттерны и корреляции\n5. Генерирует рекомендации и предсказания"
        elif "что умеет" in question_lower or "возможности" in question_lower:
            return "⚡ **Возможности MQEA:**\n\n• Анализ квантовой запутанности\n• Заполнение пропущенных данных\n• Обнаружение паттернов\n• Генерация вопросов\n• Предсказание изменений\n• Выявление аномалий\n• Персонализированные рекомендации"
        else:
            return self.knowledge_base["mqea_description"]
    
    def _generate_about_me_response(self, question: str) -> str:
        """Генерирует ответ о себе."""
        return self.knowledge_base["about_me"]
    
    def _generate_help_response(self, question: str) -> str:
        """Генерирует ответ с помощью."""
        return self.knowledge_base["help_commands"]
    
    def _generate_general_response(self, question: str) -> str:
        """Генерирует общий ответ на вопрос."""
        # Проверяем, есть ли сохраненный ответ
        if question.lower() in self.learning_data.get("learned_responses", {}):
            return self.learning_data["learned_responses"][question.lower()]["response"]
        
        # Генерируем новый ответ на основе контекста
        context = self._generate_contextual_response(question)
        
        # Анализируем ключевые слова
        keywords = question.lower().split()
        relevant_info = []
        
        if "данные" in keywords or "анализ" in keywords:
            relevant_info.append("📊 Для работы с данными используйте команды 'загрузить данные' или 'создать пример'")
        
        if "здоровье" in keywords or "медицина" in keywords:
            relevant_info.append("🏥 Я могу объяснить медицинские термины и проанализировать ваши показатели")
        
        if "рекомендации" in keywords or "советы" in keywords:
            relevant_info.append("💊 Для получения рекомендаций выполните анализ данных")
        
        if "паттерны" in keywords or "закономерности" in keywords:
            relevant_info.append("🔍 Для поиска паттернов используйте команду 'найти паттерны'")
        
        # Формируем ответ
        response = context
        
        if relevant_info:
            response += "💡 **Возможные варианты:**\n\n" + "\n".join(relevant_info)
        else:
            response += "🤔 **Я понимаю ваш вопрос, но не уверен в точном ответе.**\n\n"
            response += "Попробуйте переформулировать вопрос или используйте команду 'помощь' для получения списка доступных команд.\n\n"
            response += "Я постоянно обучаюсь, поэтому ваши вопросы помогают мне стать лучше! 😊"
        
        return response
    
    def process_query(self, query: str) -> str:
        """Обрабатывает запрос пользователя и генерирует ответ."""
        query = query.strip()
        
        if not query:
            return "Пожалуйста, задайте вопрос или используйте команду 'помощь' для получения списка доступных команд."
        
        # Сохраняем вопрос в историю
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "question": query,
            "user": "user"
        })
        
        # Анализируем намерение
        intent = self._analyze_question_intent(query)
        
        # Генерируем ответ в зависимости от намерения
        if intent == "greeting":
            response = self.knowledge_base["common_questions"].get(query.lower(), "Привет! Рад вас видеть! Чем могу помочь?")
        elif intent == "about_me":
            response = self._generate_about_me_response(query)
        elif intent == "system_info":
            response = self._generate_system_response(query)
        elif intent == "medical_question":
            response = self._generate_medical_response(query)
        elif intent == "help":
            response = self._generate_help_response(query)
        elif intent == "command":
            response = self._handle_command(query)
        else:
            response = self._generate_general_response(query)
        
        # Сохраняем ответ в историю
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "question": query,
            "response": response,
            "user": "assistant"
        })
        
        # Обучаемся на основе разговора
        self._learn_from_conversation(query, response)
        
        return response
    
    def _handle_command(self, query: str) -> str:
        """Обрабатывает команды пользователя."""
        query_lower = query.lower()
        
        if "загрузить данные" in query_lower or "загрузить" in query_lower:
            return self._handle_load_data()
        elif "создать пример" in query_lower or "создать" in query_lower:
            return self._handle_generate_data()
        elif "выполнить анализ" in query_lower or "анализ" in query_lower:
            return self._handle_perform_analysis()
        elif "сгенерировать вопросы" in query_lower or "вопросы" in query_lower:
            return self._handle_generate_questions()
        elif "найти паттерны" in query_lower or "паттерны" in query_lower:
            return self._handle_find_patterns()
        elif "найти аномалии" in query_lower or "аномалии" in query_lower:
            return self._handle_find_anomalies()
        elif "предсказать" in query_lower or "прогноз" in query_lower:
            return self._handle_predict_changes()
        elif "показать отчет" in query_lower or "отчет" in query_lower:
            return self._handle_show_report()
        elif "сбросить систему" in query_lower or "очистить" in query_lower:
            return self._handle_reset_system()
        else:
            return "Не понял команду. Используйте 'помощь' для получения списка доступных команд."
    
    def _handle_generate_data(self) -> str:
        """Обрабатывает команду создания примера данных."""
        try:
            self.current_data = self.data_system.load_data(
                source_name="synthetic",
                duration_hours=24,
                sampling_rate_minutes=15,
                add_noise=True,
                add_missing_data=True
            )
            info = f"✅ **Пример данных создан!**\n\n"
            info += f"**Информация о данных:**\n"
            info += f"• Показателей: {len(self.current_data.indicators)}\n"
            info += f"• Точек данных: {len(self.current_data.timestamps)}\n"
            info += f"• Период: {self.current_data.timestamps.min().strftime('%Y-%m-%d %H:%M')} - {self.current_data.timestamps.max().strftime('%Y-%m-%d %H:%M')}\n"
            info += f"• Пропущенных данных: {self.current_data.missing_data_mask.sum().sum()}\n\n"
            info += "**Показатели:**\n"
            for ind in self.current_data.indicators:
                info += f"• {ind}\n"
            info += "\nТеперь вы можете выполнить анализ командой 'выполнить анализ'!"
            return info
        except Exception as e:
            return f"❌ Ошибка при создании примера данных: {e}"
    
    def _handle_load_data(self) -> str:
        """Обрабатывает команду загрузки данных."""
        return "Для загрузки данных, пожалуйста, укажите источник (например, 'загрузить csv data.csv' или 'загрузить из базы данных P001')."
    
    def _handle_perform_analysis(self) -> str:
        """Обрабатывает команду выполнения анализа."""
        if not self.current_data:
            return "Пожалуйста, сначала загрузите или создайте данные (например, 'создать пример')."
        try:
            print("🔬 Начинаем квантовый анализ данных...")
            self.analysis_results = self.data_system.perform_analysis(self.current_data)
            return "✅ **Квантовый анализ завершен!**\n\n" \
                   f"**Результаты:**\n" \
                   f"• Квантовая когерентность: {self.analysis_results['quantum_signatures']['quantum_coherence']:.3f}\n" \
                   f"• Обнаружено паттернов: {len(self.analysis_results['temporal_patterns'])}\n" \
                   "\nТеперь вы можете задавать вопросы или запросить отчет!"
        except Exception as e:
            return f"❌ Ошибка при выполнении анализа: {e}"
    
    def _handle_generate_questions(self) -> str:
        """Обрабатывает команду генерации вопросов."""
        if not self.current_data:
            return "Пожалуйста, сначала загрузите или создайте данные (например, 'создать пример')."
        try:
            self.current_questions = self.data_system.generate_questions(self.current_data)
            question_list = "\n".join([f"• {q.priority}] {q.question}" for q in self.current_questions])
            return f"✅ **Сгенерировано {len(self.current_questions)} важных вопросов:**\n{question_list}"
        except Exception as e:
            return f"❌ Ошибка при генерации вопросов: {e}"
    
    def _handle_find_patterns(self) -> str:
        """Обрабатывает команду поиска паттернов."""
        if not self.analysis_results:
            return "Пожалуйста, сначала выполните анализ (например, 'выполнить анализ')."
        patterns = self.analysis_results.get('temporal_patterns', [])
        if not patterns:
            return "Паттерны не обнаружены."
        pattern_str = "\n".join([f"• {p.type}: {p.indicators} ({p.start_time.strftime('%Y-%m-%d %H:%M')} - {p.end_time.strftime('%Y-%m-%d %H:%M')}, уверенность: {p.confidence})" for p in patterns])
        return f"✅ **Обнаружены следующие паттерны:**\n{pattern_str}"
    
    def _handle_find_anomalies(self) -> str:
        """Обрабатывает команду поиска аномалий."""
        if not self.analysis_results:
            return "Пожалуйста, сначала выполните анализ (например, 'выполнить анализ')."
        anomalies = self.analysis_results.get('anomalies', {})
        if not anomalies:
            return "Аномалии не обнаружены."
        anomaly_str = "\n".join([f"• {ind}: {count} аномалий" for ind, count in anomalies.items()])
        return f"✅ **Обнаружены аномалии:**\n{anomaly_str}"
    
    def _handle_predict_changes(self) -> str:
        """Обрабатывает команду предсказания изменений."""
        if not self.current_data:
            return "Пожалуйста, сначала загрузите или создайте данные (например, 'создать пример')."
        try:
            predictions = self.data_system.predict_next_values(self.current_data)
            prediction_str = "\n".join([f"• {ind}: {val:.2f}" for ind, val in predictions.items()])
            return f"🔮 **Предсказания на основе текущих данных:**\n\n{prediction_str}\n\n*Предсказания основаны на трендах последних значений.*"
        except Exception as e:
            return f"❌ Ошибка при предсказании изменений: {e}"
    
    def _handle_show_report(self) -> str:
        """Обрабатывает команду показа отчета."""
        if not self.analysis_results:
            return "Пожалуйста, сначала выполните анализ (например, 'выполнить анализ')."
        report = self.data_system.generate_summary_report(self.analysis_results, self.current_questions)
        return f"📊 **Сводный отчет:**\n\n{report}"
    
    def _handle_reset_system(self) -> str:
        """Обрабатывает команду сброса системы."""
        self.current_data = None
        self.current_questions = []
        self.analysis_results = {}
        self.analyzer.reset()
        return "✅ Система сброшена. Вы можете начать новый анализ."
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Возвращает историю разговора."""
        return self.conversation_history
    
    def clear_conversation_history(self):
        """Очищает историю разговора."""
        self.conversation_history = []
    
    def get_learning_stats(self) -> Dict[str, Any]:
        """Возвращает статистику обучения."""
        return {
            "learned_responses": len(self.learning_data.get("learned_responses", {})),
            "conversation_patterns": len(self.learning_data.get("conversation_patterns", {})),
            "conversation_history_length": len(self.conversation_history),
            "last_learning_update": datetime.now().isoformat()
        }


# Класс для интеграции с системой данных и вопросов
class MedicalDataQuestionSystem:
    """Система для работы с данными и вопросами."""
    
    def __init__(self, analyzer: MQEAAnalyzer):
        self.analyzer = analyzer
        self.data_sources = create_default_sources()
        self.question_generator = QuestionGenerator()
        self.recommendation_engine = MedicalRecommendationEngine()
    
    def load_data(self, source_name: str, **kwargs) -> MedicalTimeSeries:
        """Загружает данные из указанного источника."""
        return self.data_sources[source_name].load_data(**kwargs)
    
    def generate_questions(self, time_series: MedicalTimeSeries) -> List[MedicalQuestion]:
        """Генерирует вопросы на основе данных."""
        return self.question_generator.generate_questions(time_series)
    
    def perform_analysis(self, time_series: MedicalTimeSeries) -> Dict[str, Any]:
        """Выполняет анализ данных."""
        return self.analyzer.quantum_entanglement_analysis(time_series)
    
    def predict_next_values(self, time_series: MedicalTimeSeries) -> Dict[str, float]:
        """Предсказывает следующие значения показателей."""
        predictions = {}
        for indicator in time_series.indicators:
            # Простое предсказание на основе тренда
            values = time_series.data[indicator].dropna()
            if len(values) > 1:
                trend = (values.iloc[-1] - values.iloc[-2]) / (values.index[-1] - values.index[-2]).total_seconds() * 3600
                predictions[indicator] = values.iloc[-1] + trend
            else:
                predictions[indicator] = values.iloc[-1] if len(values) > 0 else 0.0
        return predictions
    
    def generate_summary_report(self, analysis_results: Dict[str, Any], questions: List[MedicalQuestion]) -> str:
        """Генерирует сводный отчет."""
        report = "📊 **СВОДНЫЙ ОТЧЕТ MQEA**\n\n"
        
        # Результаты анализа
        if 'quantum_signatures' in analysis_results:
            coherence = analysis_results['quantum_signatures'].get('quantum_coherence', 0)
            report += f"**Квантовая когерентность:** {coherence:.3f}\n"
        
        # Паттерны
        patterns = analysis_results.get('temporal_patterns', [])
        report += f"**Обнаружено паттернов:** {len(patterns)}\n"
        
        # Аномалии
        anomalies = analysis_results.get('anomalies', {})
        total_anomalies = sum(anomalies.values())
        report += f"**Обнаружено аномалий:** {total_anomalies}\n"
        
        # Вопросы
        report += f"**Сгенерировано вопросов:** {len(questions)}\n"
        
        return report

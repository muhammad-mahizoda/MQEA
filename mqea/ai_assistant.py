"""
Искусственный помощник по анализу MQEA.

Автор: Мухаммад Махизода
Таджикский национальный университет
"""

import re
import json
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import numpy as np
import pandas as pd

from .data_question_integration import MedicalDataQuestionSystem
from .core import MQEAAnalyzer


class MQEAAssistant:
    """Искусственный помощник по анализу MQEA."""
    
    def __init__(self):
        self.system = MedicalDataQuestionSystem()
        self.analyzer = MQEAAnalyzer()
        self.conversation_history = []
        self.current_data = None
        self.analysis_results = None
        
        # База знаний о MQEA
        self.knowledge_base = self._initialize_knowledge_base()
        
        # Шаблоны вопросов и ответов
        self.question_patterns = self._initialize_question_patterns()
        
        # Контекстные ключевые слова
        self.context_keywords = {
            'data_loading': ['загрузить', 'данные', 'файл', 'csv', 'база', 'database'],
            'analysis': ['анализ', 'анализировать', 'квантовый', 'запутанность', 'когерентность'],
            'questions': ['вопрос', 'вопросы', 'сгенерировать', 'генерировать'],
            'patterns': ['паттерн', 'паттерны', 'обнаружить', 'найти'],
            'anomalies': ['аномалия', 'аномалии', 'отклонение', 'проблема'],
            'predictions': ['предсказание', 'прогноз', 'будущее', 'предсказать'],
            'help': ['помощь', 'помочь', 'как', 'что', 'объясни', 'расскажи'],
            'technical': ['технический', 'алгоритм', 'принцип', 'работает', 'функция']
        }
    
    def _initialize_knowledge_base(self) -> Dict[str, Any]:
        """Инициализирует базу знаний о MQEA."""
        
        return {
            'about_mqea': {
                'name': 'Medical Quantum Entanglement Analysis (MQEA)',
                'founder': 'Мухаммад Махизода',
                'institution': 'Таджикский национальный университет',
                'description': 'Революционный алгоритм для анализа многомерных медицинских временных рядов на основе принципов квантовой запутанности',
                'version': '1.0.0'
            },
            'capabilities': [
                'Анализ квантовой запутанности между медицинскими показателями',
                'Заполнение пропущенных данных квантовым методом',
                'Обнаружение скрытых паттернов и корреляций',
                'Генерация важных вопросов для анализа',
                'Предсказание изменений в показателях',
                'Выявление аномалий и критических состояний'
            ],
            'medical_indicators': {
                'heart_rate': 'Частота пульса (уд/мин)',
                'blood_pressure_systolic': 'Систолическое давление (мм рт.ст.)',
                'blood_pressure_diastolic': 'Диастолическое давление (мм рт.ст.)',
                'temperature': 'Температура тела (°C)',
                'oxygen_saturation': 'Насыщение кислородом (%)',
                'respiratory_rate': 'Частота дыхания (дых/мин)',
                'glucose': 'Уровень глюкозы (мг/дл)',
                'cholesterol': 'Уровень холестерина (мг/дл)'
            },
            'data_sources': [
                'Синтетические данные (для тестирования)',
                'CSV файлы (для реальных данных)',
                'База данных SQLite (для больших объемов)',
                'API интеграция (для внешних источников)'
            ],
            'analysis_methods': [
                'Квантовая запутанность - обнаружение скрытых связей',
                'Временная неопределенность - обработка неполных данных',
                'Многомерный анализ - анализ всех показателей как единой системы',
                'Квантовое состояние - представление каждого показателя как квантового состояния',
                'Квантовая интерференция - учет временных задержек между измерениями'
            ]
        }
    
    def _initialize_question_patterns(self) -> Dict[str, List[str]]:
        """Инициализирует шаблоны вопросов и ответов."""
        
        return {
            'greeting': [
                r'привет|здравствуй|hello|hi',
                r'как дела|как поживаешь|как ты'
            ],
            'about_mqea': [
                r'что такое mqea|что такое мкea|расскажи о mqea|расскажи о мкea',
                r'что умеет mqea|что умеет мкea|возможности mqea|возможности мкea',
                r'кто создал mqea|кто создал мкea|автор mqea|автор мкea'
            ],
            'data_loading': [
                r'как загрузить данные|как загрузить файл|загрузить csv|загрузить базу',
                r'какой формат данных|какие поля нужны|структура данных',
                r'создать пример|пример данных|тестовые данные'
            ],
            'analysis': [
                r'как анализировать|выполнить анализ|запустить анализ',
                r'квантовая запутанность|когерентность|квантовый анализ',
                r'что показывает анализ|результаты анализа|интерпретация'
            ],
            'questions': [
                r'сгенерировать вопросы|важные вопросы|какие вопросы',
                r'что спросить|о чем спросить|вопросы для анализа'
            ],
            'patterns': [
                r'найти паттерны|обнаружить паттерны|какие паттерны',
                r'скрытые связи|корреляции|зависимости'
            ],
            'anomalies': [
                r'найти аномалии|обнаружить аномалии|проблемы в данных',
                r'критические значения|отклонения|необычные значения'
            ],
            'predictions': [
                r'предсказать|прогноз|что будет|будущие значения',
                r'тренды|изменения|динамика'
            ],
            'help': [
                r'помощь|помочь|как использовать|инструкция',
                r'что можно делать|возможности|функции'
            ],
            'technical': [
                r'как работает|принцип работы|алгоритм|технические детали',
                r'квантовая механика|запутанность|неопределенность'
            ]
        }
    
    def chat(self, user_input: str) -> str:
        """Основной метод для общения с пользователем."""
        
        # Сохраняем историю разговора
        self.conversation_history.append({
            'timestamp': datetime.now(),
            'user': user_input,
            'assistant': None
        })
        
        # Обрабатываем ввод пользователя
        response = self._process_user_input(user_input)
        
        # Сохраняем ответ
        self.conversation_history[-1]['assistant'] = response
        
        return response
    
    def _process_user_input(self, user_input: str) -> str:
        """Обрабатывает ввод пользователя и генерирует ответ."""
        
        user_input_lower = user_input.lower().strip()
        
        # Определяем тип вопроса
        question_type = self._classify_question(user_input_lower)
        
        # Генерируем ответ
        if question_type == 'greeting':
            return self._handle_greeting()
        elif question_type == 'about_mqea':
            return self._handle_about_mqea()
        elif question_type == 'data_loading':
            return self._handle_data_loading(user_input_lower)
        elif question_type == 'analysis':
            return self._handle_analysis(user_input_lower)
        elif question_type == 'questions':
            return self._handle_questions()
        elif question_type == 'patterns':
            return self._handle_patterns()
        elif question_type == 'anomalies':
            return self._handle_anomalies()
        elif question_type == 'predictions':
            return self._handle_predictions()
        elif question_type == 'help':
            return self._handle_help()
        elif question_type == 'technical':
            return self._handle_technical()
        else:
            return self._handle_unknown_question(user_input)
    
    def _classify_question(self, user_input: str) -> str:
        """Классифицирует тип вопроса пользователя."""
        
        for question_type, patterns in self.question_patterns.items():
            for pattern in patterns:
                if re.search(pattern, user_input):
                    return question_type
        
        return 'unknown'
    
    def _handle_greeting(self) -> str:
        """Обрабатывает приветствие."""
        
        greetings = [
            "Привет! Я ваш помощник по анализу MQEA. Чем могу помочь?",
            "Здравствуйте! Готов помочь с анализом медицинских данных.",
            "Привет! Я здесь, чтобы помочь вам с MQEA анализом.",
            "Добро пожаловать! Я ваш AI-помощник по квантовому анализу медицинских данных."
        ]
        
        return np.random.choice(greetings)
    
    def _handle_about_mqea(self) -> str:
        """Обрабатывает вопросы о MQEA."""
        
        about = self.knowledge_base['about_mqea']
        
        response = f"""🧬⚛️ **{about['name']}**

**Описание:** {about['description']}

**Основатель:** {about['founder']}
**Учреждение:** {about['institution']}
**Версия:** {about['version']}

**Основные возможности:**
"""
        
        for capability in self.knowledge_base['capabilities']:
            response += f"• {capability}\n"
        
        response += "\n**Медицинские показатели:**\n"
        for indicator, description in self.knowledge_base['medical_indicators'].items():
            response += f"• {indicator}: {description}\n"
        
        return response
    
    def _handle_data_loading(self, user_input: str) -> str:
        """Обрабатывает вопросы о загрузке данных."""
        
        if 'пример' in user_input or 'создать' in user_input:
            return self._create_example_data()
        elif 'формат' in user_input or 'структура' in user_input:
            return self._explain_data_format()
        else:
            return self._explain_data_loading()
    
    def _handle_analysis(self, user_input: str) -> str:
        """Обрабатывает вопросы об анализе."""
        
        if self.current_data is None:
            return "Сначала загрузите данные для анализа. Используйте команду 'загрузить данные' или 'создать пример'."
        
        if 'запустить' in user_input or 'выполнить' in user_input:
            return self._perform_analysis()
        else:
            return self._explain_analysis()
    
    def _handle_questions(self) -> str:
        """Обрабатывает вопросы о генерации вопросов."""
        
        if self.current_data is None:
            return "Сначала загрузите данные. Используйте команду 'загрузить данные' или 'создать пример'."
        
        try:
            questions = self.system.generate_questions(max_questions=5)
            
            response = "❓ **Важные вопросы для анализа:**\n\n"
            for i, q in enumerate(questions, 1):
                response += f"{i}. **{q.question}**\n"
                response += f"   Тип: {q.question_type}, Приоритет: {q.priority}\n"
                response += f"   Показатели: {', '.join(q.indicators)}\n\n"
            
            return response
        except Exception as e:
            return f"Ошибка генерации вопросов: {str(e)}"
    
    def _handle_patterns(self) -> str:
        """Обрабатывает вопросы о паттернах."""
        
        if self.analysis_results is None:
            return "Сначала выполните анализ данных. Используйте команду 'выполнить анализ'."
        
        if 'patterns' not in self.analysis_results:
            return "Паттерны не обнаружены в текущих данных."
        
        patterns = self.analysis_results['patterns']
        
        response = f"🔍 **Обнаружено {len(patterns)} паттернов:**\n\n"
        
        # Группируем паттерны по типам
        pattern_types = {}
        for pattern in patterns:
            pattern_type = pattern.pattern_type
            if pattern_type not in pattern_types:
                pattern_types[pattern_type] = []
            pattern_types[pattern_type].append(pattern)
        
        for pattern_type, pattern_list in pattern_types.items():
            response += f"**{pattern_type.upper()}:** {len(pattern_list)} паттернов\n"
            for pattern in pattern_list[:3]:  # Показываем первые 3
                response += f"  • {', '.join(pattern.indicators)} (уверенность: {pattern.confidence:.3f})\n"
            if len(pattern_list) > 3:
                response += f"  • ... и еще {len(pattern_list) - 3} паттернов\n"
            response += "\n"
        
        return response
    
    def _handle_anomalies(self) -> str:
        """Обрабатывает вопросы об аномалиях."""
        
        if self.current_data is None:
            return "Сначала загрузите данные для анализа аномалий."
        
        try:
            # Простой анализ аномалий
            anomalies = []
            for indicator in self.current_data.indicators:
                data = self.current_data.data[indicator].dropna()
                if len(data) > 0:
                    q1, q3 = data.quantile([0.25, 0.75])
                    iqr = q3 - q1
                    lower_bound = q1 - 1.5 * iqr
                    upper_bound = q3 + 1.5 * iqr
                    
                    anomaly_count = len(data[(data < lower_bound) | (data > upper_bound)])
                    if anomaly_count > 0:
                        anomalies.append(f"{indicator}: {anomaly_count} аномалий")
            
            if anomalies:
                response = "⚠️ **Обнаружены аномалии:**\n\n"
                for anomaly in anomalies:
                    response += f"• {anomaly}\n"
                response += "\nРекомендуется внимательно изучить эти показатели."
            else:
                response = "✅ Аномалии не обнаружены. Данные выглядят нормально."
            
            return response
        except Exception as e:
            return f"Ошибка анализа аномалий: {str(e)}"
    
    def _handle_predictions(self) -> str:
        """Обрабатывает вопросы о предсказаниях."""
        
        if self.current_data is None:
            return "Сначала загрузите данные для предсказаний."
        
        try:
            predictions = []
            for indicator in self.current_data.indicators:
                data = self.current_data.data[indicator].dropna()
                if len(data) > 5:
                    # Простое предсказание на основе тренда
                    recent_values = data.tail(5)
                    if len(recent_values) > 1:
                        avg_change = recent_values.diff().mean()
                        last_value = recent_values.iloc[-1]
                        predicted_value = last_value + avg_change
                        predictions.append(f"{indicator}: {predicted_value:.2f}")
            
            if predictions:
                response = "🔮 **Предсказания на основе текущих данных:**\n\n"
                for prediction in predictions:
                    response += f"• {prediction}\n"
                response += "\n*Предсказания основаны на трендах последних значений.*"
            else:
                response = "Недостаточно данных для предсказаний."
            
            return response
        except Exception as e:
            return f"Ошибка предсказаний: {str(e)}"
    
    def _handle_help(self) -> str:
        """Обрабатывает запросы помощи."""
        
        return """🆘 **Помощь по MQEA**

**Основные команды:**
• `загрузить данные` - загрузить данные для анализа
• `создать пример` - создать пример данных
• `выполнить анализ` - запустить квантовый анализ
• `сгенерировать вопросы` - создать важные вопросы
• `найти паттерны` - показать обнаруженные паттерны
• `найти аномалии` - проверить на аномалии
• `предсказать` - сделать предсказания
• `помощь` - показать эту справку

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

Просто задайте вопрос, и я помогу! 😊"""
    
    def _handle_technical(self) -> str:
        """Обрабатывает технические вопросы."""
        
        return """🔬 **Технические детали MQEA**

**Принципы работы:**
• **Квантовая запутанность** - обнаружение скрытых связей между показателями
• **Временная неопределенность** - обработка неполных данных
• **Многомерный анализ** - анализ всех показателей как единой системы
• **Квантовое состояние** - представление каждого показателя как квантового состояния
• **Квантовая интерференция** - учет временных задержек между измерениями

**Алгоритм:**
1. Создание квантовых состояний для каждого показателя
2. Вычисление матрицы запутанности между показателями
3. Анализ квантовой когерентности системы
4. Обнаружение паттернов запутанности
5. Заполнение пропущенных данных квантовым методом

**Математические основы:**
• Использует принципы квантовой механики
• Применяет матрицы запутанности
• Вычисляет квантовую когерентность
• Учитывает временную эволюцию состояний

**Уникальность:**
Это первый в мире алгоритм, применяющий принципы квантовой механики для анализа медицинских данных!"""
    
    def _handle_unknown_question(self, user_input: str) -> str:
        """Обрабатывает неизвестные вопросы."""
        
        responses = [
            "Извините, я не понял ваш вопрос. Попробуйте переформулировать или используйте команду 'помощь'.",
            "Не совсем понятно, что вы имеете в виду. Можете задать более конкретный вопрос?",
            "Я не уверен, как ответить на это. Используйте 'помощь' для списка доступных команд.",
            "Попробуйте задать вопрос по-другому или используйте команду 'помощь' для справки."
        ]
        
        return np.random.choice(responses)
    
    def _create_example_data(self) -> str:
        """Создает пример данных."""
        
        try:
            self.current_data = self.system.load_data(
                source_name="synthetic",
                duration_hours=12,
                sampling_rate_minutes=30,
                add_noise=True,
                add_missing_data=True
            )
            
            response = f"""✅ **Пример данных создан!**

**Информация о данных:**
• Показателей: {len(self.current_data.indicators)}
• Точек данных: {len(self.current_data.timestamps)}
• Период: {self.current_data.timestamps[0].strftime('%Y-%m-%d %H:%M')} - {self.current_data.timestamps[-1].strftime('%Y-%m-%d %H:%M')}
• Пропущенных данных: {self.current_data.missing_data_mask.sum().sum()}

**Показатели:**
"""
            for indicator in self.current_data.indicators:
                response += f"• {indicator}\n"
            
            response += "\nТеперь вы можете выполнить анализ командой 'выполнить анализ'!"
            
            return response
        except Exception as e:
            return f"Ошибка создания примера данных: {str(e)}"
    
    def _explain_data_format(self) -> str:
        """Объясняет формат данных."""
        
        return """📋 **Формат данных для MQEA**

**Обязательные поля:**
• `heart_rate` - Частота пульса (уд/мин)
• `blood_pressure_systolic` - Систолическое давление (мм рт.ст.)
• `blood_pressure_diastolic` - Диастолическое давление (мм рт.ст.)
• `temperature` - Температура тела (°C)
• `oxygen_saturation` - Насыщение кислородом (%)
• `respiratory_rate` - Частота дыхания (дых/мин)

**Дополнительные поля:**
• `glucose` - Уровень глюкозы (мг/дл)
• `cholesterol` - Уровень холестерина (мг/дл)

**Временные метки:**
• `timestamp` - Время измерения (YYYY-MM-DD HH:MM:SS)

**Пример CSV:**
```
timestamp,heart_rate,blood_pressure_systolic,blood_pressure_diastolic,temperature,oxygen_saturation,respiratory_rate
2024-01-01 00:00:00,75,120,80,36.5,98,16
2024-01-01 00:30:00,78,122,82,36.6,97,17
```

Используйте команду 'создать пример' для генерации тестовых данных!"""
    
    def _explain_data_loading(self) -> str:
        """Объясняет загрузку данных."""
        
        return """📊 **Загрузка данных в MQEA**

**Способы загрузки:**
1. **Синтетические данные** - используйте команду 'создать пример'
2. **CSV файлы** - загрузите файл с медицинскими данными
3. **База данных** - подключитесь к SQLite базе данных
4. **API** - подключитесь к внешнему API

**Рекомендации:**
• Начните с синтетических данных для тестирования
• Убедитесь, что данные содержат временные метки
• Пропущенные значения будут заполнены автоматически
• Минимум 10 точек данных для качественного анализа

**Команды:**
• 'создать пример' - создать тестовые данные
• 'загрузить данные' - загрузить из файла
• 'формат данных' - показать требуемый формат"""
    
    def _explain_analysis(self) -> str:
        """Объясняет анализ."""
        
        return """🔬 **Квантовый анализ MQEA**

**Что происходит при анализе:**
1. **Заполнение пропусков** - квантовый метод восстановления данных
2. **Создание квантовых состояний** - каждый показатель как квантовое состояние
3. **Вычисление запутанности** - поиск скрытых связей между показателями
4. **Анализ когерентности** - оценка целостности системы
5. **Обнаружение паттернов** - поиск значимых закономерностей

**Результаты анализа:**
• Квантовая когерентность (0-1, чем выше, тем лучше)
• Матрица запутанности между показателями
• Обнаруженные паттерны и их типы
• Критические периоды и аномалии

**Команды:**
• 'выполнить анализ' - запустить полный анализ
• 'найти паттерны' - показать обнаруженные паттерны
• 'найти аномалии' - проверить на отклонения"""
    
    def _perform_analysis(self) -> str:
        """Выполняет анализ данных."""
        
        if self.current_data is None:
            return "Сначала загрузите данные командой 'создать пример' или 'загрузить данные'."
        
        try:
            self.analysis_results = self.system.analyze_data(
                quantum_threshold=0.3,
                fill_missing=True
            )
            
            response = f"""✅ **Анализ завершен!**

**Результаты:**
• Квантовая когерентность: {self.analysis_results.get('quantum_signatures', {}).get('quantum_coherence', 0):.3f}
• Окон анализа: {len(self.analysis_results.get('quantum_entanglements', []))}
• Обнаружено паттернов: {len(self.analysis_results.get('patterns', []))}

**Что дальше:**
• 'найти паттерны' - показать обнаруженные паттерны
• 'найти аномалии' - проверить на отклонения
• 'сгенерировать вопросы' - создать важные вопросы
• 'предсказать' - сделать предсказания"""
            
            return response
        except Exception as e:
            return f"Ошибка анализа: {str(e)}"
    
    def get_conversation_history(self) -> List[Dict]:
        """Возвращает историю разговора."""
        return self.conversation_history
    
    def clear_history(self):
        """Очищает историю разговора."""
        self.conversation_history = []
    
    def get_status(self) -> Dict[str, Any]:
        """Возвращает текущий статус помощника."""
        return {
            'has_data': self.current_data is not None,
            'has_analysis': self.analysis_results is not None,
            'conversation_length': len(self.conversation_history),
            'data_indicators': len(self.current_data.indicators) if self.current_data else 0,
            'data_points': len(self.current_data.timestamps) if self.current_data else 0
        }

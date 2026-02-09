"""
Улучшенный веб-интерфейс MQEA с интегрированным AI-помощником.

Автор: Мухаммад Махизода
Таджикский национальный университет
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import sys
import os
from datetime import datetime, timedelta
import time

# Добавляем путь к модулям
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Импорты MQEA
from mqea import MQEAAnalyzer, MQEAAssistant

# Настройки страницы
st.set_page_config(
    page_title="MQEA - Medical Quantum Entanglement Analysis",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Инициализация состояния сессии
def initialize_session_state():
    """Инициализирует состояние сессии."""
    if 'analyzer' not in st.session_state:
        st.session_state.analyzer = MQEAAnalyzer()
    if 'assistant' not in st.session_state:
        st.session_state.assistant = MQEAAssistant()
    if 'current_data' not in st.session_state:
        st.session_state.current_data = None
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []
    if 'show_chat' not in st.session_state:
        st.session_state.show_chat = False

# Инициализация
initialize_session_state()

# Заголовок приложения
st.title("🧬 MQEA - Medical Quantum Entanglement Analysis")
st.markdown("**Революционный алгоритм для анализа медицинских данных на основе принципов квантовой запутанности**")

# Информация об основателе
with st.expander("ℹ️ Информация об основателе"):
    st.markdown("""
    **Основатель и разработчик:** Мухаммад Махизода  
    **Должность:** Администратор сети  
    **Университет:** Таджикский национальный университет  
    **Email:** muhammad.mahizoda@tnu.tj
    """)

# Главная навигация
tab1, tab2, tab3, tab4 = st.tabs(["📊 Анализ данных", "🤖 AI-Помощник", "📈 Результаты", "⚙️ Настройки"])

# Вкладка 1: Анализ данных
with tab1:
    st.header("📊 Анализ медицинских данных")
    
    # Боковая панель для настроек
    with st.sidebar:
        st.subheader("⚙️ Настройки анализа")
        
        # Выбор режима работы
        analysis_mode = st.selectbox(
            "Режим анализа",
            ["Генерация данных", "Загрузка файла"],
            help="Выберите способ получения данных для анализа"
        )
        
        if analysis_mode == "Генерация данных":
            # Параметры генерации
            duration_hours = st.slider("Продолжительность (часы)", 1, 48, 24)
            sampling_minutes = st.slider("Интервал выборки (минуты)", 5, 60, 15)
            add_noise = st.checkbox("Добавить шум", value=True)
            add_missing = st.checkbox("Добавить пропущенные данные", value=True)
            
            # Профиль пациента
            st.subheader("👤 Профиль пациента")
            patient_profile = {}
            
            col1, col2 = st.columns(2)
            with col1:
                patient_profile['heart_rate'] = st.number_input("Частота пульса", 40, 120, 75)
                patient_profile['blood_pressure_systolic'] = st.number_input("Систолическое давление", 80, 200, 120)
                patient_profile['blood_pressure_diastolic'] = st.number_input("Диастолическое давление", 50, 120, 80)
                patient_profile['temperature'] = st.number_input("Температура", 35.0, 40.0, 36.5, 0.1)
            
            with col2:
                patient_profile['oxygen_saturation'] = st.number_input("Насыщение кислородом", 85, 100, 98)
                patient_profile['respiratory_rate'] = st.number_input("Частота дыхания", 8, 30, 16)
                patient_profile['glucose'] = st.number_input("Уровень глюкозы", 50, 200, 90)
                patient_profile['cholesterol'] = st.number_input("Уровень холестерина", 100, 300, 180)
        
        else:  # Загрузка файла
            uploaded_file = st.file_uploader(
                "Загрузите CSV файл с медицинскими данными",
                type=['csv'],
                help="Файл должен содержать колонки: timestamp, heart_rate, blood_pressure_systolic, blood_pressure_diastolic, temperature, oxygen_saturation, respiratory_rate"
            )
        
        # Настройки анализа
        st.subheader("🔬 Параметры анализа")
        quantum_threshold = st.slider("Порог квантовой запутанности", 0.1, 0.9, 0.3, 0.1)
        fill_missing = st.checkbox("Заполнить пропущенные данные", value=True)
        max_iterations = st.slider("Максимум итераций заполнения", 10, 100, 50)
        
        # Кнопки управления
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🚀 Запустить анализ", type="primary"):
                run_analysis()
        
        with col2:
            if st.button("🔄 Сбросить", type="secondary"):
                reset_analysis()
        
        # Дополнительные функции
        st.subheader("🔧 Дополнительные функции")
        
        if st.button("📊 Создать пример данных"):
            create_sample_data()
        
        if st.button("🔍 Быстрый анализ"):
            quick_analysis()
        
        if st.button("📈 Показать статистику"):
            show_statistics()
            with st.spinner("Выполняется анализ..."):
                try:
                    if analysis_mode == "Генерация данных":
                        # Генерация синтетических данных
                        st.session_state.current_data = st.session_state.analyzer.generate_synthetic_data(
                            duration_hours=duration_hours,
                            sampling_rate_minutes=sampling_minutes,
                            add_noise=add_noise,
                            add_missing_data=add_missing,
                            patient_profile=patient_profile
                        )
                    else:
                        # Загрузка из файла
                        if uploaded_file is not None:
                            df = pd.read_csv(uploaded_file)
                            df['timestamp'] = pd.to_datetime(df['timestamp'])
                            df.set_index('timestamp', inplace=True)
                            
                            # Создание объекта временного ряда
                            from mqea.data_processor import MedicalTimeSeries
                            missing_mask = df.isnull()
                            
                            st.session_state.current_data = MedicalTimeSeries(
                                data=df,
                                indicators=list(df.columns),
                                timestamps=df.index,
                                missing_data_mask=missing_mask,
                                quantum_states={},
                                metadata={'source': 'uploaded_file'}
                            )
                        else:
                            st.error("Пожалуйста, загрузите файл")
                            st.stop()
                    
                    # Выполнение анализа
                    if fill_missing and st.session_state.current_data.missing_data_mask.sum().sum() > 0:
                        st.session_state.current_data = st.session_state.analyzer.fill_missing_data(
                            st.session_state.current_data, 
                            method='quantum',
                            max_iterations=max_iterations
                        )
                    
                    st.session_state.analysis_results = st.session_state.analyzer.quantum_entanglement_analysis(
                        st.session_state.current_data, 
                        quantum_threshold
                    )
                    
                    st.success("✅ Анализ завершен успешно!")
                    
                except Exception as e:
                    st.error(f"❌ Ошибка анализа: {str(e)}")
    
    # Отображение данных
    if st.session_state.current_data is not None:
        st.subheader("📋 Информация о данных")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Показателей", len(st.session_state.current_data.indicators))
        with col2:
            st.metric("Точек данных", len(st.session_state.current_data.timestamps))
        with col3:
            missing_count = st.session_state.current_data.missing_data_mask.sum().sum()
            st.metric("Пропущенных данных", missing_count)
        with col4:
            if st.session_state.analysis_results:
                coherence = st.session_state.analysis_results.get('quantum_signatures', {}).get('quantum_coherence', 0)
                st.metric("Квантовая когерентность", f"{coherence:.3f}")
        
        # График временных рядов
        st.subheader("📈 Временные ряды")
        
        # Переводы названий показателей
        indicator_translations = {
            'heart_rate': 'Частота пульса',
            'blood_pressure_systolic': 'Систолическое давление',
            'blood_pressure_diastolic': 'Диастолическое давление',
            'temperature': 'Температура тела',
            'oxygen_saturation': 'Насыщение кислородом',
            'respiratory_rate': 'Частота дыхания',
            'glucose': 'Уровень глюкозы',
            'cholesterol': 'Уровень холестерина'
        }
        
        # Создание графика
        fig = go.Figure()
        
        for indicator in st.session_state.current_data.indicators[:4]:  # Показываем первые 4 показателя
            display_name = indicator_translations.get(indicator, indicator.replace('_', ' ').title())
            fig.add_trace(go.Scatter(
                x=st.session_state.current_data.timestamps,
                y=st.session_state.current_data.data[indicator],
                mode='lines+markers',
                name=display_name,
                line=dict(width=2)
            ))
        
        fig.update_layout(
            title="Медицинские показатели во времени",
            xaxis_title="Время",
            yaxis_title="Значение",
            hovermode='x unified',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Таблица данных
        st.subheader("📊 Таблица данных")
        display_data = st.session_state.current_data.data.copy()
        display_data.columns = [indicator_translations.get(col, col) for col in display_data.columns]
        st.dataframe(display_data.head(20), use_container_width=True)

# Вкладка 2: AI-Помощник
with tab2:
    st.header("🤖 AI-Помощник MQEA")
    st.markdown("**Ваш интеллектуальный помощник по анализу медицинских данных**")
    
    # Область чата
    chat_container = st.container()
    
    with chat_container:
        # Отображение сообщений чата
        for message in st.session_state.chat_messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Поле ввода
        if user_input := st.chat_input("Задайте вопрос AI-помощнику..."):
            # Добавляем сообщение пользователя
            st.session_state.chat_messages.append({
                "role": "user",
                "content": user_input
            })
            
            # Получаем ответ от помощника
            try:
                response = st.session_state.assistant.chat(user_input)
                
                # Добавляем ответ помощника
                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": response
                })
                
                # Обновляем интерфейс
                st.rerun()
                
            except Exception as e:
                error_message = f"❌ Ошибка: {str(e)}"
                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": error_message
                })
                st.rerun()
    
    # Боковая панель для быстрых команд
    with st.sidebar:
        st.subheader("⚡ Быстрые команды")
        
        if st.button("👋 Приветствие"):
            process_chat_message("Привет!")
        
        if st.button("📚 Что такое MQEA?"):
            process_chat_message("Что такое MQEA?")
        
        if st.button("📊 Создать пример данных"):
            process_chat_message("Создай пример данных")
        
        if st.button("🔬 Выполнить анализ"):
            process_chat_message("Выполни анализ")
        
        if st.button("❓ Сгенерировать вопросы"):
            process_chat_message("Сгенерируй вопросы")
        
        if st.button("🔍 Найти паттерны"):
            process_chat_message("Найди паттерны")
        
        if st.button("⚠️ Найти аномалии"):
            process_chat_message("Найди аномалии")
        
        if st.button("🔮 Предсказать"):
            process_chat_message("Предскажи изменения")
        
        if st.button("🆘 Помощь"):
            process_chat_message("Помощь")
        
        # Управление чатом
        st.subheader("🎛️ Управление")
        
        if st.button("🔄 Очистить чат"):
            st.session_state.chat_messages = []
            st.session_state.assistant.clear_history()
            st.rerun()
        
        if st.button("📊 Показать статус"):
            show_assistant_status()

# Вкладка 3: Результаты
with tab3:
    st.header("📈 Результаты анализа")
    
    if st.session_state.analysis_results is not None:
        # Квантовая когерентность
        if 'quantum_signatures' in st.session_state.analysis_results:
            coherence = st.session_state.analysis_results['quantum_signatures'].get('quantum_coherence', 0)
            st.metric("Квантовая когерентность", f"{coherence:.3f}")
        
        # Матрица запутанности
        if 'quantum_entanglements' in st.session_state.analysis_results:
            entanglements = st.session_state.analysis_results['quantum_entanglements']
            st.subheader("🔗 Квантовая запутанность")
            st.write(f"Обнаружено {len(entanglements)} окон квантовой запутанности")
            
            # Показываем последнее окно
            if entanglements:
                latest = entanglements[-1]
                if isinstance(latest, dict) and 'entanglement_matrix' in latest:
                    matrix = latest['entanglement_matrix']
                    
                    # Создаем тепловую карту
                    fig = go.Figure(data=go.Heatmap(
                        z=matrix,
                        x=st.session_state.current_data.indicators,
                        y=st.session_state.current_data.indicators,
                        colorscale='Viridis'
                    ))
                    
                    fig.update_layout(
                        title="Матрица квантовой запутанности",
                        height=500
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
        
        # Паттерны
        patterns = st.session_state.analyzer.detect_patterns(st.session_state.current_data)
        if patterns:
            st.subheader("🔍 Обнаруженные паттерны")
            st.write(f"Найдено {len(patterns)} паттернов")
            
            # Группируем по типам
            pattern_types = {}
            for pattern in patterns:
                pattern_type = pattern.pattern_type
                if pattern_type not in pattern_types:
                    pattern_types[pattern_type] = []
                pattern_types[pattern_type].append(pattern)
            
            for pattern_type, pattern_list in pattern_types.items():
                with st.expander(f"{pattern_type.upper()} ({len(pattern_list)} паттернов)"):
                    for i, pattern in enumerate(pattern_list[:5]):  # Показываем первые 5
                        st.write(f"{i+1}. {', '.join(pattern.indicators)} (уверенность: {pattern.confidence:.3f})")
    
    else:
        st.info("Сначала выполните анализ данных на вкладке 'Анализ данных'")

# Вкладка 4: Настройки
with tab4:
    st.header("⚙️ Настройки системы")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔬 Параметры анализа")
        
        # Настройки квантового анализа
        st.number_input("Постоянная Планка (hbar)", 0.1, 2.0, 1.0, 0.1, key="hbar")
        st.number_input("Порог запутанности", 0.1, 0.9, 0.3, 0.1, key="entanglement_threshold")
        st.number_input("Порог паттернов", 0.1, 0.9, 0.4, 0.1, key="pattern_threshold")
        
        # Настройки заполнения пропусков
        st.checkbox("Включить квантовое заполнение", value=True, key="enable_quantum_imputation")
        st.checkbox("Включить обнаружение паттернов", value=True, key="enable_pattern_detection")
    
    with col2:
        st.subheader("🎨 Настройки интерфейса")
        
        # Настройки отображения
        st.selectbox("Тема", ["Светлая", "Темная"], key="theme")
        st.selectbox("Язык", ["Русский", "English"], key="language")
        st.number_input("Количество строк в таблице", 10, 100, 20, key="table_rows")
        
        # Настройки AI-помощника
        st.subheader("🤖 AI-Помощник")
        st.checkbox("Автоматические подсказки", value=True, key="auto_suggestions")
        st.checkbox("Детальные ответы", value=True, key="detailed_responses")
        st.number_input("Максимум сообщений в чате", 50, 500, 100, key="max_chat_messages")

# Вспомогательные функции
def process_chat_message(message):
    """Обрабатывает сообщение чата."""
    st.session_state.chat_messages.append({
        "role": "user",
        "content": message
    })
    
    try:
        response = st.session_state.assistant.chat(message)
        st.session_state.chat_messages.append({
            "role": "assistant",
            "content": response
        })
        st.rerun()
    except Exception as e:
        st.session_state.chat_messages.append({
            "role": "assistant",
            "content": f"❌ Ошибка: {str(e)}"
        })
        st.rerun()

def show_assistant_status():
    """Показывает статус AI-помощника."""
    status = st.session_state.assistant.get_status()
    
    st.subheader("📊 Статус AI-помощника")
    st.metric("Данные загружены", "Да" if status['has_data'] else "Нет")
    st.metric("Анализ выполнен", "Да" if status['has_analysis'] else "Нет")
    st.metric("Сообщений в чате", status['conversation_length'])
    
    if status['has_data']:
        st.metric("Показателей", status['data_indicators'])
        st.metric("Точек данных", status['data_points'])

# Футер
st.markdown("---")
st.markdown("**MQEA - Medical Quantum Entanglement Analysis** | **Автор:** Мухаммад Махизода | **Таджикский национальный университет**")

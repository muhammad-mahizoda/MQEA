#!/usr/bin/env python3
"""
Упрощенный веб-интерфейс MQEA без медицинской диагностической системы
для избежания ошибок импорта.

Автор: Мухаммад Махизода
Таджикский национальный университет
"""

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import sys
import os
from datetime import datetime, timedelta
import time
import uuid

# Добавляем путь к модулям
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Импорты MQEA
from mqea import (
    MQEAAnalyzer, 
    MedicalRecommendationEngine,
    PatientProfile,
    Gender,
    ActivityLevel,
    MedicalHistory
)
from mqea.enhanced_ai_assistant import EnhancedMQEAAssistant

def generate_patient_id():
    """Генерирует последовательный ID для пациента (P001, P002, P003...)"""
    if 'patient_counter' not in st.session_state:
        st.session_state.patient_counter = 1
    else:
        st.session_state.patient_counter += 1
    return f"P{st.session_state.patient_counter:03d}"

def get_next_patient_number():
    """Получает следующий номер пациента из сессии"""
    if 'patient_counter' not in st.session_state:
        st.session_state.patient_counter = 1
    else:
        st.session_state.patient_counter += 1
    return st.session_state.patient_counter

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
        st.session_state.assistant = EnhancedMQEAAssistant(st.session_state.analyzer)
    if 'recommendation_engine' not in st.session_state:
        st.session_state.recommendation_engine = MedicalRecommendationEngine()
    if 'patient_profiles' not in st.session_state:
        st.session_state.patient_profiles = []
    if 'current_patient_profile' not in st.session_state:
        st.session_state.current_patient_profile = None
    if 'current_data' not in st.session_state:
        st.session_state.current_data = None
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    if 'recommendations' not in st.session_state:
        st.session_state.recommendations = []
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []
    if 'show_chat' not in st.session_state:
        st.session_state.show_chat = False
    if 'show_print_info' not in st.session_state:
        st.session_state.show_print_info = False

# Вспомогательные функции
def run_analysis():
    """Запускает полный анализ данных."""
    with st.spinner("Выполняется анализ..."):
        try:
            analysis_mode = st.session_state.get('analysis_mode', 'Генерация данных')
            
            if analysis_mode == "Генерация данных":
                # Генерация синтетических данных
                duration_hours = st.session_state.get('duration_hours', 24)
                sampling_minutes = st.session_state.get('sampling_minutes', 15)
                add_noise = st.session_state.get('add_noise', True)
                add_missing = st.session_state.get('add_missing', True)
                patient_profile = st.session_state.get('patient_profile', {})
                
                st.session_state.current_data = st.session_state.analyzer.generate_synthetic_data(
                    duration_hours=duration_hours,
                    sampling_rate_minutes=sampling_minutes,
                    add_noise=add_noise,
                    add_missing_data=add_missing,
                    patient_profile=patient_profile
                )
            else:
                # Загрузка из файла
                uploaded_file = st.session_state.get('uploaded_file')
                if uploaded_file is not None:
                    df = pd.read_csv(uploaded_file)
                    
                    # Проверяем наличие колонки timestamp
                    if 'timestamp' in df.columns:
                        df['timestamp'] = pd.to_datetime(df['timestamp'])
                        df.set_index('timestamp', inplace=True)
                    else:
                        # Создаем временные метки автоматически
                        st.warning("⚠️ Колонка 'timestamp' не найдена. Создаем временные метки автоматически.")
                        start_time = datetime.now() - timedelta(hours=24)
                        df['timestamp'] = pd.date_range(
                            start=start_time,
                            periods=len(df),
                            freq='15T'  # 15 минут
                        )
                        df.set_index('timestamp', inplace=True)
                    
                    # Проверяем совместимость колонок с медицинскими показателями
                    expected_indicators = [
                        'heart_rate', 'blood_pressure_systolic', 'blood_pressure_diastolic',
                        'temperature', 'oxygen_saturation', 'respiratory_rate',
                        'glucose', 'cholesterol'
                    ]
                    
                    available_indicators = [col for col in df.columns if col in expected_indicators]
                    if not available_indicators:
                        st.error("❌ В файле не найдены совместимые медицинские показатели. Ожидаемые колонки: " + ", ".join(expected_indicators))
                        return
                    
                    # Фильтруем только совместимые колонки
                    df_filtered = df[available_indicators].copy()
                    
                    # Создание объекта временного ряда
                    from mqea.data_processor import MedicalTimeSeries
                    missing_mask = df_filtered.isnull()
                    
                    st.session_state.current_data = MedicalTimeSeries(
                        data=df_filtered,
                        indicators=available_indicators,
                        timestamps=df.index,
                        missing_data_mask=missing_mask,
                        quantum_states={},
                        metadata={'source': 'uploaded_file', 'original_columns': list(df.columns)}
                    )
                    
                    st.success(f"✅ Данные загружены: {len(available_indicators)} совместимых показателей")
                else:
                    st.error("Пожалуйста, загрузите файл")
                    return
            
            # Выполнение анализа
            fill_missing = st.session_state.get('fill_missing', True)
            max_iterations = st.session_state.get('max_iterations', 50)
            
            if fill_missing and st.session_state.current_data.missing_data_mask.sum().sum() > 0:
                st.session_state.current_data = st.session_state.analyzer.fill_missing_data(
                    st.session_state.current_data, 
                    method='quantum',
                    max_iterations=max_iterations
                )
            
            quantum_threshold = st.session_state.get('quantum_threshold', 0.3)
            st.session_state.analysis_results = st.session_state.analyzer.quantum_entanglement_analysis(
                st.session_state.current_data, 
                quantum_threshold
            )
            
            # Генерируем медицинские рекомендации с учетом профиля пациента
            if st.session_state.current_patient_profile:
                # Создаем новый движок рекомендаций с профилем пациента
                personalized_engine = MedicalRecommendationEngine(st.session_state.current_patient_profile)
                st.session_state.recommendations = personalized_engine.analyze_patient_data(
                    st.session_state.current_data,
                    st.session_state.analysis_results
                )
            else:
                # Используем стандартный движок без профиля
                st.session_state.recommendations = st.session_state.recommendation_engine.analyze_patient_data(
                    st.session_state.current_data,
                    st.session_state.analysis_results
                )
            
            st.success("✅ Анализ завершен успешно!")
            
        except Exception as e:
            st.error(f"❌ Ошибка анализа: {str(e)}")

def reset_analysis():
    """Сбрасывает текущий анализ."""
    st.session_state.current_data = None
    st.session_state.analysis_results = None
    st.session_state.analyzer.reset()
    st.success("🔄 Анализ сброшен")

def create_sample_data():
    """Создает пример данных для демонстрации."""
    with st.spinner("Создаем пример данных..."):
        try:
            st.session_state.current_data = st.session_state.analyzer.generate_synthetic_data(
                duration_hours=24,
                sampling_rate_minutes=15,
                add_noise=True,
                add_missing_data=True
            )
            st.success("✅ Пример данных создан!")
        except Exception as e:
            st.error(f"❌ Ошибка создания данных: {str(e)}")

def quick_analysis():
    """Выполняет быстрый анализ."""
    if st.session_state.current_data is None:
        st.warning("Сначала создайте или загрузите данные")
        return
    
    with st.spinner("Выполняется быстрый анализ..."):
        try:
            st.session_state.analysis_results = st.session_state.analyzer.quantum_entanglement_analysis(
                st.session_state.current_data, 
                quantum_threshold=0.3
            )
            st.success("✅ Быстрый анализ завершен!")
        except Exception as e:
            st.error(f"❌ Ошибка анализа: {str(e)}")

def show_statistics():
    """Показывает статистику данных."""
    if st.session_state.current_data is None:
        st.warning("Нет данных для анализа")
        return
    
    st.subheader("📊 Статистика данных")
    
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

def process_chat_message(message):
    """Обрабатывает сообщение чата."""
    st.session_state.chat_messages.append({
        "role": "user",
        "content": message
    })
    
    try:
        response = st.session_state.assistant.process_query(message)
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
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Анализ данных", 
    "👤 Профиль пациента", 
    "🤖 AI-Помощник", 
    "📈 Результаты", 
    "💊 Рекомендации", 
    "⚙️ Настройки"
])

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
        st.session_state.analysis_mode = analysis_mode
        
        if analysis_mode == "Генерация данных":
            # Параметры генерации
            duration_hours = st.slider("Продолжительность (часы)", 1, 48, 24)
            sampling_minutes = st.slider("Интервал выборки (минуты)", 5, 60, 15)
            add_noise = st.checkbox("Добавить шум", value=True)
            add_missing = st.checkbox("Добавить пропущенные данные", value=True)
            
            # Сохраняем в session_state
            st.session_state.duration_hours = duration_hours
            st.session_state.sampling_minutes = sampling_minutes
            st.session_state.add_noise = add_noise
            st.session_state.add_missing = add_missing
            
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
                patient_profile['glucose'] = st.number_input("Уровень глюкозы (ммоль/л)", 2.0, 15.0, 5.0)
                patient_profile['cholesterol'] = st.number_input("Уровень холестерина", 100, 300, 180)
            
            st.session_state.patient_profile = patient_profile
        
        else:  # Загрузка файла
            uploaded_file = st.file_uploader(
                "Загрузите CSV файл с медицинскими данными",
                type=['csv'],
                help="Файл должен содержать колонки с медицинскими показателями. Колонка 'timestamp' опциональна - если отсутствует, будет создана автоматически."
            )
            st.session_state.uploaded_file = uploaded_file
            
            if uploaded_file is not None:
                # Показываем информацию о загруженном файле
                try:
                    df_preview = pd.read_csv(uploaded_file)
                    st.success(f"✅ Файл загружен: {len(df_preview)} строк, {len(df_preview.columns)} колонок")
                    st.write("**Колонки в файле:**")
                    st.write(list(df_preview.columns))
                    
                    # Показываем первые строки
                    st.write("**Предварительный просмотр:**")
                    st.dataframe(df_preview.head(5))
                    
                except Exception as e:
                    st.error(f"❌ Ошибка чтения файла: {str(e)}")
        
        # Настройки анализа
        st.subheader("🔬 Параметры анализа")
        quantum_threshold = st.slider("Порог квантовой запутанности", 0.1, 0.9, 0.3, 0.1)
        fill_missing = st.checkbox("Заполнить пропущенные данные", value=True)
        max_iterations = st.slider("Максимум итераций заполнения", 10, 100, 50)
        
        # Сохраняем в session_state
        st.session_state.quantum_threshold = quantum_threshold
        st.session_state.fill_missing = fill_missing
        st.session_state.max_iterations = max_iterations
        
        # Кнопки управления
        st.subheader("🎮 Управление")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🚀 Запустить анализ", type="primary", key="main_run_analysis"):
                run_analysis()
        
        with col2:
            if st.button("🔄 Сбросить", type="secondary", key="main_reset"):
                reset_analysis()
        
        # Дополнительные функции
        st.subheader("🔧 Дополнительные функции")
        
        if st.button("📊 Создать пример данных", key="main_create_sample"):
            create_sample_data()
        
        if st.button("🔍 Быстрый анализ", key="main_quick_analysis"):
            quick_analysis()
        
        if st.button("📈 Показать статистику", key="main_show_stats"):
            show_statistics()
    
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
    
    else:
        st.info("👆 Выберите режим анализа и настройте параметры в боковой панели, затем нажмите 'Запустить анализ'")

# Остальные вкладки остаются без изменений...
# (Профиль пациента, AI-Помощник, Результаты, Рекомендации, Настройки)

# Футер
st.markdown("---")
st.markdown("**MQEA - Medical Quantum Entanglement Analysis** | **Автор:** Мухаммад Махизода | **Таджикский национальный университет**")

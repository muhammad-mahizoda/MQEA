#!/usr/bin/env python3
"""
Единый главный интерфейс MQEA со всеми функциями на одном экране.

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
from utils.logo_utils import display_main_logo, display_sidebar_logo


def generate_patient_id():
    """Генерирует последовательный ID для пациента (P001, P002, P003...)"""
    if 'patient_counter' not in st.session_state:
        st.session_state.patient_counter = 1
    else:
        st.session_state.patient_counter += 1
    return f"P{st.session_state.patient_counter:03d}"

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
                            freq='15min'  # 15 минут
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

# Главный интерфейс - все функции на одном экране
st.markdown("---")

# Секция 1: Быстрые действия
st.header("⚡ Быстрые действия")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("🚀 Запустить анализ", type="primary", key="run_analysis"):
        run_analysis()

with col2:
    if st.button("🔄 Сбросить", type="secondary", key="reset_analysis"):
        st.session_state.current_data = None
        st.session_state.analysis_results = None
        st.session_state.analyzer.reset()
        st.success("🔄 Анализ сброшен")
        st.rerun()

with col3:
    if st.button("👤 Создать профиль", key="create_profile"):
        st.session_state.show_profile_creation = True

with col4:
    if st.button("👥 Управление профилей", key="manage_profiles"):
        st.session_state.show_profile_management = True

with col5:
    if st.button("💬 AI-Помощник", key="open_chat"):
        st.session_state.show_chat = not st.session_state.show_chat

# Секция 2: Настройки анализа
st.markdown("---")
st.header("🔬 Настройки анализа")

# Режим анализа
analysis_mode = st.selectbox(
    "📊 Режим анализа:",
    ["Генерация данных", "Загрузка файла"],
    help="Выберите способ получения данных для анализа"
)
st.session_state.analysis_mode = analysis_mode

if analysis_mode == "Генерация данных":
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.subheader("⏱️ Временные параметры")
        duration_hours = st.slider("Продолжительность (часы)", 1, 48, 24)
        sampling_minutes = st.slider("Интервал выборки (минуты)", 5, 60, 15)
        st.session_state.duration_hours = duration_hours
        st.session_state.sampling_minutes = sampling_minutes
    
    with col2:
        st.subheader("🎲 Качество данных")
        add_noise = st.checkbox("Добавить шум", value=True)
        add_missing = st.checkbox("Добавить пропущенные данные", value=True)
        st.session_state.add_noise = add_noise
        st.session_state.add_missing = add_missing
    
    with col3:
        st.subheader("👤 Профиль пациента")
        patient_profile = {}
        patient_profile['heart_rate'] = st.number_input("Частота пульса", 40, 120, 75)
        patient_profile['blood_pressure_systolic'] = st.number_input("Систолическое давление", 80, 200, 120)
        patient_profile['blood_pressure_diastolic'] = st.number_input("Диастолическое давление", 50, 120, 80)
        patient_profile['temperature'] = st.number_input("Температура", 35.0, 40.0, 36.5, 0.1)
        st.session_state.patient_profile = patient_profile
    
    with col4:
        st.subheader("🔬 Параметры анализа")
        quantum_threshold = st.slider("Порог квантовой запутанности", 0.1, 0.9, 0.3, 0.1)
        fill_missing = st.checkbox("Заполнить пропущенные данные", value=True)
        max_iterations = st.slider("Максимум итераций заполнения", 10, 100, 50)
        st.session_state.quantum_threshold = quantum_threshold
        st.session_state.fill_missing = fill_missing
        st.session_state.max_iterations = max_iterations

else:  # Загрузка файла
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📁 Загрузка файла")
        uploaded_file = st.file_uploader(
            "Загрузите CSV файл с медицинскими данными",
            type=['csv'],
            help="Файл должен содержать колонки с медицинскими показателями. Колонка 'timestamp' опциональна - если отсутствует, будет создана автоматически."
        )
        st.session_state.uploaded_file = uploaded_file
        
        if uploaded_file is not None:
            try:
                df_preview = pd.read_csv(uploaded_file)
                st.success(f"✅ Файл загружен: {len(df_preview)} строк, {len(df_preview.columns)} колонок")
                st.write("**Колонки в файле:**")
                st.write(list(df_preview.columns))
            except Exception as e:
                st.error(f"❌ Ошибка чтения файла: {str(e)}")
    
    with col2:
        st.subheader("🔬 Параметры анализа")
        quantum_threshold = st.slider("Порог квантовой запутанности", 0.1, 0.9, 0.3, 0.1)
        fill_missing = st.checkbox("Заполнить пропущенные данные", value=True)
        max_iterations = st.slider("Максимум итераций заполнения", 10, 100, 50)
        st.session_state.quantum_threshold = quantum_threshold
        st.session_state.fill_missing = fill_missing
        st.session_state.max_iterations = max_iterations

# Секция 3: Профили пациентов
if st.session_state.get('show_profile_creation', False) or st.session_state.get('show_profile_management', False):
    st.markdown("---")
    st.header("👥 Управление профилями пациентов")
    
    # Переключатель между созданием и управлением
    tab_create, tab_manage = st.tabs(["➕ Создать профиль", "👥 Управление профилями"])
    
    with tab_create:
        st.subheader("👤 Создание нового профиля пациента")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📋 Основная информация")
            name = st.text_input("Имя пациента", value="")
            age = st.number_input("Возраст", 1, 120, 30)
            gender = st.selectbox("Пол", ["Мужской", "Женский"])
            weight = st.number_input("Вес (кг)", 20.0, 200.0, 70.0, 0.1)
            height = st.number_input("Рост (см)", 100.0, 250.0, 170.0, 0.1)
            
            # Расчет ИМТ
            if height > 0:
                bmi = weight / ((height / 100) ** 2)
                st.metric("ИМТ", f"{bmi:.1f}")
        
        with col2:
            st.subheader("🏥 Медицинская информация")
            activity_level = st.selectbox("Уровень активности", ["Низкий", "Умеренный", "Высокий"])
            
            st.write("**Медицинская история:**")
            diabetes = st.checkbox("Диабет")
            hypertension = st.checkbox("Гипертония")
            heart_disease = st.checkbox("Заболевания сердца")
            other_conditions = st.text_area("Другие состояния", placeholder="Опишите другие медицинские состояния...")
            
            st.write("**Факторы образа жизни:**")
            smoking = st.checkbox("Курение")
            alcohol = st.checkbox("Употребление алкоголя")
            exercise = st.checkbox("Регулярные физические упражнения")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("💾 Сохранить профиль", type="primary"):
                try:
                    # Создание профиля пациента
                    gender_enum = Gender.MALE if gender == "Мужской" else Gender.FEMALE
                    activity_enum = ActivityLevel.LOW if activity_level == "Низкий" else ActivityLevel.MODERATE if activity_level == "Умеренный" else ActivityLevel.HIGH
                    
                    medical_history = MedicalHistory()
                    if diabetes:
                        medical_history.add_condition("diabetes", "Диабет")
                    if hypertension:
                        medical_history.add_condition("hypertension", "Гипертония")
                    if heart_disease:
                        medical_history.add_condition("heart_disease", "Заболевания сердца")
                    
                    patient_profile = PatientProfile(
                        patient_id=generate_patient_id(),
                        name=name if name else f"Пациент {st.session_state.patient_counter}",
                        age=age,
                        gender=gender_enum,
                        weight=weight,
                        height=height,
                        activity_level=activity_enum,
                        medical_history=medical_history
                    )
                    
                    st.session_state.patient_profiles.append(patient_profile)
                    st.session_state.current_patient_profile = patient_profile
                    st.session_state.show_profile_creation = False
                    st.success(f"✅ Профиль пациента {patient_profile.patient_id} создан!")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Ошибка создания профиля: {str(e)}")
        
        with col2:
            if st.button("❌ Отмена"):
                st.session_state.show_profile_creation = False
                st.rerun()
    
    with tab_manage:
        st.subheader("👥 Управление существующими профилями")
        
        if st.session_state.patient_profiles:
            for i, profile in enumerate(st.session_state.patient_profiles):
                with st.expander(f"👤 {profile.patient_id} - {profile.name} ({profile.age} лет, {profile.gender.value})"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write(f"**ИМТ:** {profile.bmi:.1f}")
                        st.write(f"**Уровень активности:** {profile.activity_level.value}")
                    
                    with col2:
                        st.write("**Медицинская история:**")
                        if profile.medical_history.conditions:
                            for condition in profile.medical_history.conditions:
                                st.write(f"• {condition}")
                        else:
                            st.write("Нет записей")
                    
                    with col3:
                        if st.button(f"Выбрать", key=f"select_profile_{i}"):
                            st.session_state.current_patient_profile = profile
                            st.success(f"✅ Выбран профиль {profile.patient_id}")
                            st.rerun()
                        
                        if st.button(f"Удалить", key=f"delete_profile_{i}"):
                            st.session_state.patient_profiles.pop(i)
                            if st.session_state.current_patient_profile == profile:
                                st.session_state.current_patient_profile = None
                            st.success(f"✅ Профиль {profile.patient_id} удален")
                            st.rerun()
        else:
            st.info("👆 Создайте первый профиль пациента")

# Секция 5: AI-Помощник
if st.session_state.show_chat:
    st.markdown("---")
    st.header("🤖 AI-Помощник MQEA")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("**Интеллектуальный помощник для работы с MQEA**")
    
    with col2:
        if st.button("❌ Закрыть чат"):
            st.session_state.show_chat = False
            st.rerun()
    
    # Отображение истории чата
    if st.session_state.chat_messages:
        for message in st.session_state.chat_messages:
            if message["role"] == "user":
                st.markdown(f"**👤 Вы:** {message['content']}")
            else:
                st.markdown(f"**🤖 AI:** {message['content']}")
    
    # Поле ввода
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_input("Введите ваш вопрос:", placeholder="Например: 'Объясни результаты анализа' или 'Как работает квантовая запутанность?'")
    
    with col2:
        if st.button("📤 Отправить", type="primary"):
            if user_input:
                process_chat_message(user_input)
            else:
                st.warning("Введите сообщение")
    
    # Быстрые команды
    st.subheader("⚡ Быстрые команды")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📊 Объясни результаты"):
            process_chat_message("Объясни результаты анализа")
    
    with col2:
        if st.button("🔬 Что такое квантовая запутанность?"):
            process_chat_message("Что такое квантовая запутанность в медицинских данных?")
    
    with col3:
        if st.button("💊 Покажи рекомендации"):
            process_chat_message("Покажи медицинские рекомендации")
    
    with col4:
        if st.button("📈 Анализ данных"):
            process_chat_message("Как интерпретировать графики анализа?")

# Секция 6: Статус и результаты
st.markdown("---")
st.header("📊 Статус системы")

# Индикатор статуса
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.session_state.current_data is not None:
        st.success("✅ Данные загружены")
    else:
        st.warning("⚠️ Данные не загружены")

with col2:
    if st.session_state.analysis_results is not None:
        st.success("✅ Анализ выполнен")
    else:
        st.info("ℹ️ Анализ не выполнен")

with col3:
    if st.session_state.current_patient_profile is not None:
        st.success(f"✅ Профиль: {st.session_state.current_patient_profile.patient_id}")
    else:
        st.info("ℹ️ Профиль не выбран")

with col4:
    if st.session_state.recommendations:
        st.success(f"✅ Рекомендаций: {len(st.session_state.recommendations)}")
    else:
        st.info("ℹ️ Рекомендаций нет")

# Результаты анализа
if st.session_state.current_data is not None:
    st.markdown("---")
    st.header("📈 Результаты анализа")
    
    # Статистика данных
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
    st.subheader("📊 Временные ряды")
    
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
    
    st.plotly_chart(fig, width='stretch')
    
    # Результаты квантового анализа
    if st.session_state.analysis_results:
        st.subheader("🔬 Результаты квантового анализа")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Квантовая когерентность:**")
            coherence = st.session_state.analysis_results.get('quantum_signatures', {}).get('quantum_coherence', 0)
            st.metric("Когерентность", f"{coherence:.3f}")
            
            st.write("**Статистика запутанности:**")
            entanglement_stats = st.session_state.analysis_results.get('entanglement_statistics', {})
            st.write(f"• Всего квантовых состояний: {entanglement_stats.get('total_quantum_states', 0)}")
            st.write(f"• Запутанных пар: {entanglement_stats.get('entangled_pairs', 0)}")
            st.write(f"• Максимальная запутанность: {entanglement_stats.get('max_entanglement', 0):.3f}")
        
        with col2:
            st.write("**Матрица запутанности:**")
            entanglement_matrix = st.session_state.analysis_results.get('entanglement_matrix')
            if entanglement_matrix is not None and np.any(entanglement_matrix > 0):
                fig_heatmap = px.imshow(
                    entanglement_matrix,
                    title="Матрица квантовой запутанности",
                    color_continuous_scale='Viridis'
                )
                st.plotly_chart(fig_heatmap, width='stretch')
            else:
                st.info("ℹ️ Матрица квантовой запутанности недоступна. Проверьте настройки анализа.")

# Секция 7: Медицинские рекомендации
if st.session_state.recommendations:
    st.markdown("---")
    st.header("💊 Медицинские рекомендации")
    
    # Группировка рекомендаций по приоритету
    priority_groups = {
        "Срочные": [],
        "Предупреждения": [],
        "Осторожность": [],
        "Мониторинг": []
    }
    
    for rec in st.session_state.recommendations:
        # Получаем приоритет из объекта MedicalRecommendation
        if hasattr(rec, 'priority'):
            priority = rec.priority
        elif hasattr(rec, 'get'):
            priority = rec.get('priority', 'Мониторинг')
        else:
            priority = 'Мониторинг'
        
        if priority in priority_groups:
            priority_groups[priority].append(rec)
    
    # Отображение рекомендаций по группам
    for priority, recommendations in priority_groups.items():
        if recommendations:
            with st.expander(f"🚨 {priority} ({len(recommendations)} рекомендаций)"):
                for i, rec in enumerate(recommendations):
                    # Получаем данные из объекта MedicalRecommendation
                    if hasattr(rec, 'title'):
                        title = rec.title
                    elif hasattr(rec, 'get'):
                        title = rec.get('title', 'Рекомендация')
                    else:
                        title = 'Рекомендация'
                    
                    if hasattr(rec, 'description'):
                        description = rec.description
                    elif hasattr(rec, 'get'):
                        description = rec.get('description', 'Описание недоступно')
                    else:
                        description = 'Описание недоступно'
                    
                    if hasattr(rec, 'confidence'):
                        confidence = rec.confidence
                    elif hasattr(rec, 'get'):
                        confidence = rec.get('confidence', None)
                    else:
                        confidence = None
                    
                    st.write(f"**{i+1}. {title}**")
                    st.write(f"   {description}")
                    if confidence:
                        st.write(f"   *Уверенность: {confidence:.1%}*")
                    st.write("---")

# Секция 8: Таблица данных
if st.session_state.current_data is not None:
    st.markdown("---")
    st.header("📊 Таблица данных")
    
    display_data = st.session_state.current_data.data.copy()
    display_data.columns = [indicator_translations.get(col, col) for col in display_data.columns]
    
    # Показываем первые 20 строк
    st.dataframe(display_data.head(20), width='stretch')
    
    if len(display_data) > 20:
        st.info(f"Показаны первые 20 строк из {len(display_data)}. Используйте прокрутку для просмотра всех данных.")

# Футер
st.markdown("---")
st.markdown("**MQEA - Medical Quantum Entanglement Analysis** | **Автор:** Мухаммад Махизода | **Таджикский национальный университет**")

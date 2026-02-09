"""
Улучшенный веб-интерфейс MQEA с интегрированным AI-помощником.

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

# Импорты медицинской диагностической системы
try:
    from mqea.medical_diagnostic_system import (
        MedicalDiagnosticSystem, 
        PatientProfile as MedPatientProfile, 
        DiagnosticResult, 
        RiskLevel, 
        DiagnosticCategory
    )
except ImportError:
    # Если модуль не найден, создаем заглушки
    MedPatientProfile = None
    MedicalDiagnosticSystem = None
    DiagnosticResult = None
    RiskLevel = None
    DiagnosticCategory = None

def generate_patient_id():
    """Генерирует последовательный ID для пациента (P001, P002, P003...)"""
    if 'patient_counter' not in st.session_state:
        st.session_state.patient_counter = 1
    else:
        st.session_state.patient_counter += 1
    return f"P{st.session_state.patient_counter:03d}"

def generate_medical_data_for_diagnosis(patient, days: int):
    """Генерация медицинских данных для диагностики."""
    n_records = days * 24  # Каждый час
    
    # Базовые значения
    base_values = {
        'heart_rate': 75 if patient.age < 50 else 80,
        'blood_pressure_systolic': 120 if 'hypertension' not in patient.medical_history else 140,
        'blood_pressure_diastolic': 80 if 'hypertension' not in patient.medical_history else 90,
        'temperature': 36.6,
        'oxygen_saturation': 98,
        'respiratory_rate': 16,
        'glucose': 5.0 if 'diabetes' not in patient.medical_history else 7.5,
        'cholesterol': 180 if patient.age < 50 else 220
    }
    
    # Корректировка на основе факторов риска
    if patient.lifestyle_factors.get('smoking', False):
        base_values['oxygen_saturation'] -= 2
        base_values['respiratory_rate'] += 2
    
    if patient.lifestyle_factors.get('sedentary', False):
        base_values['heart_rate'] += 5
        base_values['glucose'] += 0.5
    
    if patient.bmi > 30:
        base_values['blood_pressure_systolic'] += 10
        base_values['glucose'] += 1.0
    
    # Генерация данных
    data = []
    for i in range(n_records):
        timestamp = datetime.now() - timedelta(hours=n_records-i)
        
        record = {
            'patient_id': patient.patient_id,
            'timestamp': timestamp,
            'age': patient.age,
            'gender': patient.gender,
            'bmi': patient.bmi
        }
        
        for indicator, base_value in base_values.items():
            daily_cycle = 0.1 * np.sin(2 * np.pi * i / 24)
            noise = np.random.normal(0, base_value * 0.05)
            trend = i * 0.001 if patient.age > 65 else 0
            
            value = base_value + daily_cycle + noise + trend
            
            # Ограничение значений
            if indicator == 'heart_rate':
                value = max(40, min(200, value))
            elif indicator in ['blood_pressure_systolic', 'blood_pressure_diastolic']:
                value = max(60, min(250, value))
            elif indicator == 'temperature':
                value = max(35, min(42, value))
            elif indicator == 'oxygen_saturation':
                value = max(70, min(100, value))
            elif indicator == 'respiratory_rate':
                value = max(8, min(40, value))
            elif indicator == 'glucose':
                value = max(2, min(20, value))
            elif indicator == 'cholesterol':
                value = max(100, min(400, value))
            
            record[indicator] = round(value, 1)
        
        data.append(record)
    
    return pd.DataFrame(data)

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
        st.session_state.patient_profiles = []  # Пустой список вместо тестовых пациентов
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
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "📊 Анализ данных", 
    "👤 Профиль пациента", 
    "🤖 AI-Помощник", 
    "📈 Результаты", 
    "💊 Рекомендации", 
    "🏥 Медицинская диагностика",
    "🔮 Прогнозирование рисков",
    "📊 Большие данные",
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

# Вкладка 2: Профиль пациента
with tab2:
    st.header("👤 Профиль пациента")
    st.markdown("**Выберите существующий профиль или создайте нового пациента для персонализированных рекомендаций**")
    
    # Переключатель между выбором и созданием
    profile_mode = st.radio(
        "Режим работы:",
        ["📋 Выбрать существующий профиль", "➕ Создать нового пациента"],
        horizontal=True
    )
    
    if profile_mode == "➕ Создать нового пациента":
        st.subheader("➕ Создание нового профиля пациента")
        
        # Показываем информацию о следующем ID
        next_id = f"P{(st.session_state.get('patient_counter', 0) + 1):03d}"
        st.info(f"📋 Следующий ID пациента: **{next_id}**")
        
        with st.form("create_patient_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Основная информация:**")
                first_name = st.text_input("Имя", value="", key="new_first_name")
                last_name = st.text_input("Фамилия", value="", key="new_last_name")
                
                # Показываем следующий ID, который будет назначен
                next_id = f"P{(st.session_state.get('patient_counter', 0) + 1):03d}"
                patient_id = st.text_input("ID пациента", value=next_id, key="new_patient_id", disabled=True)
                
                # Дата рождения
                birth_year = st.number_input("Год рождения", 1900, 2024, 1990, key="new_birth_year")
                birth_month = st.number_input("Месяц рождения", 1, 12, 1, key="new_birth_month")
                birth_day = st.number_input("День рождения", 1, 31, 1, key="new_birth_day")
                
                gender = st.selectbox("Пол", ["male", "female", "other"], key="new_gender")
                gender_enum = Gender.MALE if gender == "male" else Gender.FEMALE if gender == "female" else Gender.OTHER
                
                height_cm = st.number_input("Рост (см)", 50, 250, 170, key="new_height")
                weight_kg = st.number_input("Вес (кг)", 10, 200, 70, key="new_weight")
            
            with col2:
                st.markdown("**Медицинская информация:**")
                
                # Медицинская история
                medical_history_options = ["none", "diabetes", "hypertension", "heart_disease", "respiratory_disease", "kidney_disease", "liver_disease", "thyroid_disease", "cancer", "autoimmune"]
                selected_conditions = st.multiselect("Медицинская история", medical_history_options, key="new_medical_history")
                medical_history = [MedicalHistory(condition) for condition in selected_conditions]
                
                medications = st.text_area("Текущие лекарства (через запятую)", key="new_medications")
                medications_list = [med.strip() for med in medications.split(",") if med.strip()]
                
                allergies = st.text_area("Аллергии (через запятую)", key="new_allergies")
                allergies_list = [allergy.strip() for allergy in allergies.split(",") if allergy.strip()]
                
                activity_level = st.selectbox("Уровень активности", ["sedentary", "light", "moderate", "high", "very_high"], key="new_activity")
                activity_enum = ActivityLevel(activity_level)
                
                smoking = st.checkbox("Курение", key="new_smoking")
                alcohol = st.checkbox("Употребление алкоголя", key="new_alcohol")
            
            # Кнопка создания
            if st.form_submit_button("✅ Создать профиль пациента", key="create_patient_btn"):
                if first_name and last_name:
                    try:
                        from datetime import date
                        
                        # Создаем новый профиль
                        new_profile = PatientProfile(
                            patient_id=generate_patient_id(),
                            name=f"{first_name} {last_name}",
                            birth_date=date(birth_year, birth_month, birth_day),
                            gender=gender_enum,
                            height_cm=height_cm,
                            weight_kg=weight_kg,
                            medical_history=medical_history,
                            current_medications=medications_list,
                            allergies=allergies_list,
                            activity_level=activity_enum,
                            smoking=smoking,
                            alcohol_consumption=alcohol
                        )
                        
                        # Добавляем в список профилей
                        st.session_state.patient_profiles.append(new_profile)
                        st.session_state.current_patient_profile = new_profile
                        
                        st.success(f"✅ Профиль пациента {first_name} {last_name} создан и выбран!")
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Ошибка создания профиля: {e}")
                else:
                    st.error("❌ Пожалуйста, заполните обязательные поля: Имя, Фамилия")
    
    else:
        # Выбор существующего профиля
        st.subheader("📋 Выбор профиля пациента")
    
    if st.session_state.patient_profiles:
        profile_names = [f"{p.name} ({p.age} лет, {p.gender.value})" for p in st.session_state.patient_profiles]
        selected_profile_idx = st.selectbox(
            "Выберите профиль пациента:",
            range(len(profile_names)),
            format_func=lambda x: profile_names[x],
            help="Выберите один из предустановленных профилей пациентов"
        )
        
        if st.button("✅ Выбрать профиль", key="select_profile"):
            st.session_state.current_patient_profile = st.session_state.patient_profiles[selected_profile_idx]
            st.success(f"✅ Выбран профиль: {st.session_state.patient_profiles[selected_profile_idx].name}")
            st.rerun()
    
    # Отображение информации о выбранном профиле
    if st.session_state.current_patient_profile:
        profile = st.session_state.current_patient_profile
        st.subheader("👤 Информация о пациенте")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**Имя:** {profile.name}")
            st.markdown(f"**ID:** {profile.patient_id}")
            st.markdown(f"**Возраст:** {profile.age} лет")
            st.markdown(f"**Пол:** {profile.gender.value}")
            st.markdown(f"**Рост:** {profile.height_cm} см")
            st.markdown(f"**Вес:** {profile.weight_kg} кг")
        
        with col2:
            st.markdown(f"**BMI:** {profile.bmi:.1f} ({profile.bmi_category})")
            st.markdown(f"**Медицинская история:** {', '.join([h.value for h in profile.medical_history])}")
            st.markdown(f"**Лекарства:** {', '.join(profile.current_medications) if profile.current_medications else 'Нет'}")
            st.markdown(f"**Аллергии:** {', '.join(profile.allergies) if profile.allergies else 'Нет'}")
            st.markdown(f"**Активность:** {profile.activity_level.value}")
            st.markdown(f"**Курение:** {'Да' if profile.smoking else 'Нет'}")
        
        # Факторы риска
        risk_factors = profile.get_risk_factors()
        if risk_factors:
            st.subheader("⚠️ Факторы риска")
            for factor in risk_factors:
                st.markdown(f"• {factor}")
        
        # Персонализированные рекомендации из профиля
        personalized_recs = profile.get_personalized_recommendations()
        if personalized_recs:
            st.subheader("🎯 Персонализированные рекомендации")
            for i, rec in enumerate(personalized_recs, 1):
                st.markdown(f"{i}. {rec}")
        
        # Кнопки управления профилем
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 Сбросить профиль", key="reset_profile"):
                st.session_state.current_patient_profile = None
                st.success("✅ Профиль сброшен")
                st.rerun()
        
        with col2:
            if st.button("🔬 Автоматический анализ", key="auto_analysis"):
                if st.session_state.current_patient_profile:
                    # Генерируем данные на основе профиля
                    patient_profile = st.session_state.current_patient_profile
                    
                    # Создаем профиль для генерации данных
                    profile_data = {
                        'heart_rate': np.random.normal(patient_profile.get_age_adjusted_ranges('heart_rate')['normal'][0] + 10, 5),
                        'blood_pressure_systolic': np.random.normal(patient_profile.get_age_adjusted_ranges('blood_pressure_systolic')['normal'][0] + 20, 10),
                        'blood_pressure_diastolic': np.random.normal(patient_profile.get_age_adjusted_ranges('blood_pressure_diastolic')['normal'][0] + 15, 8),
                        'temperature': np.random.normal(36.8, 0.2),
                        'oxygen_saturation': np.random.normal(97, 1),
                        'respiratory_rate': np.random.normal(patient_profile.get_age_adjusted_ranges('respiratory_rate')['normal'][0] + 5, 2),
                        'glucose': np.random.normal(patient_profile.get_age_adjusted_ranges('glucose')['normal'][0] + 3, 1.5),
                        'cholesterol': np.random.normal(200, 20)
                    }
                    
                    # Генерируем данные
                    st.session_state.current_data = st.session_state.analyzer.generate_synthetic_data(
                        duration_hours=24,
                        sampling_rate_minutes=15,
                        add_noise=True,
                        add_missing_data=True,
                        patient_profile=profile_data
                    )
                    
                    # Выполняем анализ
                    st.session_state.analysis_results = st.session_state.analyzer.quantum_entanglement_analysis(
                        st.session_state.current_data, 
                        quantum_threshold=0.3
                    )
                    
                    # Генерируем рекомендации
                    personalized_engine = MedicalRecommendationEngine(patient_profile)
                    st.session_state.recommendations = personalized_engine.analyze_patient_data(
                        st.session_state.current_data,
                        st.session_state.analysis_results
                    )
                    
                    st.success("✅ Автоматический анализ завершен! Перейдите на вкладки 'Результаты' и 'Рекомендации' для просмотра.")
                    st.rerun()
                else:
                    st.warning("⚠️ Сначала выберите профиль пациента")
        
        with col3:
            if st.button("🖨️ Печать полной информации", key="print_full_info"):
                if st.session_state.current_patient_profile:
                    st.session_state.show_print_info = True
                    st.rerun()
                else:
                    st.warning("⚠️ Сначала выберите профиль пациента")
    
    else:
        st.info("👆 Выберите профиль пациента из списка выше")
        
        # Показываем примеры профилей
        if st.session_state.patient_profiles:
            st.subheader("📚 Доступные профили пациентов")
            
            for i, profile in enumerate(st.session_state.patient_profiles):
                with st.expander(f"👤 {profile.name} ({profile.age} лет)"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"**Пол:** {profile.gender.value}")
                        st.markdown(f"**BMI:** {profile.bmi:.1f} ({profile.bmi_category})")
                        st.markdown(f"**Активность:** {profile.activity_level.value}")
                    
                    with col2:
                        st.markdown(f"**Медицинская история:** {', '.join([h.value for h in profile.medical_history])}")
                        st.markdown(f"**Курение:** {'Да' if profile.smoking else 'Нет'}")
                        st.markdown(f"**Алкоголь:** {'Да' if profile.alcohol_consumption else 'Нет'}")
                    
                    # Факторы риска
                    risk_factors = profile.get_risk_factors()
                    if risk_factors:
                        st.markdown("**Факторы риска:**")
                        for factor in risk_factors:
                            st.markdown(f"• {factor}")
    
    # Секция печати полной информации
    if st.session_state.get('show_print_info', False) and st.session_state.current_patient_profile:
        st.markdown("---")
        st.subheader("🖨️ Полная информация для печати")
        
        profile = st.session_state.current_patient_profile
        
        # Создаем полный отчет
        print_content = f"""
# МЕДИЦИНСКИЙ ОТЧЕТ ПАЦИЕНТА
## MQEA - Medical Quantum Entanglement Analysis

**Дата создания отчета:** {datetime.now().strftime('%d.%m.%Y %H:%M')}
**Основатель алгоритма:** Мухаммад Махизода
**Университет:** Таджикский национальный университет

---

## ИНФОРМАЦИЯ О ПАЦИЕНТЕ

**Основные данные:**
• ID пациента: {profile.patient_id}
• ФИО: {profile.name}
• Возраст: {profile.age} лет
• Пол: {profile.gender.value}
• Рост: {profile.height_cm} см
• Вес: {profile.weight_kg} кг
• BMI: {profile.bmi:.1f} ({profile.bmi_category})

**Медицинская информация:**
• Медицинская история: {', '.join([h.value for h in profile.medical_history]) if profile.medical_history else 'Нет'}
• Текущие лекарства: {', '.join(profile.current_medications) if profile.current_medications else 'Нет'}
• Аллергии: {', '.join(profile.allergies) if profile.allergies else 'Нет'}
• Уровень активности: {profile.activity_level.value}
• Курение: {'Да' if profile.smoking else 'Нет'}
• Употребление алкоголя: {'Да' if profile.alcohol_consumption else 'Нет'}

**Факторы риска:**
"""
        
        risk_factors = profile.get_risk_factors()
        if risk_factors:
            for i, factor in enumerate(risk_factors, 1):
                print_content += f"• {i}. {factor}\n"
        else:
            print_content += "• Факторы риска не выявлены\n"
        
        # Добавляем данные анализа, если есть
        if st.session_state.current_data is not None:
            print_content += f"""
---

## ДАННЫЕ АНАЛИЗА

**Показатели (последние значения):**
"""
            for indicator in st.session_state.current_data.indicators:
                value = st.session_state.current_data.data[indicator].iloc[-1]
                print_content += f"• {indicator}: {value:.2f}\n"
        
        if st.session_state.analysis_results is not None:
            coherence = st.session_state.analysis_results.get('quantum_signatures', {}).get('quantum_coherence', 0)
            print_content += f"""
**Результаты квантового анализа:**
• Квантовая когерентность: {coherence:.3f}
• Окон запутанности: {len(st.session_state.analysis_results.get('quantum_entanglements', []))}
"""
        
        # Добавляем рекомендации, если есть
        if st.session_state.recommendations:
            print_content += f"""
---

## МЕДИЦИНСКИЕ РЕКОМЕНДАЦИИ

**Статистика рекомендаций:**
• Срочные: {len([r for r in st.session_state.recommendations if r.type.value == "urgent"])}
• Предупреждения: {len([r for r in st.session_state.recommendations if r.type.value == "warning"])}
• Осторожность: {len([r for r in st.session_state.recommendations if r.type.value == "caution"])}
• Мониторинг: {len([r for r in st.session_state.recommendations if r.type.value == "monitoring"])}

**Детальные рекомендации:**
"""
            for i, rec in enumerate(st.session_state.recommendations, 1):
                print_content += f"""
{i}. {rec.title}
   Тип: {rec.type.value.upper()}
   Уровень риска: {rec.risk_level.value.upper()}
   Приоритет: {rec.priority}/10
   Уверенность: {rec.confidence:.1%}
   Описание: {rec.description}
   Требуемое действие: {rec.action_required}
   Временные рамки: {rec.timeframe}
   Медицинское обоснование: {rec.medical_justification}
   Затронутые показатели: {', '.join(rec.indicators)}
"""
        
        print_content += f"""
---

## ПЕРСОНАЛИЗИРОВАННЫЕ РЕКОМЕНДАЦИИ ИЗ ПРОФИЛЯ

"""
        personalized_recs = profile.get_personalized_recommendations()
        if personalized_recs:
            for i, rec in enumerate(personalized_recs, 1):
                print_content += f"{i}. {rec}\n"
        else:
            print_content += "Персонализированные рекомендации не сгенерированы.\n"
        
        print_content += f"""
---

**Отчет создан системой MQEA v1.0.0**
**Автор алгоритма:** Мухаммад Махизода
**Таджикский национальный университет**
**Дата:** {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}
"""
        
        # Отображаем содержимое для печати
        st.text_area("Содержимое отчета:", print_content, height=600)
        
        # Кнопки для печати и скачивания
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🖨️ Печать отчета", key="print_report_btn"):
                # Создаем HTML содержимое отчета
                report_html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Медицинский отчет пациента - {profile.patient_id}</title>
                    <style>
                        body {{ 
                            font-family: Arial, sans-serif; 
                            margin: 20px; 
                            line-height: 1.6;
                            background-color: white;
                        }}
                        .header {{ 
                            text-align: center; 
                            border-bottom: 2px solid #333; 
                            padding-bottom: 10px; 
                            margin-bottom: 20px; 
                        }}
                        .section {{ 
                            margin-bottom: 20px; 
                        }}
                        .section h2 {{ 
                            color: #2c3e50; 
                            border-bottom: 1px solid #bdc3c7; 
                            padding-bottom: 5px; 
                        }}
                        .info-table {{ 
                            width: 100%; 
                            border-collapse: collapse; 
                            margin: 10px 0; 
                        }}
                        .info-table td {{ 
                            padding: 8px; 
                            border: 1px solid #ddd; 
                        }}
                        .info-table td:first-child {{ 
                            font-weight: bold; 
                            background-color: #f8f9fa; 
                        }}
                        .recommendation {{ 
                            margin: 10px 0; 
                            padding: 10px; 
                            border-left: 4px solid #3498db; 
                            background-color: #f8f9fa; 
                        }}
                        .urgent {{ border-left-color: #e74c3c; }}
                        .warning {{ border-left-color: #f39c12; }}
                        .caution {{ border-left-color: #f1c40f; }}
                        .monitoring {{ border-left-color: #27ae60; }}
                        @media print {{
                            body {{ margin: 0; }}
                            .no-print {{ display: none; }}
                        }}
                    </style>
                </head>
                <body>
                    <div class="header">
                        <h1>МЕДИЦИНСКИЙ ОТЧЕТ ПАЦИЕНТА</h1>
                        <h2>MQEA - Medical Quantum Entanglement Analysis</h2>
                        <p><strong>Дата создания отчета:</strong> {datetime.now().strftime('%d.%m.%Y %H:%M')}</p>
                        <p><strong>Основатель алгоритма:</strong> Мухаммад Махизода</p>
                        <p><strong>Университет:</strong> Таджикский национальный университет</p>
                    </div>
                    
                    <div class="section">
                        <h2>ИНФОРМАЦИЯ О ПАЦИЕНТЕ</h2>
                        <table class="info-table">
                            <tr><td>ID пациента</td><td>{profile.patient_id}</td></tr>
                            <tr><td>ФИО</td><td>{profile.name}</td></tr>
                            <tr><td>Возраст</td><td>{profile.age} лет</td></tr>
                            <tr><td>Пол</td><td>{profile.gender.value}</td></tr>
                            <tr><td>Рост</td><td>{profile.height_cm} см</td></tr>
                            <tr><td>Вес</td><td>{profile.weight_kg} кг</td></tr>
                            <tr><td>BMI</td><td>{profile.bmi:.1f} ({profile.bmi_category})</td></tr>
                            <tr><td>Медицинская история</td><td>{', '.join([h.value for h in profile.medical_history]) if profile.medical_history else 'Нет'}</td></tr>
                            <tr><td>Текущие лекарства</td><td>{', '.join(profile.current_medications) if profile.current_medications else 'Нет'}</td></tr>
                            <tr><td>Аллергии</td><td>{', '.join(profile.allergies) if profile.allergies else 'Нет'}</td></tr>
                            <tr><td>Уровень активности</td><td>{profile.activity_level.value}</td></tr>
                            <tr><td>Курение</td><td>{'Да' if profile.smoking else 'Нет'}</td></tr>
                            <tr><td>Употребление алкоголя</td><td>{'Да' if profile.alcohol_consumption else 'Нет'}</td></tr>
                        </table>
                    </div>
                    
                    <div class="section">
                        <h2>ФАКТОРЫ РИСКА</h2>
                        <ul>
                """
                
                risk_factors = profile.get_risk_factors()
                if risk_factors:
                    for i, factor in enumerate(risk_factors, 1):
                        report_html += f"<li>{i}. {factor}</li>"
                else:
                    report_html += "<li>Факторы риска не выявлены</li>"
                
                report_html += "</ul></div>"
                
                # Добавляем данные анализа, если есть
                if st.session_state.current_data is not None:
                    report_html += """
                    <div class="section">
                        <h2>ДАННЫЕ АНАЛИЗА</h2>
                        <table class="info-table">
                    """
                    for indicator in st.session_state.current_data.indicators:
                        value = st.session_state.current_data.data[indicator].iloc[-1]
                        report_html += f"<tr><td>{indicator}</td><td>{value:.2f}</td></tr>"
                    report_html += "</table></div>"
                
                # Добавляем результаты квантового анализа, если есть
                if st.session_state.analysis_results is not None:
                    coherence = st.session_state.analysis_results.get('quantum_signatures', {}).get('quantum_coherence', 0)
                    report_html += f"""
                    <div class="section">
                        <h2>РЕЗУЛЬТАТЫ КВАНТОВОГО АНАЛИЗА</h2>
                        <table class="info-table">
                            <tr><td>Квантовая когерентность</td><td>{coherence:.3f}</td></tr>
                            <tr><td>Окон запутанности</td><td>{len(st.session_state.analysis_results.get('quantum_entanglements', []))}</td></tr>
                        </table>
                    </div>
                    """
                
                # Добавляем рекомендации, если есть
                if st.session_state.recommendations:
                    report_html += """
                    <div class="section">
                        <h2>МЕДИЦИНСКИЕ РЕКОМЕНДАЦИИ</h2>
                    """
                    
                    urgent_count = len([r for r in st.session_state.recommendations if r.type.value == "urgent"])
                    warning_count = len([r for r in st.session_state.recommendations if r.type.value == "warning"])
                    caution_count = len([r for r in st.session_state.recommendations if r.type.value == "caution"])
                    monitoring_count = len([r for r in st.session_state.recommendations if r.type.value == "monitoring"])
                    
                    report_html += f"""
                        <table class="info-table">
                            <tr><td>Срочные</td><td>{urgent_count}</td></tr>
                            <tr><td>Предупреждения</td><td>{warning_count}</td></tr>
                            <tr><td>Осторожность</td><td>{caution_count}</td></tr>
                            <tr><td>Мониторинг</td><td>{monitoring_count}</td></tr>
                        </table>
                    """
                    
                    for i, rec in enumerate(st.session_state.recommendations, 1):
                        rec_class = rec.type.value
                        report_html += f"""
                        <div class="recommendation {rec_class}">
                            <h3>{i}. {rec.title}</h3>
                            <p><strong>Тип:</strong> {rec.type.value.upper()}</p>
                            <p><strong>Уровень риска:</strong> {rec.risk_level.value.upper()}</p>
                            <p><strong>Приоритет:</strong> {rec.priority}/10</p>
                            <p><strong>Уверенность:</strong> {rec.confidence:.1%}</p>
                            <p><strong>Описание:</strong> {rec.description}</p>
                            <p><strong>Требуемое действие:</strong> {rec.action_required}</p>
                            <p><strong>Временные рамки:</strong> {rec.timeframe}</p>
                            <p><strong>Медицинское обоснование:</strong> {rec.medical_justification}</p>
                            <p><strong>Затронутые показатели:</strong> {', '.join(rec.indicators)}</p>
                        </div>
                        """
                    
                    report_html += "</div>"
                
                # Персонализированные рекомендации из профиля
                personalized_recs = profile.get_personalized_recommendations()
                if personalized_recs:
                    report_html += """
                    <div class="section">
                        <h2>ПЕРСОНАЛИЗИРОВАННЫЕ РЕКОМЕНДАЦИИ ИЗ ПРОФИЛЯ</h2>
                        <ul>
                    """
                    for i, rec in enumerate(personalized_recs, 1):
                        report_html += f"<li>{i}. {rec}</li>"
                    report_html += "</ul></div>"
                
                report_html += f"""
                    <div class="section">
                        <p><strong>Отчет создан системой MQEA v1.0.0</strong></p>
                        <p><strong>Автор алгоритма:</strong> Мухаммад Махизода</p>
                        <p><strong>Таджикский национальный университет</strong></p>
                        <p><strong>Дата:</strong> {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}</p>
                    </div>
                </body>
                </html>
                """
                
                # Открываем окно печати с содержимым отчета
                components.html(f"""
                <script>
                    var printWindow = window.open('', '_blank', 'width=800,height=600');
                    printWindow.document.write(`{report_html}`);
                    printWindow.document.close();
                    printWindow.focus();
                    // Автоматически открываем диалог печати
                    setTimeout(function() {{
                        printWindow.print();
                    }}, 500);
                </script>
                """, height=0)
        
        with col2:
            # Создаем файл для скачивания
            st.download_button(
                label="💾 Скачать отчет",
                data=print_content,
                file_name=f"medical_report_{profile.patient_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
        
        with col3:
            if st.button("❌ Закрыть отчет", key="close_report_btn"):
                st.session_state.show_print_info = False
                st.rerun()

# Вкладка 3: AI-Помощник
with tab3:
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
                response = st.session_state.assistant.process_query(user_input)
                
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
        
        if st.button("👋 Приветствие", key="chat_hello"):
            process_chat_message("Привет!")
        
        if st.button("📚 Что такое MQEA?", key="chat_what_is_mqea"):
            process_chat_message("Что такое MQEA?")
        
        if st.button("📊 Создать пример данных", key="chat_create_sample"):
            process_chat_message("Создай пример данных")
        
        if st.button("🔬 Выполнить анализ", key="chat_run_analysis"):
            process_chat_message("Выполни анализ")
        
        if st.button("❓ Сгенерировать вопросы", key="chat_generate_questions"):
            process_chat_message("Сгенерируй вопросы")
        
        if st.button("🔍 Найти паттерны", key="chat_find_patterns"):
            process_chat_message("Найди паттерны")
        
        if st.button("⚠️ Найти аномалии", key="chat_find_anomalies"):
            process_chat_message("Найди аномалии")
        
        if st.button("🔮 Предсказать", key="chat_predict"):
            process_chat_message("Предскажи изменения")
        
        if st.button("🆘 Помощь", key="chat_help"):
            process_chat_message("Помощь")
        
        # Управление чатом
        st.subheader("🎛️ Управление")
        
        if st.button("🔄 Очистить чат", key="chat_clear"):
            st.session_state.chat_messages = []
            st.session_state.assistant.clear_conversation_history()
            st.rerun()

# Вкладка 4: Результаты
with tab4:
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
        if st.session_state.current_data:
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

# Вкладка 5: Рекомендации
with tab5:
    st.header("💊 Медицинские рекомендации")
    st.markdown("**Персонализированные рекомендации на основе анализа MQEA**")
    
    if st.session_state.recommendations:
        # Статистика рекомендаций
        urgent_count = len([r for r in st.session_state.recommendations if r.type.value == "urgent"])
        warning_count = len([r for r in st.session_state.recommendations if r.type.value == "warning"])
        caution_count = len([r for r in st.session_state.recommendations if r.type.value == "caution"])
        monitoring_count = len([r for r in st.session_state.recommendations if r.type.value == "monitoring"])
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("🚨 Срочные", urgent_count, delta=None)
        with col2:
            st.metric("⚠️ Предупреждения", warning_count, delta=None)
        with col3:
            st.metric("🔶 Осторожность", caution_count, delta=None)
        with col4:
            st.metric("👁️ Мониторинг", monitoring_count, delta=None)
        
        # Группировка рекомендаций по типам
        urgent_recs = [r for r in st.session_state.recommendations if r.type.value == "urgent"]
        warning_recs = [r for r in st.session_state.recommendations if r.type.value == "warning"]
        caution_recs = [r for r in st.session_state.recommendations if r.type.value == "caution"]
        monitoring_recs = [r for r in st.session_state.recommendations if r.type.value == "monitoring"]
        
        # Срочные рекомендации
        if urgent_recs:
            st.subheader("🚨 Срочные рекомендации")
            for i, rec in enumerate(urgent_recs, 1):
                with st.expander(f"**{i}. {rec.title}** (Приоритет: {rec.priority}/10)", expanded=True):
                    st.markdown(f"**Описание:** {rec.description}")
                    st.markdown(f"**Требуемое действие:** {rec.action_required}")
                    st.markdown(f"**Временные рамки:** {rec.timeframe}")
                    st.markdown(f"**Медицинское обоснование:** {rec.medical_justification}")
                    st.markdown(f"**Уверенность:** {rec.confidence:.1%}")
                    st.markdown(f"**Затронутые показатели:** {', '.join(rec.indicators)}")
        
        # Предупреждения
        if warning_recs:
            st.subheader("⚠️ Предупреждения")
            for i, rec in enumerate(warning_recs, 1):
                with st.expander(f"**{i}. {rec.title}** (Приоритет: {rec.priority}/10)"):
                    st.markdown(f"**Описание:** {rec.description}")
                    st.markdown(f"**Требуемое действие:** {rec.action_required}")
                    st.markdown(f"**Временные рамки:** {rec.timeframe}")
                    st.markdown(f"**Медицинское обоснование:** {rec.medical_justification}")
                    st.markdown(f"**Уверенность:** {rec.confidence:.1%}")
                    st.markdown(f"**Затронутые показатели:** {', '.join(rec.indicators)}")
        
        # Осторожность
        if caution_recs:
            st.subheader("🔶 Рекомендации по осторожности")
            for i, rec in enumerate(caution_recs, 1):
                with st.expander(f"**{i}. {rec.title}** (Приоритет: {rec.priority}/10)"):
                    st.markdown(f"**Описание:** {rec.description}")
                    st.markdown(f"**Требуемое действие:** {rec.action_required}")
                    st.markdown(f"**Временные рамки:** {rec.timeframe}")
                    st.markdown(f"**Медицинское обоснование:** {rec.medical_justification}")
                    st.markdown(f"**Уверенность:** {rec.confidence:.1%}")
                    st.markdown(f"**Затронутые показатели:** {', '.join(rec.indicators)}")
        
        # Мониторинг
        if monitoring_recs:
            st.subheader("👁️ Рекомендации по мониторингу")
            for i, rec in enumerate(monitoring_recs, 1):
                with st.expander(f"**{i}. {rec.title}** (Приоритет: {rec.priority}/10)"):
                    st.markdown(f"**Описание:** {rec.description}")
                    st.markdown(f"**Требуемое действие:** {rec.action_required}")
                    st.markdown(f"**Временные рамки:** {rec.timeframe}")
                    st.markdown(f"**Медицинское обоснование:** {rec.medical_justification}")
                    st.markdown(f"**Уверенность:** {rec.confidence:.1%}")
                    st.markdown(f"**Затронутые показатели:** {', '.join(rec.indicators)}")
        
        # Сводный отчет
        st.subheader("📋 Сводный отчет")
        if st.button("📄 Сгенерировать полный отчет", key="generate_full_report"):
            report = st.session_state.recommendation_engine.generate_summary_report(st.session_state.recommendations)
            st.markdown(report)
        
        # Экспорт рекомендаций
        st.subheader("📤 Экспорт рекомендаций")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("💾 Сохранить в файл", key="save_recommendations"):
                # Создаем CSV файл с рекомендациями
                rec_data = []
                for rec in st.session_state.recommendations:
                    rec_data.append({
                        'Тип': rec.type.value,
                        'Уровень_риска': rec.risk_level.value,
                        'Заголовок': rec.title,
                        'Описание': rec.description,
                        'Действие': rec.action_required,
                        'Временные_рамки': rec.timeframe,
                        'Приоритет': rec.priority,
                        'Уверенность': f"{rec.confidence:.1%}",
                        'Показатели': ', '.join(rec.indicators)
                    })
                
                df_recs = pd.DataFrame(rec_data)
                csv = df_recs.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="Скачать CSV",
                    data=csv,
                    file_name=f"medical_recommendations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        
        with col2:
            if st.button("🖨️ Печать отчета", key="print_report"):
                st.info("Используйте Ctrl+P для печати страницы")
    
    else:
        st.info("Сначала выполните анализ данных на вкладке 'Анализ данных' для получения рекомендаций")

# Вкладка 6: Медицинская диагностика
with tab6:
    st.header("🏥 Медицинская диагностика")
    st.markdown("**Расширенная диагностическая система с квантовым анализом**")
    
    # Проверка доступности медицинской системы
    if MedPatientProfile is None:
        st.error("❌ Модуль медицинской диагностической системы не найден")
        st.info("💡 Убедитесь, что файл `mqea/medical_diagnostic_system.py` существует")
        st.stop()
    
    # Инициализация медицинской системы
    if 'medical_system' not in st.session_state:
        st.session_state.medical_system = MedicalDiagnosticSystem()
        st.session_state.med_patients = {}
        st.session_state.diagnostic_results = {}
    
    # Управление пациентами
    st.subheader("👥 Управление пациентами")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("➕ Добавить пациента", use_container_width=True):
            st.session_state.show_add_med_patient = True
    
    with col2:
        if st.button("📋 Список пациентов", use_container_width=True):
            st.session_state.show_patient_list = True
    
    # Добавление пациента
    if st.session_state.get('show_add_med_patient', False):
        with st.expander("➕ Добавить нового пациента", expanded=True):
            with st.form("add_med_patient"):
                col1, col2 = st.columns(2)
                
                with col1:
                    patient_id = st.text_input("ID пациента", value=f"P{len(st.session_state.med_patients)+1:04d}")
                    age = st.number_input("Возраст", min_value=0, max_value=120, value=50)
                    gender = st.selectbox("Пол", ["male", "female"])
                    weight = st.number_input("Вес (кг)", min_value=20.0, max_value=200.0, value=70.0)
                
                with col2:
                    height = st.number_input("Рост (см)", min_value=100.0, max_value=250.0, value=175.0)
                    medical_history = st.multiselect(
                        "Медицинская история",
                        ["diabetes", "hypertension", "heart_disease", "cancer", "asthma", "none"]
                    )
                    smoking = st.checkbox("Курит")
                    sedentary = st.checkbox("Малоподвижный образ жизни")
                
                if st.form_submit_button("➕ Добавить пациента"):
                    try:
                        profile = MedPatientProfile(
                            patient_id=patient_id,
                            age=age,
                            gender=gender,
                            weight=weight,
                            height=height,
                            medical_history=medical_history if medical_history != ["none"] else [],
                            current_medications=[],
                            allergies=[],
                            lifestyle_factors={
                                "smoking": smoking,
                                "sedentary": sedentary,
                                "alcohol": "none"
                            }
                        )
                        
                        success = st.session_state.medical_system.add_patient_profile(profile)
                        
                        if success:
                            st.session_state.med_patients[patient_id] = profile
                            st.success(f"✅ Пациент {patient_id} добавлен!")
                            st.session_state.show_add_med_patient = False
                            st.rerun()
                        else:
                            st.error("❌ Ошибка добавления пациента")
                            
                    except Exception as e:
                        st.error(f"❌ Ошибка: {e}")
    
    # Список пациентов
    if st.session_state.get('show_patient_list', False) or st.session_state.med_patients:
        st.subheader("📋 Список пациентов")
        
        if st.session_state.med_patients:
            for patient_id, patient in st.session_state.med_patients.items():
                with st.expander(f"👤 {patient_id} - {patient.age} лет, {patient.gender}"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write(f"**Возраст:** {patient.age}")
                        st.write(f"**Пол:** {patient.gender}")
                        st.write(f"**ИМТ:** {patient.bmi:.1f}")
                    
                    with col2:
                        st.write(f"**История болезней:** {', '.join(patient.medical_history) if patient.medical_history else 'Нет'}")
                        st.write(f"**Курит:** {'Да' if patient.lifestyle_factors.get('smoking', False) else 'Нет'}")
                        st.write(f"**Малоподвижный:** {'Да' if patient.lifestyle_factors.get('sedentary', False) else 'Нет'}")
                    
                    with col3:
                        # Простой расчет риска
                        risk_score = 0
                        if patient.age > 65:
                            risk_score += 0.3
                        if patient.bmi > 30:
                            risk_score += 0.3
                        if patient.lifestyle_factors.get('smoking', False):
                            risk_score += 0.2
                        if 'diabetes' in patient.medical_history:
                            risk_score += 0.3
                        
                        if risk_score < 0.3:
                            risk_level = "low"
                        elif risk_score < 0.6:
                            risk_level = "medium"
                        elif risk_score < 0.8:
                            risk_level = "high"
                        else:
                            risk_level = "critical"
                        
                        st.markdown(f"**Уровень риска:** {risk_level.upper()}")
                        
                        if st.button(f"🔍 Диагностика", key=f"med_diag_{patient_id}"):
                            st.session_state.selected_med_patient = patient_id
                            st.session_state.show_med_diagnosis = True
                            st.rerun()
        else:
            st.info("👥 Пациенты не добавлены. Добавьте первого пациента выше.")
    
    # Диагностика
    if st.session_state.get('show_med_diagnosis', False) and st.session_state.med_patients:
        st.subheader("🔍 Диагностика пациента")
        
        if st.session_state.get('selected_med_patient'):
            patient_id = st.session_state.selected_med_patient
            patient = st.session_state.med_patients[patient_id]
            
            st.write(f"**Пациент:** {patient_id} - {patient.age} лет, {patient.gender}")
            
            # Генерация медицинских данных
            col1, col2 = st.columns(2)
            
            with col1:
                duration_days = st.slider("Продолжительность (дни)", 1, 30, 7)
            
            with col2:
                add_noise = st.checkbox("Добавить шум", value=True)
            
            if st.button("🔄 Сгенерировать данные"):
                with st.spinner("Генерация медицинских данных..."):
                    try:
                        # Генерация данных
                        medical_data = generate_medical_data_for_diagnosis(patient, duration_days)
                        st.session_state.current_med_data = medical_data
                        st.session_state.current_med_patient_id = patient_id
                        st.success(f"✅ Данные сгенерированы: {len(medical_data)} записей")
                    except Exception as e:
                        st.error(f"❌ Ошибка генерации данных: {e}")
            
            # Анализ
            if 'current_med_data' in st.session_state:
                st.subheader("⚛️ Квантовый анализ")
                
                if st.button("🔬 Запустить анализ"):
                    with st.spinner("Анализ..."):
                        try:
                            medical_data = st.session_state.current_med_data
                            indicators = ['heart_rate', 'blood_pressure_systolic', 'blood_pressure_diastolic',
                                        'temperature', 'oxygen_saturation', 'respiratory_rate', 'glucose', 'cholesterol']
                            
                            from mqea.data_processor import MedicalTimeSeries
                            time_series = MedicalTimeSeries(
                                data=medical_data.set_index('timestamp'),
                                indicators=indicators,
                                timestamps=medical_data['timestamp'].tolist(),
                                missing_data_mask=medical_data[indicators].isnull(),
                                quantum_states={},
                                metadata={'patient_id': st.session_state.current_med_patient_id}
                            )
                            
                            diagnostic = st.session_state.medical_system.analyze_patient_data(
                                patient_id=st.session_state.current_med_patient_id,
                                medical_data=time_series
                            )
                            
                            st.session_state.diagnostic_results[st.session_state.current_med_patient_id] = diagnostic
                            st.success("✅ Анализ завершен!")
                            
                        except Exception as e:
                            st.error(f"❌ Ошибка анализа: {e}")
                
                # Результаты
                if st.session_state.current_med_patient_id in st.session_state.diagnostic_results:
                    diagnostic = st.session_state.diagnostic_results[st.session_state.current_med_patient_id]
                    
                    # Метрики
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Категория", diagnostic.category.value)
                    
                    with col2:
                        st.metric("Уровень риска", diagnostic.risk_level.value.upper())
                    
                    with col3:
                        st.metric("Уверенность", f"{diagnostic.confidence:.2f}")
                    
                    with col4:
                        st.metric("Срочность", f"{diagnostic.urgency_score:.2f}")
                    
                    # Рекомендации
                    st.subheader("💡 Рекомендации")
                    for i, rec in enumerate(diagnostic.recommendations, 1):
                        st.write(f"{i}. {rec}")
                    
                    # График
                    st.subheader("📈 Визуализация")
                    
                    medical_data = st.session_state.current_med_data
                    indicators = ['heart_rate', 'blood_pressure_systolic', 'blood_pressure_diastolic',
                                'temperature', 'oxygen_saturation', 'respiratory_rate', 'glucose', 'cholesterol']
                    
                    fig = make_subplots(
                        rows=4, cols=2,
                        subplot_titles=indicators,
                        vertical_spacing=0.1
                    )
                    
                    for i, indicator in enumerate(indicators):
                        row = (i // 2) + 1
                        col = (i % 2) + 1
                        
                        fig.add_trace(
                            go.Scatter(
                                x=medical_data['timestamp'],
                                y=medical_data[indicator],
                                mode='lines+markers',
                                name=indicator,
                                line=dict(width=2)
                            ),
                            row=row, col=col
                        )
                    
                    fig.update_layout(height=800, showlegend=False, title_text="Медицинские показатели")
                    st.plotly_chart(fig, use_container_width=True)

# Вкладка 7: Прогнозирование рисков
with tab7:
    st.header("🔮 Прогнозирование рисков заболеваний")
    st.markdown("**ML-модели для предсказания рисков заболеваний**")
    
    # Проверка доступности медицинской системы
    if MedPatientProfile is None:
        st.error("❌ Модуль медицинской диагностической системы не найден")
        st.info("💡 Убедитесь, что файл `mqea/medical_diagnostic_system.py` существует")
    elif not st.session_state.get('med_patients', {}):
        st.warning("⚠️ Сначала добавьте пациентов в разделе 'Медицинская диагностика'")
    else:
        # Выбор пациента
        patient_options = {f"{pid} - {p.age} лет, {p.gender}": pid for pid, p in st.session_state.med_patients.items()}
        selected_patient_display = st.selectbox("Выберите пациента:", list(patient_options.keys()))
        selected_patient_id = patient_options[selected_patient_display]
        
        # Настройки прогноза
        col1, col2 = st.columns(2)
        
        with col1:
            time_horizon = st.slider("Временной горизонт (дни)", 7, 365, 30)
        
        with col2:
            include_genetic = st.checkbox("Учитывать генетические факторы", value=False)
        
        if st.button("🔮 Прогнозировать риски", use_container_width=True):
            with st.spinner("Выполнение прогнозирования рисков..."):
                try:
                    # Прогнозирование рисков
                    risk_predictions = st.session_state.medical_system.predict_disease_risk(
                        patient_id=selected_patient_id,
                        time_horizon_days=time_horizon
                    )
                    
                    # Отображение результатов
                    st.subheader("📊 Результаты прогнозирования")
                    
                    # Метрики рисков
                    cols = st.columns(len(risk_predictions))
                    for i, (category, risk) in enumerate(risk_predictions.items()):
                        with cols[i]:
                            risk_level = "низкий" if risk < 0.3 else "средний" if risk < 0.6 else "высокий" if risk < 0.8 else "критический"
                            
                            st.metric(
                                label=category.replace('_', ' ').title(),
                                value=f"{risk:.1%}",
                                delta=risk_level
                            )
                    
                    # График рисков
                    fig = px.bar(
                        x=list(risk_predictions.keys()),
                        y=list(risk_predictions.values()),
                        title=f"Прогноз рисков на {time_horizon} дней",
                        labels={'x': 'Категория заболевания', 'y': 'Уровень риска'}
                    )
                    fig.update_layout(xaxis_tickangle=-45)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Рекомендации по снижению рисков
                    st.subheader("💡 Рекомендации по снижению рисков")
                    
                    high_risk_categories = [cat for cat, risk in risk_predictions.items() if risk > 0.6]
                    
                    if high_risk_categories:
                        st.warning(f"⚠️ Высокий риск в категориях: {', '.join(high_risk_categories)}")
                        
                        recommendations = {
                            'cardiovascular': [
                                "Регулярный мониторинг артериального давления",
                                "Контроль уровня холестерина",
                                "Физическая активность 30 минут в день",
                                "Ограничение соли в рационе"
                            ],
                            'metabolic': [
                                "Контроль уровня глюкозы",
                                "Сбалансированное питание",
                                "Регулярные физические упражнения",
                                "Контроль веса"
                            ],
                            'respiratory': [
                                "Мониторинг насыщения кислородом",
                                "Дыхательные упражнения",
                                "Избегание курения и загрязненного воздуха"
                            ]
                        }
                        
                        for category in high_risk_categories:
                            if category in recommendations:
                                st.markdown(f"**{category.replace('_', ' ').title()}:**")
                                for rec in recommendations[category]:
                                    st.write(f"• {rec}")
                    else:
                        st.success("✅ Риски находятся в пределах нормы")
                    
                except Exception as e:
                    st.error(f"❌ Ошибка прогнозирования: {e}")

# Вкладка 8: Большие данные
with tab8:
    st.header("📊 Обработка больших данных")
    st.markdown("**Распределенная обработка медицинских данных**")
    
    # Настройки обработки
    col1, col2 = st.columns(2)
    
    with col1:
        chunk_size = st.number_input("Размер чанка", min_value=1000, max_value=50000, value=5000)
        max_workers = st.number_input("Количество процессов", min_value=1, max_value=16, value=4)
    
    with col2:
        enable_dask = st.checkbox("Использовать Dask", value=False)
        memory_limit = st.number_input("Лимит памяти (ГБ)", min_value=1, max_value=32, value=8)
    
    # Генерация тестовых данных
    if st.button("🔄 Сгенерировать тестовые данные", use_container_width=True):
        with st.spinner("Генерация больших данных..."):
            try:
                # Генерация данных для всех пациентов
                big_data = []
                for patient in st.session_state.get('med_patients', {}).values():
                    patient_data = generate_medical_data_for_diagnosis(patient, days=1)
                    big_data.append(patient_data)
                
                if big_data:
                    import pandas as pd
                    big_dataframe = pd.concat(big_data, ignore_index=True)
                    st.session_state.big_data = big_dataframe
                    st.success(f"✅ Сгенерированы данные: {len(big_dataframe):,} записей")
                else:
                    st.warning("⚠️ Сначала добавьте пациентов")
                
            except Exception as e:
                st.error(f"❌ Ошибка генерации данных: {e}")
    
    # Обработка больших данных
    if 'big_data' in st.session_state and st.button("⚡ Обработать большие данные", use_container_width=True):
        with st.spinner("Обработка больших данных..."):
            try:
                from mqea.big_data_processor import BigDataProcessor
                
                # Создание процессора
                processor = BigDataProcessor(
                    chunk_size=chunk_size,
                    max_workers=max_workers,
                    enable_dask=enable_dask,
                    memory_limit_gb=memory_limit
                )
                
                # Обработка данных
                start_time = time.time()
                results = processor.process_large_dataset(
                    data_source=st.session_state.big_data,
                    output_format="json",
                    output_path="output/big_data_analysis"
                )
                processing_time = time.time() - start_time
                
                # Отображение результатов
                st.subheader("📊 Результаты обработки")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Чанков обработано", f"{results['successful_chunks']}/{results['total_chunks']}")
                
                with col2:
                    st.metric("Пациентов проанализировано", results['total_patients'])
                
                with col3:
                    st.metric("Время обработки", f"{processing_time:.2f} сек")
                
                with col4:
                    if processing_time > 0:
                        speed = results['total_patients'] / processing_time
                        st.metric("Скорость", f"{speed:.1f} пациентов/сек")
                
                # Статистика
                stats = processor.get_processing_statistics()
                
                st.subheader("📈 Статистика производительности")
                st.json(stats)
                
                processor.close()
                
            except Exception as e:
                st.error(f"❌ Ошибка обработки: {e}")

# Вкладка 9: Настройки
with tab9:
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

# Футер
st.markdown("---")
st.markdown("**MQEA - Medical Quantum Entanglement Analysis** | **Автор:** Мухаммад Махизода | **Таджикский национальный университет**")

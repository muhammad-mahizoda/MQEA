#!/usr/bin/env python3
"""
Расширенный медицинский веб-интерфейс MQEA
с полной интеграцией диагностической системы, работы с большими данными
и персонализированного лечения.

Автор: Мухаммад Махизода
Таджикский национальный университет
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from datetime import datetime, timedelta
import time
import sys
import os
from pathlib import Path

# Добавляем путь к модулям
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mqea.medical_diagnostic_system import (
    MedicalDiagnosticSystem, PatientProfile, DiagnosticResult, 
    RiskLevel, DiagnosticCategory, TreatmentRecommendation
)
from mqea.big_data_processor import BigDataProcessor
from mqea.core import MQEAAnalyzer
from mqea.data_processor import MedicalTimeSeries
from utils.logo_utils import display_main_logo, display_sidebar_logo



# Настройка страницы
st.set_page_config(
    page_title="MQEA - Медицинская Диагностическая Система",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS стили
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .risk-critical { color: #e74c3c; font-weight: bold; }
    .risk-high { color: #f39c12; font-weight: bold; }
    .risk-medium { color: #f1c40f; font-weight: bold; }
    .risk-low { color: #27ae60; font-weight: bold; }
    .success-message { color: #27ae60; font-weight: bold; }
    .error-message { color: #e74c3c; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Инициализация сессии
if 'medical_system' not in st.session_state:
    st.session_state.medical_system = MedicalDiagnosticSystem()
    st.session_state.big_data_processor = BigDataProcessor()
    st.session_state.mqea_analyzer = MQEAAnalyzer()
    st.session_state.patients = {}
    st.session_state.diagnostic_results = {}
    st.session_state.treatment_plans = {}


# Функция для отображения логотипа
def display_mqea_logo():
    """Отображает основной логотип MQEA."""
    try:
        logo_path = "mqea_logo.png"
        if os.path.exists(logo_path):
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image(logo_path, width=200)
        else:
            st.markdown("### 🏥 MQEA")
    except Exception as e:
        st.markdown("### 🏥 MQEA")

def main():
    """Главная функция веб-интерфейса."""
    
    # Заголовок
    st.markdown('<h1 class="main-header">🏥 MQEA - Медицинская Диагностическая Система</h1>', unsafe_allow_html=True)
    st.markdown("**Автор:** Мухаммад Махизода | **Университет:** Таджикский национальный университет")
    
    # Боковая панель навигации
    st.sidebar.title("🧭 Навигация")
    page = st.sidebar.selectbox(
        "Выберите раздел:",
        [
            "🏠 Главная",
            "👥 Управление пациентами", 
            "🔍 Диагностика",
            "🔮 Прогнозирование рисков",
            "💊 Планы лечения",
            "📊 Большие данные",
            "📈 Аналитика",
            "⚙️ Настройки"
        ]
    )
    
    # Маршрутизация страниц
    if page == "🏠 Главная":
        show_home_page()
    elif page == "👥 Управление пациентами":
        show_patient_management()
    elif page == "🔍 Диагностика":
        show_diagnostic_page()
    elif page == "🔮 Прогнозирование рисков":
        show_risk_prediction()
    elif page == "💊 Планы лечения":
        show_treatment_plans()
    elif page == "📊 Большие данные":
        show_big_data_page()
    elif page == "📈 Аналитика":
        show_analytics_page()
    elif page == "⚙️ Настройки":
        show_settings_page()


def show_home_page():
    """Главная страница с обзором системы."""
    st.markdown('<h2 class="section-header">🏠 Обзор системы</h2>', unsafe_allow_html=True)
    
    # Статистика системы
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="👥 Пациентов",
            value=len(st.session_state.patients),
            delta=None
        )
    
    with col2:
        st.metric(
            label="🔍 Диагнозов",
            value=len(st.session_state.diagnostic_results),
            delta=None
        )
    
    with col3:
        st.metric(
            label="💊 Планов лечения",
            value=sum(len(plans) for plans in st.session_state.treatment_plans.values()),
            delta=None
        )
    
    with col4:
        st.metric(
            label="⚡ Статус системы",
            value="🟢 Активна",
            delta=None
        )
    
    # Быстрые действия
    st.markdown('<h3 class="section-header">🚀 Быстрые действия</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("➕ Добавить пациента", use_container_width=True):
            st.session_state.show_add_patient = True
            st.rerun()
    
    with col2:
        if st.button("🔍 Запустить диагностику", use_container_width=True):
            st.session_state.show_diagnosis = True
            st.rerun()
    
    with col3:
        if st.button("📊 Анализ больших данных", use_container_width=True):
            st.session_state.show_big_data = True
            st.rerun()
    
    # Последние результаты
    if st.session_state.diagnostic_results:
        st.markdown('<h3 class="section-header">📋 Последние результаты диагностики</h3>', unsafe_allow_html=True)
        
        recent_results = list(st.session_state.diagnostic_results.values())[-5:]
        
        for result in recent_results:
            risk_class = f"risk-{result.risk_level.value}"
            st.markdown(f"""
            <div class="metric-card">
                <strong>Пациент:</strong> {result.patient_id} | 
                <strong>Категория:</strong> {result.category.value} | 
                <strong>Риск:</strong> <span class="{risk_class}">{result.risk_level.value.upper()}</span> |
                <strong>Уверенность:</strong> {result.confidence:.2f}
            </div>
            """, unsafe_allow_html=True)


def show_patient_management():
    """Страница управления пациентами."""
    st.markdown('<h2 class="section-header">👥 Управление пациентами</h2>', unsafe_allow_html=True)
    
    # Вкладки
    tab1, tab2, tab3 = st.tabs(["➕ Добавить пациента", "📋 Список пациентов", "📊 Статистика"])
    
    with tab1:
        st.markdown("### Добавление нового пациента")
        
        with st.form("add_patient_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                patient_id = st.text_input("ID пациента", value=f"P{len(st.session_state.patients)+1:04d}")
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
            
            if st.form_submit_button("➕ Добавить пациента", use_container_width=True):
                try:
                    # Создание профиля пациента
                    profile = PatientProfile(
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
                    
                    # Добавление в систему
                    success = st.session_state.medical_system.add_patient_profile(profile)
                    
                    if success:
                        st.session_state.patients[patient_id] = profile
                        st.success(f"✅ Пациент {patient_id} успешно добавлен!")
                        st.rerun()
                    else:
                        st.error("❌ Ошибка добавления пациента")
                        
                except Exception as e:
                    st.error(f"❌ Ошибка: {e}")
    
    with tab2:
        st.markdown("### Список пациентов")
        
        if st.session_state.patients:
            # Фильтры
            col1, col2, col3 = st.columns(3)
            
            with col1:
                age_filter = st.slider("Возраст", 0, 120, (0, 120))
            
            with col2:
                gender_filter = st.selectbox("Пол", ["Все", "male", "female"])
            
            with col3:
                risk_filter = st.selectbox("Уровень риска", ["Все", "low", "medium", "high", "critical"])
            
            # Фильтрация пациентов
            filtered_patients = []
            for patient_id, patient in st.session_state.patients.items():
                if age_filter[0] <= patient.age <= age_filter[1]:
                    if gender_filter == "Все" or patient.gender == gender_filter:
                        # Проверка уровня риска (упрощенная)
                        risk_level = "low"
                        if patient.age > 65 or patient.bmi > 30:
                            risk_level = "high"
                        elif patient.age > 45 or patient.bmi > 25:
                            risk_level = "medium"
                        
                        if risk_filter == "Все" or risk_level == risk_filter:
                            filtered_patients.append((patient_id, patient, risk_level))
            
            # Отображение пациентов
            for patient_id, patient, risk_level in filtered_patients:
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
                        risk_class = f"risk-{risk_level}"
                        st.markdown(f"**Уровень риска:** <span class='{risk_class}'>{risk_level.upper()}</span>", unsafe_allow_html=True)
                        
                        if st.button(f"🔍 Диагностика", key=f"diag_{patient_id}"):
                            st.session_state.selected_patient = patient_id
                            st.session_state.show_diagnosis = True
                            st.rerun()
        else:
            st.info("👥 Пациенты не добавлены. Добавьте первого пациента во вкладке 'Добавить пациента'.")
    
    with tab3:
        st.markdown("### Статистика пациентов")
        
        if st.session_state.patients:
            # Основная статистика
            patients_data = list(st.session_state.patients.values())
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Распределение по возрасту
                ages = [p.age for p in patients_data]
                fig_age = px.histogram(x=ages, nbins=10, title="Распределение по возрасту")
                st.plotly_chart(fig_age, use_container_width=True)
            
            with col2:
                # Распределение по полу
                genders = [p.gender for p in patients_data]
                gender_counts = pd.Series(genders).value_counts()
                fig_gender = px.pie(values=gender_counts.values, names=gender_counts.index, title="Распределение по полу")
                st.plotly_chart(fig_gender, use_container_width=True)
            
            # ИМТ анализ
            bmis = [p.bmi for p in patients_data]
            fig_bmi = px.box(y=bmis, title="Распределение ИМТ")
            st.plotly_chart(fig_bmi, use_container_width=True)
        else:
            st.info("📊 Нет данных для отображения статистики.")


def show_diagnostic_page():
    """Страница диагностики."""
    st.markdown('<h2 class="section-header">🔍 Медицинская диагностика</h2>', unsafe_allow_html=True)
    
    if not st.session_state.patients:
        st.warning("⚠️ Сначала добавьте пациентов в разделе 'Управление пациентами'")
        return
    
    # Выбор пациента
    patient_options = {f"{pid} - {p.age} лет, {p.gender}": pid for pid, p in st.session_state.patients.items()}
    selected_patient_display = st.selectbox("Выберите пациента:", list(patient_options.keys()))
    selected_patient_id = patient_options[selected_patient_display]
    
    # Генерация медицинских данных
    st.markdown("### 📊 Генерация медицинских данных")
    
    col1, col2 = st.columns(2)
    
    with col1:
        duration_days = st.slider("Продолжительность (дни)", 1, 30, 7)
        sampling_hours = st.slider("Интервал измерений (часы)", 1, 24, 1)
    
    with col2:
        add_noise = st.checkbox("Добавить шум", value=True)
        add_missing = st.checkbox("Добавить пропущенные данные", value=True)
    
    if st.button("🔄 Сгенерировать данные", use_container_width=True):
        with st.spinner("Генерация медицинских данных..."):
            try:
                # Генерация данных
                patient = st.session_state.patients[selected_patient_id]
                medical_data = generate_medical_data(patient, duration_days)
                
                # Сохранение в сессии
                st.session_state.current_medical_data = medical_data
                st.session_state.current_patient_id = selected_patient_id
                
                st.success(f"✅ Данные сгенерированы: {len(medical_data)} записей")
                
            except Exception as e:
                st.error(f"❌ Ошибка генерации данных: {e}")
    
    # Анализ данных
    if 'current_medical_data' in st.session_state:
        st.markdown("### 🔬 Квантовый анализ")
        
        if st.button("⚛️ Запустить квантовый анализ", use_container_width=True):
            with st.spinner("Выполнение квантового анализа..."):
                try:
                    # Создание MedicalTimeSeries
                    medical_data = st.session_state.current_medical_data
                    indicators = ['heart_rate', 'blood_pressure_systolic', 'blood_pressure_diastolic',
                                'temperature', 'oxygen_saturation', 'respiratory_rate', 'glucose', 'cholesterol']
                    
                    time_series = MedicalTimeSeries(
                        data=medical_data.set_index('timestamp'),
                        indicators=indicators,
                        timestamps=medical_data['timestamp'].tolist(),
                        missing_data_mask=medical_data[indicators].isnull(),
                        quantum_states={},
                        metadata={'patient_id': st.session_state.current_patient_id}
                    )
                    
                    # Диагностика
                    diagnostic = st.session_state.medical_system.analyze_patient_data(
                        patient_id=st.session_state.current_patient_id,
                        medical_data=time_series
                    )
                    
                    # Сохранение результата
                    st.session_state.diagnostic_results[st.session_state.current_patient_id] = diagnostic
                    
                    st.success("✅ Квантовый анализ завершен!")
                    
                except Exception as e:
                    st.error(f"❌ Ошибка анализа: {e}")
        
        # Отображение результатов
        if st.session_state.current_patient_id in st.session_state.diagnostic_results:
            diagnostic = st.session_state.diagnostic_results[st.session_state.current_patient_id]
            
            # Основные метрики
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Категория", diagnostic.category.value)
            
            with col2:
                risk_class = f"risk-{diagnostic.risk_level.value}"
                st.markdown(f"**Уровень риска:** <span class='{risk_class}'>{diagnostic.risk_level.value.upper()}</span>", unsafe_allow_html=True)
            
            with col3:
                st.metric("Уверенность", f"{diagnostic.confidence:.2f}")
            
            with col4:
                st.metric("Срочность", f"{diagnostic.urgency_score:.2f}")
            
            # Рекомендации
            st.markdown("### 💡 Рекомендации")
            for i, rec in enumerate(diagnostic.recommendations, 1):
                st.write(f"{i}. {rec}")
            
            # Визуализация данных
            st.markdown("### 📈 Визуализация медицинских данных")
            
            medical_data = st.session_state.current_medical_data
            indicators = ['heart_rate', 'blood_pressure_systolic', 'blood_pressure_diastolic',
                        'temperature', 'oxygen_saturation', 'respiratory_rate', 'glucose', 'cholesterol']
            
            # График временных рядов
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


def generate_medical_data(patient: PatientProfile, days: int) -> pd.DataFrame:
    """Генерация медицинских данных для пациента."""
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


def show_risk_prediction():
    """Страница прогнозирования рисков."""
    st.markdown('<h2 class="section-header">🔮 Прогнозирование рисков заболеваний</h2>', unsafe_allow_html=True)
    
    if not st.session_state.patients:
        st.warning("⚠️ Сначала добавьте пациентов в разделе 'Управление пациентами'")
        return
    
    # Выбор пациента
    patient_options = {f"{pid} - {p.age} лет, {p.gender}": pid for pid, p in st.session_state.patients.items()}
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
                st.markdown("### 📊 Результаты прогнозирования")
                
                # Метрики рисков
                cols = st.columns(len(risk_predictions))
                for i, (category, risk) in enumerate(risk_predictions.items()):
                    with cols[i]:
                        risk_level = "низкий" if risk < 0.3 else "средний" if risk < 0.6 else "высокий" if risk < 0.8 else "критический"
                        risk_class = f"risk-{risk_level.replace('низкий', 'low').replace('средний', 'medium').replace('высокий', 'high').replace('критический', 'critical')}"
                        
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
                st.markdown("### 💡 Рекомендации по снижению рисков")
                
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


def show_treatment_plans():
    """Страница планов лечения."""
    st.markdown('<h2 class="section-header">💊 Планы лечения</h2>', unsafe_allow_html=True)
    
    if not st.session_state.diagnostic_results:
        st.warning("⚠️ Сначала выполните диагностику пациентов")
        return
    
    # Выбор пациента с диагнозом
    diagnostic_options = {f"{pid} - {result.category.value}": pid for pid, result in st.session_state.diagnostic_results.items()}
    selected_diagnostic_display = st.selectbox("Выберите диагноз:", list(diagnostic_options.keys()))
    selected_patient_id = diagnostic_options[selected_diagnostic_display]
    
    diagnostic = st.session_state.diagnostic_results[selected_patient_id]
    
    # Генерация плана лечения
    if st.button("💊 Создать план лечения", use_container_width=True):
        with st.spinner("Создание плана лечения..."):
            try:
                # Генерация плана лечения
                treatment_plan = st.session_state.medical_system.generate_treatment_plan(
                    patient_id=selected_patient_id,
                    diagnostic_result=diagnostic
                )
                
                # Сохранение плана
                st.session_state.treatment_plans[selected_patient_id] = treatment_plan
                
                st.success(f"✅ План лечения создан: {len(treatment_plan)} рекомендаций")
                
            except Exception as e:
                st.error(f"❌ Ошибка создания плана: {e}")
    
    # Отображение плана лечения
    if selected_patient_id in st.session_state.treatment_plans:
        treatment_plan = st.session_state.treatment_plans[selected_patient_id]
        
        st.markdown("### 📋 План лечения")
        
        for i, treatment in enumerate(treatment_plan, 1):
            with st.expander(f"💊 {treatment.description}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Тип:** {treatment.recommendation_type}")
                    st.write(f"**Приоритет:** {treatment.priority}")
                    st.write(f"**Эффективность:** {treatment.expected_effectiveness:.1%}")
                
                with col2:
                    st.write(f"**Побочные эффекты:** {', '.join(treatment.side_effects) if treatment.side_effects else 'Нет'}")
                    st.write(f"**Противопоказания:** {', '.join(treatment.contraindications) if treatment.contraindications else 'Нет'}")
                
                if treatment.monitoring_required:
                    st.write(f"**Мониторинг:** {', '.join(treatment.monitoring_required)}")


def show_big_data_page():
    """Страница работы с большими данными."""
    st.markdown('<h2 class="section-header">📊 Обработка больших данных</h2>', unsafe_allow_html=True)
    
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
                for patient in st.session_state.patients.values():
                    patient_data = generate_medical_data(patient, days=1)
                    big_data.append(patient_data)
                
                big_dataframe = pd.concat(big_data, ignore_index=True)
                st.session_state.big_data = big_dataframe
                
                st.success(f"✅ Сгенерированы данные: {len(big_dataframe):,} записей")
                
            except Exception as e:
                st.error(f"❌ Ошибка генерации данных: {e}")
    
    # Обработка больших данных
    if 'big_data' in st.session_state and st.button("⚡ Обработать большие данные", use_container_width=True):
        with st.spinner("Обработка больших данных..."):
            try:
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
                st.markdown("### 📊 Результаты обработки")
                
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
                
                st.markdown("### 📈 Статистика производительности")
                st.json(stats)
                
                processor.close()
                
            except Exception as e:
                st.error(f"❌ Ошибка обработки: {e}")


def show_analytics_page():
    """Страница аналитики."""
    st.markdown('<h2 class="section-header">📈 Аналитика и отчеты</h2>', unsafe_allow_html=True)
    
    if not st.session_state.diagnostic_results:
        st.warning("⚠️ Нет данных для анализа")
        return
    
    # Общая статистика
    st.markdown("### 📊 Общая статистика")
    
    # Распределение по категориям
    categories = [result.category.value for result in st.session_state.diagnostic_results.values()]
    category_counts = pd.Series(categories).value_counts()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_categories = px.pie(values=category_counts.values, names=category_counts.index, title="Распределение по категориям")
        st.plotly_chart(fig_categories, use_container_width=True)
    
    with col2:
        # Распределение по уровням риска
        risk_levels = [result.risk_level.value for result in st.session_state.diagnostic_results.values()]
        risk_counts = pd.Series(risk_levels).value_counts()
        
        fig_risks = px.bar(x=risk_counts.index, y=risk_counts.values, title="Распределение по уровням риска")
        st.plotly_chart(fig_risks, use_container_width=True)
    
    # Тренды уверенности
    confidences = [result.confidence for result in st.session_state.diagnostic_results.values()]
    timestamps = [result.timestamp for result in st.session_state.diagnostic_results.values()]
    
    fig_confidence = px.line(
        x=timestamps, 
        y=confidences, 
        title="Тренд уверенности диагностики",
        labels={'x': 'Время', 'y': 'Уверенность'}
    )
    st.plotly_chart(fig_confidence, use_container_width=True)


def show_settings_page():
    """Страница настроек."""
    st.markdown('<h2 class="section-header">⚙️ Настройки системы</h2>', unsafe_allow_html=True)
    
    # Настройки MQEA
    st.markdown("### 🔬 Настройки MQEA")
    
    col1, col2 = st.columns(2)
    
    with col1:
        quantum_hbar = st.number_input("Постоянная Планка", min_value=0.1, max_value=2.0, value=1.0, step=0.1)
        quantum_threshold = st.number_input("Порог квантовой запутанности", min_value=0.1, max_value=1.0, value=0.3, step=0.1)
    
    with col2:
        enable_imputation = st.checkbox("Квантовое заполнение пропусков", value=True)
        enable_patterns = st.checkbox("Обнаружение паттернов", value=True)
    
    # Настройки медицинской системы
    st.markdown("### 🏥 Настройки медицинской системы")
    
    col1, col2 = st.columns(2)
    
    with col1:
        max_workers = st.number_input("Максимальное количество процессов", min_value=1, max_value=16, value=4)
        enable_ml = st.checkbox("Машинное обучение", value=True)
    
    with col2:
        enable_realtime = st.checkbox("Мониторинг в реальном времени", value=True)
        memory_limit = st.number_input("Лимит памяти (ГБ)", min_value=1, max_value=32, value=8)
    
    if st.button("💾 Сохранить настройки", use_container_width=True):
        st.success("✅ Настройки сохранены!")
    
    # Информация о системе
    st.markdown("### ℹ️ Информация о системе")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"""
        **Версия MQEA:** 2.0.0  
        **Автор:** Мухаммад Махизода  
        **Университет:** Таджикский национальный университет  
        **Статус:** Активна
        """)
    
    with col2:
        st.info(f"""
        **Пациентов:** {len(st.session_state.patients)}  
        **Диагнозов:** {len(st.session_state.diagnostic_results)}  
        **Планов лечения:** {sum(len(plans) for plans in st.session_state.treatment_plans.values())}  
        **Время работы:** {datetime.now().strftime('%H:%M:%S')}
        """)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Упрощенный медицинский веб-интерфейс MQEA
с основными функциями диагностики и управления пациентами.

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

# Добавляем путь к модулям
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mqea.medical_diagnostic_system import (
    MedicalDiagnosticSystem, PatientProfile, DiagnosticResult, 
    RiskLevel, DiagnosticCategory
)
from mqea.core import MQEAAnalyzer
from mqea.data_processor import MedicalTimeSeries


# Настройка страницы
st.set_page_config(
    page_title="MQEA - Медицинская Система",
    page_icon="🏥",
    layout="wide"
)

# CSS стили
st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
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
</style>
""", unsafe_allow_html=True)

# Инициализация сессии
if 'medical_system' not in st.session_state:
    st.session_state.medical_system = MedicalDiagnosticSystem()
    st.session_state.patients = {}
    st.session_state.diagnostic_results = {}

def main():
    """Главная функция."""
    
    # Заголовок
    st.markdown('<h1 class="main-header">🏥 MQEA - Медицинская Диагностическая Система</h1>', unsafe_allow_html=True)
    st.markdown("**Автор:** Мухаммад Махизода | **Университет:** Таджикский национальный университет")
    
    # Вкладки
    tab1, tab2, tab3, tab4 = st.tabs(["🏠 Главная", "👥 Пациенты", "🔍 Диагностика", "📊 Аналитика"])
    
    with tab1:
        show_home()
    
    with tab2:
        show_patients()
    
    with tab3:
        show_diagnostics()
    
    with tab4:
        show_analytics()


def show_home():
    """Главная страница."""
    st.markdown("### 🏠 Обзор системы")
    
    # Статистика
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("👥 Пациентов", len(st.session_state.patients))
    
    with col2:
        st.metric("🔍 Диагнозов", len(st.session_state.diagnostic_results))
    
    with col3:
        st.metric("⚡ Статус", "🟢 Активна")
    
    # Быстрые действия
    st.markdown("### 🚀 Быстрые действия")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("➕ Добавить пациента", use_container_width=True):
            st.session_state.show_add_patient = True
            st.rerun()
    
    with col2:
        if st.button("🔍 Запустить диагностику", use_container_width=True):
            st.session_state.show_diagnosis = True
            st.rerun()
    
    # Последние результаты
    if st.session_state.diagnostic_results:
        st.markdown("### 📋 Последние результаты")
        
        recent_results = list(st.session_state.diagnostic_results.values())[-3:]
        
        for result in recent_results:
            risk_class = f"risk-{result.risk_level.value}"
            st.markdown(f"""
            <div class="metric-card">
                <strong>Пациент:</strong> {result.patient_id} | 
                <strong>Категория:</strong> {result.category.value} | 
                <strong>Риск:</strong> <span class="{risk_class}">{result.risk_level.value.upper()}</span>
            </div>
            """, unsafe_allow_html=True)


def show_patients():
    """Управление пациентами."""
    st.markdown("### 👥 Управление пациентами")
    
    # Добавление пациента
    with st.expander("➕ Добавить нового пациента"):
        with st.form("add_patient"):
            col1, col2 = st.columns(2)
            
            with col1:
                patient_id = st.text_input("ID пациента", value=f"P{len(st.session_state.patients)+1:04d}")
                age = st.number_input("Возраст", min_value=0, max_value=120, value=50)
                gender = st.selectbox("Пол", ["male", "female"])
            
            with col2:
                weight = st.number_input("Вес (кг)", min_value=20.0, max_value=200.0, value=70.0)
                height = st.number_input("Рост (см)", min_value=100.0, max_value=250.0, value=175.0)
                medical_history = st.multiselect(
                    "Медицинская история",
                    ["diabetes", "hypertension", "heart_disease", "cancer", "asthma", "none"]
                )
            
            smoking = st.checkbox("Курит")
            sedentary = st.checkbox("Малоподвижный образ жизни")
            
            if st.form_submit_button("➕ Добавить пациента"):
                try:
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
                    
                    success = st.session_state.medical_system.add_patient_profile(profile)
                    
                    if success:
                        st.session_state.patients[patient_id] = profile
                        st.success(f"✅ Пациент {patient_id} добавлен!")
                        st.rerun()
                    else:
                        st.error("❌ Ошибка добавления пациента")
                        
                except Exception as e:
                    st.error(f"❌ Ошибка: {e}")
    
    # Список пациентов
    if st.session_state.patients:
        st.markdown("### 📋 Список пациентов")
        
        for patient_id, patient in st.session_state.patients.items():
            with st.expander(f"👤 {patient_id} - {patient.age} лет, {patient.gender}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**Возраст:** {patient.age}")
                    st.write(f"**Пол:** {patient.gender}")
                    st.write(f"**ИМТ:** {patient.bmi:.1f}")
                
                with col2:
                    st.write(f"**История болезней:** {', '.join(patient.medical_history) if patient.medical_history else 'Нет'}")
                    st.write(f"**Курит:** {'Да' if patient.lifestyle_factors.get('smoking', False) else 'Нет'}")
                
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
                    
                    risk_class = f"risk-{risk_level}"
                    st.markdown(f"**Уровень риска:** <span class='{risk_class}'>{risk_level.upper()}</span>", unsafe_allow_html=True)
                    
                    if st.button(f"🔍 Диагностика", key=f"diag_{patient_id}"):
                        st.session_state.selected_patient = patient_id
                        st.session_state.show_diagnosis = True
                        st.rerun()
    else:
        st.info("👥 Пациенты не добавлены. Добавьте первого пациента выше.")


def show_diagnostics():
    """Диагностика."""
    st.markdown("### 🔍 Медицинская диагностика")
    
    if not st.session_state.patients:
        st.warning("⚠️ Сначала добавьте пациентов")
        return
    
    # Выбор пациента
    patient_options = {f"{pid} - {p.age} лет, {p.gender}": pid for pid, p in st.session_state.patients.items()}
    selected_patient_display = st.selectbox("Выберите пациента:", list(patient_options.keys()))
    selected_patient_id = patient_options[selected_patient_display]
    
    # Генерация данных
    st.markdown("#### 📊 Генерация медицинских данных")
    
    col1, col2 = st.columns(2)
    
    with col1:
        duration_days = st.slider("Продолжительность (дни)", 1, 30, 7)
    
    with col2:
        add_noise = st.checkbox("Добавить шум", value=True)
    
    if st.button("🔄 Сгенерировать данные"):
        with st.spinner("Генерация данных..."):
            try:
                patient = st.session_state.patients[selected_patient_id]
                medical_data = generate_medical_data(patient, duration_days)
                st.session_state.current_medical_data = medical_data
                st.session_state.current_patient_id = selected_patient_id
                st.success(f"✅ Данные сгенерированы: {len(medical_data)} записей")
            except Exception as e:
                st.error(f"❌ Ошибка: {e}")
    
    # Анализ
    if 'current_medical_data' in st.session_state:
        st.markdown("#### ⚛️ Квантовый анализ")
        
        if st.button("🔬 Запустить анализ"):
            with st.spinner("Анализ..."):
                try:
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
                    
                    diagnostic = st.session_state.medical_system.analyze_patient_data(
                        patient_id=st.session_state.current_patient_id,
                        medical_data=time_series
                    )
                    
                    st.session_state.diagnostic_results[st.session_state.current_patient_id] = diagnostic
                    st.success("✅ Анализ завершен!")
                    
                except Exception as e:
                    st.error(f"❌ Ошибка анализа: {e}")
        
        # Результаты
        if st.session_state.current_patient_id in st.session_state.diagnostic_results:
            diagnostic = st.session_state.diagnostic_results[st.session_state.current_patient_id]
            
            # Метрики
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Категория", diagnostic.category.value)
            
            with col2:
                risk_class = f"risk-{diagnostic.risk_level.value}"
                st.markdown(f"**Риск:** <span class='{risk_class}'>{diagnostic.risk_level.value.upper()}</span>", unsafe_allow_html=True)
            
            with col3:
                st.metric("Уверенность", f"{diagnostic.confidence:.2f}")
            
            with col4:
                st.metric("Срочность", f"{diagnostic.urgency_score:.2f}")
            
            # Рекомендации
            st.markdown("#### 💡 Рекомендации")
            for i, rec in enumerate(diagnostic.recommendations, 1):
                st.write(f"{i}. {rec}")
            
            # График
            st.markdown("#### 📈 Визуализация")
            
            medical_data = st.session_state.current_medical_data
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


def generate_medical_data(patient: PatientProfile, days: int) -> pd.DataFrame:
    """Генерация медицинских данных."""
    n_records = days * 24
    
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
    
    if patient.lifestyle_factors.get('smoking', False):
        base_values['oxygen_saturation'] -= 2
        base_values['respiratory_rate'] += 2
    
    if patient.lifestyle_factors.get('sedentary', False):
        base_values['heart_rate'] += 5
        base_values['glucose'] += 0.5
    
    if patient.bmi > 30:
        base_values['blood_pressure_systolic'] += 10
        base_values['glucose'] += 1.0
    
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


def show_analytics():
    """Аналитика."""
    st.markdown("### 📊 Аналитика")
    
    if not st.session_state.diagnostic_results:
        st.warning("⚠️ Нет данных для анализа")
        return
    
    # Статистика
    categories = [result.category.value for result in st.session_state.diagnostic_results.values()]
    category_counts = pd.Series(categories).value_counts()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_categories = px.pie(values=category_counts.values, names=category_counts.index, title="Категории заболеваний")
        st.plotly_chart(fig_categories, use_container_width=True)
    
    with col2:
        risk_levels = [result.risk_level.value for result in st.session_state.diagnostic_results.values()]
        risk_counts = pd.Series(risk_levels).value_counts()
        
        fig_risks = px.bar(x=risk_counts.index, y=risk_counts.values, title="Уровни риска")
        st.plotly_chart(fig_risks, use_container_width=True)
    
    # Таблица результатов
    st.markdown("#### 📋 Все результаты диагностики")
    
    results_data = []
    for result in st.session_state.diagnostic_results.values():
        results_data.append({
            'Пациент': result.patient_id,
            'Категория': result.category.value,
            'Уровень риска': result.risk_level.value,
            'Уверенность': f"{result.confidence:.2f}",
            'Срочность': f"{result.urgency_score:.2f}",
            'Время': result.timestamp.strftime('%Y-%m-%d %H:%M')
        })
    
    if results_data:
        df_results = pd.DataFrame(results_data)
        st.dataframe(df_results, use_container_width=True)


if __name__ == "__main__":
    main()

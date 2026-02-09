"""
Демонстрация детской квантовой диагностической системы MQEA-Pediatric.
Система для выявления заболеваний у детей от рождения до 10 лет.

Особенности демо:
- Интерактивный интерфейс для ввода детских данных
- Визуализация квантового анализа
- Рекомендации по лечению и наблюдению
- Адаптивные нормы для разных возрастов
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import json

# Импорт нашей детской квантовой системы
from mqea.pediatric_quantum_system import (
    PediatricQuantumEngine, 
    PediatricVitalSigns, 
    AgeGroup, 
    PediatricCondition
)

# Настройка страницы
st.set_page_config(
    page_title="MQEA-Pediatric: Квантовая диагностика детей",
    page_icon="👶",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Кастомный CSS для детского интерфейса
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #FF6B9D, #C44569, #F8B500);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        font-size: 2rem;
        font-weight: bold;
    }
    
    .age-group-card {
        background: #E8F4FD;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #3498DB;
        margin: 0.5rem 0;
    }
    
    .condition-alert {
        background: #FFE6E6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #E74C3C;
        margin: 0.5rem 0;
    }
    
    .condition-warning {
        background: #FFF3CD;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #F39C12;
        margin: 0.5rem 0;
    }
    
    .condition-info {
        background: #D1ECF1;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #17A2B8;
        margin: 0.5rem 0;
    }
    
    .quantum-stats {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #FF6B9D, #C44569);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, #C44569, #FF6B9D);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Главная функция демонстрации."""
    
    # Заголовок
    st.markdown("""
    <div class="main-header">
        👶 MQEA-Pediatric: Квантовая диагностика детей
        <br><small style="font-size: 1rem; opacity: 0.9;">
        Революционная система раннего выявления заболеваний у детей от рождения до 10 лет
        </small>
    </div>
    """, unsafe_allow_html=True)
    
    # Инициализация квантового движка
    if 'pediatric_engine' not in st.session_state:
        st.session_state.pediatric_engine = PediatricQuantumEngine()
    
    # Сайдбар для ввода данных
    with st.sidebar:
        st.markdown("## 📋 Данные ребенка")
        
        # Возраст
        age_input = st.selectbox(
            "Выберите возрастную группу:",
            ["0-1 месяц", "1-12 месяцев", "1-3 года", "3-6 лет", "6-10 лет"]
        )
        
        age_months = get_age_months(age_input)
        
        # Основные показатели
        st.markdown("### 🩺 Жизненные показатели")
        
        heart_rate = st.number_input(
            "Частота сердечных сокращений (уд/мин):",
            min_value=30, max_value=300, value=get_default_value('heart_rate', age_months)
        )
        
        respiratory_rate = st.number_input(
            "Частота дыхания (дых/мин):",
            min_value=5, max_value=80, value=get_default_value('respiratory_rate', age_months)
        )
        
        bp_systolic = st.number_input(
            "Систолическое давление (мм рт.ст.):",
            min_value=40, max_value=200, value=get_default_value('blood_pressure_systolic', age_months)
        )
        
        bp_diastolic = st.number_input(
            "Диастолическое давление (мм рт.ст.):",
            min_value=20, max_value=150, value=get_default_value('blood_pressure_diastolic', age_months)
        )
        
        temperature = st.number_input(
            "Температура тела (°C):",
            min_value=35.0, max_value=42.0, value=36.8, step=0.1
        )
        
        oxygen_saturation = st.number_input(
            "Насыщение кислородом (%):",
            min_value=70, max_value=100, value=98
        )
        
        st.markdown("### 📏 Антропометрические данные")
        
        weight = st.number_input(
            "Вес (кг):",
            min_value=1.0, max_value=50.0, value=get_default_value('weight', age_months), step=0.1
        )
        
        height = st.number_input(
            "Рост (см):",
            min_value=30.0, max_value=200.0, value=get_default_value('height', age_months), step=0.5
        )
        
        head_circumference = st.number_input(
            "Окружность головы (см):",
            min_value=25.0, max_value=70.0, value=get_default_value('head_circumference', age_months), step=0.1
        )
        
        # Кнопка анализа
        analyze_button = st.button("🔬 Запустить квантовый анализ", type="primary")
    
    # Основной контент
    if analyze_button:
        # Создаем объект жизненных показателей
        vital_signs = PediatricVitalSigns(
            age_months=age_months,
            heart_rate=heart_rate,
            respiratory_rate=respiratory_rate,
            blood_pressure_systolic=bp_systolic,
            blood_pressure_diastolic=bp_diastolic,
            temperature=temperature,
            oxygen_saturation=oxygen_saturation,
            weight_kg=weight,
            height_cm=height,
            head_circumference_cm=head_circumference
        )
        
        # Выполняем квантовый анализ
        with st.spinner("🔄 Выполняется квантовый анализ..."):
            detected_conditions = st.session_state.pediatric_engine.detect_pediatric_conditions(
                vital_signs, quantum_threshold=0.6
            )
            
            quantum_report = st.session_state.pediatric_engine.generate_pediatric_quantum_report(
                vital_signs, detected_conditions
            )
        
        # Отображаем результаты
        display_results(vital_signs, detected_conditions, quantum_report)
    
    else:
        # Показываем информацию о системе
        display_system_info()

def get_age_months(age_input: str) -> int:
    """Преобразует текстовый ввод возраста в месяцы."""
    age_mapping = {
        "0-1 месяц": 0.5,
        "1-12 месяцев": 6,
        "1-3 года": 18,
        "3-6 лет": 48,
        "6-10 лет": 84
    }
    return int(age_mapping[age_input])

def get_default_value(indicator: str, age_months: int) -> float:
    """Возвращает нормальные значения для показателя в зависимости от возраста."""
    engine = PediatricQuantumEngine()
    age_group = engine._determine_age_group(age_months)
    
    # Получаем нормальный диапазон для возраста
    normal_range = engine.pediatric_ranges[age_group].get(indicator, (50, 100))
    
    # Возвращаем среднее значение диапазона
    return (normal_range[0] + normal_range[1]) / 2

def display_system_info():
    """Отображает информацию о системе."""
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ## 🌟 Возможности системы MQEA-Pediatric
        
        ### ⚛️ Квантовые технологии:
        - **Квантовая запутанность** для анализа корреляций между показателями
        - **Квантовая когерентность** для оценки стабильности функций
        - **Квантовая суперпозиция** для множественной диагностики
        
        ### 👶 Специализация для детей:
        - Возрастные нормы от рождения до 10 лет
        - Факторы роста и развития
        - Раннее выявление врожденных патологий
        - Адаптивные квантовые алгоритмы
        
        ### 🔍 Обнаруживаемые состояния:
        - Врожденные пороки сердца
        - Респираторные инфекции
        - Задержка развития
        - Метаболические нарушения
        """)
    
    with col2:
        # Создаем диаграмму возрастных групп
        age_groups = ["Новорожденные\n(0-1 мес)", "Младенцы\n(1-12 мес)", 
                     "Дети раннего возраста\n(1-3 года)", "Дошкольники\n(3-6 лет)", 
                     "Школьники\n(6-10 лет)"]
        
        heart_rate_norms = [130, 120, 110, 100, 85]  # Средние нормы ЧСС
        respiratory_norms = [45, 32, 25, 22, 20]     # Средние нормы ЧДД
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=("Частота сердечных сокращений", "Частота дыхания"),
            specs=[[{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        fig.add_trace(
            go.Bar(x=age_groups, y=heart_rate_norms, name="ЧСС", marker_color="#FF6B9D"),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Bar(x=age_groups, y=respiratory_norms, name="ЧДД", marker_color="#3498DB"),
            row=1, col=2
        )
        
        fig.update_layout(
            title="Возрастные нормы жизненных показателей",
            showlegend=False,
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Показываем примеры квантовых состояний
        st.markdown("### ⚛️ Примеры квантовых состояний:")
        
        quantum_examples = pd.DataFrame({
            "Показатель": ["ЧСС", "ЧДД", "АД", "Температура", "SpO2"],
            "Квантовое состояние": ["|ψ_HR⟩", "|ψ_RR⟩", "|ψ_BP⟩", "|ψ_T⟩", "|ψ_SpO2⟩"],
            "Амплитуда": ["α₁", "α₂", "α₃", "α₄", "α₅"],
            "Фаза": ["φ₁", "φ₂", "φ₃", "φ₄", "φ₅"]
        })
        
        st.dataframe(quantum_examples, use_container_width=True)

def display_results(vital_signs: PediatricVitalSigns, 
                   detected_conditions: list, 
                   quantum_report: dict):
    """Отображает результаты анализа."""
    
    # Общая оценка
    st.markdown("## 📊 Результаты квантового анализа")
    
    assessment = quantum_report['overall_assessment']
    if "✅" in assessment:
        st.success(assessment)
    elif "🚨" in assessment:
        st.error(assessment)
    elif "⚠️" in assessment:
        st.warning(assessment)
    else:
        st.info(assessment)
    
    # Квантовая статистика
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="quantum-stats">
            <h3>{quantum_report['quantum_analysis']['total_quantum_states']}</h3>
            <p>Квантовых состояний</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="quantum-stats">
            <h3>{quantum_report['quantum_analysis']['entangled_pairs']}</h3>
            <p>Запутанных пар</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        coherence = quantum_report['quantum_analysis']['quantum_coherence']
        st.markdown(f"""
        <div class="quantum-stats">
            <h3>{coherence:.3f}</h3>
            <p>Квантовая когерентность</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        dev_factor = quantum_report['quantum_analysis']['developmental_quantum_factor']
        st.markdown(f"""
        <div class="quantum-stats">
            <h3>{dev_factor:.1f}</h3>
            <p>Фактор развития</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Информация о пациенте
    st.markdown("## 👶 Информация о ребенке")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="age-group-card">
            <h4>📅 Возрастная группа</h4>
            <p><strong>Возраст:</strong> {vital_signs.age_months} месяцев</p>
            <p><strong>Группа:</strong> {quantum_report['patient_info']['age_group']}</p>
            <p><strong>Стадия развития:</strong> {quantum_report['patient_info']['developmental_stage']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Создаем радиальную диаграмму жизненных показателей
        indicators = ['ЧСС', 'ЧДД', 'АД сист.', 'АД диаст.', 'Темп.', 'SpO2']
        values = [
            vital_signs.heart_rate,
            vital_signs.respiratory_rate,
            vital_signs.blood_pressure_systolic,
            vital_signs.blood_pressure_diastolic,
            vital_signs.temperature * 10,  # Масштабируем для визуализации
            vital_signs.oxygen_saturation
        ]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=indicators,
            fill='toself',
            name='Текущие значения',
            line_color='#FF6B9D'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max(values) * 1.1]
                )),
            showlegend=True,
            title="Жизненные показатели"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Обнаруженные состояния
    if detected_conditions:
        st.markdown("## 🚨 Обнаруженные состояния")
        
        for i, condition in enumerate(detected_conditions):
            probability = condition['probability']
            condition_name = condition['condition']
            
            if probability > 0.8:
                alert_class = "condition-alert"
                icon = "🚨"
            elif probability > 0.6:
                alert_class = "condition-warning"
                icon = "⚠️"
            else:
                alert_class = "condition-info"
                icon = "ℹ️"
            
            st.markdown(f"""
            <div class="{alert_class}">
                <h4>{icon} {condition_name}</h4>
                <p><strong>Вероятность:</strong> {probability:.1%}</p>
                <p><strong>Квантовая подпись:</strong> {condition['quantum_signature']}</p>
                
                <h5>📋 Рекомендации:</h5>
                <ul>
            """, unsafe_allow_html=True)
            
            for rec in condition['recommendations']:
                st.markdown(f"<li>{rec}</li>", unsafe_allow_html=True)
            
            st.markdown("</ul></div>", unsafe_allow_html=True)
            
            # Показываем детали анализа
            with st.expander(f"🔬 Детали квантового анализа: {condition_name}"):
                st.json(condition['matched_indicators'])
    
    else:
        st.success("✅ Квантовый анализ не выявил значимых отклонений от нормы для данного возраста.")
    
    # Рекомендации
    st.markdown("## 📋 Общие рекомендации")
    
    recommendations = quantum_report['recommendations']
    for i, rec in enumerate(recommendations, 1):
        st.markdown(f"{i}. {rec}")
    
    # Экспорт отчета
    st.markdown("## 💾 Экспорт отчета")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📄 Скачать PDF отчет"):
            st.info("Функция экспорта PDF будет добавлена в следующей версии")
    
    with col2:
        if st.button("📊 Экспорт JSON данных"):
            # Создаем JSON для экспорта
            export_data = {
                "timestamp": quantum_report['timestamp'],
                "patient_info": quantum_report['patient_info'],
                "vital_signs": quantum_report['vital_signs'],
                "quantum_analysis": quantum_report['quantum_analysis'],
                "detected_conditions": detected_conditions,
                "recommendations": recommendations
            }
            
            st.download_button(
                label="💾 Скачать JSON",
                data=json.dumps(export_data, indent=2, ensure_ascii=False),
                file_name=f"pediatric_quantum_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

if __name__ == "__main__":
    main()

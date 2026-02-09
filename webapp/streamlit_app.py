"""
Современный веб-интерфейс MQEA на Streamlit.

Автор: Мухаммад Махизода
Таджикский национальный университет
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import requests
import json
from datetime import datetime, timedelta
import time
import sys
import os

# Добавляем путь к модулям
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mqea import MQEAAnalyzer, MQEAVisualizer
from config import get_settings
from utils.logo_utils import display_main_logo, display_sidebar_logo


# Настройки страницы
st.set_page_config(
    page_title="MQEA - Medical Quantum Entanglement Analysis",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Получение настроек
settings = get_settings()

# Инициализация анализатора
@st.cache_resource
def get_analyzer():
    return MQEAAnalyzer()

@st.cache_resource  
def get_visualizer():
    return MQEAVisualizer()

analyzer = get_analyzer()
visualizer = get_visualizer()

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

# Боковая панель
st.sidebar.title("⚙️ Настройки анализа")

# Кнопка AI-помощника
if st.sidebar.button("🤖 AI Помощник", type="primary", use_container_width=True):
    st.switch_page("ai_chat_app.py")

st.sidebar.markdown("---")

# Выбор режима работы с данными
analysis_mode = st.sidebar.selectbox(
    "Режим анализа",
    ["Генерация данных", "Загрузка файла", "API подключение"],
    help="Выберите способ получения данных для анализа"
)

# Настройки генерации данных
if analysis_mode == "Генерация данных":
    st.sidebar.subheader("📊 Параметры генерации")
    
    duration_hours = st.sidebar.slider(
        "Продолжительность (часы)",
        min_value=1,
        max_value=168,  # неделя
        value=24,
        help="Продолжительность генерируемых данных"
    )
    
    sampling_rate = st.sidebar.selectbox(
        "Частота дискретизации",
        [1, 5, 10, 15, 30, 60],
        index=2,  # 10 минут по умолчанию
        help="Интервал между измерениями в минутах"
    )
    
    add_noise = st.sidebar.checkbox("Добавить шум", value=True)
    add_missing = st.sidebar.checkbox("Добавить пропуски", value=True)
    
    if st.sidebar.button("🔄 Сгенерировать данные", type="primary"):
        with st.spinner("Генерация данных..."):
            time_series = analyzer.generate_synthetic_data(
                duration_hours=duration_hours,
                sampling_rate_minutes=sampling_rate,
                add_noise=add_noise,
                add_missing_data=add_missing
            )
            st.session_state['time_series'] = time_series
            st.session_state['data_ready'] = True
        st.success("Данные успешно сгенерированы!")

# Загрузка файла
elif analysis_mode == "Загрузка файла":
    st.sidebar.subheader("📁 Загрузка файла")
    
    uploaded_file = st.sidebar.file_uploader(
        "Выберите файл с медицинскими данными",
        type=['csv', 'xlsx', 'json'],
        help="Поддерживаются форматы CSV, XLSX и JSON"
    )
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
            elif uploaded_file.name.endswith('.json'):
                df = pd.read_json(uploaded_file)
            
            st.session_state['uploaded_data'] = df
            st.session_state['data_ready'] = True
            st.success(f"Файл {uploaded_file.name} успешно загружен!")
            
        except Exception as e:
            st.error(f"Ошибка при загрузке файла: {str(e)}")

# API подключение
elif analysis_mode == "API подключение":
    st.sidebar.subheader("🌐 API настройки")
    
    api_url = st.sidebar.text_input(
        "URL API",
        value="http://localhost:8000",
        help="Адрес MQEA API сервера"
    )
    
    if st.sidebar.button("🔗 Подключиться к API"):
        try:
            response = requests.get(f"{api_url}/health", timeout=5)
            if response.status_code == 200:
                st.success("Успешно подключено к API!")
                st.session_state['api_connected'] = True
                st.session_state['api_url'] = api_url
            else:
                st.error("Ошибка подключения к API")
        except Exception as e:
            st.error(f"Ошибка подключения: {str(e)}")

# Основная область анализа
if st.session_state.get('data_ready', False):
    
    # Вкладки для разных типов анализа
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Данные", 
        "🔬 Квантовый анализ", 
        "🔧 Заполнение пропусков",
        "🔍 Обнаружение паттернов",
        "📈 Визуализация"
    ])
    
    with tab1:
        st.subheader("📊 Медицинские данные")
        
        if 'time_series' in st.session_state:
            time_series = st.session_state['time_series']
            
            # Статистика данных
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Показателей", len(time_series.indicators))
            with col2:
                st.metric("Точек данных", len(time_series.timestamps))
            with col3:
                st.metric("Пропущенных данных", f"{time_series.metadata['missing_percentage']:.1f}%")
            with col4:
                duration = (time_series.timestamps[-1] - time_series.timestamps[0]).total_seconds() / 3600
                st.metric("Продолжительность", f"{duration:.1f} ч")
            
            # Таблица данных
            st.subheader("Таблица данных")
            df_display = time_series.data.copy()
            df_display.index = df_display.index.strftime('%Y-%m-%d %H:%M')
            st.dataframe(df_display, use_container_width=True)
            
            # График временных рядов
            st.subheader("Временные ряды")
            fig = visualizer.plot_time_series(
                time_series, 
                indicators=time_series.indicators[:4],  # Первые 4 показателя
                interactive=True
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("🔬 Квантовый анализ запутанности")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            quantum_threshold = st.slider(
                "Порог запутанности",
                min_value=0.0,
                max_value=1.0,
                value=0.5,
                step=0.1,
                help="Минимальная сила запутанности для учета"
            )
            
            time_windows = st.multiselect(
                "Временные окна",
                options=[12, 24, 48, 72],
                default=[24, 48],
                help="Окна для анализа в часах"
            )
            
            if st.button("🚀 Запустить квантовый анализ", type="primary"):
                with st.spinner("Выполнение квантового анализа..."):
                    start_time = time.time()
                    
                    quantum_results = analyzer.quantum_entanglement_analysis(
                        time_series=time_series,
                        quantum_threshold=quantum_threshold,
                        time_windows=time_windows
                    )
                    
                    analysis_time = time.time() - start_time
                    st.session_state['quantum_results'] = quantum_results
                    st.session_state['analysis_time'] = analysis_time
                
                st.success(f"Анализ завершен за {analysis_time:.2f} секунд!")
        
        with col2:
            if 'quantum_results' in st.session_state:
                results = st.session_state['quantum_results']
                
                # Метрики анализа
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Когерентность", f"{results['quantum_signatures']['quantum_coherence']:.3f}")
                with col2:
                    st.metric("Энтропия", f"{results['quantum_signatures']['entanglement_entropy']:.3f}")
                with col3:
                    st.metric("Состояний", results['quantum_signatures']['total_quantum_states'])
                
                # Матрица запутанности
                if results['quantum_entanglements']:
                    latest_entanglement = results['quantum_entanglements'][-1]
                    entanglement_matrix = np.array(latest_entanglement['entanglement_matrix'])
                    
                    fig = visualizer.plot_entanglement_heatmap(
                        entanglement_matrix,
                        time_series.indicators,
                        "Матрица квантовой запутанности"
                    )
                    st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("🔧 Заполнение пропущенных данных")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            method = st.selectbox(
                "Метод заполнения",
                ["quantum", "linear", "mean"],
                help="Выберите метод заполнения пропусков"
            )
            
            max_iterations = st.slider(
                "Максимальные итерации",
                min_value=10,
                max_value=200,
                value=100,
                help="Максимальное количество итераций для квантового метода"
            )
            
            if st.button("🔧 Заполнить пропуски", type="primary"):
                with st.spinner("Заполнение пропущенных данных..."):
                    start_time = time.time()
                    
                    filled_data = analyzer.fill_missing_data(
                        time_series=time_series,
                        method=method,
                        max_iterations=max_iterations
                    )
                    
                    processing_time = time.time() - start_time
                    st.session_state['filled_data'] = filled_data
                    st.session_state['processing_time'] = processing_time
                
                st.success(f"Заполнение завершено за {processing_time:.2f} секунд!")
        
        with col2:
            if 'filled_data' in st.session_state:
                filled_data = st.session_state['filled_data']
                
                # Сравнение до и после
                st.subheader("Сравнение данных")
                
                original_missing = time_series.missing_data_mask.sum().sum()
                filled_missing = filled_data.missing_data_mask.sum().sum()
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Пропусков до", original_missing)
                with col2:
                    st.metric("Пропусков после", filled_missing)
                
                # График заполненных данных
                fig = visualizer.plot_time_series(
                    filled_data,
                    indicators=time_series.indicators[:4],
                    interactive=True
                )
                st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.subheader("🔍 Обнаружение паттернов")
        
        if st.button("🔍 Найти паттерны", type="primary"):
            with st.spinner("Обнаружение паттернов..."):
                start_time = time.time()
                
                patterns = analyzer.detect_patterns(time_series=time_series)
                
                detection_time = time.time() - start_time
                st.session_state['patterns'] = patterns
                st.session_state['detection_time'] = detection_time
            
            st.success(f"Обнаружено {len(patterns)} паттернов за {detection_time:.2f} секунд!")
        
        if 'patterns' in st.session_state:
            patterns = st.session_state['patterns']
            
            # Статистика паттернов
            pattern_types = {}
            for pattern in patterns:
                pattern_type = pattern.pattern_type
                pattern_types[pattern_type] = pattern_types.get(pattern_type, 0) + 1
            
            st.subheader("Статистика паттернов")
            for pattern_type, count in pattern_types.items():
                st.metric(pattern_type.replace('_', ' ').title(), count)
            
            # Список паттернов
            st.subheader("Обнаруженные паттерны")
            for i, pattern in enumerate(patterns):
                with st.expander(f"Паттерн {i+1}: {pattern.pattern_type}"):
                    st.write(f"**Показатели:** {', '.join(pattern.indicators)}")
                    st.write(f"**Время:** {pattern.start_time} - {pattern.end_time}")
                    st.write(f"**Уверенность:** {pattern.confidence:.3f}")
                    if pattern.quantum_signature:
                        st.write(f"**Квантовая подпись:** {pattern.quantum_signature}")
    
    with tab5:
        st.subheader("📈 Визуализация результатов")
        
        if 'quantum_results' in st.session_state:
            results = st.session_state['quantum_results']
            
            # Дашборд анализа
            fig = visualizer.plot_quantum_analysis_dashboard(
                results, time_series
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # График паттернов
            if 'patterns' in st.session_state:
                patterns = st.session_state['patterns']
                fig = visualizer.plot_patterns(time_series, patterns)
                st.plotly_chart(fig, use_container_width=True)

else:
    # Приветственный экран
    st.markdown("""
    ## Добро пожаловать в MQEA! 🧬
    
    **Medical Quantum Entanglement Analysis** - это революционный алгоритм для анализа медицинских данных 
    на основе принципов квантовой запутанности.
    
    ### Возможности системы:
    - 🔬 **Квантовая запутанность** между медицинскими показателями
    - 🔧 **Заполнение пропущенных данных** на основе квантовых принципов  
    - 🔍 **Обнаружение паттернов** через квантовые состояния
    - 📊 **Интерактивная визуализация** результатов
    - 🌐 **REST API** для интеграции с другими системами
    
    ### Для начала работы:
    1. Выберите режим анализа в боковой панели
    2. Настройте параметры
    3. Запустите анализ
    4. Изучите результаты
    """)
    
    # Информация о системе
    with st.expander("ℹ️ Информация о системе"):
        st.markdown(f"""
        **Версия:** {settings.api.version}  
        **Окружение:** {settings.environment}  
        **Режим отладки:** {'Включен' if settings.debug else 'Отключен'}  
        **Поддерживаемые показатели:** {', '.join(settings.supported_indicators)}
        """)

# Футер
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p><strong>MQEA - Medical Quantum Entanglement Analysis</strong></p>
    <p>Основатель: <strong>Мухаммад Махизода</strong> | Таджикский национальный университет</p>
    <p>© 2025 Все права защищены</p>
</div>
""", unsafe_allow_html=True)

"""
Отдельное приложение для системы мониторинга в реальном времени MQEA.

Автор: Мухаммад Махизода
Таджикский национальный университет
"""

import streamlit as st
import sys
import os
from datetime import datetime

# Добавляем путь к модулям
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Настройки страницы
st.set_page_config(
    page_title="MQEA - Мониторинг в реальном времени",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Кастомные CSS стили
st.markdown("""
<style>
/* Скрытие стандартной навигации Streamlit */
.stSidebar [data-testid="stSidebarNav"] {display:none !important;}
.stSidebar .css-1d391kg {display:none !important;}
.stSidebar .css-1oe5cao {display:none !important;}

/* Стили для табов навигации */
.nav-tab {
    background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
    border: none;
    border-radius: 8px;
    color: white;
    padding: 8px 16px;
    margin: 2px;
    font-weight: bold;
    transition: all 0.3s ease;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.nav-tab:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

/* Индикатор активного приложения */
.app-indicator {
    background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
    color: white;
    padding: 12px;
    border-radius: 10px;
    text-align: center;
    font-weight: bold;
    margin: 10px 0;
    box-shadow: 0 4px 12px rgba(255, 107, 107, 0.3);
    border: 2px solid rgba(255,255,255,0.2);
}

/* Анимация пульсации для активного индикатора */
@keyframes pulse-monitoring {
    0% { box-shadow: 0 4px 12px rgba(255, 107, 107, 0.3); }
    50% { box-shadow: 0 4px 20px rgba(255, 107, 107, 0.6); }
    100% { box-shadow: 0 4px 12px rgba(255, 107, 107, 0.3); }
}

.app-indicator {
    animation: pulse-monitoring 2s infinite;
}

/* Стили для разделителей */
.section-divider {
    border-top: 2px solid #ff6b6b;
    margin: 20px 0;
    border-radius: 2px;
}

/* Стили для карточек мониторинга */
.monitoring-card {
    background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
    border-radius: 12px;
    padding: 20px;
    margin: 10px 0;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    border: 1px solid rgba(255,255,255,0.3);
}

/* Кастомные кнопки-таблетки */
.pill-button {
    background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
    color: white;
    border: none;
    border-radius: 25px;
    padding: 12px 24px;
    font-weight: bold;
    font-size: 14px;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 12px rgba(255, 107, 107, 0.3);
    text-decoration: none;
    display: inline-block;
    margin: 5px;
}

.pill-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(255, 107, 107, 0.4);
}

.pill-button.active {
    background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
    animation: pulse-monitoring 2s infinite;
}
</style>
<script>
// Скрытие стандартной навигации
setInterval(function() {
    // Скрываем только стандартную навигацию Streamlit, но не наши кастомные элементы
    const navElements = document.querySelectorAll('[data-testid="stSidebarNav"]');
    navElements.forEach(el => {
        if (el && !el.closest('.custom-navigation')) {
            el.style.display = 'none';
            el.style.visibility = 'hidden';
        }
    });
}, 100);
</script>
""", unsafe_allow_html=True)

# Импорты для системы мониторинга
try:
    from mqea.iot_sensors import create_sensor_manager
    from mqea.realtime_monitoring import create_monitoring_system
    from mqea.notification_system import create_notification_system
    from mqea.realtime_charts import create_chart_manager
except ImportError as e:
    st.error(f"Ошибка импорта модулей мониторинга: {e}")
    st.stop()

def initialize_session_state():
    """Инициализация состояния сессии."""
    if 'monitoring_initialized' not in st.session_state:
        st.session_state.monitoring_initialized = True
        
        # Инициализация компонентов мониторинга
        try:
            st.session_state.sensor_manager = create_sensor_manager()
            st.session_state.monitoring_system = create_monitoring_system()
            st.session_state.notification_system = create_notification_system()
            st.session_state.chart_manager = create_chart_manager()
        except Exception as e:
            st.error(f"Ошибка инициализации системы мониторинга: {e}")
            st.stop()

def show_header():
    """Заголовок приложения."""
    # Заголовок с градиентом
    st.markdown("""
    <div style='background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); 
                color: white; padding: 30px; border-radius: 15px; text-align: center; 
                margin-bottom: 30px; box-shadow: 0 8px 32px rgba(255, 107, 107, 0.3);'>
        <h1 style='margin: 0; font-size: 2.5em; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>
            📡 MQEA Мониторинг
        </h1>
        <h2 style='margin: 10px 0; font-size: 1.2em; opacity: 0.9;'>
            Real-time Medical Monitoring System
        </h2>
        <p style='margin: 0; font-size: 1.1em; opacity: 0.8;'>
            Система непрерывного мониторинга медицинских показателей с IoT датчиками
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Информация о системе
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📡 Датчики", "8 активных", "2 новых")
    
    with col2:
        st.metric("⚡ Пациенты", "12 под наблюдением", "3 критических")
    
    with col3:
        st.metric("🚨 Тревоги", "5 активных", "2 новых")

def show_iot_sensors():
    """Раздел IoT датчиков."""
    st.header("📡 IoT Датчики")
    
    sensor_manager = st.session_state.sensor_manager
    
    # Управление датчиками
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🚀 Запустить все датчики", type="primary"):
            try:
                sensor_manager._running = True
                for sensor in sensor_manager.sensors.values():
                    sensor.status = sensor.status.__class__("active")
                st.success("🚀 Все датчики запущены")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Ошибка запуска: {e}")
    
    with col2:
        if st.button("⏹️ Остановить все датчики"):
            try:
                sensor_manager._running = False
                for sensor in sensor_manager.sensors.values():
                    sensor.status = sensor.status.__class__("inactive")
                st.success("⏹️ Все датчики остановлены")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Ошибка остановки: {e}")
    
    with col3:
        if st.button("🔄 Обновить данные"):
            # Генерируем новые данные для всех активных датчиков
            for sensor_id, sensor in sensor_manager.sensors.items():
                if sensor.status.value == "active":
                    sensor.current_value = sensor._generate_value()
            st.rerun()
    
    # Статус датчиков
    st.subheader("📊 Статус датчиков")
    
    # Индикатор времени обновления
    current_time = datetime.now()
    st.markdown(f"""
    <div style='text-align: center; color: #ff6b6b; font-size: 0.9em; margin: 5px 0;'>
        🕐 Последнее обновление данных: {current_time.strftime("%H:%M:%S")}
    </div>
    """, unsafe_allow_html=True)
    
    # Генерируем новые данные для активных датчиков
    sensors_data = []
    
    for sensor_id, sensor in sensor_manager.sensors.items():
        # Если датчик активен, генерируем новое значение
        if sensor.status.value == "active" and sensor_manager._running:
            sensor.current_value = sensor._generate_value()
        
        # Определяем цвет статуса
        status_color = "🟢" if sensor.status.value == "active" else "🔴"
        
        sensors_data.append({
            "ID": sensor_id,
            "Тип": sensor.config.name,
            "Статус": f"{status_color} {str(sensor.status)}",
            "Последнее обновление": current_time.strftime("%H:%M:%S"),
            "Значение": f"{sensor.current_value:.2f}",
            "Единица": sensor.config.unit,
            "Тренд": f"{sensor.trend:+.2f}"
        })
    
    if sensors_data:
        import pandas as pd
        df = pd.DataFrame(sensors_data)
        
        # Выделяем активные датчики
        st.dataframe(df, width='stretch')
        
        # Показываем статистику
        active_sensors = len([s for s in sensor_manager.sensors.values() if s.status.value == "active"])
        total_sensors = len(sensor_manager.sensors)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📡 Всего датчиков", total_sensors)
        with col2:
            st.metric("🟢 Активных", active_sensors)
        with col3:
            st.metric("🔴 Неактивных", total_sensors - active_sensors)
    
    # График показаний датчиков
    st.subheader("📈 График показаний в реальном времени")
    
    if sensor_manager._running:
        # Инициализируем историю данных если её нет
        if 'sensor_history' not in st.session_state:
            st.session_state.sensor_history = []
        
        # Генерируем новые данные
        current_time = datetime.now()
        new_readings = []
        
        for sensor_id, sensor in sensor_manager.sensors.items():
            if sensor.status.value == "active":
                new_readings.append({
                    "Время": current_time,
                    "Датчик": sensor_id,
                    "Значение": sensor.current_value,
                    "Тип": sensor.config.name,
                    "Единица": sensor.config.unit
                })
        
        # Добавляем новые данные к истории (храним последние 50 точек)
        if new_readings:
            st.session_state.sensor_history.extend(new_readings)
            # Ограничиваем историю последними 50 точками
            if len(st.session_state.sensor_history) > 50:
                st.session_state.sensor_history = st.session_state.sensor_history[-50:]
        
        # Создаем график
        if st.session_state.sensor_history:
            import plotly.express as px
            import plotly.graph_objects as go
            from plotly.subplots import make_subplots
            
            df_history = pd.DataFrame(st.session_state.sensor_history)
            
            # Создаем subplot для каждого типа датчика
            sensor_types = df_history['Тип'].unique()
            
            if len(sensor_types) <= 4:
                # Для небольшого количества датчиков используем subplots
                fig = make_subplots(
                    rows=len(sensor_types), cols=1,
                    subplot_titles=[f"📊 {sensor_type}" for sensor_type in sensor_types],
                    vertical_spacing=0.1
                )
                
                for i, sensor_type in enumerate(sensor_types, 1):
                    sensor_data = df_history[df_history['Тип'] == sensor_type]
                    fig.add_trace(
                        go.Scatter(
                            x=sensor_data['Время'],
                            y=sensor_data['Значение'],
                            mode='lines+markers',
                            name=sensor_type,
                            line=dict(width=2),
                            marker=dict(size=4)
                        ),
                        row=i, col=1
                    )
                
                fig.update_layout(
                    height=200 * len(sensor_types),
                    showlegend=False,
                    title="Показания датчиков в реальном времени"
                )
            else:
                # Для большого количества датчиков используем один график
                fig = px.line(
                    df_history, 
                    x="Время", 
                    y="Значение", 
                    color="Тип",
                    title="Показания датчиков в реальном времени",
                    line_shape='spline'
                )
            
            fig.update_layout(
                xaxis_title="Время",
                yaxis_title="Значение",
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Показываем последние значения
            st.subheader("📋 Последние показания")
            latest_readings = df_history.groupby('Тип').last().reset_index()
            latest_readings = latest_readings[['Тип', 'Значение', 'Единица', 'Время']]
            latest_readings['Время'] = latest_readings['Время'].dt.strftime('%H:%M:%S')
            st.dataframe(latest_readings, width='stretch')
    else:
        st.info("🚀 Запустите датчики для отображения данных в реальном времени")

def show_patient_monitoring():
    """Раздел мониторинга пациентов."""
    st.header("⚡ Мониторинг пациентов")
    
    monitoring_system = st.session_state.monitoring_system
    
    # Управление сессиями мониторинга
    col1, col2 = st.columns(2)
    
    with col1:
        patient_id = st.text_input("ID пациента", placeholder="Введите ID пациента")
        patient_name = st.text_input("Имя пациента", placeholder="Введите имя пациента")
        if st.button("➕ Начать мониторинг"):
            if patient_id and patient_name:
                try:
                    session_id = monitoring_system.start_monitoring_session(patient_id, patient_name)
                    st.success(f"✅ Мониторинг начат для пациента {patient_name} (ID: {session_id})")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Ошибка: {e}")
            else:
                st.error("Введите ID и имя пациента")
    
    with col2:
        if st.button("⏹️ Остановить все сессии"):
            try:
                active_sessions = monitoring_system.get_active_sessions()
                for session in active_sessions:
                    monitoring_system.stop_monitoring_session(session.session_id)
                st.success(f"⏹️ Остановлено {len(active_sessions)} сессий мониторинга")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Ошибка: {e}")
    
    # Активные сессии
    st.subheader("📋 Активные сессии мониторинга")
    
    sessions = monitoring_system.get_active_sessions()
    if sessions:
        sessions_data = []
        for session in sessions:
            sessions_data.append({
                "ID сессии": session.session_id,
                "ID пациента": session.patient_id,
                "Имя": session.patient_name,
                "Начало": session.start_time.strftime("%H:%M:%S"),
                "Длительность": str(datetime.now() - session.start_time).split('.')[0],
                "Статус": "Активна" if session.is_active else "Остановлена",
                "Тревог": len([a for a in session.alerts if not a.is_resolved])
            })
        
        import pandas as pd
        df = pd.DataFrame(sessions_data)
        st.dataframe(df, width='stretch')
    else:
        st.info("Нет активных сессий мониторинга")

def show_alerts_system():
    """Раздел системы тревог."""
    st.header("🚨 Система тревог")
    
    monitoring_system = st.session_state.monitoring_system
    
    # Настройки тревог
    st.subheader("⚙️ Настройки тревог")
    
    col1, col2 = st.columns(2)
    
    with col1:
        critical_threshold = st.slider("Порог критических тревог", 0.0, 1.0, 0.8)
        warning_threshold = st.slider("Порог предупреждений", 0.0, 1.0, 0.6)
    
    with col2:
        auto_resolve = st.checkbox("Автоматическое разрешение", value=True)
        email_notifications = st.checkbox("Email уведомления", value=True)
    
    # Активные тревоги
    st.subheader("🔴 Активные тревоги")
    
    # Получаем тревоги из всех активных сессий
    all_alerts = []
    active_sessions = monitoring_system.get_active_sessions()
    for session in active_sessions:
        all_alerts.extend([alert for alert in session.alerts if not alert.is_resolved])
    
    if all_alerts:
        alerts_data = []
        for alert in all_alerts:
            alerts_data.append({
                "Время": alert.timestamp.strftime("%H:%M:%S"),
                "Пациент": alert.patient_id,
                "Датчик": alert.sensor_id,
                "Уровень": alert.alert_level.value,
                "Описание": alert.message,
                "Значение": f"{alert.value:.2f}",
                "Статус": "Активна" if not alert.is_resolved else "Разрешена"
            })
        
        import pandas as pd
        df = pd.DataFrame(alerts_data)
        st.dataframe(df, width='stretch')
        
        # Кнопки управления тревогами
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("✅ Разрешить все"):
                for alert in all_alerts:
                    alert.is_resolved = True
                st.success("✅ Все тревоги разрешены")
                st.rerun()
        
        with col2:
            if st.button("🔔 Отправить уведомления"):
                st.info("📧 Уведомления отправлены")
        
        with col3:
            if st.button("📊 Статистика тревог"):
                st.info("📈 Статистика тревог обновлена")
    else:
        st.success("✅ Нет активных тревог")

def show_realtime_charts():
    """Раздел графиков в реальном времени."""
    st.header("📊 Графики в реальном времени")
    
    chart_manager = st.session_state.chart_manager
    
    # Настройки графиков
    st.subheader("⚙️ Настройки графиков")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        chart_type = st.selectbox("Тип графика", ["Линейный", "Столбчатый", "Точечный"])
        time_range = st.selectbox("Временной диапазон", ["1 час", "6 часов", "24 часа", "7 дней"])
    
    with col2:
        update_interval = st.slider("Интервал обновления (сек)", 1, 60, 5)
        auto_refresh = st.checkbox("Автообновление", value=True)
    
    with col3:
        if st.button("🔄 Обновить графики"):
            st.rerun()
    
    # Графики
    st.subheader("📈 Графики показателей")
    
    # Генерируем тестовые данные
    import pandas as pd
    import numpy as np
    from datetime import datetime, timedelta
    
    now = datetime.now()
    time_points = [now - timedelta(minutes=i) for i in range(60, 0, -1)]
    
    data = {
        "Время": time_points,
        "Пульс": np.random.normal(75, 10, 60),
        "Давление": np.random.normal(120, 15, 60),
        "Температура": np.random.normal(36.6, 0.5, 60),
        "Кислород": np.random.normal(98, 2, 60)
    }
    
    df = pd.DataFrame(data)
    
    # Создаем график
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("Пульс (уд/мин)", "Давление (мм рт.ст.)", 
                       "Температура (°C)", "Насыщение кислородом (%)"),
        vertical_spacing=0.1
    )
    
    fig.add_trace(go.Scatter(x=df["Время"], y=df["Пульс"], name="Пульс"), row=1, col=1)
    fig.add_trace(go.Scatter(x=df["Время"], y=df["Давление"], name="Давление"), row=1, col=2)
    fig.add_trace(go.Scatter(x=df["Время"], y=df["Температура"], name="Температура"), row=2, col=1)
    fig.add_trace(go.Scatter(x=df["Время"], y=df["Кислород"], name="Кислород"), row=2, col=2)
    
    fig.update_layout(height=600, title_text="Медицинские показатели в реальном времени")
    fig.update_xaxes(title_text="Время")
    
    st.plotly_chart(fig, use_container_width=True)

def show_notifications_system():
    """Раздел системы уведомлений."""
    st.header("📧 Система уведомлений")
    
    notification_system = st.session_state.notification_system
    
    # Настройки уведомлений
    st.subheader("⚙️ Настройки уведомлений")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Каналы уведомлений:**")
        email_enabled = st.checkbox("Email", value=True)
        sms_enabled = st.checkbox("SMS", value=False)
        push_enabled = st.checkbox("Push", value=True)
        webhook_enabled = st.checkbox("Webhook", value=False)
    
    with col2:
        st.write("**Настройки:**")
        critical_only = st.checkbox("Только критические", value=False)
        quiet_hours = st.checkbox("Тихие часы (22:00-08:00)", value=True)
        batch_notifications = st.checkbox("Пакетные уведомления", value=True)
    
    # История уведомлений
    st.subheader("📋 История уведомлений")
    
    # Получаем историю уведомлений
    history = notification_system.get_notification_history()
    
    if history:
        import pandas as pd
        df = pd.DataFrame(history)
        
        # Исправляем типы данных для совместимости с Streamlit
        if 'timestamp' in df.columns:
            df['timestamp'] = df['timestamp'].astype(str)
        if 'subject' in df.columns:
            df['subject'] = df['subject'].astype(str)
        if 'body' in df.columns:
            df['body'] = df['body'].astype(str)
        if 'recipient' in df.columns:
            df['recipient'] = df['recipient'].astype(str)
        if 'status' in df.columns:
            df['status'] = df['status'].astype(str)
        
        st.dataframe(df, width='stretch')
    else:
        st.info("История уведомлений пуста")
    
    # Тестирование уведомлений
    st.subheader("🧪 Тестирование уведомлений")
    
    col1, col2 = st.columns(2)
    
    with col1:
        test_email = st.text_input("Тестовый email", placeholder="test@example.com")
        if st.button("📧 Отправить тестовое email"):
            if test_email:
                st.success(f"📧 Тестовое email отправлено на {test_email}")
            else:
                st.error("Введите email адрес")
    
    with col2:
        if st.button("🔔 Отправить тестовое уведомление"):
            st.success("🔔 Тестовое уведомление отправлено")

def show_sidebar():
    """Боковая панель навигации."""
    st.sidebar.title("🏥 Мониторинг")
    
    # Навигационные табы между приложениями
    st.sidebar.markdown("### 🎛️ Навигация")
    
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        if st.button("🏥 MQEA", use_container_width=True):
            st.switch_page("modern_medical_app.py")
    
    with col2:
        if st.button("📡 Мониторинг", type="primary", use_container_width=True):
            st.rerun()  # Остаемся на текущей странице
    
    # Индикатор активного приложения
    st.sidebar.markdown("""
    <div class="app-indicator">
        📡 МОНИТОРИНГ АКТИВНО
        <br><small>IoT датчики и уведомления</small>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    
    # Навигация по разделам мониторинга
    st.sidebar.markdown("### 📋 Разделы")
    page = st.sidebar.radio(
        "Выберите раздел:",
        [
            "📊 Дашборд",
            "📡 IoT Датчики", 
            "⚡ Мониторинг пациентов",
            "🚨 Система тревог",
            "📊 Графики в реальном времени",
            "📧 Уведомления"
        ]
    )
    
    st.sidebar.markdown("---")
    
    # Быстрые действия
    st.sidebar.subheader("⚡ Быстрые действия")
    
    if st.sidebar.button("🚀 Запустить все системы"):
        st.session_state.sensor_manager._running = True
        st.success("🚀 Все системы запущены")
        st.rerun()
    
    if st.sidebar.button("⏹️ Остановить все системы"):
        st.session_state.sensor_manager._running = False
        st.success("⏹️ Все системы остановлены")
        st.rerun()
    
    if st.sidebar.button("🔄 Обновить данные"):
        st.rerun()
    
    st.sidebar.markdown("---")
    
    # Информация о системе
    st.sidebar.subheader("ℹ️ Информация")
    st.sidebar.info("""
    **MQEA Мониторинг v1.0**
    
    Система непрерывного мониторинга медицинских показателей с использованием IoT датчиков и квантовых алгоритмов.
    """)
    
    
    return page

def show_dashboard():
    """Главный дашборд мониторинга."""
    st.header("📊 Дашборд мониторинга")
    
    sensor_manager = st.session_state.sensor_manager
    monitoring_system = st.session_state.monitoring_system
    
    # Подсчитываем реальную статистику
    total_sensors = len(sensor_manager.sensors)
    active_sensors = len([s for s in sensor_manager.sensors.values() if s.status.value == "active"])
    
    active_sessions = monitoring_system.get_active_sessions()
    total_patients = len(active_sessions)
    critical_patients = len([s for s in active_sessions if len([a for a in s.alerts if not a.is_resolved]) > 0])
    
    all_alerts = []
    for session in active_sessions:
        all_alerts.extend([alert for alert in session.alerts if not alert.is_resolved])
    
    total_alerts = len(all_alerts)
    new_alerts = len([a for a in all_alerts if (datetime.now() - a.timestamp).seconds < 300])  # Новые за последние 5 минут
    
    # Общая статистика
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "📡 Датчики", 
            f"{total_sensors}", 
            f"{active_sensors} активных",
            delta_color="normal"
        )
    
    with col2:
        st.metric(
            "⚡ Пациенты", 
            f"{total_patients}", 
            f"{critical_patients} критических",
            delta_color="inverse" if critical_patients > 0 else "normal"
        )
    
    with col3:
        st.metric(
            "🚨 Тревоги", 
            f"{total_alerts}", 
            f"{new_alerts} новых",
            delta_color="inverse" if new_alerts > 0 else "normal"
        )
    
    with col4:
        st.metric(
            "📧 Уведомления", 
            "23", 
            "5 сегодня",
            delta_color="normal"
        )
    
    # График активности
    st.subheader("📈 Активность системы")
    
    import pandas as pd
    import numpy as np
    from datetime import datetime, timedelta
    
    # Генерируем данные активности
    now = datetime.now()
    hours = [now - timedelta(hours=i) for i in range(24, 0, -1)]
    activity_data = {
        "Время": hours,
        "Датчики": np.random.poisson(5, 24),
        "Тревоги": np.random.poisson(2, 24),
        "Уведомления": np.random.poisson(3, 24)
    }
    
    df_activity = pd.DataFrame(activity_data)
    
    import plotly.express as px
    fig = px.line(df_activity, x="Время", y=["Датчики", "Тревоги", "Уведомления"], 
                  title="Активность системы за последние 24 часа")
    st.plotly_chart(fig, use_container_width=True)
    
    # Последние события
    st.subheader("📋 Последние события")
    
    events = [
        {"Время": "14:30", "Событие": "Новая тревога: Критический пульс", "Статус": "🔴"},
        {"Время": "14:25", "Событие": "Датчик температуры восстановлен", "Статус": "🟢"},
        {"Время": "14:20", "Событие": "Email уведомление отправлено", "Статус": "📧"},
        {"Время": "14:15", "Событие": "Новый пациент добавлен в мониторинг", "Статус": "➕"},
        {"Время": "14:10", "Событие": "Система обновлена", "Статус": "🔄"}
    ]
    
    df_events = pd.DataFrame(events)
    st.dataframe(df_events, width='stretch')

def main():
    """Главная функция приложения."""
    # Инициализация
    initialize_session_state()
    
    # Боковая панель
    page = show_sidebar()
    
    # Заголовок
    show_header()
    
    # Маршрутизация
    if page == "📊 Дашборд":
        show_dashboard()
    elif page == "📡 IoT Датчики":
        show_iot_sensors()
    elif page == "⚡ Мониторинг пациентов":
        show_patient_monitoring()
    elif page == "🚨 Система тревог":
        show_alerts_system()
    elif page == "📊 Графики в реальном времени":
        show_realtime_charts()
    elif page == "📧 Уведомления":
        show_notifications_system()

if __name__ == "__main__":
    main()

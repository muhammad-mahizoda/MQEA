"""
Демонстрация системы мониторинга в реальном времени MQEA.

Автор: Мухаммад Махизода
Таджикский национальный университет
"""

import asyncio
import time
from datetime import datetime
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

from mqea.realtime_monitoring import create_monitoring_system
from mqea.notification_system import create_notification_system
from mqea.realtime_charts import create_chart_manager


def print_banner():
    """Выводит баннер демонстрации."""
    banner = """
    ╔══════════════════════════════════════════════════════════════════════════════╗
    ║                                                                              ║
    ║    🏥 MQEA - Система мониторинга в реальном времени                         ║
    ║                                                                              ║
    ║    🚀 Новые возможности:                                                     ║
    ║    • IoT датчики для непрерывного мониторинга                                ║
    ║    • Уведомления о критических состояниях                                    ║
    ║    • Графики в реальном времени                                              ║
    ║    • Система тревог и алертов                                               ║
    ║                                                                              ║
    ║    Автор: Мухаммад Махизода                                                 ║
    ║    Таджикский национальный университет                                      ║
    ║                                                                              ║
    ╚══════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)


async def run_console_demo():
    """Запускает консольную демонстрацию."""
    print_banner()
    
    print("🚀 Запуск демонстрации системы мониторинга в реальном времени...")
    print("=" * 70)
    
    # Создаем системы
    monitoring = create_monitoring_system()
    notifications = create_notification_system()
    charts = create_chart_manager()
    
    # Настраиваем уведомления
    notifications.add_recipient(
        "doctor1",
        email="doctor1@hospital.com",
        phone="+992123456789"
    )
    notifications.add_recipient(
        "nurse1", 
        email="nurse1@hospital.com",
        phone="+992123456790"
    )
    
    # Подключаем уведомления к мониторингу
    def on_alert(alert):
        asyncio.create_task(notifications.process_alert(alert, f"Пациент {alert.patient_id}"))
    
    monitoring.add_alert_callback(on_alert)
    
    # Подключаем графики к мониторингу
    def on_reading(reading, source):
        charts.add_sensor_reading(reading)
    
    monitoring.add_reading_callback(on_reading)
    
    # Запускаем все системы
    await monitoring.start()
    charts.start_monitoring()
    
    print("✅ Все системы запущены")
    
    # Создаем тестовых пациентов
    patients = [
        ("P001", "Али Хасанов", 45, "мужской"),
        ("P002", "Фатима Алимова", 32, "женский"),
        ("P003", "Ахмад Рахимов", 67, "мужской"),
        ("P004", "Зухра Каримова", 28, "женский")
    ]
    
    session_ids = []
    for patient_id, patient_name, age, gender in patients:
        session_id = monitoring.start_monitoring_session(
            patient_id=patient_id,
            patient_name=patient_name
        )
        session_ids.append(session_id)
        print(f"👤 Пациент {patient_name} подключен к мониторингу")
    
    print(f"\n📊 Мониторинг запущен для {len(patients)} пациентов")
    print("⏱️ Демонстрация будет работать 60 секунд...")
    print("💡 Наблюдайте за данными в реальном времени и уведомлениями\n")
    
    # Основной цикл демонстрации
    for i in range(12):  # 12 итераций по 5 секунд = 60 секунд
        await asyncio.sleep(5)
        
        current_time = datetime.now().strftime("%H:%M:%S")
        print(f"\n📈 Статистика [{current_time}] - {(i+1)*5}с:")
        
        # Показываем данные дашборда
        dashboard = monitoring.get_monitoring_dashboard_data()
        print(f"   🏥 Активных сессий: {dashboard['total_active_sessions']}")
        print(f"   🚨 Тревог за час: {dashboard['total_alerts_last_hour']}")
        
        # Статистика по пациентам
        for session_data in dashboard['active_sessions']:
            patient_name = session_data['patient_name']
            alerts_count = session_data['active_alerts_count']
            duration = session_data['duration_minutes']
            
            alert_emoji = "🚨" if alerts_count > 0 else "✅"
            print(f"   {alert_emoji} {patient_name}: {alerts_count} тревог, {duration:.1f} мин")
            
            # Показываем последние показания
            for sensor_id, reading_data in session_data['latest_readings'].items():
                value = reading_data['value']
                unit = reading_data['unit']
                alert_level = reading_data['alert_level']
                
                level_emoji = {
                    'normal': '✅',
                    'warning': '⚠️',
                    'critical': '🔴',
                    'emergency': '🚨'
                }
                
                emoji = level_emoji.get(alert_level, '❓')
                print(f"      {emoji} {sensor_id}: {value:.1f} {unit}")
        
        # Статистика графиков
        chart_stats = charts.get_charts_statistics()
        total_points = sum(
            sum(sensor_stat['data_points_count'] for sensor_stat in chart_stat.values())
            for chart_stat in chart_stats.values()
        )
        print(f"   📊 Всего точек данных: {total_points}")
        
        # Статистика уведомлений
        notification_stats = notifications.get_statistics()
        print(f"   📧 Уведомлений отправлено: {notification_stats['sent_notifications']}")
    
    print(f"\n⏹️ Завершение демонстрации...")
    
    # Останавливаем сессии
    for session_id in session_ids:
        summary = monitoring.stop_monitoring_session(session_id)
        if summary:
            print(f"   📊 {summary['patient_name']}: {summary['total_readings']} показаний, "
                  f"{summary['total_alerts']} тревог")
    
    # Останавливаем системы
    await monitoring.stop()
    charts.stop_monitoring()
    
    # Итоговая статистика
    print(f"\n📊 ИТОГОВАЯ СТАТИСТИКА:")
    print(f"   🏥 Всего сессий: {len(monitoring.active_sessions)}")
    print(f"   📊 Всего точек данных: {sum(len(s.readings_history) for s in monitoring.active_sessions.values())}")
    
    notification_stats = notifications.get_statistics()
    print(f"   📧 Уведомлений: {notification_stats['total_notifications']} "
          f"(успешно: {notification_stats['sent_notifications']}, "
          f"ошибок: {notification_stats['failed_notifications']})")
    
    print(f"   ✅ Успешность уведомлений: {notification_stats['success_rate']:.1f}%")
    
    print("\n🎉 Демонстрация завершена успешно!")
    print("💡 Система готова к использованию в реальных условиях")


def create_streamlit_app():
    """Создает Streamlit приложение."""
    st.set_page_config(
        page_title="MQEA - Мониторинг в реальном времени",
        page_icon="🏥",
        layout="wide"
    )
    
    st.title("🏥 MQEA - Система мониторинга в реальном времени")
    st.markdown("**Автор:** Мухаммад Махизода | **Университет:** Таджикский национальный университет")
    
    # Создаем системы (в реальном приложении они должны быть в session_state)
    if 'monitoring_system' not in st.session_state:
        st.session_state.monitoring_system = create_monitoring_system()
        st.session_state.notification_system = create_notification_system()
        st.session_state.chart_manager = create_chart_manager()
    
    monitoring = st.session_state.monitoring_system
    notifications = st.session_state.notification_system
    charts = st.session_state.chart_manager
    
    # Боковая панель для управления
    with st.sidebar:
        st.header("🎛️ Управление")
        
        # Статус системы
        st.subheader("📊 Статус системы")
        dashboard = monitoring.get_monitoring_dashboard_data()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Активные сессии", dashboard['total_active_sessions'])
        with col2:
            st.metric("Тревог за час", dashboard['total_alerts_last_hour'])
        
        # Управление пациентами
        st.subheader("👥 Пациенты")
        
        if st.button("🆕 Добавить тестового пациента"):
            patient_id = f"P{len(dashboard['active_sessions']) + 1:03d}"
            patient_name = f"Пациент {patient_id}"
            
            session_id = monitoring.start_monitoring_session(
                patient_id=patient_id,
                patient_name=patient_name
            )
            st.success(f"Пациент {patient_name} добавлен")
            st.rerun()
        
        # Настройки уведомлений
        st.subheader("🔔 Уведомления")
        
        notification_stats = notifications.get_statistics()
        st.metric("Отправлено", notification_stats['sent_notifications'])
        st.metric("Успешность", f"{notification_stats['success_rate']:.1f}%")
    
    # Основной контент
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Дашборд", "📈 Графики", "🚨 Тревоги", "📧 Уведомления"])
    
    with tab1:
        st.header("📊 Дашборд мониторинга")
        
        # Общая статистика
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Активные сессии", dashboard['total_active_sessions'])
        with col2:
            st.metric("Всего датчиков", dashboard['sensor_status']['total_sensors'])
        with col3:
            st.metric("Активных датчиков", dashboard['sensor_status']['active_sensors'])
        with col4:
            st.metric("Тревог за час", dashboard['total_alerts_last_hour'])
        
        # Список активных сессий
        if dashboard['active_sessions']:
            st.subheader("👥 Активные сессии мониторинга")
            
            for session in dashboard['active_sessions']:
                with st.expander(f"👤 {session['patient_name']} (ID: {session['patient_id']})"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Длительность", f"{session['duration_minutes']:.1f} мин")
                    with col2:
                        st.metric("Активных тревог", session['active_alerts_count'])
                    with col3:
                        if session['active_alerts_count'] > 0:
                            st.error(f"🚨 {session['active_alerts_count']} тревог")
                        else:
                            st.success("✅ Нет тревог")
                    
                    # Последние показания
                    st.subheader("📊 Последние показания")
                    readings_data = []
                    
                    for sensor_id, reading in session['latest_readings'].items():
                        alert_level = reading['alert_level']
                        color = {
                            'normal': 'green',
                            'warning': 'orange', 
                            'critical': 'red',
                            'emergency': 'darkred'
                        }.get(alert_level, 'gray')
                        
                        readings_data.append({
                            'Датчик': sensor_id,
                            'Значение': f"{reading['value']:.1f} {reading['unit']}",
                            'Уровень тревоги': alert_level,
                            'Время': reading['timestamp']
                        })
                    
                    if readings_data:
                        df = pd.DataFrame(readings_data)
                        st.dataframe(df, use_container_width=True)
        else:
            st.info("Нет активных сессий мониторинга. Добавьте пациента в боковой панели.")
    
    with tab2:
        st.header("📈 Графики в реальном времени")
        
        # Выбор графика
        chart_ids = list(charts.charts.keys())
        if chart_ids:
            selected_chart = st.selectbox(
                "Выберите график:",
                chart_ids,
                format_func=lambda x: charts.chart_configs[x].name
            )
            
            # Настройки
            col1, col2 = st.columns(2)
            with col1:
                time_window = st.slider("Временное окно (минуты)", 5, 120, 30)
            with col2:
                auto_refresh = st.checkbox("Автообновление", value=True)
            
            # Создание графика
            if st.button("🔄 Обновить график") or auto_refresh:
                fig = charts.create_plotly_chart(selected_chart, time_window)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.error("Не удалось создать график")
            
            # Статистика графика
            chart_stats = charts.get_charts_statistics()
            if selected_chart in chart_stats:
                st.subheader("📊 Статистика")
                
                for sensor_id, sensor_stat in chart_stats[selected_chart].items():
                    with st.expander(f"📈 {sensor_id}"):
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric("Текущее", f"{sensor_stat['current_value']:.1f}")
                        with col2:
                            st.metric("Среднее", f"{sensor_stat['avg_value']:.1f}")
                        with col3:
                            st.metric("Тренд", sensor_stat['trend'])
                        with col4:
                            st.metric("Точек", sensor_stat['data_points_count'])
        else:
            st.info("Графики не созданы")
    
    with tab3:
        st.header("🚨 Тревоги и алерты")
        
        # Последние тревоги
        recent_alerts = dashboard['recent_alerts']
        
        if recent_alerts:
            st.subheader("🔥 Последние тревоги")
            
            for alert in recent_alerts:
                alert_level = alert['alert_level']
                color = {
                    'warning': 'orange',
                    'critical': 'red',
                    'emergency': 'darkred'
                }.get(alert_level, 'gray')
                
                with st.expander(f"🚨 {alert['message']} - {alert['patient_id']}"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Уровень", alert_level)
                    with col2:
                        st.metric("Значение", f"{alert['value']:.1f}")
                    with col3:
                        st.metric("Время", alert['timestamp'])
        else:
            st.success("✅ Нет активных тревог")
    
    with tab4:
        st.header("📧 Система уведомлений")
        
        # Статистика уведомлений
        notification_stats = notifications.get_statistics()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Всего", notification_stats['total_notifications'])
        with col2:
            st.metric("Отправлено", notification_stats['sent_notifications'])
        with col3:
            st.metric("Ошибок", notification_stats['failed_notifications'])
        with col4:
            st.metric("Успешность", f"{notification_stats['success_rate']:.1f}%")
        
        # История уведомлений
        st.subheader("📋 История уведомлений")
        history = notifications.get_notification_history(20)
        
        if history:
            df = pd.DataFrame(history)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("История уведомлений пуста")
    
    # Автообновление
    if auto_refresh:
        time.sleep(2)
        st.rerun()


def main():
    """Главная функция."""
    print_banner()
    
    print("\n🎯 Выберите режим демонстрации:")
    print("1. 🖥️ Консольная демонстрация")
    print("2. 🌐 Веб-интерфейс (Streamlit)")
    print("3. ❌ Выход")
    
    choice = input("\nВведите номер (1-3): ").strip()
    
    if choice == '1':
        print("\n🚀 Запуск консольной демонстрации...")
        asyncio.run(run_console_demo())
    elif choice == '2':
        print("\n🌐 Запуск веб-интерфейса...")
        print("💡 Откройте браузер по адресу: http://localhost:8501")
        print("⚠️ Для остановки нажмите Ctrl+C")
        
        try:
            import subprocess
            import sys
            subprocess.run([sys.executable, "-m", "streamlit", "run", __file__, "--server.port", "8501"])
        except KeyboardInterrupt:
            print("\n👋 Веб-интерфейс остановлен")
        except Exception as e:
            print(f"❌ Ошибка запуска: {e}")
            print("💡 Попробуйте запустить вручную:")
            print("   streamlit run demo_realtime_monitoring.py")
    elif choice == '3':
        print("\n👋 До свидания!")
    else:
        print("\n❌ Неверный выбор")


if __name__ == "__main__":
    # Проверяем, запущено ли через Streamlit
    try:
        import streamlit as st
        create_streamlit_app()
    except ImportError:
        # Если Streamlit не импортируется, значит запущено как обычный скрипт
        main()


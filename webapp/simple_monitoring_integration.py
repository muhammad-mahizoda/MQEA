"""
Упрощенная интеграция системы мониторинга в реальном времени для Streamlit.

Автор: Мухаммад Махизода
Таджикский национальный университет
"""

import streamlit as st
import time
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any
import pandas as pd


class SimpleSensorData:
    """Упрощенные данные датчика для Streamlit."""
    
    def __init__(self, sensor_id: str, name: str, unit: str, 
                 min_val: float, max_val: float, normal_min: float, normal_max: float):
        self.sensor_id = sensor_id
        self.name = name
        self.unit = unit
        self.min_val = min_val
        self.max_val = max_val
        self.normal_min = normal_min
        self.normal_max = normal_max
        self.current_value = (normal_min + normal_max) / 2
        self.is_active = True
        self.last_update = datetime.now()
    
    def update_value(self):
        """Обновляет значение датчика."""
        if not self.is_active:
            return
        
        # Генерируем новое значение с небольшим изменением
        change = random.uniform(-0.05, 0.05)
        self.current_value += self.current_value * change
        
        # Ограничиваем диапазон
        self.current_value = max(self.min_val, min(self.max_val, self.current_value))
        
        # Иногда добавляем аномалии
        if random.random() < 0.02:  # 2% вероятность аномалии
            anomaly = random.uniform(-0.2, 0.2)
            self.current_value = self.current_value * (1 + anomaly)
        
        self.last_update = datetime.now()
    
    def get_alert_level(self) -> str:
        """Определяет уровень тревоги."""
        if self.current_value <= self.min_val * 1.1 or self.current_value >= self.max_val * 0.9:
            return "emergency"
        elif self.current_value < self.normal_min or self.current_value > self.normal_max:
            return "critical"
        elif self.current_value < self.normal_min * 1.1 or self.current_value > self.normal_max * 1.1:
            return "warning"
        else:
            return "normal"


class SimpleMonitoringSystem:
    """Упрощенная система мониторинга для Streamlit."""
    
    def __init__(self):
        self.sensors: Dict[str, SimpleSensorData] = {}
        self.patients: Dict[str, Dict] = {}
        self.alerts: List[Dict] = []
        self.is_running = False
        
        # Создаем датчики по умолчанию
        self._create_default_sensors()
    
    def _create_default_sensors(self):
        """Создает датчики по умолчанию."""
        sensors_config = [
            ("heart_rate", "Частота сердечных сокращений", "уд/мин", 30, 200, 60, 100),
            ("blood_pressure_systolic", "Систолическое давление", "мм рт.ст.", 70, 250, 90, 140),
            ("blood_pressure_diastolic", "Диастолическое давление", "мм рт.ст.", 40, 150, 60, 90),
            ("temperature", "Температура тела", "°C", 35.0, 42.0, 36.0, 37.5),
            ("oxygen_saturation", "Насыщение кислородом", "%", 70, 100, 95, 100),
            ("respiratory_rate", "Частота дыхания", "дых/мин", 5, 40, 12, 20),
            ("glucose", "Уровень глюкозы", "мг/дл", 50, 400, 70, 140),
            ("cholesterol", "Уровень холестерина", "мг/дл", 100, 400, 150, 200)
        ]
        
        for sensor_id, name, unit, min_val, max_val, normal_min, normal_max in sensors_config:
            self.sensors[sensor_id] = SimpleSensorData(
                sensor_id, name, unit, min_val, max_val, normal_min, normal_max
            )
    
    def start_monitoring(self):
        """Запускает мониторинг."""
        self.is_running = True
    
    def stop_monitoring(self):
        """Останавливает мониторинг."""
        self.is_running = False
    
    def update_sensors(self):
        """Обновляет все датчики."""
        if not self.is_running:
            return
        
        for sensor in self.sensors.values():
            sensor.update_value()
            
            # Проверяем на тревоги
            alert_level = sensor.get_alert_level()
            if alert_level in ['critical', 'emergency']:
                self._create_alert(sensor, alert_level)
    
    def _create_alert(self, sensor: SimpleSensorData, alert_level: str):
        """Создает тревогу."""
        # Проверяем, не было ли недавней тревоги
        recent_alerts = [
            alert for alert in self.alerts
            if (alert['sensor_id'] == sensor.sensor_id and 
                alert['alert_level'] == alert_level and
                (datetime.now() - alert['timestamp']).total_seconds() < 300)
        ]
        
        if not recent_alerts:
            alert = {
                'alert_id': f"alert_{len(self.alerts)}",
                'sensor_id': sensor.sensor_id,
                'sensor_name': sensor.name,
                'alert_level': alert_level,
                'value': sensor.current_value,
                'unit': sensor.unit,
                'timestamp': datetime.now(),
                'message': f"{alert_level.title()} уровень: {sensor.name} {sensor.current_value:.1f} {sensor.unit}"
            }
            self.alerts.append(alert)
    
    def add_patient(self, patient_id: str, patient_name: str):
        """Добавляет пациента."""
        self.patients[patient_id] = {
            'name': patient_name,
            'start_time': datetime.now(),
            'is_active': True
        }
    
    def remove_patient(self, patient_id: str):
        """Удаляет пациента."""
        if patient_id in self.patients:
            self.patients[patient_id]['is_active'] = False
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Получает данные для дашборда."""
        active_patients = [p for p in self.patients.values() if p['is_active']]
        recent_alerts = [a for a in self.alerts if (datetime.now() - a['timestamp']).total_seconds() < 3600]
        
        return {
            'total_active_sessions': len(active_patients),
            'total_alerts_last_hour': len(recent_alerts),
            'sensor_status': {
                'total_sensors': len(self.sensors),
                'active_sensors': len([s for s in self.sensors.values() if s.is_active])
            },
            'active_sessions': [
                {
                    'patient_id': pid,
                    'patient_name': pdata['name'],
                    'duration_minutes': (datetime.now() - pdata['start_time']).total_seconds() / 60,
                    'active_alerts_count': len([a for a in recent_alerts if a.get('patient_id') == pid]),
                    'latest_readings': {
                        sensor_id: {
                            'value': sensor.current_value,
                            'unit': sensor.unit,
                            'alert_level': sensor.get_alert_level(),
                            'timestamp': sensor.last_update.isoformat()
                        }
                        for sensor_id, sensor in self.sensors.items()
                    }
                }
                for pid, pdata in self.patients.items() if pdata['is_active']
            ],
            'recent_alerts': recent_alerts[-10:]  # последние 10 тревог
        }
    
    def get_sensor_statistics(self) -> Dict[str, Any]:
        """Получает статистику датчиков."""
        stats = {}
        for sensor_id, sensor in self.sensors.items():
            stats[sensor_id] = {
                'current_value': sensor.current_value,
                'alert_level': sensor.get_alert_level(),
                'is_active': sensor.is_active,
                'last_update': sensor.last_update.isoformat()
            }
        return stats


def get_monitoring_system():
    """Получает или создает систему мониторинга в session_state."""
    if 'simple_monitoring' not in st.session_state:
        st.session_state.simple_monitoring = SimpleMonitoringSystem()
    return st.session_state.simple_monitoring


def show_iot_sensors_simple():
    """Упрощенное отображение IoT датчиков."""
    st.header("📡 IoT Датчики - Система мониторинга в реальном времени")
    st.markdown("**Непрерывный мониторинг медицинских показателей с помощью IoT датчиков**")
    
    monitoring = get_monitoring_system()
    
    # Статус датчиков
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Всего датчиков", len(monitoring.sensors))
    with col2:
        active_count = len([s for s in monitoring.sensors.values() if s.is_active])
        st.metric("Активных", active_count)
    with col3:
        st.metric("Статус", "🟢 Работает" if monitoring.is_running else "🔴 Остановлено")
    with col4:
        alerts_count = len([a for a in monitoring.alerts if (datetime.now() - a['timestamp']).total_seconds() < 3600])
        st.metric("Тревог за час", alerts_count)
    
    # Управление датчиками
    st.subheader("🎛️ Управление датчиками")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🚀 Запустить мониторинг"):
            monitoring.start_monitoring()
            st.success("🚀 Мониторинг запущен")
            st.rerun()
    
    with col2:
        if st.button("⏹️ Остановить мониторинг"):
            monitoring.stop_monitoring()
            st.success("⏹️ Мониторинг остановлен")
            st.rerun()
    
    # Обновление датчиков
    if monitoring.is_running:
        monitoring.update_sensors()
    
    # Список датчиков
    st.subheader("📊 Список датчиков")
    
    for sensor_id, sensor in monitoring.sensors.items():
        with st.expander(f"📡 {sensor.name} ({sensor_id})"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write(f"**Текущее значение:** {sensor.current_value:.1f} {sensor.unit}")
                st.write(f"**Статус:** {'🟢 Активен' if sensor.is_active else '🔴 Неактивен'}")
            
            with col2:
                st.write(f"**Диапазон:** {sensor.min_val} - {sensor.max_val} {sensor.unit}")
                st.write(f"**Норма:** {sensor.normal_min} - {sensor.normal_max} {sensor.unit}")
            
            with col3:
                alert_level = sensor.get_alert_level()
                color = {"normal": "🟢", "warning": "🟡", "critical": "🔴", "emergency": "🚨"}
                st.write(f"**Уровень тревоги:** {color.get(alert_level, '⚪')} {alert_level}")
                
                if st.button(f"🔄 Обновить {sensor_id}", key=f"update_{sensor_id}"):
                    sensor.update_value()
                    st.rerun()


def show_patient_monitoring_simple():
    """Упрощенное отображение мониторинга пациентов."""
    st.header("⚡ Мониторинг пациентов в реальном времени")
    st.markdown("**Система непрерывного наблюдения за состоянием пациентов**")
    
    monitoring = get_monitoring_system()
    
    # Статистика
    dashboard = monitoring.get_dashboard_data()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Активных сессий", dashboard['total_active_sessions'])
    with col2:
        st.metric("Тревог за час", dashboard['total_alerts_last_hour'])
    with col3:
        st.metric("Всего датчиков", dashboard['sensor_status']['total_sensors'])
    with col4:
        st.metric("Активных датчиков", dashboard['sensor_status']['active_sensors'])
    
    # Управление сессиями
    st.subheader("👥 Управление сессиями мониторинга")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Добавить нового пациента:**")
        patient_id = st.text_input("ID пациента", value="P001")
        patient_name = st.text_input("Имя пациента", value="Али Хасанов")
        
        if st.button("🏥 Начать мониторинг"):
            monitoring.add_patient(patient_id, patient_name)
            st.success(f"✅ Мониторинг начат для {patient_name}")
            st.rerun()
    
    with col2:
        st.write("**Остановить сессию:**")
        active_patients = [pid for pid, pdata in monitoring.patients.items() if pdata['is_active']]
        if active_patients:
            selected_patient = st.selectbox("Выберите пациента", active_patients)
            
            if st.button("⏹️ Остановить мониторинг"):
                monitoring.remove_patient(selected_patient)
                st.success(f"✅ Мониторинг остановлен для {selected_patient}")
                st.rerun()
        else:
            st.info("Нет активных сессий мониторинга")
    
    # Активные сессии
    st.subheader("📊 Активные сессии мониторинга")
    
    if dashboard['active_sessions']:
        for session in dashboard['active_sessions']:
            with st.expander(f"👤 {session['patient_name']} (ID: {session['patient_id']}) - {session['duration_minutes']:.1f} мин"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Длительность", f"{session['duration_minutes']:.1f} мин")
                    st.metric("Активных тревог", session['active_alerts_count'])
                
                with col2:
                    if session['active_alerts_count'] > 0:
                        st.error(f"🚨 {session['active_alerts_count']} активных тревог")
                    else:
                        st.success("✅ Нет тревог")
                
                with col3:
                    st.write("**Последние показания:**")
                    for sensor_id, reading in session['latest_readings'].items():
                        alert_emoji = {"normal": "✅", "warning": "⚠️", "critical": "🔴", "emergency": "🚨"}
                        emoji = alert_emoji.get(reading['alert_level'], "❓")
                        st.write(f"{emoji} {sensor_id}: {reading['value']:.1f} {reading['unit']}")
    else:
        st.info("Нет активных сессий мониторинга")


def show_alerts_system_simple():
    """Упрощенное отображение системы тревог."""
    st.header("🚨 Система тревог и алертов")
    st.markdown("**Автоматическое обнаружение критических состояний пациентов**")
    
    monitoring = get_monitoring_system()
    dashboard = monitoring.get_dashboard_data()
    
    # Статистика тревог
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Всего тревог", len(dashboard['recent_alerts']))
    with col2:
        critical_alerts = len([a for a in dashboard['recent_alerts'] if a['alert_level'] in ['critical', 'emergency']])
        st.metric("Критических", critical_alerts)
    with col3:
        warning_alerts = len([a for a in dashboard['recent_alerts'] if a['alert_level'] == 'warning'])
        st.metric("Предупреждений", warning_alerts)
    with col4:
        st.metric("Тревог за час", dashboard['total_alerts_last_hour'])
    
    # Последние тревоги
    st.subheader("🔥 Последние тревоги")
    
    if dashboard['recent_alerts']:
        for alert in dashboard['recent_alerts']:
            alert_level = alert['alert_level']
            color = {
                'warning': "🟡",
                'critical': "🔴", 
                'emergency': "🚨"
            }.get(alert_level, "⚪")
            
            with st.expander(f"{color} {alert['message']}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**Датчик:** {alert['sensor_name']}")
                    st.write(f"**Время:** {alert['timestamp'].strftime('%H:%M:%S')}")
                
                with col2:
                    st.write(f"**Уровень:** {alert['alert_level']}")
                    st.write(f"**Значение:** {alert['value']:.1f} {alert['unit']}")
                
                with col3:
                    if alert_level in ['critical', 'emergency']:
                        st.error("🚨 Требуется немедленное внимание!")
                    else:
                        st.warning("⚠️ Требуется мониторинг")
                    
                    if st.button(f"✅ Разрешить тревогу", key=f"resolve_{alert['alert_id']}"):
                        # Удаляем тревогу из списка
                        monitoring.alerts = [a for a in monitoring.alerts if a['alert_id'] != alert['alert_id']]
                        st.success("✅ Тревога разрешена")
                        st.rerun()
    else:
        st.success("✅ Нет активных тревог")


def show_realtime_charts_simple():
    """Упрощенное отображение графиков в реальном времени."""
    st.header("📊 Графики в реальном времени")
    st.markdown("**Интерактивная визуализация медицинских показателей**")
    
    monitoring = get_monitoring_system()
    
    # Простые графики с использованием Streamlit
    st.subheader("📈 Текущие показания датчиков")
    
    sensor_stats = monitoring.get_sensor_statistics()
    
    # Создаем DataFrame для отображения
    data = []
    for sensor_id, stats in sensor_stats.items():
        sensor = monitoring.sensors[sensor_id]
        data.append({
            'Датчик': sensor.name,
            'Значение': f"{stats['current_value']:.1f} {sensor.unit}",
            'Уровень тревоги': stats['alert_level'],
            'Статус': '🟢 Активен' if stats['is_active'] else '🔴 Неактивен'
        })
    
    df = pd.DataFrame(data)
    st.dataframe(df, width='stretch')
    
    # Простые метрики
    st.subheader("📊 Ключевые показатели")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        heart_rate = monitoring.sensors['heart_rate']
        st.metric("Пульс", f"{heart_rate.current_value:.0f} уд/мин")
    
    with col2:
        temperature = monitoring.sensors['temperature']
        st.metric("Температура", f"{temperature.current_value:.1f} °C")
    
    with col3:
        oxygen = monitoring.sensors['oxygen_saturation']
        st.metric("Кислород", f"{oxygen.current_value:.0f}%")
    
    with col4:
        pressure_sys = monitoring.sensors['blood_pressure_systolic']
        st.metric("Давление", f"{pressure_sys.current_value:.0f} мм рт.ст.")


def show_notifications_system_simple():
    """Упрощенное отображение системы уведомлений."""
    st.header("📧 Система уведомлений")
    st.markdown("**Многоканальные уведомления о критических состояниях**")
    
    monitoring = get_monitoring_system()
    
    # Статистика уведомлений
    col1, col2, col3, col4 = st.columns(4)
    
    total_alerts = len(monitoring.alerts)
    recent_alerts = len([a for a in monitoring.alerts if (datetime.now() - a['timestamp']).total_seconds() < 3600])
    
    with col1:
        st.metric("Всего тревог", total_alerts)
    with col2:
        st.metric("За последний час", recent_alerts)
    with col3:
        critical_count = len([a for a in monitoring.alerts if a['alert_level'] in ['critical', 'emergency']])
        st.metric("Критических", critical_count)
    with col4:
        success_rate = 95.0  # Фиксированная для демонстрации
        st.metric("Успешность", f"{success_rate:.1f}%")
    
    # Управление получателями
    st.subheader("👥 Управление получателями")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Добавить получателя:**")
        recipient_id = st.text_input("ID получателя", value="doctor1")
        email = st.text_input("Email", value="doctor1@hospital.com")
        phone = st.text_input("Телефон", value="+992123456789")
        
        if st.button("➕ Добавить получателя"):
            st.success(f"✅ Получатель {recipient_id} добавлен")
            st.info(f"Email: {email}, Телефон: {phone}")
    
    with col2:
        st.write("**Текущие получатели:**")
        recipients = ["doctor1@hospital.com", "nurse1@hospital.com", "admin@hospital.com"]
        for recipient in recipients:
            st.write(f"• {recipient}")
    
    # История тревог
    st.subheader("📋 История тревог")
    
    if monitoring.alerts:
        alert_data = []
        for alert in monitoring.alerts[-20:]:  # последние 20
            alert_data.append({
                'Время': alert['timestamp'].strftime('%H:%M:%S'),
                'Датчик': alert['sensor_name'],
                'Уровень': alert['alert_level'],
                'Значение': f"{alert['value']:.1f} {alert['unit']}",
                'Сообщение': alert['message']
            })
        
        df = pd.DataFrame(alert_data)
        st.dataframe(df, width='stretch')
    else:
        st.info("История тревог пуста")

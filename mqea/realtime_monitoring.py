"""
Система мониторинга в реальном времени для MQEA.

Автор: Мухаммад Махизода
Таджикский национальный университет
"""

import asyncio
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable, Any, Tuple
from collections import deque, defaultdict
import threading
from dataclasses import dataclass, asdict
import uuid

from .iot_sensors import (
    IoTMedicalSensorManager, SensorReading, AlertLevel, 
    SensorStatus, create_sensor_manager
)


@dataclass
class MonitoringAlert:
    """Тревога системы мониторинга."""
    alert_id: str
    sensor_id: str
    patient_id: str
    alert_level: AlertLevel
    message: str
    timestamp: datetime
    value: float
    threshold: Tuple[float, float]
    is_resolved: bool = False
    resolved_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict:
        """Преобразует в словарь."""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        data['alert_level'] = self.alert_level.value
        data['resolved_at'] = self.resolved_at.isoformat() if self.resolved_at else None
        return data


@dataclass
class PatientMonitoringSession:
    """Сессия мониторинга пациента."""
    session_id: str
    patient_id: str
    patient_name: str
    start_time: datetime
    end_time: Optional[datetime] = None
    is_active: bool = True
    sensors: Dict[str, bool] = None  # активные датчики
    alerts: List[MonitoringAlert] = None
    readings_history: Dict[str, deque] = None
    
    def __post_init__(self):
        if self.sensors is None:
            self.sensors = {}
        if self.alerts is None:
            self.alerts = []
        if self.readings_history is None:
            self.readings_history = defaultdict(lambda: deque(maxlen=1000))
    
    def add_reading(self, reading: SensorReading):
        """Добавляет показание в историю."""
        self.readings_history[reading.sensor_id].append(reading)
    
    def add_alert(self, alert: MonitoringAlert):
        """Добавляет тревогу."""
        self.alerts.append(alert)
    
    def resolve_alert(self, alert_id: str):
        """Разрешает тревогу."""
        for alert in self.alerts:
            if alert.alert_id == alert_id and not alert.is_resolved:
                alert.is_resolved = True
                alert.resolved_at = datetime.now()
                break
    
    def get_latest_readings(self) -> Dict[str, SensorReading]:
        """Получает последние показания всех датчиков."""
        latest = {}
        for sensor_id, history in self.readings_history.items():
            if history:
                latest[sensor_id] = history[-1]
        return latest
    
    def get_session_summary(self) -> Dict:
        """Получает сводку сессии."""
        latest_readings = self.get_latest_readings()
        active_alerts = [a for a in self.alerts if not a.is_resolved]
        
        return {
            'session_id': self.session_id,
            'patient_id': self.patient_id,
            'patient_name': self.patient_name,
            'duration_minutes': (datetime.now() - self.start_time).total_seconds() / 60,
            'total_readings': sum(len(h) for h in self.readings_history.values()),
            'total_alerts': len(self.alerts),
            'active_alerts': len(active_alerts),
            'sensors_count': len(self.sensors),
            'latest_readings': {
                sensor_id: {
                    'value': reading.value,
                    'unit': reading.unit,
                    'alert_level': reading.alert_level.value,
                    'timestamp': reading.timestamp.isoformat()
                }
                for sensor_id, reading in latest_readings.items()
            }
        }


class RealtimeMonitoringSystem:
    """Система мониторинга в реальном времени."""
    
    def __init__(self):
        self.sensor_manager = create_sensor_manager()
        self.active_sessions: Dict[str, PatientMonitoringSession] = {}
        self.alert_callbacks: List[Callable[[MonitoringAlert], None]] = []
        self.reading_callbacks: List[Callable[[SensorReading, str], None]] = []
        self._running = False
        self._alert_history: deque = deque(maxlen=1000)
        
        # Подписываемся на данные датчиков
        self.sensor_manager.add_global_callback(self._on_sensor_reading)
    
    def add_alert_callback(self, callback: Callable[[MonitoringAlert], None]):
        """Добавляет callback для тревог."""
        self.alert_callbacks.append(callback)
    
    def add_reading_callback(self, callback: Callable[[SensorReading, str], None]):
        """Добавляет callback для показаний."""
        self.reading_callbacks.append(callback)
    
    def _on_sensor_reading(self, reading: SensorReading):
        """Обработчик показаний датчиков."""
        # Отправляем показания всем активным сессиям
        for session in self.active_sessions.values():
            if session.is_active and reading.sensor_id in session.sensors:
                session.add_reading(reading)
                
                # Проверяем на тревоги
                alert = self._check_for_alert(reading, session)
                if alert:
                    session.add_alert(alert)
                    self._alert_history.append(alert)
                    
                    # Отправляем уведомления
                    for callback in self.alert_callbacks:
                        try:
                            callback(alert)
                        except Exception as e:
                            print(f"Ошибка в callback тревоги: {e}")
        
        # Отправляем показания глобальным подписчикам
        for callback in self.reading_callbacks:
            try:
                callback(reading, "global")
            except Exception as e:
                print(f"Ошибка в callback показаний: {e}")
    
    def _check_for_alert(self, reading: SensorReading, session: PatientMonitoringSession) -> Optional[MonitoringAlert]:
        """Проверяет показание на наличие тревоги."""
        if reading.alert_level in [AlertLevel.CRITICAL, AlertLevel.EMERGENCY]:
            # Проверяем, не было ли уже подобной тревоги в последние 5 минут
            recent_alerts = [
                alert for alert in session.alerts
                if (alert.sensor_id == reading.sensor_id and 
                    alert.alert_level == reading.alert_level and
                    not alert.is_resolved and
                    (datetime.now() - alert.timestamp).total_seconds() < 300)
            ]
            
            if not recent_alerts:  # Нет недавних тревог
                alert = MonitoringAlert(
                    alert_id=str(uuid.uuid4()),
                    sensor_id=reading.sensor_id,
                    patient_id=session.patient_id,
                    alert_level=reading.alert_level,
                    message=self._generate_alert_message(reading),
                    timestamp=datetime.now(),
                    value=reading.value,
                    threshold=self._get_threshold(reading.sensor_id, reading.alert_level)
                )
                return alert
        
        return None
    
    def _generate_alert_message(self, reading: SensorReading) -> str:
        """Генерирует сообщение тревоги."""
        sensor_names = {
            'heart_rate': 'частота сердечных сокращений',
            'blood_pressure_systolic': 'систолическое давление',
            'blood_pressure_diastolic': 'диастолическое давление',
            'temperature': 'температура тела',
            'oxygen_saturation': 'насыщение кислородом',
            'respiratory_rate': 'частота дыхания',
            'glucose': 'уровень глюкозы',
            'cholesterol': 'уровень холестерина'
        }
        
        sensor_name = sensor_names.get(reading.sensor_id, reading.sensor_id)
        level_names = {
            AlertLevel.CRITICAL: 'критический',
            AlertLevel.EMERGENCY: 'экстренный'
        }
        
        level_name = level_names.get(reading.alert_level, 'предупреждение')
        
        return (f"{level_name.title()} уровень: {sensor_name} "
                f"{reading.value:.1f} {reading.unit}")
    
    def _get_threshold(self, sensor_id: str, alert_level: AlertLevel) -> Tuple[float, float]:
        """Получает пороговые значения для датчика."""
        sensor = self.sensor_manager.get_sensor(sensor_id)
        if sensor:
            config = sensor.config
            if alert_level == AlertLevel.CRITICAL:
                return (config.warning_min, config.warning_max)
            elif alert_level == AlertLevel.EMERGENCY:
                return (config.critical_min, config.critical_max)
        return (0.0, 0.0)
    
    def start_monitoring_session(self, patient_id: str, patient_name: str, 
                               sensors: List[str] = None) -> str:
        """Запускает сессию мониторинга для пациента."""
        if sensors is None:
            # Активируем все датчики по умолчанию
            sensors = list(self.sensor_manager.sensors.keys())
        
        session_id = str(uuid.uuid4())
        session = PatientMonitoringSession(
            session_id=session_id,
            patient_id=patient_id,
            patient_name=patient_name,
            start_time=datetime.now(),
            sensors={sensor_id: True for sensor_id in sensors}
        )
        
        self.active_sessions[session_id] = session
        print(f"🏥 Начата сессия мониторинга для {patient_name} (ID: {patient_id})")
        print(f"📊 Активные датчики: {', '.join(sensors)}")
        
        return session_id
    
    def stop_monitoring_session(self, session_id: str):
        """Останавливает сессию мониторинга."""
        if session_id in self.active_sessions:
            session = self.active_sessions[session_id]
            session.is_active = False
            session.end_time = datetime.now()
            print(f"⏹️ Сессия мониторинга остановлена для {session.patient_name}")
            return session.get_session_summary()
        return None
    
    def get_session(self, session_id: str) -> Optional[PatientMonitoringSession]:
        """Получает сессию по ID."""
        return self.active_sessions.get(session_id)
    
    def get_active_sessions(self) -> List[PatientMonitoringSession]:
        """Получает все активные сессии."""
        return [s for s in self.active_sessions.values() if s.is_active]
    
    def resolve_alert(self, session_id: str, alert_id: str):
        """Разрешает тревогу."""
        if session_id in self.active_sessions:
            self.active_sessions[session_id].resolve_alert(alert_id)
    
    def get_monitoring_dashboard_data(self) -> Dict:
        """Получает данные для дашборда мониторинга."""
        active_sessions = self.get_active_sessions()
        recent_alerts = list(self._alert_history)[-10:]  # последние 10 тревог
        
        dashboard_data = {
            'timestamp': datetime.now().isoformat(),
            'total_active_sessions': len(active_sessions),
            'total_alerts_last_hour': len([
                a for a in self._alert_history 
                if (datetime.now() - a.timestamp).total_seconds() < 3600
            ]),
            'active_sessions': [],
            'recent_alerts': [alert.to_dict() for alert in recent_alerts],
            'sensor_status': self.sensor_manager.get_status_summary()
        }
        
        for session in active_sessions:
            latest_readings = session.get_latest_readings()
            active_alerts = [a for a in session.alerts if not a.is_resolved]
            
            session_data = {
                'session_id': session.session_id,
                'patient_id': session.patient_id,
                'patient_name': session.patient_name,
                'duration_minutes': (datetime.now() - session.start_time).total_seconds() / 60,
                'active_alerts_count': len(active_alerts),
                'latest_readings': {
                    sensor_id: {
                        'value': reading.value,
                        'unit': reading.unit,
                        'alert_level': reading.alert_level.value,
                        'timestamp': reading.timestamp.isoformat()
                    }
                    for sensor_id, reading in latest_readings.items()
                }
            }
            dashboard_data['active_sessions'].append(session_data)
        
        return dashboard_data
    
    async def start(self):
        """Запускает систему мониторинга."""
        if not self._running:
            self._running = True
            await self.sensor_manager.start_all()
            print("🚀 Система мониторинга в реальном времени запущена")
    
    async def stop(self):
        """Останавливает систему мониторинга."""
        self._running = False
        await self.sensor_manager.stop_all()
        
        # Останавливаем все активные сессии
        for session in self.active_sessions.values():
            if session.is_active:
                session.is_active = False
                session.end_time = datetime.now()
        
        print("⏹️ Система мониторинга остановлена")


# Функции для создания и управления системой
def create_monitoring_system() -> RealtimeMonitoringSystem:
    """Создает систему мониторинга."""
    return RealtimeMonitoringSystem()


async def demo_monitoring_system():
    """Демонстрация системы мониторинга."""
    print("🏥 MQEA - Демонстрация системы мониторинга в реальном времени")
    print("=" * 70)
    
    # Создаем систему мониторинга
    monitoring = create_monitoring_system()
    
    # Добавляем callback для отображения тревог
    def on_alert(alert: MonitoringAlert):
        timestamp = alert.timestamp.strftime("%H:%M:%S")
        alert_emoji = {
            AlertLevel.CRITICAL: "🔴",
            AlertLevel.EMERGENCY: "🚨"
        }
        
        print(f"\n{alert_emoji[alert.alert_level]} ТРЕВОГА [{timestamp}]")
        print(f"   Пациент: {alert.patient_id}")
        print(f"   Датчик: {alert.sensor_id}")
        print(f"   Сообщение: {alert.message}")
        print(f"   Значение: {alert.value} (порог: {alert.threshold})")
    
    monitoring.add_alert_callback(on_alert)
    
    # Запускаем систему
    await monitoring.start()
    
    # Создаем тестовых пациентов
    patients = [
        ("P001", "Али Хасанов"),
        ("P002", "Фатима Алимова"),
        ("P003", "Ахмад Рахимов")
    ]
    
    session_ids = []
    for patient_id, patient_name in patients:
        session_id = monitoring.start_monitoring_session(
            patient_id=patient_id,
            patient_name=patient_name
        )
        session_ids.append(session_id)
    
    print(f"\n📊 Мониторинг запущен для {len(patients)} пациентов")
    print("⏱️ Демонстрация будет работать 60 секунд...")
    
    # Показываем статистику каждые 10 секунд
    for i in range(6):
        await asyncio.sleep(10)
        
        dashboard = monitoring.get_monitoring_dashboard_data()
        print(f"\n📈 Статистика ({(i+1)*10}с):")
        print(f"   Активных сессий: {dashboard['total_active_sessions']}")
        print(f"   Тревог за час: {dashboard['total_alerts_last_hour']}")
        
        for session in dashboard['active_sessions']:
            print(f"   👤 {session['patient_name']}: {session['active_alerts_count']} тревог")
    
    # Останавливаем сессии
    print(f"\n⏹️ Остановка сессий мониторинга...")
    for session_id in session_ids:
        summary = monitoring.stop_monitoring_session(session_id)
        if summary:
            print(f"   📊 {summary['patient_name']}: {summary['total_readings']} показаний, "
                  f"{summary['total_alerts']} тревог")
    
    # Останавливаем систему
    await monitoring.stop()
    print("\n✅ Демонстрация завершена")


if __name__ == "__main__":
    asyncio.run(demo_monitoring_system())


"""
IoT датчики для системы мониторинга в реальном времени MQEA.

Автор: Мухаммад Махизода
Таджикский национальный университет
"""

import asyncio
import random
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable, Any
import json
import threading
from dataclasses import dataclass, asdict
from enum import Enum


class SensorStatus(Enum):
    """Статус датчика."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"
    MAINTENANCE = "maintenance"


class AlertLevel(Enum):
    """Уровень тревоги."""
    NORMAL = "normal"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


@dataclass
class SensorReading:
    """Показание датчика."""
    sensor_id: str
    timestamp: datetime
    value: float
    unit: str
    status: SensorStatus
    alert_level: AlertLevel
    metadata: Dict[str, Any] = None

    def to_dict(self) -> Dict:
        """Преобразует в словарь."""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        data['status'] = self.status.value
        data['alert_level'] = self.alert_level.value
        return data


@dataclass
class SensorConfig:
    """Конфигурация датчика."""
    sensor_id: str
    name: str
    unit: str
    min_value: float
    max_value: float
    normal_min: float
    normal_max: float
    warning_min: float
    warning_max: float
    critical_min: float
    critical_max: float
    update_interval: float = 1.0  # секунды
    noise_level: float = 0.05  # уровень шума (5%)


class IoTMedicalSensor:
    """Базовый класс IoT датчика для медицинских показателей."""
    
    def __init__(self, config: SensorConfig):
        self.config = config
        self.status = SensorStatus.ACTIVE
        self.current_value = (config.normal_min + config.normal_max) / 2
        self.trend = 0.0  # тренд изменения
        self.callbacks: List[Callable[[SensorReading], None]] = []
        self._running = False
        self._task: Optional[asyncio.Task] = None
        
    def add_callback(self, callback: Callable[[SensorReading], None]):
        """Добавляет callback для получения данных."""
        self.callbacks.append(callback)
    
    def remove_callback(self, callback: Callable[[SensorReading], None]):
        """Удаляет callback."""
        if callback in self.callbacks:
            self.callbacks.remove(callback)
    
    def _generate_value(self) -> float:
        """Генерирует новое значение датчика."""
        # Добавляем тренд
        trend_change = random.uniform(-0.01, 0.01)
        self.trend += trend_change
        self.trend = max(-0.1, min(0.1, self.trend))  # ограничиваем тренд
        
        # Генерируем значение с учетом тренда
        base_value = self.current_value + self.trend * self.current_value
        
        # Добавляем шум
        noise = random.uniform(-self.config.noise_level, self.config.noise_level)
        new_value = base_value * (1 + noise)
        
        # Ограничиваем диапазон
        new_value = max(self.config.min_value, min(self.config.max_value, new_value))
        
        # Иногда добавляем случайные аномалии
        if random.random() < 0.02:  # 2% вероятность аномалии
            anomaly = random.uniform(-0.2, 0.2)
            new_value = new_value * (1 + anomaly)
        
        self.current_value = new_value
        return new_value
    
    def _determine_alert_level(self, value: float) -> AlertLevel:
        """Определяет уровень тревоги на основе значения."""
        if value <= self.config.critical_min or value >= self.config.critical_max:
            return AlertLevel.EMERGENCY
        elif value <= self.config.warning_min or value >= self.config.warning_max:
            return AlertLevel.CRITICAL
        elif value < self.config.normal_min or value > self.config.normal_max:
            return AlertLevel.WARNING
        else:
            return AlertLevel.NORMAL
    
    async def _reading_loop(self):
        """Основной цикл получения данных."""
        while self._running:
            try:
                if self.status == SensorStatus.ACTIVE:
                    value = self._generate_value()
                    alert_level = self._determine_alert_level(value)
                    
                    reading = SensorReading(
                        sensor_id=self.config.sensor_id,
                        timestamp=datetime.now(),
                        value=value,
                        unit=self.config.unit,
                        status=self.status,
                        alert_level=alert_level,
                        metadata={
                            'trend': self.trend,
                            'battery_level': random.uniform(80, 100),
                            'signal_strength': random.uniform(70, 100)
                        }
                    )
                    
                    # Отправляем данные всем подписчикам
                    for callback in self.callbacks:
                        try:
                            callback(reading)
                        except Exception as e:
                            print(f"Ошибка в callback для датчика {self.config.sensor_id}: {e}")
                
                await asyncio.sleep(self.config.update_interval)
                
            except Exception as e:
                print(f"Ошибка в цикле датчика {self.config.sensor_id}: {e}")
                await asyncio.sleep(1.0)
    
    async def start(self):
        """Запускает датчик."""
        if not self._running:
            self._running = True
            self.status = SensorStatus.ACTIVE
            self._task = asyncio.create_task(self._reading_loop())
            print(f"🔴 Датчик {self.config.name} запущен")
    
    async def stop(self):
        """Останавливает датчик."""
        self._running = False
        self.status = SensorStatus.INACTIVE
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        print(f"⏹️ Датчик {self.config.name} остановлен")
    
    def set_status(self, status: SensorStatus):
        """Устанавливает статус датчика."""
        self.status = status
        print(f"📊 Датчик {self.config.name}: статус изменен на {status.value}")


class IoTMedicalSensorManager:
    """Менеджер IoT датчиков."""
    
    def __init__(self):
        self.sensors: Dict[str, IoTMedicalSensor] = {}
        self.global_callbacks: List[Callable[[SensorReading], None]] = []
        self._running = False
        
    def create_default_sensors(self) -> Dict[str, IoTMedicalSensor]:
        """Создает набор стандартных медицинских датчиков."""
        sensors_configs = [
            SensorConfig(
                sensor_id="heart_rate",
                name="Частота сердечных сокращений",
                unit="уд/мин",
                min_value=30, max_value=200,
                normal_min=60, normal_max=100,
                warning_min=50, warning_max=120,
                critical_min=40, critical_max=150,
                update_interval=2.0
            ),
            SensorConfig(
                sensor_id="blood_pressure_systolic",
                name="Систолическое давление",
                unit="мм рт.ст.",
                min_value=70, max_value=250,
                normal_min=90, normal_max=140,
                warning_min=80, warning_max=160,
                critical_min=70, critical_max=180,
                update_interval=5.0
            ),
            SensorConfig(
                sensor_id="blood_pressure_diastolic",
                name="Диастолическое давление",
                unit="мм рт.ст.",
                min_value=40, max_value=150,
                normal_min=60, normal_max=90,
                warning_min=50, warning_max=100,
                critical_min=40, critical_max=110,
                update_interval=5.0
            ),
            SensorConfig(
                sensor_id="temperature",
                name="Температура тела",
                unit="°C",
                min_value=35.0, max_value=42.0,
                normal_min=36.0, normal_max=37.5,
                warning_min=35.5, warning_max=38.0,
                critical_min=35.0, critical_max=39.0,
                update_interval=10.0
            ),
            SensorConfig(
                sensor_id="oxygen_saturation",
                name="Насыщение кислородом",
                unit="%",
                min_value=70, max_value=100,
                normal_min=95, normal_max=100,
                warning_min=90, warning_max=95,
                critical_min=85, critical_max=90,
                update_interval=3.0
            ),
            SensorConfig(
                sensor_id="respiratory_rate",
                name="Частота дыхания",
                unit="дых/мин",
                min_value=5, max_value=40,
                normal_min=12, normal_max=20,
                warning_min=10, warning_max=25,
                critical_min=8, critical_max=30,
                update_interval=4.0
            ),
            SensorConfig(
                sensor_id="glucose",
                name="Уровень глюкозы",
                unit="мг/дл",
                min_value=50, max_value=400,
                normal_min=70, normal_max=140,
                warning_min=60, warning_max=180,
                critical_min=50, critical_max=250,
                update_interval=15.0
            ),
            SensorConfig(
                sensor_id="cholesterol",
                name="Уровень холестерина",
                unit="мг/дл",
                min_value=100, max_value=400,
                normal_min=150, normal_max=200,
                warning_min=130, warning_max=240,
                critical_min=100, critical_max=300,
                update_interval=60.0
            )
        ]
        
        sensors = {}
        for config in sensors_configs:
            sensor = IoTMedicalSensor(config)
            sensor.add_callback(self._on_sensor_reading)
            sensors[config.sensor_id] = sensor
            
        return sensors
    
    def _on_sensor_reading(self, reading: SensorReading):
        """Обработчик показаний датчиков."""
        # Отправляем глобальным подписчикам
        for callback in self.global_callbacks:
            try:
                callback(reading)
            except Exception as e:
                print(f"Ошибка в глобальном callback: {e}")
    
    def add_sensor(self, sensor: IoTMedicalSensor):
        """Добавляет датчик."""
        self.sensors[sensor.config.sensor_id] = sensor
        sensor.add_callback(self._on_sensor_reading)
        print(f"➕ Датчик {sensor.config.name} добавлен")
    
    def remove_sensor(self, sensor_id: str):
        """Удаляет датчик."""
        if sensor_id in self.sensors:
            sensor = self.sensors[sensor_id]
            asyncio.create_task(sensor.stop())
            del self.sensors[sensor_id]
            print(f"➖ Датчик {sensor_id} удален")
    
    def get_sensor(self, sensor_id: str) -> Optional[IoTMedicalSensor]:
        """Получает датчик по ID."""
        return self.sensors.get(sensor_id)
    
    def add_global_callback(self, callback: Callable[[SensorReading], None]):
        """Добавляет глобальный callback."""
        self.global_callbacks.append(callback)
    
    def remove_global_callback(self, callback: Callable[[SensorReading], None]):
        """Удаляет глобальный callback."""
        if callback in self.global_callbacks:
            self.global_callbacks.remove(callback)
    
    async def start_all(self):
        """Запускает все датчики."""
        self._running = True
        tasks = []
        for sensor in self.sensors.values():
            tasks.append(sensor.start())
        
        if tasks:
            await asyncio.gather(*tasks)
        print("🚀 Все датчики запущены")
    
    async def stop_all(self):
        """Останавливает все датчики."""
        self._running = False
        tasks = []
        for sensor in self.sensors.values():
            tasks.append(sensor.stop())
        
        if tasks:
            await asyncio.gather(*tasks)
        print("⏹️ Все датчики остановлены")
    
    def get_status_summary(self) -> Dict:
        """Получает сводку по всем датчикам."""
        summary = {
            'total_sensors': len(self.sensors),
            'active_sensors': sum(1 for s in self.sensors.values() if s.status == SensorStatus.ACTIVE),
            'inactive_sensors': sum(1 for s in self.sensors.values() if s.status == SensorStatus.INACTIVE),
            'error_sensors': sum(1 for s in self.sensors.values() if s.status == SensorStatus.ERROR),
            'sensors': {}
        }
        
        for sensor_id, sensor in self.sensors.items():
            summary['sensors'][sensor_id] = {
                'name': sensor.config.name,
                'status': sensor.status.value,
                'current_value': sensor.current_value,
                'unit': sensor.config.unit,
                'alert_level': sensor._determine_alert_level(sensor.current_value).value
            }
        
        return summary


# Функции для создания и управления датчиками
def create_sensor_manager() -> IoTMedicalSensorManager:
    """Создает менеджер датчиков с набором по умолчанию."""
    manager = IoTMedicalSensorManager()
    default_sensors = manager.create_default_sensors()
    for sensor in default_sensors.values():
        manager.add_sensor(sensor)
    return manager


async def demo_sensors():
    """Демонстрация работы датчиков."""
    print("🧬 MQEA - Демонстрация IoT датчиков")
    print("=" * 50)
    
    # Создаем менеджер датчиков
    manager = create_sensor_manager()
    
    # Добавляем callback для отображения данных
    def print_reading(reading: SensorReading):
        timestamp = reading.timestamp.strftime("%H:%M:%S")
        alert_emoji = {
            AlertLevel.NORMAL: "✅",
            AlertLevel.WARNING: "⚠️",
            AlertLevel.CRITICAL: "🔴",
            AlertLevel.EMERGENCY: "🚨"
        }
        
        print(f"{alert_emoji[reading.alert_level]} {timestamp} | "
              f"{reading.sensor_id}: {reading.value:.1f} {reading.unit} "
              f"[{reading.alert_level.value}]")
    
    manager.add_global_callback(print_reading)
    
    # Запускаем датчики
    print("\n🚀 Запуск датчиков...")
    await manager.start_all()
    
    # Работаем 30 секунд
    print("\n📊 Мониторинг в реальном времени (30 секунд)...")
    await asyncio.sleep(30)
    
    # Останавливаем
    print("\n⏹️ Остановка датчиков...")
    await manager.stop_all()
    
    # Показываем итоговую статистику
    summary = manager.get_status_summary()
    print(f"\n📈 Итоговая статистика:")
    print(f"   Всего датчиков: {summary['total_sensors']}")
    print(f"   Активных: {summary['active_sensors']}")
    print(f"   Неактивных: {summary['inactive_sensors']}")


if __name__ == "__main__":
    asyncio.run(demo_sensors())


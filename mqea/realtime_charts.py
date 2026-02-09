"""
Система графиков в реальном времени для MQEA.

Автор: Мухаммад Махизода
Таджикский национальный университет
"""

import asyncio
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from collections import deque
import threading
from dataclasses import dataclass, asdict
import uuid

try:
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    print("⚠️ Plotly не установлен. Графики будут недоступны.")

try:
    import streamlit as st
    STREAMLIT_AVAILABLE = True
except ImportError:
    STREAMLIT_AVAILABLE = False

from .iot_sensors import SensorReading, AlertLevel, SensorStatus
from .realtime_monitoring import PatientMonitoringSession


@dataclass
class ChartConfig:
    """Конфигурация графика."""
    chart_id: str
    name: str
    chart_type: str  # line, bar, scatter, heatmap
    sensors: List[str]
    time_window_minutes: int = 30
    update_interval_seconds: int = 2
    colors: Dict[str, str] = None
    y_range: Tuple[float, float] = None
    show_alerts: bool = True
    
    def __post_init__(self):
        if self.colors is None:
            self.colors = {
                'heart_rate': '#FF6B6B',
                'blood_pressure_systolic': '#4ECDC4',
                'blood_pressure_diastolic': '#45B7D1',
                'temperature': '#FFA07A',
                'oxygen_saturation': '#98D8C8',
                'respiratory_rate': '#F7DC6F',
                'glucose': '#BB8FCE',
                'cholesterol': '#85C1E9'
            }


@dataclass
class ChartDataPoint:
    """Точка данных для графика."""
    timestamp: datetime
    sensor_id: str
    value: float
    alert_level: AlertLevel
    metadata: Dict[str, Any] = None
    
    def to_dict(self) -> Dict:
        """Преобразует в словарь."""
        return {
            'timestamp': self.timestamp.isoformat(),
            'sensor_id': self.sensor_id,
            'value': self.value,
            'alert_level': self.alert_level.value,
            'metadata': self.metadata or {}
        }


class RealtimeChart:
    """График в реальном времени."""
    
    def __init__(self, config: ChartConfig):
        self.config = config
        self.data_points: deque = deque(maxlen=1000)  # последние 1000 точек
        self.sensor_data: Dict[str, deque] = {}
        self.alert_points: List[ChartDataPoint] = []
        self.last_update = datetime.now()
        self.is_active = True
        
        # Инициализируем очереди для каждого датчика
        for sensor_id in config.sensors:
            self.sensor_data[sensor_id] = deque(maxlen=500)
    
    def add_data_point(self, reading: SensorReading):
        """Добавляет точку данных."""
        if reading.sensor_id not in self.config.sensors:
            return
        
        data_point = ChartDataPoint(
            timestamp=reading.timestamp,
            sensor_id=reading.sensor_id,
            value=reading.value,
            alert_level=reading.alert_level,
            metadata={
                'unit': reading.unit,
                'status': reading.status.value,
                'battery_level': reading.metadata.get('battery_level', 100) if reading.metadata else 100
            }
        )
        
        self.data_points.append(data_point)
        self.sensor_data[reading.sensor_id].append(data_point)
        
        # Если это тревога, добавляем в список тревог
        if self.config.show_alerts and reading.alert_level in [AlertLevel.CRITICAL, AlertLevel.EMERGENCY]:
            self.alert_points.append(data_point)
            # Ограничиваем количество тревог
            if len(self.alert_points) > 100:
                self.alert_points = self.alert_points[-100:]
        
        self.last_update = datetime.now()
    
    def get_chart_data(self, time_window_minutes: Optional[int] = None) -> Dict[str, Any]:
        """Получает данные для отображения на графике."""
        if time_window_minutes is None:
            time_window_minutes = self.config.time_window_minutes
        
        cutoff_time = datetime.now() - timedelta(minutes=time_window_minutes)
        
        # Фильтруем данные по времени
        filtered_data = {
            sensor_id: [
                point for point in data_queue
                if point.timestamp >= cutoff_time
            ]
            for sensor_id, data_queue in self.sensor_data.items()
        }
        
        # Фильтруем тревоги
        filtered_alerts = [
            point for point in self.alert_points
            if point.timestamp >= cutoff_time
        ]
        
        return {
            'sensor_data': filtered_data,
            'alerts': filtered_alerts,
            'time_window_minutes': time_window_minutes,
            'last_update': self.last_update.isoformat(),
            'total_points': len(self.data_points)
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Получает статистику по данным."""
        stats = {}
        
        for sensor_id, data_queue in self.sensor_data.items():
            if not data_queue:
                continue
                
            values = [point.value for point in data_queue]
            recent_values = values[-10:] if len(values) >= 10 else values
            
            stats[sensor_id] = {
                'current_value': values[-1] if values else 0,
                'min_value': min(values) if values else 0,
                'max_value': max(values) if values else 0,
                'avg_value': sum(values) / len(values) if values else 0,
                'trend': self._calculate_trend(recent_values),
                'data_points_count': len(values),
                'last_update': data_queue[-1].timestamp.isoformat() if data_queue else None
            }
        
        return stats
    
    def _calculate_trend(self, values: List[float]) -> str:
        """Вычисляет тренд по последним значениям."""
        if len(values) < 3:
            return "недостаточно данных"
        
        # Простая линейная регрессия для определения тренда
        n = len(values)
        x_sum = sum(range(n))
        y_sum = sum(values)
        xy_sum = sum(i * values[i] for i in range(n))
        x2_sum = sum(i * i for i in range(n))
        
        if n * x2_sum - x_sum * x_sum == 0:
            return "стабильный"
        
        slope = (n * xy_sum - x_sum * y_sum) / (n * x2_sum - x_sum * x_sum)
        
        if slope > 0.1:
            return "растущий"
        elif slope < -0.1:
            return "убывающий"
        else:
            return "стабильный"


class RealtimeChartManager:
    """Менеджер графиков в реальном времени."""
    
    def __init__(self):
        self.charts: Dict[str, RealtimeChart] = {}
        self.chart_configs: Dict[str, ChartConfig] = {}
        self.is_running = False
        self.update_thread: Optional[threading.Thread] = None
        
        # Создаем графики по умолчанию
        self._create_default_charts()
    
    def _create_default_charts(self):
        """Создает графики по умолчанию."""
        default_charts = [
            ChartConfig(
                chart_id="vital_signs",
                name="Основные жизненные показатели",
                chart_type="line",
                sensors=["heart_rate", "temperature", "oxygen_saturation"],
                time_window_minutes=30,
                update_interval_seconds=2
            ),
            ChartConfig(
                chart_id="blood_pressure",
                name="Артериальное давление",
                chart_type="line",
                sensors=["blood_pressure_systolic", "blood_pressure_diastolic"],
                time_window_minutes=60,
                update_interval_seconds=5
            ),
            ChartConfig(
                chart_id="metabolic",
                name="Метаболические показатели",
                chart_type="line",
                sensors=["glucose", "cholesterol"],
                time_window_minutes=120,
                update_interval_seconds=15
            ),
            ChartConfig(
                chart_id="respiratory",
                name="Дыхательная система",
                chart_type="line",
                sensors=["respiratory_rate", "oxygen_saturation"],
                time_window_minutes=30,
                update_interval_seconds=3
            )
        ]
        
        for config in default_charts:
            self.add_chart(config)
    
    def add_chart(self, config: ChartConfig):
        """Добавляет график."""
        chart = RealtimeChart(config)
        self.charts[config.chart_id] = chart
        self.chart_configs[config.chart_id] = config
        print(f"📊 График '{config.name}' добавлен")
    
    def remove_chart(self, chart_id: str):
        """Удаляет график."""
        if chart_id in self.charts:
            del self.charts[chart_id]
            del self.chart_configs[chart_id]
            print(f"🗑️ График {chart_id} удален")
    
    def add_sensor_reading(self, reading: SensorReading):
        """Добавляет показание датчика во все подходящие графики."""
        for chart in self.charts.values():
            chart.add_data_point(reading)
    
    def get_chart_data(self, chart_id: str, time_window_minutes: Optional[int] = None) -> Optional[Dict]:
        """Получает данные графика."""
        if chart_id not in self.charts:
            return None
        
        return self.charts[chart_id].get_chart_data(time_window_minutes)
    
    def get_all_charts_data(self) -> Dict[str, Dict]:
        """Получает данные всех графиков."""
        return {
            chart_id: self.get_chart_data(chart_id)
            for chart_id in self.charts.keys()
        }
    
    def get_charts_statistics(self) -> Dict[str, Dict]:
        """Получает статистику всех графиков."""
        return {
            chart_id: chart.get_statistics()
            for chart_id, chart in self.charts.items()
        }
    
    def create_plotly_chart(self, chart_id: str, time_window_minutes: Optional[int] = None) -> Optional[go.Figure]:
        """Создает график Plotly."""
        if not PLOTLY_AVAILABLE:
            return None
        
        chart_data = self.get_chart_data(chart_id, time_window_minutes)
        if not chart_data:
            return None
        
        config = self.chart_configs[chart_id]
        
        # Создаем subplot для нескольких датчиков
        sensor_count = len(config.sensors)
        if sensor_count == 0:
            return None
        
        fig = make_subplots(
            rows=sensor_count,
            cols=1,
            subplot_titles=[f"{sensor_id}" for sensor_id in config.sensors],
            vertical_spacing=0.1
        )
        
        # Добавляем данные для каждого датчика
        for i, sensor_id in enumerate(config.sensors):
            sensor_points = chart_data['sensor_data'].get(sensor_id, [])
            
            if not sensor_points:
                continue
            
            timestamps = [point.timestamp for point in sensor_points]
            values = [point.value for point in sensor_points]
            
            # Определяем цвет на основе уровня тревоги
            colors = []
            for point in sensor_points:
                if point.alert_level == AlertLevel.EMERGENCY:
                    colors.append('#FF0000')  # красный
                elif point.alert_level == AlertLevel.CRITICAL:
                    colors.append('#FFA500')  # оранжевый
                elif point.alert_level == AlertLevel.WARNING:
                    colors.append('#FFFF00')  # желтый
                else:
                    colors.append(config.colors.get(sensor_id, '#0000FF'))  # синий по умолчанию
            
            fig.add_trace(
                go.Scatter(
                    x=timestamps,
                    y=values,
                    mode='lines+markers',
                    name=sensor_id,
                    line=dict(color=config.colors.get(sensor_id, '#0000FF')),
                    marker=dict(color=colors, size=6),
                    hovertemplate=f'<b>{sensor_id}</b><br>' +
                                'Время: %{x}<br>' +
                                'Значение: %{y}<br>' +
                                '<extra></extra>'
                ),
                row=i+1,
                col=1
            )
        
        # Настраиваем layout
        fig.update_layout(
            title=f"{config.name} - Последние {chart_data['time_window_minutes']} минут",
            height=200 * sensor_count,
            showlegend=True,
            hovermode='x unified'
        )
        
        return fig
    
    def start_monitoring(self):
        """Запускает мониторинг графиков."""
        if not self.is_running:
            self.is_running = True
            print("📊 Мониторинг графиков запущен")
    
    def stop_monitoring(self):
        """Останавливает мониторинг графиков."""
        self.is_running = False
        print("⏹️ Мониторинг графиков остановлен")


def create_chart_manager() -> RealtimeChartManager:
    """Создает менеджер графиков."""
    return RealtimeChartManager()


def create_streamlit_charts(chart_manager: RealtimeChartManager):
    """Создает Streamlit интерфейс для графиков."""
    if not STREAMLIT_AVAILABLE:
        st.error("Streamlit не доступен")
        return
    
    st.title("📊 Графики в реальном времени - MQEA")
    
    # Выбор графика
    chart_ids = list(chart_manager.charts.keys())
    selected_chart = st.selectbox(
        "Выберите график:",
        chart_ids,
        format_func=lambda x: chart_manager.chart_configs[x].name
    )
    
    # Настройки времени
    col1, col2 = st.columns(2)
    with col1:
        time_window = st.slider(
            "Временное окно (минуты):",
            min_value=5,
            max_value=120,
            value=30,
            step=5
        )
    
    with col2:
        auto_refresh = st.checkbox("Автообновление", value=True)
        if auto_refresh:
            refresh_interval = st.slider(
                "Интервал обновления (секунды):",
                min_value=1,
                max_value=30,
                value=2,
                step=1
            )
    
    # Кнопка обновления
    if st.button("🔄 Обновить график") or auto_refresh:
        if PLOTLY_AVAILABLE:
            fig = chart_manager.create_plotly_chart(selected_chart, time_window)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.error("Не удалось создать график")
        else:
            st.error("Plotly не установлен. Установите: pip install plotly")
    
    # Статистика
    st.subheader("📈 Статистика")
    stats = chart_manager.get_charts_statistics()
    
    if selected_chart in stats:
        sensor_stats = stats[selected_chart]
        
        for sensor_id, sensor_stat in sensor_stats.items():
            with st.expander(f"📊 {sensor_id}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Текущее значение", f"{sensor_stat['current_value']:.1f}")
                    st.metric("Среднее значение", f"{sensor_stat['avg_value']:.1f}")
                
                with col2:
                    st.metric("Минимальное", f"{sensor_stat['min_value']:.1f}")
                    st.metric("Максимальное", f"{sensor_stat['max_value']:.1f}")
                
                with col3:
                    st.metric("Тренд", sensor_stat['trend'])
                    st.metric("Точек данных", sensor_stat['data_points_count'])
    
    # Автообновление
    if auto_refresh:
        time.sleep(refresh_interval)
        st.rerun()


async def demo_realtime_charts():
    """Демонстрация графиков в реальном времени."""
    print("📊 MQEA - Демонстрация графиков в реальном времени")
    print("=" * 60)
    
    if not PLOTLY_AVAILABLE:
        print("⚠️ Plotly не установлен. Установите: pip install plotly")
        return
    
    # Создаем менеджер графиков
    chart_manager = create_chart_manager()
    chart_manager.start_monitoring()
    
    # Создаем симулятор датчиков для демонстрации
    from .iot_sensors import create_sensor_manager
    
    sensor_manager = create_sensor_manager()
    
    # Подключаем датчики к графикам
    def on_sensor_reading(reading: SensorReading):
        chart_manager.add_sensor_reading(reading)
    
    sensor_manager.add_global_callback(on_sensor_reading)
    
    # Запускаем датчики
    await sensor_manager.start_all()
    
    print("\n📊 Создание графиков...")
    
    # Создаем и сохраняем графики
    chart_ids = list(chart_manager.charts.keys())
    
    for i in range(10):  # 10 итераций по 3 секунды = 30 секунд
        await asyncio.sleep(3)
        
        print(f"\n📈 Обновление графиков ({(i+1)*3}с)...")
        
        # Показываем статистику
        stats = chart_manager.get_charts_statistics()
        for chart_id, chart_stats in stats.items():
            config = chart_manager.chart_configs[chart_id]
            print(f"   📊 {config.name}:")
            
            for sensor_id, sensor_stat in chart_stats.items():
                print(f"      {sensor_id}: {sensor_stat['current_value']:.1f} "
                      f"(тренд: {sensor_stat['trend']})")
    
    # Останавливаем
    await sensor_manager.stop_all()
    chart_manager.stop_monitoring()
    
    print("\n✅ Демонстрация завершена")


if __name__ == "__main__":
    asyncio.run(demo_realtime_charts())


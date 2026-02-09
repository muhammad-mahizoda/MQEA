"""
Модуль визуализации результатов MQEA.

Предоставляет интерактивные и статические графики для
визуализации квантового анализа медицинских данных.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
from typing import Dict, List, Tuple, Optional, Any
import warnings

from .data_processor import MedicalTimeSeries, TemporalPattern


class MQEAVisualizer:
    """
    Визуализатор результатов MQEA.
    
    Создает интерактивные и статические графики для:
    - Временных рядов медицинских данных
    - Квантовых запутанностей между показателями
    - Обнаруженных паттернов и аномалий
    - Сетей квантовой запутанности
    """
    
    def __init__(self, theme: str = 'plotly_white'):
        """
        Инициализация визуализатора.
        
        Args:
            theme: Тема для графиков Plotly
        """
        self.theme = theme
        self.colors = {
            'primary': '#1f77b4',
            'secondary': '#ff7f0e', 
            'success': '#2ca02c',
            'danger': '#d62728',
            'warning': '#ff7f0e',
            'info': '#17a2b8',
            'quantum': '#8e44ad',
            'entangled': '#e74c3c'
        }
        
        # Настройка стилей
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
        print("MQEA Visualizer инициализирован")
    
    def plot_time_series(self, 
                        time_series: MedicalTimeSeries,
                        indicators: Optional[List[str]] = None,
                        show_missing: bool = True,
                        interactive: bool = True) -> go.Figure:
        """
        Создает график временных рядов медицинских данных.
        
        Args:
            time_series: Временной ряд для визуализации
            indicators: Список показателей для отображения
            show_missing: Показывать ли пропущенные данные
            interactive: Создавать ли интерактивный график
            
        Returns:
            go.Figure: График временных рядов
        """
        if indicators is None:
            indicators = time_series.indicators
        
        if interactive:
            return self._plot_interactive_time_series(time_series, indicators, show_missing)
        else:
            return self._plot_static_time_series(time_series, indicators, show_missing)
    
    def _plot_interactive_time_series(self, 
                                    time_series: MedicalTimeSeries,
                                    indicators: List[str],
                                    show_missing: bool) -> go.Figure:
        """Создает интерактивный график временных рядов."""
        fig = make_subplots(
            rows=len(indicators), 
            cols=1,
            subplot_titles=indicators,
            vertical_spacing=0.05,
            specs=[[{"secondary_y": False}] for _ in indicators]
        )
        
        for i, indicator in enumerate(indicators):
            data = time_series.data[indicator]
            timestamps = time_series.timestamps
            
            # Основная линия данных
            fig.add_trace(
                go.Scatter(
                    x=timestamps,
                    y=data,
                    mode='lines+markers',
                    name=indicator,
                    line=dict(color=self.colors['primary'], width=2),
                    marker=dict(size=4),
                    hovertemplate=f'<b>{indicator}</b><br>' +
                                'Время: %{x}<br>' +
                                'Значение: %{y:.2f}<br>' +
                                '<extra></extra>'
                ),
                row=i+1, col=1
            )
            
            # Выделение пропущенных данных
            if show_missing and time_series.missing_data_mask[indicator].any():
                missing_data = data[time_series.missing_data_mask[indicator]]
                missing_times = timestamps[time_series.missing_data_mask[indicator]]
                
                fig.add_trace(
                    go.Scatter(
                        x=missing_times,
                        y=missing_data,
                        mode='markers',
                        name=f'{indicator} (пропущено)',
                        marker=dict(
                            color=self.colors['danger'],
                            size=8,
                            symbol='x'
                        ),
                        hovertemplate=f'<b>{indicator} (пропущено)</b><br>' +
                                    'Время: %{x}<br>' +
                                    'Значение: %{y}<br>' +
                                    '<extra></extra>'
                    ),
                    row=i+1, col=1
                )
            
            # Добавляем нормальные диапазоны
            if indicator in time_series.metadata.get('normal_ranges', {}):
                normal_range = time_series.metadata['normal_ranges'][indicator]
                fig.add_hline(
                    y=normal_range[0], 
                    line_dash="dash", 
                    line_color="green",
                    opacity=0.5,
                    row=i+1, col=1
                )
                fig.add_hline(
                    y=normal_range[1], 
                    line_dash="dash", 
                    line_color="green",
                    opacity=0.5,
                    row=i+1, col=1
                )
        
        fig.update_layout(
            title="Медицинские временные ряды - MQEA",
            height=200 * len(indicators),
            showlegend=True,
            template=self.theme,
            hovermode='x unified'
        )
        
        fig.update_xaxes(title_text="Время")
        fig.update_yaxes(title_text="Значение")
        
        return fig
    
    def _plot_static_time_series(self, 
                               time_series: MedicalTimeSeries,
                               indicators: List[str],
                               show_missing: bool) -> go.Figure:
        """Создает статический график временных рядов."""
        fig, axes = plt.subplots(len(indicators), 1, figsize=(12, 3*len(indicators)))
        if len(indicators) == 1:
            axes = [axes]
        
        for i, indicator in enumerate(indicators):
            data = time_series.data[indicator]
            timestamps = time_series.timestamps
            
            # Основная линия данных
            axes[i].plot(timestamps, data, 
                        color=self.colors['primary'], 
                        linewidth=2, 
                        marker='o', 
                        markersize=3,
                        label=indicator)
            
            # Выделение пропущенных данных
            if show_missing and time_series.missing_data_mask[indicator].any():
                missing_data = data[time_series.missing_data_mask[indicator]]
                missing_times = timestamps[time_series.missing_data_mask[indicator]]
                
                axes[i].scatter(missing_times, missing_data,
                              color=self.colors['danger'],
                              marker='x',
                              s=50,
                              label=f'{indicator} (пропущено)')
            
            axes[i].set_title(f'{indicator}')
            axes[i].set_xlabel('Время')
            axes[i].set_ylabel('Значение')
            axes[i].legend()
            axes[i].grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def plot_entanglement_heatmap(self, 
                                 entanglement_matrix: np.ndarray,
                                 indicators: List[str],
                                 title: str = "Матрица квантовой запутанности") -> go.Figure:
        """
        Создает тепловую карту квантовой запутанности между показателями.
        
        Args:
            entanglement_matrix: Матрица запутанности
            indicators: Список названий показателей
            title: Заголовок графика
            
        Returns:
            go.Figure: Тепловая карта запутанности
        """
        fig = go.Figure(data=go.Heatmap(
            z=entanglement_matrix,
            x=indicators,
            y=indicators,
            colorscale='Viridis',
            hovertemplate='<b>%{y} ↔ %{x}</b><br>' +
                         'Запутанность: %{z:.3f}<br>' +
                         '<extra></extra>',
            colorbar=dict(title="Сила запутанности")
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Показатели",
            yaxis_title="Показатели",
            template=self.theme,
            width=600,
            height=600
        )
        
        return fig
    
    def plot_entanglement_network(self, 
                                 entanglement_network: Dict[str, List[str]],
                                 entanglement_strengths: Optional[Dict[Tuple[str, str], float]] = None) -> go.Figure:
        """
        Создает граф сети квантовой запутанности.
        
        Args:
            entanglement_network: Сеть запутанности
            entanglement_strengths: Силы запутанности для рёбер
            
        Returns:
            go.Figure: Граф сети запутанности
        """
        # Подготавливаем данные для графа
        nodes = list(entanglement_network.keys())
        edges = []
        edge_weights = []
        
        for node, connections in entanglement_network.items():
            for connection in connections:
                if (connection, node) not in edges:  # Избегаем дублирования
                    edges.append((node, connection))
                    
                    # Получаем вес рёбра
                    if entanglement_strengths:
                        weight = entanglement_strengths.get((node, connection), 0.5)
                    else:
                        weight = 0.5
                    edge_weights.append(weight)
        
        # Создаем граф
        fig = go.Figure()
        
        # Добавляем рёбра
        for i, (start, end) in enumerate(edges):
            fig.add_trace(go.Scatter(
                x=[start, end],
                y=[0, 0],  # Простая 2D визуализация
                mode='lines',
                line=dict(
                    width=edge_weights[i] * 5,
                    color=self.colors['quantum'],
                    opacity=0.6
                ),
                showlegend=False,
                hoverinfo='skip'
            ))
        
        # Добавляем узлы
        for i, node in enumerate(nodes):
            fig.add_trace(go.Scatter(
                x=[node],
                y=[0],
                mode='markers+text',
                marker=dict(
                    size=30,
                    color=self.colors['primary'],
                    line=dict(width=2, color='white')
                ),
                text=[node],
                textposition="middle center",
                textfont=dict(color="white", size=12),
                name=node,
                hovertemplate=f'<b>{node}</b><br>' +
                             f'Связей: {len(entanglement_network.get(node, []))}<br>' +
                             '<extra></extra>'
            ))
        
        fig.update_layout(
            title="Сеть квантовой запутанности",
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            template=self.theme,
            showlegend=False,
            height=400
        )
        
        return fig
    
    def plot_patterns(self, 
                     time_series: MedicalTimeSeries,
                     patterns: List[TemporalPattern],
                     indicators: Optional[List[str]] = None) -> go.Figure:
        """
        Визуализирует обнаруженные паттерны на временных рядах.
        
        Args:
            time_series: Временной ряд
            patterns: Список обнаруженных паттернов
            indicators: Показатели для отображения
            
        Returns:
            go.Figure: График с выделенными паттернами
        """
        if indicators is None:
            indicators = time_series.indicators
        
        fig = make_subplots(
            rows=len(indicators),
            cols=1,
            subplot_titles=indicators,
            vertical_spacing=0.05
        )
        
        # Цвета для разных типов паттернов
        pattern_colors = {
            'periodic': self.colors['info'],
            'trend_increasing': self.colors['success'],
            'trend_decreasing': self.colors['danger'],
            'anomaly': self.colors['warning'],
            'quantum_entangled': self.colors['quantum']
        }
        
        for i, indicator in enumerate(indicators):
            data = time_series.data[indicator]
            timestamps = time_series.timestamps
            
            # Основная линия данных
            fig.add_trace(
                go.Scatter(
                    x=timestamps,
                    y=data,
                    mode='lines',
                    name=indicator,
                    line=dict(color=self.colors['primary'], width=1),
                    opacity=0.7
                ),
                row=i+1, col=1
            )
            
            # Выделяем паттерны для этого показателя
            for pattern in patterns:
                if indicator in pattern.indicators:
                    pattern_start = pattern.start_time
                    pattern_end = pattern.end_time
                    
                    # Находим индексы паттерна
                    start_idx = timestamps.get_indexer([pattern_start], method='nearest')[0]
                    end_idx = timestamps.get_indexer([pattern_end], method='nearest')[0]
                    
                    if start_idx >= 0 and end_idx >= 0:
                        pattern_data = data.iloc[start_idx:end_idx+1]
                        pattern_times = timestamps[start_idx:end_idx+1]
                        
                        color = pattern_colors.get(pattern.pattern_type, self.colors['secondary'])
                        
                        fig.add_trace(
                            go.Scatter(
                                x=pattern_times,
                                y=pattern_data,
                                mode='lines+markers',
                                name=f'{pattern.pattern_type} ({indicator})',
                                line=dict(color=color, width=3),
                                marker=dict(size=6),
                                hovertemplate=f'<b>{pattern.pattern_type}</b><br>' +
                                            f'Показатель: {indicator}<br>' +
                                            f'Время: %{x}<br>' +
                                            f'Значение: %{y:.2f}<br>' +
                                            f'Уверенность: {pattern.confidence:.3f}<br>' +
                                            '<extra></extra>'
                            ),
                            row=i+1, col=1
                        )
        
        fig.update_layout(
            title="Обнаруженные паттерны в медицинских данных",
            height=200 * len(indicators),
            template=self.theme,
            showlegend=True
        )
        
        return fig
    
    def plot_quantum_analysis_dashboard(self, 
                                      analysis_results: Dict[str, Any],
                                      time_series: MedicalTimeSeries) -> go.Figure:
        """
        Создает дашборд с результатами квантового анализа.
        
        Args:
            analysis_results: Результаты квантового анализа
            time_series: Исходные данные
            
        Returns:
            go.Figure: Дашборд анализа
        """
        # Создаем субплоты
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=[
                "Временные ряды",
                "Матрица запутанности", 
                "Квантовые паттерны",
                "Статистика анализа"
            ],
            specs=[[{"type": "scatter"}, {"type": "heatmap"}],
                   [{"type": "scatter"}, {"type": "bar"}]]
        )
        
        # 1. Временные ряды (упрощенная версия)
        for indicator in time_series.indicators[:3]:  # Показываем только первые 3
            data = time_series.data[indicator]
            fig.add_trace(
                go.Scatter(
                    x=time_series.timestamps,
                    y=data,
                    mode='lines',
                    name=indicator,
                    line=dict(width=1)
                ),
                row=1, col=1
            )
        
        # 2. Матрица запутанности
        if 'quantum_entanglements' in analysis_results and analysis_results['quantum_entanglements']:
            latest_entanglement = analysis_results['quantum_entanglements'][-1]
            entanglement_matrix = np.array(latest_entanglement['entanglement_matrix'])
            
            fig.add_trace(
                go.Heatmap(
                    z=entanglement_matrix,
                    x=time_series.indicators,
                    y=time_series.indicators,
                    colorscale='Viridis',
                    showscale=False
                ),
                row=1, col=2
            )
        
        # 3. Квантовые паттерны (временная линия)
        if 'quantum_patterns' in analysis_results:
            pattern_times = []
            pattern_confidences = []
            
            for pattern in analysis_results['quantum_patterns']:
                start_time = pd.to_datetime(pattern['start_time'])
                end_time = pd.to_datetime(pattern['end_time'])
                pattern_times.append((start_time + end_time) / 2)  # Среднее время
                pattern_confidences.append(pattern['confidence'])
            
            if pattern_times:
                fig.add_trace(
                    go.Scatter(
                        x=pattern_times,
                        y=pattern_confidences,
                        mode='markers',
                        name='Квантовые паттерны',
                        marker=dict(
                            size=10,
                            color=self.colors['quantum'],
                            symbol='diamond'
                        )
                    ),
                    row=2, col=1
                )
        
        # 4. Статистика анализа
        if 'quantum_signatures' in analysis_results:
            signatures = analysis_results['quantum_signatures']
            stats = [
                signatures.get('quantum_coherence', 0),
                signatures.get('entanglement_entropy', 0),
                len(analysis_results.get('quantum_entanglements', [])),
                len(analysis_results.get('quantum_patterns', []))
            ]
            stat_labels = ['Когерентность', 'Энтропия', 'Окна анализа', 'Паттерны']
            
            fig.add_trace(
                go.Bar(
                    x=stat_labels,
                    y=stats,
                    name='Статистика',
                    marker_color=[self.colors['primary'], self.colors['secondary'], 
                                self.colors['success'], self.colors['info']]
                ),
                row=2, col=2
            )
        
        fig.update_layout(
            title="MQEA - Дашборд квантового анализа",
            height=800,
            template=self.theme,
            showlegend=True
        )
        
        return fig
    
    def save_plots(self, 
                  figures: List[go.Figure], 
                  filenames: List[str],
                  format: str = 'html') -> None:
        """
        Сохраняет графики в файлы.
        
        Args:
            figures: Список графиков для сохранения
            filenames: Список имён файлов
            format: Формат сохранения ('html', 'png', 'pdf')
        """
        for fig, filename in zip(figures, filenames):
            if format == 'html':
                fig.write_html(filename)
            elif format == 'png':
                fig.write_image(filename, width=1200, height=800)
            elif format == 'pdf':
                fig.write_image(filename, format='pdf')
            else:
                raise ValueError(f"Неподдерживаемый формат: {format}")
        
        print(f"Графики сохранены в формате {format}")
    
    def create_analysis_report(self, 
                             time_series: MedicalTimeSeries,
                             analysis_results: Dict[str, Any],
                             patterns: List[TemporalPattern],
                             output_file: str = 'mqea_report.html') -> str:
        """
        Создает HTML-отчёт с результатами анализа.
        
        Args:
            time_series: Исходные данные
            analysis_results: Результаты анализа
            patterns: Обнаруженные паттерны
            output_file: Имя файла отчёта
            
        Returns:
            str: Путь к созданному файлу
        """
        # Создаем основные графики
        time_series_fig = self.plot_time_series(time_series, interactive=True)
        
        # Матрица запутанности
        entanglement_fig = None
        if 'quantum_entanglements' in analysis_results and analysis_results['quantum_entanglements']:
            latest_entanglement = analysis_results['quantum_entanglements'][-1]
            entanglement_matrix = np.array(latest_entanglement['entanglement_matrix'])
            entanglement_fig = self.plot_entanglement_heatmap(
                entanglement_matrix, 
                time_series.indicators
            )
        
        # Паттерны
        patterns_fig = self.plot_patterns(time_series, patterns)
        
        # Дашборд
        dashboard_fig = self.plot_quantum_analysis_dashboard(analysis_results, time_series)
        
        # Создаем HTML-отчёт
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>MQEA - Отчёт анализа</title>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #f8f9fa; padding: 20px; border-radius: 5px; }}
                .section {{ margin: 20px 0; }}
                .metric {{ display: inline-block; margin: 10px; padding: 10px; 
                         background-color: #e9ecef; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>MQEA - Medical Quantum Entanglement Analysis</h1>
                <p>Отчёт квантового анализа медицинских данных</p>
                <p>Дата создания: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            
            <div class="section">
                <h2>Общая информация</h2>
                <div class="metric">
                    <strong>Показателей:</strong> {len(time_series.indicators)}
                </div>
                <div class="metric">
                    <strong>Точек данных:</strong> {len(time_series.timestamps)}
                </div>
                <div class="metric">
                    <strong>Пропущенных данных:</strong> {time_series.metadata.get('missing_percentage', 0):.1f}%
                </div>
            </div>
            
            <div class="section">
                <h2>Временные ряды</h2>
                {time_series_fig.to_html(include_plotlyjs='cdn', div_id="time_series")}
            </div>
        """
        
        if entanglement_fig:
            html_content += f"""
            <div class="section">
                <h2>Матрица квантовой запутанности</h2>
                {entanglement_fig.to_html(include_plotlyjs=False, div_id="entanglement")}
            </div>
            """
        
        html_content += f"""
            <div class="section">
                <h2>Обнаруженные паттерны</h2>
                {patterns_fig.to_html(include_plotlyjs=False, div_id="patterns")}
            </div>
            
            <div class="section">
                <h2>Дашборд анализа</h2>
                {dashboard_fig.to_html(include_plotlyjs=False, div_id="dashboard")}
            </div>
            
            <div class="section">
                <h2>Квантовые характеристики</h2>
        """
        
        if 'quantum_signatures' in analysis_results:
            signatures = analysis_results['quantum_signatures']
            html_content += f"""
                <div class="metric">
                    <strong>Квантовая когерентность:</strong> {signatures.get('quantum_coherence', 0):.3f}
                </div>
                <div class="metric">
                    <strong>Энтропия запутанности:</strong> {signatures.get('entanglement_entropy', 0):.3f}
                </div>
                <div class="metric">
                    <strong>Квантовых состояний:</strong> {signatures.get('total_quantum_states', 0)}
                </div>
            """
        
        html_content += """
            </div>
        </body>
        </html>
        """
        
        # Сохраняем отчёт
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Отчёт сохранён в файл: {output_file}")
        return output_file

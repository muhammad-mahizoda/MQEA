"""
Продвинутый пример использования MQEA.

Демонстрирует расширенные возможности:
- Работа с реальными медицинскими данными
- Настройка параметров квантового анализа
- Сравнение различных методов заполнения пропусков
- Детальный анализ квантовых паттернов
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mqea import MQEAAnalyzer, MQEAVisualizer
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt


def create_realistic_medical_data():
    """
    Создает более реалистичные медицинские данные
    с корреляциями между показателями.
    """
    print("Создание реалистичных медицинских данных...")
    
    # Параметры данных
    duration_hours = 72  # 3 дня
    sampling_rate_minutes = 10  # Каждые 10 минут
    n_points = duration_hours * 60 // sampling_rate_minutes
    
    # Создаем временные метки
    start_time = datetime.now() - timedelta(hours=duration_hours)
    timestamps = pd.date_range(start=start_time, periods=n_points, freq=f'{sampling_rate_minutes}T')
    
    # Базовые параметры для каждого показателя
    indicators_config = {
        'heart_rate': {'base': 75, 'std': 10, 'trend': 0.1},
        'blood_pressure_systolic': {'base': 120, 'std': 15, 'trend': 0.05},
        'blood_pressure_diastolic': {'base': 80, 'std': 10, 'trend': 0.03},
        'temperature': {'base': 36.5, 'std': 0.3, 'trend': 0.001},
        'oxygen_saturation': {'base': 98, 'std': 1, 'trend': -0.01},
        'respiratory_rate': {'base': 16, 'std': 2, 'trend': 0.02}
    }
    
    data = {}
    
    # Генерируем данные с корреляциями
    for indicator, config in indicators_config.items():
        # Базовый сигнал
        base_signal = np.random.normal(config['base'], config['std'], n_points)
        
        # Тренд
        trend = np.linspace(0, config['trend'] * n_points, n_points)
        
        # Суточные циклы
        daily_cycle = 5 * np.sin(2 * np.pi * np.arange(n_points) / (24 * 60 // sampling_rate_minutes))
        
        # Случайные события (например, стресс, физическая активность)
        events = np.random.poisson(0.1, n_points) * np.random.normal(0, 10, n_points)
        
        # Комбинируем все компоненты
        values = base_signal + trend + daily_cycle + events
        
        # Ограничиваем значения разумными пределами
        if indicator == 'heart_rate':
            values = np.clip(values, 40, 200)
        elif indicator in ['blood_pressure_systolic', 'blood_pressure_diastolic']:
            values = np.clip(values, 60, 200)
        elif indicator == 'temperature':
            values = np.clip(values, 35, 42)
        elif indicator == 'oxygen_saturation':
            values = np.clip(values, 85, 100)
        elif indicator == 'respiratory_rate':
            values = np.clip(values, 8, 30)
        
        data[indicator] = values
    
    # Добавляем корреляции между показателями
    # Сердечный ритм влияет на давление
    data['blood_pressure_systolic'] += 0.3 * (data['heart_rate'] - 75)
    data['blood_pressure_diastolic'] += 0.2 * (data['heart_rate'] - 75)
    
    # Температура влияет на сердечный ритм
    data['heart_rate'] += 2 * (data['temperature'] - 36.5)
    
    # Кислородное насыщение обратно коррелирует с частотой дыхания
    data['respiratory_rate'] -= 0.1 * (data['oxygen_saturation'] - 98)
    
    # Создаем DataFrame
    df = pd.DataFrame(data, index=timestamps)
    
    # Добавляем пропущенные данные (имитируем реальные условия)
    missing_percentage = 0.08  # 8% пропущенных данных
    for indicator in df.columns:
        missing_indices = np.random.choice(
            len(df), 
            size=int(len(df) * missing_percentage), 
            replace=False
        )
        df.loc[df.index[missing_indices], indicator] = np.nan
    
    # Сохраняем данные
    df.to_csv('examples/data/realistic_medical_data.csv')
    print(f"Данные сохранены в examples/data/realistic_medical_data.csv")
    print(f"  - Показателей: {len(df.columns)}")
    print(f"  - Точек данных: {len(df)}")
    print(f"  - Пропущенных данных: {df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100:.1f}%")
    
    return df


def compare_imputation_methods(analyzer, time_series):
    """Сравнивает различные методы заполнения пропущенных данных."""
    print("\nСравнение методов заполнения пропущенных данных...")
    
    methods = ['quantum', 'linear', 'mean']
    results = {}
    
    for method in methods:
        print(f"  Тестируем метод: {method}")
        
        # Заполняем данные
        filled_data = analyzer.fill_missing_data(
            time_series=time_series,
            method=method,
            max_iterations=30
        )
        
        # Вычисляем метрики качества
        original_data = time_series.data
        filled_data_values = filled_data.data
        
        # MSE для непустых значений
        mse = 0
        count = 0
        
        for indicator in time_series.indicators:
            mask = ~time_series.missing_data_mask[indicator]
            if mask.any():
                mse += np.mean((original_data[indicator][mask] - filled_data_values[indicator][mask]) ** 2)
                count += 1
        
        mse = mse / count if count > 0 else 0
        
        results[method] = {
            'mse': mse,
            'iterations': filled_data.metadata.get('quantum_imputation_iterations', 1),
            'convergence': filled_data.metadata.get('final_convergence', 0)
        }
        
        print(f"    MSE: {mse:.6f}")
        if method == 'quantum':
            print(f"    Итераций: {results[method]['iterations']}")
            print(f"    Сходимость: {results[method]['convergence']:.6f}")
    
    return results


def analyze_quantum_patterns(analyzer, time_series):
    """Детальный анализ квантовых паттернов."""
    print("\nДетальный анализ квантовых паттернов...")
    
    # Выполняем квантовый анализ с разными порогами
    thresholds = [0.2, 0.3, 0.4, 0.5, 0.6]
    pattern_analysis = {}
    
    for threshold in thresholds:
        print(f"  Анализ с порогом запутанности: {threshold}")
        
        # Квантовый анализ
        quantum_results = analyzer.quantum_entanglement_analysis(
            time_series=time_series,
            quantum_threshold=threshold
        )
        
        # Обнаружение паттернов
        patterns = analyzer.detect_patterns(time_series=time_series)
        
        # Анализируем квантовые паттерны
        quantum_patterns = [p for p in patterns if p.pattern_type == 'quantum_entangled']
        
        pattern_analysis[threshold] = {
            'total_patterns': len(patterns),
            'quantum_patterns': len(quantum_patterns),
            'quantum_coherence': quantum_results['quantum_signatures']['quantum_coherence'],
            'entanglement_entropy': quantum_results['quantum_signatures']['entanglement_entropy'],
            'max_entanglement': max([w['max_entanglement'] for w in quantum_results['quantum_entanglements']]) if quantum_results['quantum_entanglements'] else 0
        }
        
        print(f"    Всего паттернов: {len(patterns)}")
        print(f"    Квантовых паттернов: {len(quantum_patterns)}")
        print(f"    Когерентность: {pattern_analysis[threshold]['quantum_coherence']:.3f}")
    
    return pattern_analysis


def create_comparison_visualizations(imputation_results, pattern_analysis, visualizer):
    """Создает графики для сравнения результатов."""
    print("\nСоздание сравнительных визуализаций...")
    
    # 1. Сравнение методов заполнения
    methods = list(imputation_results.keys())
    mse_values = [imputation_results[method]['mse'] for method in methods]
    
    fig1 = go.Figure(data=[
        go.Bar(x=methods, y=mse_values, 
               marker_color=['#1f77b4', '#ff7f0e', '#2ca02c'],
               text=[f'{mse:.6f}' for mse in mse_values],
               textposition='auto')
    ])
    
    fig1.update_layout(
        title="Сравнение методов заполнения пропущенных данных",
        xaxis_title="Метод",
        yaxis_title="Среднеквадратичная ошибка (MSE)",
        template="plotly_white"
    )
    
    # 2. Анализ квантовых паттернов по порогам
    thresholds = list(pattern_analysis.keys())
    quantum_patterns = [pattern_analysis[t]['quantum_patterns'] for t in thresholds]
    coherence = [pattern_analysis[t]['quantum_coherence'] for t in thresholds]
    
    fig2 = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig2.add_trace(
        go.Scatter(x=thresholds, y=quantum_patterns, 
                  mode='lines+markers', name='Квантовые паттерны',
                  line=dict(color='#e74c3c', width=3)),
        secondary_y=False
    )
    
    fig2.add_trace(
        go.Scatter(x=thresholds, y=coherence, 
                  mode='lines+markers', name='Когерентность',
                  line=dict(color='#8e44ad', width=3)),
        secondary_y=True
    )
    
    fig2.update_xaxes(title_text="Порог запутанности")
    fig2.update_yaxes(title_text="Количество квантовых паттернов", secondary_y=False)
    fig2.update_yaxes(title_text="Квантовая когерентность", secondary_y=True)
    fig2.update_layout(title="Анализ квантовых паттернов по порогам")
    
    # Сохраняем графики
    os.makedirs('examples/output', exist_ok=True)
    
    fig1.write_html('examples/output/imputation_comparison.html')
    fig2.write_html('examples/output/quantum_patterns_analysis.html')
    
    print("  Графики сохранены:")
    print("    - examples/output/imputation_comparison.html")
    print("    - examples/output/quantum_patterns_analysis.html")


def main():
    """Основная функция продвинутого анализа."""
    print("=" * 70)
    print("MQEA - Продвинутый анализ медицинских данных")
    print("=" * 70)
    
    # Создаем директории
    os.makedirs('examples/data', exist_ok=True)
    os.makedirs('examples/output', exist_ok=True)
    
    # 1. Создание реалистичных данных
    medical_data = create_realistic_medical_data()
    
    # 2. Инициализация анализатора
    print("\nИнициализация MQEA анализатора...")
    analyzer = MQEAAnalyzer(
        quantum_hbar=1.0,
        enable_quantum_imputation=True,
        enable_pattern_detection=True
    )
    
    # 3. Загрузка данных
    print("\nЗагрузка медицинских данных...")
    time_series = analyzer.load_medical_data(
        'examples/data/realistic_medical_data.csv',
        time_column='timestamp'
    )
    
    # 4. Сравнение методов заполнения
    imputation_results = compare_imputation_methods(analyzer, time_series)
    
    # 5. Анализ квантовых паттернов
    pattern_analysis = analyze_quantum_patterns(analyzer, time_series)
    
    # 6. Создание визуализаций
    visualizer = MQEAVisualizer()
    create_comparison_visualizations(imputation_results, pattern_analysis, visualizer)
    
    # 7. Финальный анализ с оптимальными параметрами
    print("\nФинальный анализ с оптимальными параметрами...")
    
    # Выбираем оптимальный порог на основе анализа
    best_threshold = max(pattern_analysis.keys(), 
                        key=lambda t: pattern_analysis[t]['quantum_coherence'])
    
    print(f"Оптимальный порог запутанности: {best_threshold}")
    
    # Выполняем финальный анализ
    final_quantum_results = analyzer.quantum_entanglement_analysis(
        time_series=time_series,
        quantum_threshold=best_threshold
    )
    
    # Заполняем данные квантовым методом
    final_filled_data = analyzer.fill_missing_data(
        time_series=time_series,
        method='quantum',
        max_iterations=50
    )
    
    # Обнаруживаем паттерны
    final_patterns = analyzer.detect_patterns(time_series=final_filled_data)
    
    # 8. Создание финального отчёта
    print("\nСоздание финального отчёта...")
    final_report = visualizer.create_analysis_report(
        final_filled_data, 
        final_quantum_results, 
        final_patterns,
        'examples/output/advanced_analysis_report.html'
    )
    
    # 9. Сводка результатов
    print("\n" + "=" * 70)
    print("СВОДКА ПРОДВИНУТОГО АНАЛИЗА")
    print("=" * 70)
    
    print(f"\nСравнение методов заполнения:")
    for method, results in imputation_results.items():
        print(f"  {method}: MSE = {results['mse']:.6f}")
    
    print(f"\nАнализ квантовых паттернов:")
    print(f"  Оптимальный порог: {best_threshold}")
    print(f"  Лучшая когерентность: {pattern_analysis[best_threshold]['quantum_coherence']:.3f}")
    print(f"  Квантовых паттернов: {pattern_analysis[best_threshold]['quantum_patterns']}")
    
    print(f"\nФинальные результаты:")
    summary = analyzer.get_analysis_summary()
    print(f"  - Всего паттернов: {summary['patterns_detected']['total_patterns']}")
    print(f"  - Квантовая когерентность: {summary['quantum_analysis']['quantum_coherence']:.3f}")
    print(f"  - Энтропия запутанности: {summary['quantum_analysis']['entanglement_entropy']:.3f}")
    
    print(f"\nФайлы результатов:")
    print(f"  - Финальный отчёт: {final_report}")
    print(f"  - Сравнительные графики: examples/output/")
    
    print("\n" + "=" * 70)
    print("Продвинутый анализ MQEA завершён успешно!")
    print("=" * 70)


if __name__ == "__main__":
    # Импорты для Plotly
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    
    main()

"""
Базовый пример использования MQEA.

Демонстрирует основные возможности системы:
- Генерация синтетических медицинских данных
- Квантовый анализ запутанности
- Заполнение пропущенных данных
- Обнаружение паттернов
- Визуализация результатов
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mqea import MQEAAnalyzer
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def main():
    """Основная функция демонстрации MQEA."""
    print("=" * 60)
    print("MQEA - Medical Quantum Entanglement Analysis")
    print("Демонстрация базовых возможностей")
    print("=" * 60)
    
    # 1. Инициализация анализатора
    print("\n1. Инициализация MQEA анализатора...")
    analyzer = MQEAAnalyzer(
        quantum_hbar=1.0,
        enable_quantum_imputation=True,
        enable_pattern_detection=True
    )
    
    # 2. Генерация синтетических медицинских данных
    print("\n2. Генерация синтетических медицинских данных...")
    time_series = analyzer.generate_synthetic_data(
        duration_hours=48,  # 48 часов данных
        sampling_rate_minutes=15,  # Каждые 15 минут
        add_noise=True,
        add_missing_data=True
    )
    
    print(f"Сгенерировано данных:")
    print(f"  - Показателей: {len(time_series.indicators)}")
    print(f"  - Временных точек: {len(time_series.timestamps)}")
    print(f"  - Пропущенных данных: {time_series.metadata['missing_percentage']:.1f}%")
    
    # 3. Квантовый анализ запутанности
    print("\n3. Выполнение квантового анализа запутанности...")
    quantum_results = analyzer.quantum_entanglement_analysis(
        time_series=time_series,
        quantum_threshold=0.3,
        time_windows=[12, 24, 48]  # Анализ в окнах 12, 24 и 48 часов
    )
    
    print("Результаты квантового анализа:")
    print(f"  - Окон анализа: {len(quantum_results['quantum_entanglements'])}")
    print(f"  - Квантовая когерентность: {quantum_results['quantum_signatures']['quantum_coherence']:.3f}")
    print(f"  - Энтропия запутанности: {quantum_results['quantum_signatures']['entanglement_entropy']:.3f}")
    
    # 4. Заполнение пропущенных данных
    print("\n4. Заполнение пропущенных данных квантовым методом...")
    filled_data = analyzer.fill_missing_data(
        time_series=time_series,
        method='quantum',
        max_iterations=50
    )
    
    print(f"Заполнение завершено:")
    print(f"  - Итераций: {filled_data.metadata.get('quantum_imputation_iterations', 'N/A')}")
    print(f"  - Сходимость: {filled_data.metadata.get('final_convergence', 'N/A'):.6f}")
    
    # 5. Обнаружение паттернов
    print("\n5. Обнаружение паттернов в данных...")
    patterns = analyzer.detect_patterns(time_series=filled_data)
    
    print(f"Найдено паттернов: {len(patterns)}")
    for i, pattern in enumerate(patterns):
        print(f"  {i+1}. {pattern.pattern_type}: {pattern.indicators} "
              f"(уверенность: {pattern.confidence:.3f})")
    
    # 6. Создание визуализаций
    print("\n6. Создание визуализаций...")
    from mqea import MQEAVisualizer
    
    visualizer = MQEAVisualizer()
    
    # График временных рядов
    time_series_fig = visualizer.plot_time_series(
        filled_data, 
        indicators=filled_data.indicators[:4],  # Первые 4 показателя
        show_missing=True,
        interactive=True
    )
    
    # Матрица запутанности
    if quantum_results['quantum_entanglements']:
        latest_entanglement = quantum_results['quantum_entanglements'][-1]
        entanglement_matrix = np.array(latest_entanglement['entanglement_matrix'])
        
        entanglement_fig = visualizer.plot_entanglement_heatmap(
            entanglement_matrix,
            filled_data.indicators,
            "Матрица квантовой запутанности"
        )
    
    # График паттернов
    patterns_fig = visualizer.plot_patterns(filled_data, patterns)
    
    # Дашборд анализа
    dashboard_fig = visualizer.plot_quantum_analysis_dashboard(
        quantum_results, filled_data
    )
    
    # 7. Сохранение результатов
    print("\n7. Сохранение результатов...")
    
    # Сохраняем графики
    figures = [time_series_fig, entanglement_fig, patterns_fig, dashboard_fig]
    filenames = [
        'examples/output/time_series.html',
        'examples/output/entanglement_heatmap.html', 
        'examples/output/patterns.html',
        'examples/output/dashboard.html'
    ]
    
    # Создаем директорию для выходных файлов
    os.makedirs('examples/output', exist_ok=True)
    
    visualizer.save_plots(figures, filenames, format='html')
    
    # Создаем HTML-отчёт
    report_file = visualizer.create_analysis_report(
        filled_data, quantum_results, patterns, 'examples/output/mqea_report.html'
    )
    
    # 8. Сводка результатов
    print("\n8. Сводка результатов анализа...")
    summary = analyzer.get_analysis_summary()
    
    print("\n" + "=" * 60)
    print("СВОДКА АНАЛИЗА MQEA")
    print("=" * 60)
    print(f"Данные:")
    print(f"  - Показателей: {summary['data_info']['indicators']}")
    print(f"  - Точек данных: {summary['data_info']['data_points']}")
    print(f"  - Пропущенных данных: {summary['data_info']['missing_percentage']:.1f}%")
    
    print(f"\nКвантовый анализ:")
    print(f"  - Окон анализа: {summary['quantum_analysis']['total_entanglements']}")
    print(f"  - Когерентность: {summary['quantum_analysis']['quantum_coherence']:.3f}")
    print(f"  - Энтропия: {summary['quantum_analysis']['entanglement_entropy']:.3f}")
    
    print(f"\nПаттерны:")
    print(f"  - Всего паттернов: {summary['patterns_detected']['total_patterns']}")
    print(f"  - Типы паттернов: {summary['patterns_detected']['pattern_types']}")
    print(f"  - Квантовых паттернов: {summary['patterns_detected']['quantum_patterns']}")
    
    print(f"\nФайлы результатов:")
    print(f"  - Отчёт: {report_file}")
    print(f"  - Графики: examples/output/")
    
    print("\n" + "=" * 60)
    print("Демонстрация MQEA завершена успешно!")
    print("=" * 60)


if __name__ == "__main__":
    main()

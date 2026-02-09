"""
Современная демонстрация MQEA алгоритма.

Автор: Мухаммад Махизода
Таджикский национальный университет
"""

import sys
import os
import time
from datetime import datetime

# Добавляем путь к модулям
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def print_banner():
    """Выводит современный баннер."""
    banner = """
    ╔══════════════════════════════════════════════════════════════════════════════╗
    ║                                                                              ║
    ║    🧬 MQEA - Medical Quantum Entanglement Analysis                          ║
    ║                                                                              ║
    ║    Революционный алгоритм для анализа медицинских данных                    ║
    ║    на основе принципов квантовой запутанности                               ║
    ║                                                                              ║
    ║    Основатель: Мухаммад Махизода                                            ║
    ║    Таджикский национальный университет                                      ║
    ║                                                                              ║
    ║    🚀 Современная версия с веб-интерфейсом                                  ║
    ║                                                                              ║
    ╚══════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def demo_quantum_analysis():
    """Демонстрация квантового анализа."""
    print("\n🔬 ДЕМОНСТРАЦИЯ КВАНТОВОГО АНАЛИЗА")
    print("=" * 50)
    
    try:
        from mqea import MQEAAnalyzer, MQEAVisualizer
        import pandas as pd
        import numpy as np
        
        print("📊 Генерация тестовых медицинских данных...")
        
        # Инициализация анализатора
        analyzer = MQEAAnalyzer()
        
        # Генерация синтетических данных
        time_series = analyzer.generate_synthetic_data(
            duration_hours=12,
            sampling_rate_minutes=30,
            add_noise=True,
            add_missing_data=True
        )
        
        print(f"✅ Сгенерировано данных:")
        print(f"   - Показателей: {len(time_series.indicators)}")
        print(f"   - Точек данных: {len(time_series.timestamps)}")
        print(f"   - Пропущенных данных: {time_series.metadata['missing_percentage']:.1f}%")
        
        print("\n🔬 Выполнение квантового анализа запутанности...")
        start_time = time.time()
        
        # Квантовый анализ
        quantum_results = analyzer.quantum_entanglement_analysis(
            time_series=time_series,
            quantum_threshold=0.5
        )
        
        analysis_time = time.time() - start_time
        
        print(f"✅ Анализ завершен за {analysis_time:.2f} секунд")
        
        # Результаты анализа
        print("\n📈 РЕЗУЛЬТАТЫ КВАНТОВОГО АНАЛИЗА:")
        print("-" * 40)
        
        signatures = quantum_results['quantum_signatures']
        print(f"🔹 Квантовая когерентность: {signatures['quantum_coherence']:.4f}")
        print(f"🔹 Энтропия запутанности: {signatures['entanglement_entropy']:.4f}")
        print(f"🔹 Всего квантовых состояний: {signatures['total_quantum_states']}")
        print(f"🔹 Средняя запутанность: {signatures['average_entanglement']:.4f}")
        
        # Заполнение пропущенных данных
        print("\n🔧 Заполнение пропущенных данных квантовым методом...")
        start_time = time.time()
        
        filled_data = analyzer.fill_missing_data(
            time_series=time_series,
            method='quantum',
            max_iterations=50
        )
        
        imputation_time = time.time() - start_time
        
        print(f"✅ Заполнение завершено за {imputation_time:.2f} секунд")
        
        # Обнаружение паттернов
        print("\n🔍 Обнаружение квантовых паттернов...")
        start_time = time.time()
        
        patterns = analyzer.detect_patterns(time_series=filled_data)
        
        detection_time = time.time() - start_time
        
        print(f"✅ Обнаружено {len(patterns)} паттернов за {detection_time:.2f} секунд")
        
        # Статистика паттернов
        if patterns:
            print("\n📊 СТАТИСТИКА ПАТТЕРНОВ:")
            print("-" * 30)
            pattern_types = {}
            for pattern in patterns:
                pattern_type = pattern.pattern_type
                pattern_types[pattern_type] = pattern_types.get(pattern_type, 0) + 1
            
            for pattern_type, count in pattern_types.items():
                print(f"🔸 {pattern_type.replace('_', ' ').title()}: {count}")
        
        # Сводка анализа
        print("\n📋 СВОДКА АНАЛИЗА:")
        print("-" * 25)
        summary = analyzer.get_analysis_summary()
        print(f"🔹 Общее время анализа: {summary['total_analysis_time']:.2f} сек")
        print(f"🔹 Обработано точек данных: {summary['total_data_points']}")
        print(f"🔹 Найдено запутанностей: {summary['total_entanglements']}")
        print(f"🔹 Обнаружено паттернов: {summary['total_patterns']}")
        
        print("\n🎉 ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА УСПЕШНО!")
        print("🌐 Для интерактивной работы откройте: http://localhost:8501")
        
        return True
        
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        print("💡 Установите зависимости: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Ошибка выполнения: {e}")
        return False

def show_system_info():
    """Показывает информацию о системе."""
    print("\nℹ️ ИНФОРМАЦИЯ О СИСТЕМЕ")
    print("=" * 30)
    print(f"🔹 Основатель: Мухаммад Махизода")
    print(f"🔹 Должность: Администратор сети")
    print(f"🔹 Университет: Таджикский национальный университет")
    print(f"🔹 Email: muhammad.mahizoda@tnu.tj")
    print(f"🔹 Версия MQEA: 1.0.0")
    print(f"🔹 Дата: {datetime.now().strftime('%d.%m.%Y %H:%M')}")

def main():
    """Основная функция."""
    print_banner()
    
    print("\n🚀 Запуск современной демонстрации MQEA...")
    
    # Информация о системе
    show_system_info()
    
    # Демонстрация алгоритма
    success = demo_quantum_analysis()
    
    if success:
        print("\n" + "="*60)
        print("🎯 СЛЕДУЮЩИЕ ШАГИ:")
        print("="*60)
        print("1. 🌐 Откройте веб-интерфейс: http://localhost:8501")
        print("2. 🔌 Используйте API: http://localhost:8000/docs")
        print("3. 📚 Изучите документацию в папке docs/")
        print("4. 🐳 Запустите полную систему: docker-compose up")
        print("\n💡 Для остановки веб-интерфейса нажмите Ctrl+C")
    else:
        print("\n❌ Демонстрация завершилась с ошибками")
        print("💡 Проверьте установку зависимостей")

if __name__ == "__main__":
    main()

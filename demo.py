"""
Демонстрационный скрипт MQEA.

Запускает полную демонстрацию возможностей системы
Medical Quantum Entanglement Analysis.
"""

import os
import sys
from datetime import datetime

# Добавляем текущую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mqea import MQEAAnalyzer, MQEAVisualizer


def print_banner():
    """Выводит баннер MQEA."""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║    MQEA - Medical Quantum Entanglement Analysis             ║
    ║                                                              ║
    ║    Революционный алгоритм для анализа медицинских данных    ║
    ║    на основе принципов квантовой запутанности               ║
    ║                                                              ║
    ║    Основатель: Мухаммад Махизода                            ║
    ║    Таджикский национальный университет                      ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def run_basic_demo():
    """Запускает базовую демонстрацию."""
    print("\n" + "="*60)
    print("БАЗОВАЯ ДЕМОНСТРАЦИЯ MQEA")
    print("="*60)
    
    try:
        # Импортируем и запускаем базовый пример
        from examples.basic_usage import main as basic_main
        basic_main()
        return True
    except Exception as e:
        print(f"Ошибка в базовой демонстрации: {e}")
        return False


def run_advanced_demo():
    """Запускает продвинутую демонстрацию."""
    print("\n" + "="*60)
    print("ПРОДВИНУТАЯ ДЕМОНСТРАЦИЯ MQEA")
    print("="*60)
    
    try:
        # Импортируем и запускаем продвинутый пример
        from examples.advanced_analysis import main as advanced_main
        advanced_main()
        return True
    except Exception as e:
        print(f"Ошибка в продвинутой демонстрации: {e}")
        return False


def run_quick_test():
    """Запускает быстрый тест системы."""
    print("\n" + "="*60)
    print("БЫСТРЫЙ ТЕСТ СИСТЕМЫ MQEA")
    print("="*60)
    
    try:
        # Инициализация
        print("1. Инициализация MQEA...")
        analyzer = MQEAAnalyzer()
        
        # Генерация данных
        print("2. Генерация тестовых данных...")
        time_series = analyzer.generate_synthetic_data(
            duration_hours=6,
            sampling_rate_minutes=30,
            add_missing_data=True
        )
        
        print(f"   - Показателей: {len(time_series.indicators)}")
        print(f"   - Точек данных: {len(time_series.timestamps)}")
        print(f"   - Пропущенных данных: {time_series.metadata['missing_percentage']:.1f}%")
        
        # Квантовый анализ
        print("3. Квантовый анализ запутанности...")
        quantum_results = analyzer.quantum_entanglement_analysis(
            time_series, quantum_threshold=0.3
        )
        
        print(f"   - Квантовая когерентность: {quantum_results['quantum_signatures']['quantum_coherence']:.3f}")
        print(f"   - Энтропия запутанности: {quantum_results['quantum_signatures']['entanglement_entropy']:.3f}")
        
        # Заполнение пропусков
        print("4. Заполнение пропущенных данных...")
        filled_data = analyzer.fill_missing_data(time_series, method='quantum')
        
        print(f"   - Итераций: {filled_data.metadata.get('quantum_imputation_iterations', 'N/A')}")
        print(f"   - Сходимость: {filled_data.metadata.get('final_convergence', 'N/A'):.6f}")
        
        # Обнаружение паттернов
        print("5. Обнаружение паттернов...")
        patterns = analyzer.detect_patterns(filled_data)
        
        print(f"   - Найдено паттернов: {len(patterns)}")
        for i, pattern in enumerate(patterns[:3]):  # Показываем первые 3
            print(f"     {i+1}. {pattern.pattern_type}: {pattern.indicators} "
                  f"(уверенность: {pattern.confidence:.3f})")
        
        # Сводка
        print("6. Сводка результатов...")
        summary = analyzer.get_analysis_summary()
        
        print(f"   - Всего паттернов: {summary['patterns_detected']['total_patterns']}")
        print(f"   - Квантовых паттернов: {summary['patterns_detected']['quantum_patterns']}")
        
        print("\n✅ Быстрый тест завершён успешно!")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка в быстром тесте: {e}")
        return False


def run_tests():
    """Запускает тесты системы."""
    print("\n" + "="*60)
    print("ТЕСТИРОВАНИЕ СИСТЕМЫ MQEA")
    print("="*60)
    
    try:
        from tests.test_mqea import run_tests
        success = run_tests()
        
        if success:
            print("\n✅ Все тесты пройдены успешно!")
        else:
            print("\n❌ Некоторые тесты не прошли!")
        
        return success
        
    except Exception as e:
        print(f"❌ Ошибка при запуске тестов: {e}")
        return False


def show_menu():
    """Показывает меню выбора."""
    menu = """
    Выберите действие:
    
    1. Быстрый тест системы (рекомендуется для начала)
    2. Базовая демонстрация
    3. Продвинутая демонстрация  
    4. Запуск тестов
    5. Показать информацию о системе
    6. Выход
    
    Введите номер (1-6): """
    
    return input(menu).strip()


def show_system_info():
    """Показывает информацию о системе."""
    print("\n" + "="*60)
    print("ИНФОРМАЦИЯ О СИСТЕМЕ MQEA")
    print("="*60)
    
    print(f"Версия: 1.0.0")
    print(f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python: {sys.version}")
    
    print(f"\nОснователь и разработчик:")
    print(f"  - Имя: Мухаммад Махизода")
    print(f"  - Должность: Администратор сети")
    print(f"  - Университет: Таджикский национальный университет")
    print(f"  - Email: muhammad.mahizoda@tnu.tj")
    
    print(f"\nОсновные компоненты:")
    print(f"  - QuantumEntanglementEngine: Движок квантовой запутанности")
    print(f"  - MedicalDataProcessor: Обработка медицинских данных")
    print(f"  - MQEAAnalyzer: Основной анализатор")
    print(f"  - MQEAVisualizer: Система визуализации")
    
    print(f"\nУникальные возможности:")
    print(f"  - Квантовая запутанность между медицинскими показателями")
    print(f"  - Заполнение пропусков на основе квантовых принципов")
    print(f"  - Обнаружение квантово-запутанных паттернов")
    print(f"  - Анализ временной неопределенности")
    print(f"  - Интерактивная визуализация результатов")
    
    print(f"\nПоддерживаемые показатели:")
    indicators = [
        "heart_rate", "blood_pressure_systolic", "blood_pressure_diastolic",
        "temperature", "oxygen_saturation", "respiratory_rate", 
        "glucose", "cholesterol"
    ]
    for indicator in indicators:
        print(f"  - {indicator}")
    
    print(f"\nФайлы проекта:")
    print(f"  - examples/basic_usage.py: Базовая демонстрация")
    print(f"  - examples/advanced_analysis.py: Продвинутый анализ")
    print(f"  - tests/test_mqea.py: Тесты системы")
    print(f"  - README.md: Документация")


def main():
    """Основная функция демонстрации."""
    print_banner()
    
    print(f"Добро пожаловать в MQEA!")
    print(f"Революционный алгоритм для анализа медицинских данных")
    print(f"на основе принципов квантовой запутанности.")
    
    while True:
        try:
            choice = show_menu()
            
            if choice == '1':
                success = run_quick_test()
                if not success:
                    print("\n⚠️  Быстрый тест завершился с ошибками")
                    
            elif choice == '2':
                success = run_basic_demo()
                if not success:
                    print("\n⚠️  Базовая демонстрация завершилась с ошибками")
                    
            elif choice == '3':
                success = run_advanced_demo()
                if not success:
                    print("\n⚠️  Продвинутая демонстрация завершилась с ошибками")
                    
            elif choice == '4':
                success = run_tests()
                if not success:
                    print("\n⚠️  Тестирование завершилось с ошибками")
                    
            elif choice == '5':
                show_system_info()
                
            elif choice == '6':
                print("\n👋 До свидания! Спасибо за использование MQEA!")
                break
                
            else:
                print("\n❌ Неверный выбор. Пожалуйста, введите число от 1 до 6.")
            
            if choice in ['1', '2', '3', '4']:
                input("\nНажмите Enter для продолжения...")
                
        except KeyboardInterrupt:
            print("\n\n👋 Программа прервана пользователем. До свидания!")
            break
        except Exception as e:
            print(f"\n❌ Неожиданная ошибка: {e}")
            input("Нажмите Enter для продолжения...")


if __name__ == "__main__":
    main()

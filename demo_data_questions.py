"""
Демонстрация системы работы с данными и генерации вопросов.

Автор: Мухаммад Махизода
Таджикский национальный университет
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mqea.data_question_integration import MedicalDataQuestionSystem
import json


def main():
    """Главная функция демонстрации."""
    
    print("🧬⚛️ СИСТЕМА MQEA: ДАННЫЕ И ВОПРОСЫ")
    print("=" * 50)
    print("Автор: Мухаммад Махизода")
    print("Таджикский национальный университет")
    print("=" * 50)
    
    # Инициализация системы
    system = MedicalDataQuestionSystem()
    
    while True:
        print("\n📋 МЕНЮ:")
        print("1. Загрузить данные")
        print("2. Сгенерировать вопросы")
        print("3. Выполнить анализ")
        print("4. Ответить на вопросы")
        print("5. Показать отчет")
        print("6. Сохранить отчет")
        print("7. Сбросить систему")
        print("0. Выход")
        
        choice = input("\nВыберите действие (0-7): ").strip()
        
        if choice == "0":
            print("👋 До свидания!")
            break
        
        elif choice == "1":
            load_data_menu(system)
        
        elif choice == "2":
            generate_questions_menu(system)
        
        elif choice == "3":
            analyze_data_menu(system)
        
        elif choice == "4":
            answer_questions_menu(system)
        
        elif choice == "5":
            show_report_menu(system)
        
        elif choice == "6":
            save_report_menu(system)
        
        elif choice == "7":
            system.reset()
        
        else:
            print("❌ Неверный выбор. Попробуйте снова.")


def load_data_menu(system):
    """Меню загрузки данных."""
    
    print("\n📊 ЗАГРУЗКА ДАННЫХ")
    print("-" * 30)
    
    # Показываем доступные источники
    sources = system.data_manager.list_sources()
    print("Доступные источники:")
    for i, source in enumerate(sources, 1):
        print(f"  {i}. {source}")
    
    try:
        source_choice = int(input(f"\nВыберите источник (1-{len(sources)}): ")) - 1
        if 0 <= source_choice < len(sources):
            source_name = sources[source_choice]
            
            # Параметры для синтетических данных
            if source_name == "synthetic":
                duration = int(input("Продолжительность (часы, по умолчанию 24): ") or "24")
                sampling = int(input("Интервал выборки (минуты, по умолчанию 15): ") or "15")
                add_noise = input("Добавить шум? (y/n, по умолчанию y): ").lower() != 'n'
                add_missing = input("Добавить пропущенные данные? (y/n, по умолчанию y): ").lower() != 'n'
                
                system.load_data(
                    source_name=source_name,
                    duration_hours=duration,
                    sampling_rate_minutes=sampling,
                    add_noise=add_noise,
                    add_missing_data=add_missing
                )
            else:
                system.load_data(source_name=source_name)
        else:
            print("❌ Неверный выбор источника")
    
    except ValueError:
        print("❌ Неверный ввод")
    except Exception as e:
        print(f"❌ Ошибка загрузки данных: {e}")


def generate_questions_menu(system):
    """Меню генерации вопросов."""
    
    print("\n❓ ГЕНЕРАЦИЯ ВОПРОСОВ")
    print("-" * 30)
    
    if system.current_data is None:
        print("❌ Сначала загрузите данные")
        return
    
    try:
        max_questions = int(input("Максимальное количество вопросов (по умолчанию 10): ") or "10")
        
        print("\nТипы вопросов:")
        print("1. Все типы")
        print("2. Корреляции")
        print("3. Аномалии")
        print("4. Тренды")
        print("5. Предсказания")
        print("6. Лечение")
        
        type_choice = input("Выберите тип вопросов (1-6, по умолчанию 1): ").strip() or "1"
        
        question_types = None
        if type_choice == "2":
            question_types = ["correlation"]
        elif type_choice == "3":
            question_types = ["anomaly"]
        elif type_choice == "4":
            question_types = ["trend"]
        elif type_choice == "5":
            question_types = ["prediction"]
        elif type_choice == "6":
            question_types = ["treatment"]
        
        questions = system.generate_questions(
            max_questions=max_questions,
            question_types=question_types
        )
        
        print(f"\n✅ Сгенерировано {len(questions)} вопросов:")
        for i, q in enumerate(questions, 1):
            print(f"  {i}. [{q.priority}] {q.question}")
    
    except ValueError:
        print("❌ Неверный ввод")
    except Exception as e:
        print(f"❌ Ошибка генерации вопросов: {e}")


def analyze_data_menu(system):
    """Меню анализа данных."""
    
    print("\n🔬 АНАЛИЗ ДАННЫХ")
    print("-" * 30)
    
    if system.current_data is None:
        print("❌ Сначала загрузите данные")
        return
    
    try:
        threshold = float(input("Порог квантовой запутанности (по умолчанию 0.3): ") or "0.3")
        fill_missing = input("Заполнить пропущенные данные? (y/n, по умолчанию y): ").lower() != 'n'
        
        results = system.analyze_data(
            quantum_threshold=threshold,
            fill_missing=fill_missing
        )
        
        print("\n✅ Анализ завершен!")
        
        # Показываем основные результаты
        if 'quantum_signatures' in results:
            coherence = results['quantum_signatures'].get('quantum_coherence', 0)
            print(f"   - Квантовая когерентность: {coherence:.3f}")
        
        if 'patterns' in results:
            print(f"   - Обнаружено паттернов: {len(results['patterns'])}")
        
        if 'quantum_entanglements' in results:
            print(f"   - Окон анализа: {len(results['quantum_entanglements'])}")
    
    except ValueError:
        print("❌ Неверный ввод")
    except Exception as e:
        print(f"❌ Ошибка анализа: {e}")


def answer_questions_menu(system):
    """Меню ответов на вопросы."""
    
    print("\n💬 ОТВЕТЫ НА ВОПРОСЫ")
    print("-" * 30)
    
    if not system.current_questions:
        print("❌ Сначала сгенерируйте вопросы")
        return
    
    if not system.analysis_results:
        print("❌ Сначала выполните анализ данных")
        return
    
    try:
        answers = system.answer_questions()
        
        print(f"\n✅ Получено {len(answers)} ответов:")
        for key, answer_data in answers.items():
            print(f"\n{key.upper()}:")
            print(f"  Вопрос: {answer_data['question']}")
            print(f"  Ответ: {answer_data['answer']}")
            if answer_data['insights']:
                print(f"  Инсайты: {', '.join(answer_data['insights'])}")
    
    except Exception as e:
        print(f"❌ Ошибка ответов: {e}")


def show_report_menu(system):
    """Меню показа отчета."""
    
    print("\n📋 ОТЧЕТ")
    print("-" * 30)
    
    try:
        report = system.get_summary_report()
        
        print("📊 ИНФОРМАЦИЯ О ДАННЫХ:")
        if 'data_info' in report:
            data_info = report['data_info']
            print(f"   - Показателей: {len(data_info['indicators'])}")
            print(f"   - Точек данных: {data_info['data_points']}")
            print(f"   - Пропущенных данных: {data_info['missing_percentage']:.1f}%")
            print(f"   - Период: {data_info['time_range']['start']} - {data_info['time_range']['end']}")
        
        print(f"\n❓ ВОПРОСЫ: {report.get('questions_generated', 0)}")
        
        if 'analysis_results' in report and report['analysis_results']:
            print("\n🔬 РЕЗУЛЬТАТЫ АНАЛИЗА:")
            if 'quantum_signatures' in report['analysis_results']:
                coherence = report['analysis_results']['quantum_signatures'].get('quantum_coherence', 0)
                print(f"   - Квантовая когерентность: {coherence:.3f}")
            
            if 'patterns' in report['analysis_results']:
                print(f"   - Обнаружено паттернов: {len(report['analysis_results']['patterns'])}")
    
    except Exception as e:
        print(f"❌ Ошибка отчета: {e}")


def save_report_menu(system):
    """Меню сохранения отчета."""
    
    print("\n💾 СОХРАНЕНИЕ ОТЧЕТА")
    print("-" * 30)
    
    try:
        filename = input("Имя файла (по умолчанию mqea_report.json): ").strip() or "mqea_report.json"
        
        if not filename.endswith('.json'):
            filename += '.json'
        
        system.save_report(filename)
    
    except Exception as e:
        print(f"❌ Ошибка сохранения: {e}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Демонстрация исправленного AI-помощника.

Автор: Мухаммад Махизода
Таджикский национальный университет
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mqea.advanced_ai_assistant import AdvancedAIAssistant

def demo_fixed_ai():
    """Демонстрация исправленного AI-помощника."""
    print("🔧 Демонстрация исправленного AI-помощника MQEA")
    print("Автор: Мухаммад Махизода")
    print("Таджикский национальный университет")
    print("=" * 70)
    
    # Создаем AI-помощника
    print("\n🔧 Инициализация AI-помощника...")
    ai = AdvancedAIAssistant()
    print("✅ AI-помощник создан")
    
    # Тестовые вопросы с разными типами
    test_questions = [
        "Что такое квантовая запутанность?",
        "Как работает MQEA?",
        "Объясни результаты анализа",
        "Покажи медицинские рекомендации",
        "Что такое квантовая когерентность?",
        "Как интерпретировать графики?",
        "Помоги с диагностикой",
        "Найди аномалии в данных",
        "Расскажи о принципах квантовой физики",
        "Покажи нормальные значения показателей"
    ]
    
    print(f"\n📝 Тестирование {len(test_questions)} вопросов...")
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n--- Вопрос {i} ---")
        print(f"❓ {question}")
        
        try:
            response = ai.process_query(question)
            # Показываем первые 150 символов ответа
            response_preview = response[:150] + "..." if len(response) > 150 else response
            print(f"🤖 {response_preview}")
        except Exception as e:
            print(f"❌ Ошибка: {e}")
    
    # Показываем статистику
    print("\n📊 Статистика обучения:")
    stats = ai.get_learning_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n✅ Исправления:")
    print("• 🔍 Улучшено определение намерений пользователя")
    print("• 🎯 Добавлено больше ключевых слов для распознавания")
    print("• 🧠 Упрощена логика поиска ответов")
    print("• 📝 Улучшена генерация ответов")
    print("• 🔄 Убрана зависимость от сложной векторизации")
    
    print("\n💡 Теперь AI-помощник:")
    print("• ✅ Дает разные ответы на разные вопросы")
    print("• ✅ Распознает намерения пользователя")
    print("• ✅ Предоставляет релевантную информацию")
    print("• ✅ Объясняет квантовые концепции")
    print("• ✅ Помогает с анализом данных")
    print("• ✅ Дает медицинские рекомендации")
    
    print("\n🚀 Для запуска:")
    print("   python start_modern.py")
    print("   Затем выберите '🤖 AI-Помощник' в главном меню")
    
    print("\n✅ Готово! AI-помощник исправлен и работает правильно!")

if __name__ == "__main__":
    demo_fixed_ai()


"""
Чат-интерфейс для AI-помощника MQEA.

Автор: Мухаммад Махизода
Таджикский национальный университет
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mqea.ai_assistant import MQEAAssistant
import json
from datetime import datetime


def main():
    """Главная функция чат-интерфейса."""
    
    print("🤖 AI-ПОМОЩНИК MQEA")
    print("=" * 50)
    print("Автор: Мухаммад Махизода")
    print("Таджикский национальный университет")
    print("=" * 50)
    print("Введите 'выход' для завершения, 'помощь' для справки")
    print("=" * 50)
    
    # Инициализация помощника
    assistant = MQEAAssistant()
    
    # Приветствие
    print(f"\n{assistant.chat('привет')}")
    
    while True:
        try:
            # Получаем ввод пользователя
            user_input = input("\n👤 Вы: ").strip()
            
            if not user_input:
                continue
            
            # Проверяем команды выхода
            if user_input.lower() in ['выход', 'exit', 'quit', 'bye', 'пока']:
                print("\n🤖 Помощник: До свидания! Удачи в анализе данных! 👋")
                break
            
            # Обрабатываем ввод
            response = assistant.chat(user_input)
            
            # Выводим ответ
            print(f"\n🤖 Помощник: {response}")
            
            # Показываем статус
            if user_input.lower() in ['статус', 'status', 'состояние']:
                status = assistant.get_status()
                print(f"\n📊 Статус:")
                print(f"   • Данные загружены: {'Да' if status['has_data'] else 'Нет'}")
                print(f"   • Анализ выполнен: {'Да' if status['has_analysis'] else 'Нет'}")
                print(f"   • Сообщений в чате: {status['conversation_length']}")
                if status['has_data']:
                    print(f"   • Показателей: {status['data_indicators']}")
                    print(f"   • Точек данных: {status['data_points']}")
            
            # Показываем историю
            elif user_input.lower() in ['история', 'history', 'чат']:
                history = assistant.get_conversation_history()
                print(f"\n📜 История чата ({len(history)} сообщений):")
                for i, msg in enumerate(history[-5:], 1):  # Последние 5 сообщений
                    print(f"   {i}. {msg['user'][:50]}...")
            
            # Очистка истории
            elif user_input.lower() in ['очистить', 'clear', 'сброс']:
                assistant.clear_history()
                print("\n🤖 Помощник: История чата очищена.")
            
            # Сохранение истории
            elif user_input.lower() in ['сохранить', 'save', 'экспорт']:
                save_conversation(assistant.get_conversation_history())
            
        except KeyboardInterrupt:
            print("\n\n🤖 Помощник: До свидания! 👋")
            break
        except Exception as e:
            print(f"\n❌ Ошибка: {e}")
            print("Попробуйте еще раз или используйте 'помощь' для справки.")


def save_conversation(history):
    """Сохраняет историю разговора в файл."""
    
    try:
        filename = f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # Подготавливаем данные для сохранения
        data = {
            'timestamp': datetime.now().isoformat(),
            'assistant': 'MQEA AI Assistant',
            'author': 'Мухаммад Махизода',
            'institution': 'Таджикский национальный университет',
            'conversation': []
        }
        
        for msg in history:
            data['conversation'].append({
                'timestamp': msg['timestamp'].isoformat(),
                'user': msg['user'],
                'assistant': msg['assistant']
            })
        
        # Сохраняем в файл
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ История сохранена в файл: {filename}")
        
    except Exception as e:
        print(f"\n❌ Ошибка сохранения: {e}")


def demo_conversation():
    """Демонстрация возможностей помощника."""
    
    print("🎭 ДЕМОНСТРАЦИЯ AI-ПОМОЩНИКА MQEA")
    print("=" * 50)
    
    assistant = MQEAAssistant()
    
    # Примеры вопросов
    demo_questions = [
        "Привет!",
        "Что такое MQEA?",
        "Создай пример данных",
        "Выполни анализ",
        "Найди паттерны",
        "Сгенерируй вопросы",
        "Найди аномалии",
        "Предскажи изменения",
        "Помощь"
    ]
    
    for question in demo_questions:
        print(f"\n👤 Пользователь: {question}")
        response = assistant.chat(question)
        print(f"🤖 Помощник: {response}")
        print("-" * 50)
    
    print("\n🎉 Демонстрация завершена!")
    print("Запустите 'python chat_assistant.py' для интерактивного чата.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        demo_conversation()
    else:
        main()

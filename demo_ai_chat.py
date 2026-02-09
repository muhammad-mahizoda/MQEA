#!/usr/bin/env python3
"""
Демонстрация AI-помощника MQEA.

Автор: Мухаммад Махизода
Таджикский национальный университет
"""

import sys
import os

# Добавляем путь к модулям
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mqea.ai_assistant import MQEAAssistant

def demo_ai_chat():
    """Демонстрация работы AI-помощника."""
    print("🤖 Демонстрация AI-помощника MQEA")
    print("Автор: Мухаммад Махизода")
    print("Таджикский национальный университет")
    print("=" * 60)
    
    # Создаем AI-помощника
    assistant = MQEAAssistant()
    
    # Демонстрационные вопросы
    demo_questions = [
        "Привет!",
        "Что такое MQEA?",
        "Как загрузить данные?",
        "Помощь",
        "Технические детали"
    ]
    
    print("\n📝 Демонстрационные вопросы и ответы:\n")
    
    for i, question in enumerate(demo_questions, 1):
        print(f"❓ Вопрос {i}: {question}")
        print("🤖 Ответ:")
        
        try:
            response = assistant.chat(question)
            print(f"   {response}")
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")
        
        print("-" * 60)
    
    # Показываем статус
    print("\n📊 Статус AI-помощника:")
    status = assistant.get_status()
    for key, value in status.items():
        print(f"   {key}: {value}")
    
    # Показываем историю разговора
    print(f"\n💬 История разговора ({len(assistant.conversation_history)} сообщений):")
    for i, message in enumerate(assistant.conversation_history, 1):
        role = "Пользователь" if message['user'] else "AI"
        content = message['assistant'] if not message['user'] else message['user']
        print(f"   {i}. {role}: {content[:100]}{'...' if len(content) > 100 else ''}")
    
    print("\n✅ Демонстрация завершена!")
    print("\n🚀 Для запуска веб-интерфейса используйте:")
    print("   streamlit run webapp/ai_chat_app.py")

if __name__ == "__main__":
    demo_ai_chat()


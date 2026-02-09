"""
Веб-интерфейс для AI-помощника MQEA.

Автор: Мухаммад Махизода
Таджикский национальный университет
"""

import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mqea.ai_assistant import MQEAAssistant
import json
from datetime import datetime


def initialize_session_state():
    """Инициализирует состояние сессии."""
    if 'assistant' not in st.session_state:
        st.session_state.assistant = MQEAAssistant()
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'show_status' not in st.session_state:
        st.session_state.show_status = False


def main():
    """Главная функция веб-приложения."""
    
    st.set_page_config(
        page_title="MQEA AI Assistant",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Инициализация
    initialize_session_state()
    
    # Заголовок
    st.title("🤖 AI-Помощник MQEA")
    st.markdown("**Автор:** Мухаммад Махизода | **Учреждение:** Таджикский национальный университет")
    
    # Боковая панель
    with st.sidebar:
        st.header("🎛️ Управление")
        
        # Кнопки управления
        if st.button("🔄 Сбросить чат"):
            st.session_state.messages = []
            st.session_state.assistant.clear_history()
            st.rerun()
        
        if st.button("📊 Показать статус"):
            st.session_state.show_status = not st.session_state.show_status
        
        if st.button("💾 Сохранить чат"):
            save_chat_to_file()
        
        # Статус
        if st.session_state.show_status:
            st.subheader("📊 Статус системы")
            status = st.session_state.assistant.get_status()
            
            st.metric("Данные загружены", "Да" if status['has_data'] else "Нет")
            st.metric("Анализ выполнен", "Да" if status['has_analysis'] else "Нет")
            st.metric("Сообщений в чате", status['conversation_length'])
            
            if status['has_data']:
                st.metric("Показателей", status['data_indicators'])
                st.metric("Точек данных", status['data_points'])
        
        # Быстрые команды
        st.subheader("⚡ Быстрые команды")
        
        if st.button("👋 Приветствие"):
            process_message("Привет!")
        
        if st.button("📚 Что такое MQEA?"):
            process_message("Что такое MQEA?")
        
        if st.button("📊 Создать пример данных"):
            process_message("Создай пример данных")
        
        if st.button("🔬 Выполнить анализ"):
            process_message("Выполни анализ")
        
        if st.button("❓ Сгенерировать вопросы"):
            process_message("Сгенерируй вопросы")
        
        if st.button("🔍 Найти паттерны"):
            process_message("Найди паттерны")
        
        if st.button("⚠️ Найти аномалии"):
            process_message("Найди аномалии")
        
        if st.button("🔮 Предсказать"):
            process_message("Предскажи изменения")
        
        if st.button("🆘 Помощь"):
            process_message("Помощь")
    
    # Основная область
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Область чата
        st.subheader("💬 Чат с AI-помощником")
        
        # Отображение сообщений
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Поле ввода
        if prompt := st.chat_input("Введите ваш вопрос..."):
            process_message(prompt)
    
    with col2:
        # Информационная панель
        st.subheader("ℹ️ Информация")
        
        st.markdown("""
        **MQEA AI Assistant** - ваш интеллектуальный помощник по анализу медицинских данных.
        
        **Возможности:**
        • Загрузка и анализ данных
        • Генерация важных вопросов
        • Обнаружение паттернов и аномалий
        • Предсказание изменений
        • Техническая поддержка
        
        **Примеры вопросов:**
        • "Что такое MQEA?"
        • "Как загрузить данные?"
        • "Выполни анализ"
        • "Какие паттерны найдены?"
        """)
        
        # Статистика
        if st.session_state.messages:
            st.subheader("📈 Статистика")
            st.metric("Всего сообщений", len(st.session_state.messages))
            
            user_messages = len([m for m in st.session_state.messages if m["role"] == "user"])
            assistant_messages = len([m for m in st.session_state.messages if m["role"] == "assistant"])
            
            st.metric("Ваших сообщений", user_messages)
            st.metric("Ответов помощника", assistant_messages)


def process_message(user_input):
    """Обрабатывает сообщение пользователя."""
    
    # Добавляем сообщение пользователя
    st.session_state.messages.append({
        "role": "user", 
        "content": user_input
    })
    
    # Получаем ответ от помощника
    try:
        response = st.session_state.assistant.chat(user_input)
        
        # Добавляем ответ помощника
        st.session_state.messages.append({
            "role": "assistant", 
            "content": response
        })
        
        # Обновляем интерфейс
        st.rerun()
        
    except Exception as e:
        error_message = f"❌ Ошибка: {str(e)}"
        st.session_state.messages.append({
            "role": "assistant", 
            "content": error_message
        })
        st.rerun()


def save_chat_to_file():
    """Сохраняет чат в файл."""
    
    try:
        filename = f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # Подготавливаем данные
        data = {
            'timestamp': datetime.now().isoformat(),
            'assistant': 'MQEA AI Assistant',
            'author': 'Мухаммад Махизода',
            'institution': 'Таджикский национальный университет',
            'messages': st.session_state.messages
        }
        
        # Сохраняем
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        st.success(f"✅ Чат сохранен в файл: {filename}")
        
    except Exception as e:
        st.error(f"❌ Ошибка сохранения: {e}")


def display_welcome_message():
    """Отображает приветственное сообщение."""
    
    if not st.session_state.messages:
        welcome_message = """
        👋 **Добро пожаловать в MQEA AI Assistant!**
        
        Я ваш интеллектуальный помощник по анализу медицинских данных. 
        Могу помочь с:
        
        • Загрузкой и анализом данных
        • Генерацией важных вопросов
        • Обнаружением паттернов и аномалий
        • Предсказанием изменений
        • Техническими вопросами
        
        **Начните с вопроса или используйте быстрые команды в боковой панели!**
        """
        
        st.session_state.messages.append({
            "role": "assistant", 
            "content": welcome_message
        })


if __name__ == "__main__":
    main()

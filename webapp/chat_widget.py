"""
Компактный виджет чата для встраивания в другие интерфейсы.

Автор: Мухаммад Махизода
Таджикский национальный университет
"""

import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mqea.ai_assistant import MQEAAssistant


def chat_widget(assistant=None, key_prefix="chat"):
    """Создает компактный виджет чата."""
    
    if assistant is None:
        if f'{key_prefix}_assistant' not in st.session_state:
            st.session_state[f'{key_prefix}_assistant'] = MQEAAssistant()
        assistant = st.session_state[f'{key_prefix}_assistant']
    
    if f'{key_prefix}_messages' not in st.session_state:
        st.session_state[f'{key_prefix}_messages'] = []
    
    # Контейнер для чата
    with st.container():
        # Заголовок виджета
        st.markdown("### 🤖 AI-Помощник")
        
        # Область сообщений (ограниченная высота)
        chat_container = st.container()
        
        with chat_container:
            # Показываем последние 5 сообщений
            messages_to_show = st.session_state[f'{key_prefix}_messages'][-5:]
            
            for message in messages_to_show:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
        
        # Поле ввода
        if user_input := st.chat_input("Задайте вопрос...", key=f"{key_prefix}_input"):
            # Добавляем сообщение пользователя
            st.session_state[f'{key_prefix}_messages'].append({
                "role": "user",
                "content": user_input
            })
            
            # Получаем ответ от помощника
            try:
                response = assistant.chat(user_input)
                
                # Добавляем ответ помощника
                st.session_state[f'{key_prefix}_messages'].append({
                    "role": "assistant",
                    "content": response
                })
                
                # Обновляем интерфейс
                st.rerun()
                
            except Exception as e:
                error_message = f"❌ Ошибка: {str(e)}"
                st.session_state[f'{key_prefix}_messages'].append({
                    "role": "assistant",
                    "content": error_message
                })
                st.rerun()
        
        # Быстрые команды
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("👋 Привет", key=f"{key_prefix}_hello"):
                process_message("Привет!", assistant, key_prefix)
        
        with col2:
            if st.button("❓ Помощь", key=f"{key_prefix}_help"):
                process_message("Помощь", assistant, key_prefix)
        
        with col3:
            if st.button("🔄 Очистить", key=f"{key_prefix}_clear"):
                st.session_state[f'{key_prefix}_messages'] = []
                assistant.clear_history()
                st.rerun()


def process_message(message, assistant, key_prefix):
    """Обрабатывает сообщение."""
    st.session_state[f'{key_prefix}_messages'].append({
        "role": "user",
        "content": message
    })
    
    try:
        response = assistant.chat(message)
        st.session_state[f'{key_prefix}_messages'].append({
            "role": "assistant",
            "content": response
        })
        st.rerun()
    except Exception as e:
        st.session_state[f'{key_prefix}_messages'].append({
            "role": "assistant",
            "content": f"❌ Ошибка: {str(e)}"
        })
        st.rerun()


def compact_chat_widget(assistant=None, height=300):
    """Создает очень компактный виджет чата."""
    
    if assistant is None:
        if 'compact_assistant' not in st.session_state:
            st.session_state.compact_assistant = MQEAAssistant()
        assistant = st.session_state.compact_assistant
    
    if 'compact_messages' not in st.session_state:
        st.session_state.compact_messages = []
    
    # Компактный контейнер
    with st.container():
        # Заголовок
        st.markdown("#### 🤖 AI-Помощник")
        
        # Область сообщений с ограниченной высотой
        with st.container():
            # Показываем последние 3 сообщения
            messages_to_show = st.session_state.compact_messages[-3:]
            
            for message in messages_to_show:
                if message["role"] == "user":
                    st.markdown(f"**Вы:** {message['content']}")
                else:
                    st.markdown(f"**AI:** {message['content']}")
        
        # Поле ввода
        user_input = st.text_input("Вопрос:", key="compact_input", placeholder="Задайте вопрос...")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Отправить", key="compact_send"):
                if user_input:
                    process_compact_message(user_input, assistant)
        
        with col2:
            if st.button("Очистить", key="compact_clear"):
                st.session_state.compact_messages = []
                assistant.clear_history()
                st.rerun()


def process_compact_message(message, assistant):
    """Обрабатывает сообщение в компактном виджете."""
    st.session_state.compact_messages.append({
        "role": "user",
        "content": message
    })
    
    try:
        response = assistant.chat(message)
        st.session_state.compact_messages.append({
            "role": "assistant",
            "content": response
        })
        st.rerun()
    except Exception as e:
        st.session_state.compact_messages.append({
            "role": "assistant",
            "content": f"❌ Ошибка: {str(e)}"
        })
        st.rerun()


# Демонстрация виджета
if __name__ == "__main__":
    st.set_page_config(
        page_title="MQEA Chat Widget Demo",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 Демонстрация виджета чата MQEA")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Полный виджет")
        chat_widget()
    
    with col2:
        st.subheader("Компактный виджет")
        compact_chat_widget()

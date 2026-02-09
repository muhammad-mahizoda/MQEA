"""
Отдельное приложение для AI-помощника MQEA.

Автор: Мухаммад Махизода
Таджикский национальный университет
"""

import streamlit as st
import sys
import os

# Добавляем путь к модулям
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mqea.ai_assistant import MQEAAssistant

# Настройки страницы
st.set_page_config(
    page_title="AI Помощник MQEA",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Логотип
def display_logo():
    """Отображает основной логотип MQEA."""
    try:
        logo_path = "mqea_logo.png"
        if os.path.exists(logo_path):
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image(logo_path, width=200)
        else:
            st.markdown("### 🏥 MQEA")
    except Exception as e:
        st.markdown("### 🏥 MQEA")

# Логотип
display_logo()

# Заголовок приложения
st.title("🤖 AI Помощник MQEA")
st.markdown("**Ваш интеллектуальный помощник по анализу медицинских данных**")

# Информация об основателе
with st.expander("ℹ️ Информация об основателе"):
    st.markdown("""
    **Основатель и разработчик:** Мухаммад Махизода  
    **Должность:** Администратор сети  
    **Университет:** Таджикский национальный университет  
    **Email:** muhammad.mahizoda@tnu.tj
    """)

# Боковая панель с навигацией
with st.sidebar:
    try:
        logo_path = "mqea_logo.png"
        if os.path.exists(logo_path):
            st.image(logo_path, width=120)
        st.markdown("### 🤖 AI Помощник")
        st.markdown("**MQEA**")
        st.markdown("*Автор: Мухаммад Махизода*")
        st.markdown("---")
    except Exception as e:
        st.markdown("### 🤖 AI Помощник")
        st.markdown("---")

# Кнопка возврата к главному приложению
if st.sidebar.button("🏠 Вернуться к анализу данных", type="primary"):
    st.switch_page("streamlit_app.py")

st.sidebar.markdown("---")

# Инициализация AI помощника
if 'ai_assistant' not in st.session_state:
    with st.spinner("Инициализация AI помощника..."):
        st.session_state['ai_assistant'] = MQEAAssistant()

ai_assistant = st.session_state['ai_assistant']

# История разговора
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Основная область чата
col1, col2 = st.columns([3, 1])

with col1:
    # Отображение истории чата
    chat_container = st.container()
    with chat_container:
        if st.session_state['chat_history']:
            for message in st.session_state['chat_history']:
                if message['role'] == 'user':
                    st.markdown(f"""
                    <div style="background-color: #e3f2fd; padding: 10px; border-radius: 10px; margin: 5px 0;">
                        <strong>Вы:</strong> {message['content']}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="background-color: #f3e5f5; padding: 10px; border-radius: 10px; margin: 5px 0;">
                        <strong>AI:</strong> {message['content']}
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("👋 Привет! Я ваш AI-помощник по MQEA. Задайте мне любой вопрос!")
    
    # Поле ввода
    st.markdown("---")
    user_input = st.text_area(
        "Задайте вопрос AI помощнику:",
        placeholder="Например: Что такое MQEA? Как загрузить данные? Выполни анализ...",
        height=100,
        key="ai_input"
    )
    
    col_send, col_clear = st.columns([1, 1])
    with col_send:
        if st.button("📤 Отправить", type="primary", use_container_width=True):
            if user_input.strip():
                # Добавляем сообщение пользователя в историю
                st.session_state['chat_history'].append({
                    'role': 'user',
                    'content': user_input
                })
                
                # Получаем ответ от AI
                with st.spinner("🤔 AI думает..."):
                    response = ai_assistant.chat(user_input)
                
                # Добавляем ответ AI в историю
                st.session_state['chat_history'].append({
                    'role': 'assistant',
                    'content': response
                })
                
                # Очищаем поле ввода
                st.session_state['ai_input'] = ""
                st.rerun()
    
    with col_clear:
        if st.button("🗑️ Очистить", use_container_width=True):
            st.session_state['chat_history'] = []
            st.rerun()

with col2:
    # Быстрые команды
    st.subheader("🚀 Быстрые команды")
    
    quick_commands = [
        ("Что такое MQEA?", "ℹ️"),
        ("Как загрузить данные?", "📊"),
        ("Выполни анализ", "🔬"),
        ("Найди паттерны", "🔍"),
        ("Найди аномалии", "⚠️"),
        ("Предскажи", "🔮"),
        ("Помощь", "🆘"),
        ("Технические детали", "🔧")
    ]
    
    for command, icon in quick_commands:
        if st.button(f"{icon} {command}", use_container_width=True, key=f"quick_{command}"):
            st.session_state['ai_input'] = command
            st.rerun()
    
    st.markdown("---")
    
    # Статус AI помощника
    st.subheader("📊 Статус")
    status = ai_assistant.get_status()
    
    st.metric("Есть данные", "✅" if status['has_data'] else "❌")
    st.metric("Есть анализ", "✅" if status['has_analysis'] else "❌")
    st.metric("Сообщений", status['conversation_length'])
    
    if status['has_data']:
        st.metric("Показателей", status['data_indicators'])
        st.metric("Точек данных", status['data_points'])
    
    # Дополнительные функции
    st.markdown("---")
    st.subheader("🛠️ Дополнительно")
    
    if st.button("🔄 Перезапустить AI", use_container_width=True):
        st.session_state['ai_assistant'] = MQEAAssistant()
        st.session_state['chat_history'] = []
        st.rerun()
    
    if st.button("📋 Экспорт истории", use_container_width=True):
        if st.session_state['chat_history']:
            import json
            history_json = json.dumps(st.session_state['chat_history'], ensure_ascii=False, indent=2)
            st.download_button(
                label="Скачать историю",
                data=history_json,
                file_name=f"mqea_chat_history_{st.session_state.get('session_id', 'unknown')}.json",
                mime="application/json"
            )
        else:
            st.warning("История пуста")

# Футер
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p><strong>🤖 AI Помощник MQEA</strong></p>
    <p>Основатель: <strong>Мухаммад Махизода</strong> | Таджикский национальный университет</p>
    <p>© 2025 Все права защищены</p>
</div>
""", unsafe_allow_html=True)


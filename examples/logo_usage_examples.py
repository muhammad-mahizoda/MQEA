"""
Примеры использования логотипов MQEA.

Автор: Мухаммад Махизода
Таджикский национальный университет
"""

import streamlit as st
import os
from pathlib import Path

# Пример 1: Базовое использование в Streamlit
def example_streamlit_logo():
    """Пример использования логотипа в Streamlit."""
    logo_path = "webapp/static/logos/quantum_medical_cross_blue.png"
    
    if os.path.exists(logo_path):
        st.image(logo_path, width=200)
        st.markdown("### 🏥 MQEA - Medical Quantum Entanglement Analysis")
    else:
        st.markdown("### 🏥 MQEA")

# Пример 2: Логотип в сайдбаре
def example_sidebar_logo():
    """Пример логотипа в сайдбаре."""
    with st.sidebar:
        logo_path = "webapp/static/logos/quantum_medical_cross_blue.png"
        
        if os.path.exists(logo_path):
            st.image(logo_path, width=150)
        
        st.markdown("---")
        st.markdown("### 🏥 MQEA")
        st.markdown("**Medical Quantum Entanglement Analysis**")
        st.markdown("*Автор: Мухаммад Махизода*")

# Пример 3: Адаптивный логотип
def example_responsive_logo():
    """Пример адаптивного логотипа."""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        logo_path = "webapp/static/logos/quantum_medical_cross_blue.png"
        
        if os.path.exists(logo_path):
            st.image(logo_path, width=300)
        
        st.markdown("### 🏥 MQEA")
        st.markdown("**Medical Quantum Entanglement Analysis**")
        st.markdown("*Революционный алгоритм для анализа медицинских данных*")

# Пример 4: Логотип с информацией
def example_logo_with_info():
    """Пример логотипа с дополнительной информацией."""
    logo_path = "webapp/static/logos/quantum_medical_cross_blue.png"
    
    if os.path.exists(logo_path):
        st.image(logo_path, width=200)
    
    st.markdown("### 🏥 MQEA")
    st.markdown("**Medical Quantum Entanglement Analysis**")
    
    # Информация о проекте
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**👨‍💻 Автор:**")
        st.markdown("Мухаммад Махизода")
        st.markdown("Администратор сети")
        st.markdown("Таджикский национальный университет")
    
    with col2:
        st.markdown("**🎯 Особенности:**")
        st.markdown("• Квантовая запутанность")
        st.markdown("• Медицинский анализ")
        st.markdown("• Машинное обучение")
        st.markdown("• Современный интерфейс")

# Пример 5: Выбор логотипа
def example_logo_selector():
    """Пример выбора логотипа."""
    st.markdown("### 🎨 Выбор логотипа")
    
    logo_type = st.selectbox(
        "Тип логотипа:",
        ["quantum_medical_cross", "dna_medical", "quantum_entanglement", 
         "medical_shield", "heart_medical"]
    )
    
    color = st.selectbox(
        "Цвет:",
        ["blue", "green", "red"]
    )
    
    logo_filename = f"{logo_type}_{color}.png"
    logo_path = f"webapp/static/logos/{logo_filename}"
    
    if os.path.exists(logo_path):
        st.image(logo_path, width=300)
        st.markdown(f"**Файл:** {logo_filename}")
    else:
        st.error(f"Логотип {logo_filename} не найден!")

if __name__ == "__main__":
    st.title("🏥 Примеры использования логотипов MQEA")
    
    example_streamlit_logo()
    st.markdown("---")
    example_sidebar_logo()
    st.markdown("---")
    example_responsive_logo()
    st.markdown("---")
    example_logo_with_info()
    st.markdown("---")
    example_logo_selector()

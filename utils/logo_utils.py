#!/usr/bin/env python3
"""
Утилиты для работы с логотипами MQEA.

Автор: Мухаммад Махизода
Таджикский национальный университет
"""

import streamlit as st
import os
from pathlib import Path
from typing import Optional, Tuple

class MQEALogoDisplay:
    """Класс для отображения логотипов MQEA в Streamlit."""
    
    def __init__(self):
        self.logo_path = Path("mqea_logo.png")
        self.logo_dir = Path("webapp/static/logos")
        self.fallback_logo = "🏥"
    
    def display_main_logo(self, width: int = 200, centered: bool = True) -> bool:
        """
        Отображает основной логотип MQEA.
        
        Args:
            width: Ширина логотипа в пикселях
            centered: Центрировать ли логотип
            
        Returns:
            bool: True если логотип отображен успешно, False иначе
        """
        try:
            if self.logo_path.exists():
                if centered:
                    col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.image(str(self.logo_path), width=width, use_container_width=False)
                else:
                    st.image(str(self.logo_path), width=width, use_container_width=False)
                return True
            else:
                st.markdown(f"### {self.fallback_logo} MQEA")
                return False
        except Exception as e:
            st.markdown(f"### {self.fallback_logo} MQEA")
            return False
    
    def display_sidebar_logo(self, width: int = 150) -> bool:
        """
        Отображает логотип в сайдбаре.
        
        Args:
            width: Ширина логотипа в пикселях
            
        Returns:
            bool: True если логотип отображен успешно, False иначе
        """
        try:
            if self.logo_path.exists():
                st.image(str(self.logo_path), width=width, use_container_width=False)
                st.markdown("### 🏥 MQEA")
                st.markdown("**Medical Quantum Entanglement Analysis**")
                st.markdown("*Автор: Мухаммад Махизода*")
                st.markdown("---")
                return True
            else:
                st.markdown("### 🏥 MQEA")
                st.markdown("---")
                return False
        except Exception as e:
            st.markdown("### 🏥 MQEA")
            st.markdown("---")
            return False
    
    def display_logo_with_info(self, width: int = 200) -> bool:
        """
        Отображает логотип с дополнительной информацией.
        
        Args:
            width: Ширина логотипа в пикселях
            
        Returns:
            bool: True если логотип отображен успешно, False иначе
        """
        try:
            if self.logo_path.exists():
                st.image(str(self.logo_path), width=width, use_container_width=False)
            
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
            
            return True
        except Exception as e:
            st.markdown("### 🏥 MQEA")
            return False
    
    def display_logo_header(self, title: str = "MQEA", subtitle: str = "Medical Quantum Entanglement Analysis") -> bool:
        """
        Отображает логотип в заголовке страницы.
        
        Args:
            title: Заголовок страницы
            subtitle: Подзаголовок
            
        Returns:
            bool: True если логотип отображен успешно, False иначе
        """
        try:
            if self.logo_path.exists():
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.image(str(self.logo_path), width=200)
            
            st.title(f"🏥 {title}")
            st.markdown(f"**{subtitle}**")
            
            return True
        except Exception as e:
            st.title(f"🏥 {title}")
            st.markdown(f"**{subtitle}**")
            return False
    
    def get_logo_path(self) -> Optional[Path]:
        """
        Получает путь к основному логотипу.
        
        Returns:
            Path или None если логотип не найден
        """
        if self.logo_path.exists():
            return self.logo_path
        return None
    
    def is_logo_available(self) -> bool:
        """
        Проверяет доступность основного логотипа.
        
        Returns:
            bool: True если логотип доступен, False иначе
        """
        return self.logo_path.exists()
    
    def get_logo_info(self) -> dict:
        """
        Получает информацию о логотипе.
        
        Returns:
            dict: Информация о логотипе
        """
        return {
            "path": str(self.logo_path),
            "exists": self.logo_path.exists(),
            "size": self.logo_path.stat().st_size if self.logo_path.exists() else 0,
            "name": "Сердце с медицинским символом (синий)",
            "description": "Основной логотип проекта MQEA - символ заботы и здоровья",
            "motto": "Спокойствие, доверие, стабильность",
            "motto_en": "Calm, Trust, Stability",
            "author": "Мухаммад Махизода",
            "university": "Таджикский национальный университет"
        }

# Глобальный экземпляр для использования в приложениях
logo_display = MQEALogoDisplay()

# Функции для быстрого доступа
def display_main_logo(width: int = 200, centered: bool = True) -> bool:
    """Быстрое отображение основного логотипа."""
    return logo_display.display_main_logo(width, centered)

def display_sidebar_logo(width: int = 150) -> bool:
    """Быстрое отображение логотипа в сайдбаре."""
    return logo_display.display_sidebar_logo(width)

def display_logo_with_info(width: int = 200) -> bool:
    """Быстрое отображение логотипа с информацией."""
    return logo_display.display_logo_with_info(width)

def display_logo_header(title: str = "MQEA", subtitle: str = "Medical Quantum Entanglement Analysis") -> bool:
    """Быстрое отображение логотипа в заголовке."""
    return logo_display.display_logo_header(title, subtitle)

def is_logo_available() -> bool:
    """Быстрая проверка доступности логотипа."""
    return logo_display.is_logo_available()

def get_logo_info() -> dict:
    """Быстрое получение информации о логотипе."""
    return logo_display.get_logo_info()

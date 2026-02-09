#!/usr/bin/env python3
"""
Оптимизированное отображение логотипов MQEA в Streamlit.

Автор: Мухаммад Махизода
Таджикский национальный университет
"""

import streamlit as st
import os
from pathlib import Path
from typing import Optional, Tuple

class OptimizedLogoDisplay:
    """Класс для оптимизированного отображения логотипов MQEA."""
    
    def __init__(self):
        self.logo_path = Path("mqea_logo.png")
        self.premium_logo = Path("mqea_logo_premium.png")
        self.card_logo = Path("mqea_logo_card_optimized.png")
        self.sidebar_logo = Path("mqea_logo_sidebar_optimized.png")
        
        # Девиз проекта
        self.motto = "Спокойствие, доверие, стабильность"
        self.motto_en = "Calm, Trust, Stability"
        
        # Настройки качества
        self.quality_settings = {
            'high': {'width': 300, 'quality': 'high'},
            'medium': {'width': 200, 'quality': 'medium'},
            'low': {'width': 150, 'quality': 'low'}
        }
    
    def display_centered_logo(self, width: int = 200, quality: str = 'medium') -> bool:
        """
        Отображает логотип по центру с оптимизированным качеством.
        
        Args:
            width: Ширина логотипа
            quality: Качество отображения ('high', 'medium', 'low')
            
        Returns:
            bool: True если логотип отображен успешно
        """
        try:
            if self.logo_path.exists():
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.image(str(self.logo_path), width=width, use_container_width=False)
                return True
            else:
                self._display_fallback_logo()
                return False
        except Exception as e:
            self._display_fallback_logo()
            return False
    
    def display_premium_logo(self, width: int = 300) -> bool:
        """
        Отображает премиум версию логотипа.
        
        Args:
            width: Ширина логотипа
            
        Returns:
            bool: True если логотип отображен успешно
        """
        try:
            if self.premium_logo.exists():
                st.image(str(self.premium_logo), width=width, use_container_width=False)
                return True
            else:
                return self.display_centered_logo(width)
        except Exception as e:
            return self.display_centered_logo(width)
    
    def display_card_logo(self, width: int = 250) -> bool:
        """
        Отображает логотип в стиле карточки.
        
        Args:
            width: Ширина логотипа
            
        Returns:
            bool: True если логотип отображен успешно
        """
        try:
            if self.card_logo.exists():
                st.image(str(self.card_logo), width=width, use_container_width=False)
                return True
            else:
                return self.display_centered_logo(width)
        except Exception as e:
            return self.display_centered_logo(width)
    
    def display_sidebar_logo(self, width: int = 150) -> bool:
        """
        Отображает оптимизированный логотип в сайдбаре.
        
        Args:
            width: Ширина логотипа
            
        Returns:
            bool: True если логотип отображен успешно
        """
        try:
            if self.sidebar_logo.exists():
                st.image(str(self.sidebar_logo), width=width, use_container_width=False)
            else:
                st.image(str(self.logo_path), width=width, use_container_width=False)
            
            # Информация о проекте
            st.markdown("### 🏥 MQEA")
            st.markdown("**Medical Quantum Entanglement Analysis**")
            st.markdown(f"*{self.motto}*")
            st.markdown("---")
            st.markdown("**👨‍💻 Автор:**")
            st.markdown("Мухаммад Махизода")
            st.markdown("Таджикский национальный университет")
            st.markdown("---")
            
            return True
        except Exception as e:
            st.markdown("### 🏥 MQEA")
            st.markdown("---")
            return False
    
    def display_logo_with_info(self, width: int = 200) -> bool:
        """
        Отображает логотип с подробной информацией.
        
        Args:
            width: Ширина логотипа
            
        Returns:
            bool: True если логотип отображен успешно
        """
        try:
            # Логотип
            if self.logo_path.exists():
                st.image(str(self.logo_path), width=width, use_container_width=False)
            
            # Информация о проекте
            st.markdown("### 🏥 MQEA")
            st.markdown("**Medical Quantum Entanglement Analysis**")
            
            # Девиз
            st.markdown(f"**🎯 Девиз:** *{self.motto}*")
            st.markdown(f"**🎯 Motto:** *{self.motto_en}*")
            
            # Информация об авторе
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
    
    def display_adaptive_logo(self, container_width: int = 800) -> bool:
        """
        Отображает адаптивный логотип в зависимости от ширины контейнера.
        
        Args:
            container_width: Ширина контейнера
            
        Returns:
            bool: True если логотип отображен успешно
        """
        try:
            # Определяем размер логотипа в зависимости от ширины контейнера
            if container_width >= 1000:
                logo_width = 300
                use_premium = True
            elif container_width >= 600:
                logo_width = 200
                use_premium = False
            else:
                logo_width = 150
                use_premium = False
            
            # Выбираем подходящий логотип
            if use_premium and self.premium_logo.exists():
                st.image(str(self.premium_logo), width=logo_width, use_container_width=False)
            elif self.logo_path.exists():
                st.image(str(self.logo_path), width=logo_width, use_container_width=False)
            else:
                self._display_fallback_logo()
                return False
            
            return True
        except Exception as e:
            self._display_fallback_logo()
            return False
    
    def _display_fallback_logo(self):
        """Отображает резервный логотип."""
        st.markdown("### 🏥 MQEA")
        st.markdown("**Medical Quantum Entanglement Analysis**")
        st.markdown(f"*{self.motto}*")
    
    def get_logo_info(self) -> dict:
        """
        Получает информацию о доступных логотипах.
        
        Returns:
            dict: Информация о логотипах
        """
        return {
            "main_logo": {
                "path": str(self.logo_path),
                "exists": self.logo_path.exists(),
                "size": self.logo_path.stat().st_size if self.logo_path.exists() else 0
            },
            "premium_logo": {
                "path": str(self.premium_logo),
                "exists": self.premium_logo.exists(),
                "size": self.premium_logo.stat().st_size if self.premium_logo.exists() else 0
            },
            "card_logo": {
                "path": str(self.card_logo),
                "exists": self.card_logo.exists(),
                "size": self.card_logo.stat().st_size if self.card_logo.exists() else 0
            },
            "sidebar_logo": {
                "path": str(self.sidebar_logo),
                "exists": self.sidebar_logo.exists(),
                "size": self.sidebar_logo.stat().st_size if self.sidebar_logo.exists() else 0
            },
            "motto": self.motto,
            "motto_en": self.motto_en
        }

# Глобальный экземпляр для использования в приложениях
optimized_logo_display = OptimizedLogoDisplay()

# Функции для быстрого доступа
def display_centered_logo(width: int = 200, quality: str = 'medium') -> bool:
    """Быстрое отображение центрированного логотипа."""
    return optimized_logo_display.display_centered_logo(width, quality)

def display_premium_logo(width: int = 300) -> bool:
    """Быстрое отображение премиум логотипа."""
    return optimized_logo_display.display_premium_logo(width)

def display_card_logo(width: int = 250) -> bool:
    """Быстрое отображение логотипа в стиле карточки."""
    return optimized_logo_display.display_card_logo(width)

def display_sidebar_logo(width: int = 150) -> bool:
    """Быстрое отображение логотипа в сайдбаре."""
    return optimized_logo_display.display_sidebar_logo(width)

def display_logo_with_info(width: int = 200) -> bool:
    """Быстрое отображение логотипа с информацией."""
    return optimized_logo_display.display_logo_with_info(width)

def display_adaptive_logo(container_width: int = 800) -> bool:
    """Быстрое отображение адаптивного логотипа."""
    return optimized_logo_display.display_adaptive_logo(container_width)

def get_logo_info() -> dict:
    """Быстрое получение информации о логотипах."""
    return optimized_logo_display.get_logo_info()

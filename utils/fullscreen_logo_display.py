#!/usr/bin/env python3
"""
Функции отображения полноэкранных логотипов MQEA с прозрачным фоном.

Автор: Мухаммад Махизода
Таджикский национальный университет
"""

import streamlit as st
from pathlib import Path
import os

class FullscreenLogoDisplay:
    """Класс для отображения полноэкранных логотипов MQEA."""
    
    def __init__(self):
        self.base_path = Path(".")
        
        # Пути к правильным медицинским логотипам
        self.fullscreen_logo = self.base_path / "mqea_logo_proper_main.png"
        self.wide_logo = self.base_path / "mqea_logo_proper_main.png"
        self.header_logo = self.base_path / "mqea_logo_proper_header.png"
        self.centered_logo = self.base_path / "mqea_logo_proper_centered.png"
        self.minimal_logo = self.base_path / "mqea_logo_proper_sidebar.png"
        self.sidebar_logo = self.base_path / "mqea_logo_proper_sidebar.png"
        self.text_logo = self.base_path / "mqea_logo_proper_sidebar.png"
        
        # Девиз проекта
        self.motto = "Спокойствие, доверие, стабильность"
        self.motto_en = "Calm, Trust, Stability"
        
        # Информация о проекте
        self.project_info = {
            'name': 'MQEA',
            'full_name': 'Medical Quantum Entanglement Analysis',
            'motto': self.motto,
            'motto_en': self.motto_en,
            'description': 'Система анализа медицинских данных на основе квантовой запутанности'
        }
    
    def display_fullscreen_logo(self, width=None, use_container_width=True):
        """
        Отображает полноэкранный логотип.
        
        Args:
            width: Ширина изображения
            use_container_width: Использовать ширину контейнера
            
        Returns:
            bool: True если логотип отображен успешно
        """
        try:
            if self.fullscreen_logo.exists():
                # Полноэкранное отображение
                st.image(str(self.fullscreen_logo), 
                        width=width, 
                        use_container_width=use_container_width)
                return True
            else:
                self._display_fallback_logo()
                return False
        except Exception as e:
            st.error(f"Ошибка отображения полноэкранного логотипа: {e}")
            return False
    
    def display_wide_logo(self, width=None, use_container_width=True):
        """
        Отображает широкий логотип для главного экрана.
        
        Args:
            width: Ширина изображения
            use_container_width: Использовать ширину контейнера
            
        Returns:
            bool: True если логотип отображен успешно
        """
        try:
            if self.wide_logo.exists():
                # Широкое отображение без белого фона
                st.image(str(self.wide_logo), 
                        width=width, 
                        use_container_width=use_container_width)
                return True
            else:
                return self.display_fullscreen_logo(width, use_container_width)
        except Exception as e:
            st.error(f"Ошибка отображения широкого логотипа: {e}")
            return False
    
    def display_header_logo(self, width=None, use_container_width=True):
        """
        Отображает логотип для заголовка.
        
        Args:
            width: Ширина изображения
            use_container_width: Использовать ширину контейнера
            
        Returns:
            bool: True если логотип отображен успешно
        """
        try:
            if self.header_logo.exists():
                st.image(str(self.header_logo), 
                        width=width, 
                        use_container_width=use_container_width)
                return True
            else:
                return self.display_wide_logo(width, use_container_width)
        except Exception as e:
            st.error(f"Ошибка отображения логотипа заголовка: {e}")
            return False
    
    def display_main_screen_logo(self, width=None):
        """
        Отображает логотип для главного экрана (оптимизированный).
        
        Args:
            width: Ширина изображения
            
        Returns:
            bool: True если логотип отображен успешно
        """
        try:
            # Используем широкий логотип для главного экрана
            if self.wide_logo.exists():
                # Отображение без белого фона, на полную ширину
                st.image(str(self.wide_logo), 
                        width=width, 
                        use_container_width=True)
                
                # Добавляем информацию о проекте
                st.markdown("---")
                st.markdown(f"### 🏥 {self.project_info['name']}")
                st.markdown(f"**{self.project_info['full_name']}**")
                st.markdown(f"*{self.project_info['motto']}*")
                st.markdown(f"*{self.project_info['motto_en']}*")
                
                return True
            else:
                return self.display_fullscreen_logo(width)
        except Exception as e:
            st.error(f"Ошибка отображения логотипа главного экрана: {e}")
            return False
    
    def display_centered_logo(self, width=None, use_container_width=True):
        """
        Отображает центрированный логотип с текстом под ним.
        
        Args:
            width: Ширина изображения
            use_container_width: Использовать ширину контейнера
            
        Returns:
            bool: True если логотип отображен успешно
        """
        try:
            if self.centered_logo.exists():
                # Центрированное отображение
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.image(str(self.centered_logo), 
                            width=width, 
                            use_container_width=use_container_width)
                return True
            else:
                return self.display_wide_logo(width, use_container_width)
        except Exception as e:
            st.error(f"Ошибка отображения центрированного логотипа: {e}")
            return False
    
    def display_minimal_logo(self, width=None, use_container_width=True):
        """
        Отображает минимальный логотип с очень маленьким топбаром.
        
        Args:
            width: Ширина изображения
            use_container_width: Использовать ширину контейнера
            
        Returns:
            bool: True если логотип отображен успешно
        """
        try:
            if self.minimal_logo.exists():
                # Минимальное отображение
                st.image(str(self.minimal_logo), 
                        width=width, 
                        use_container_width=use_container_width)
                return True
            else:
                return self.display_header_logo(width, use_container_width)
        except Exception as e:
            st.error(f"Ошибка отображения минимального логотипа: {e}")
            return False
    
    def display_sidebar_logo(self, width=None, use_container_width=True):
        """
        Отображает логотип оптимизированный для боковой панели.
        
        Args:
            width: Ширина изображения
            use_container_width: Использовать ширину контейнера
            
        Returns:
            bool: True если логотип отображен успешно
        """
        try:
            if self.sidebar_logo.exists():
                # Отображение для боковой панели
                st.image(str(self.sidebar_logo), 
                        width=width, 
                        use_container_width=use_container_width)
                return True
            else:
                return self.display_minimal_logo(width, use_container_width)
        except Exception as e:
            st.error(f"Ошибка отображения логотипа боковой панели: {e}")
            return False
    
    def display_text_logo(self, width=200, use_container_width=False):
        """
        Отображает минимальный текстовый логотип.
        
        Args:
            width: Ширина изображения
            use_container_width: Использовать ширину контейнера
            
        Returns:
            bool: True если логотип отображен успешно
        """
        try:
            if self.text_logo.exists():
                # Минимальное текстовое отображение
                st.image(str(self.text_logo), 
                        width=width, 
                        use_container_width=use_container_width)
                return True
            else:
                st.markdown("### 🏥 MQEA")
                st.markdown("*Спокойствие, доверие, стабильность*")
                return False
        except Exception as e:
            st.error(f"Ошибка отображения текстового логотипа: {e}")
            return False
    
    def display_transparent_logo(self, logo_type='wide', width=None, use_container_width=True):
        """
        Отображает прозрачный логотип.
        
        Args:
            logo_type: Тип логотипа ('fullscreen', 'wide', 'header', 'centered', 'minimal', 'sidebar')
            width: Ширина изображения
            use_container_width: Использовать ширину контейнера
            
        Returns:
            bool: True если логотип отображен успешно
        """
        try:
            # Выбираем логотип по типу
            if logo_type == 'fullscreen':
                logo_path = self.fullscreen_logo
            elif logo_type == 'wide':
                logo_path = self.wide_logo
            elif logo_type == 'header':
                logo_path = self.header_logo
            elif logo_type == 'centered':
                logo_path = self.centered_logo
            elif logo_type == 'minimal':
                logo_path = self.minimal_logo
            elif logo_type == 'sidebar':
                logo_path = self.sidebar_logo
            else:
                logo_path = self.wide_logo
            
            if logo_path.exists():
                # Отображение с прозрачным фоном
                st.image(str(logo_path), 
                        width=width, 
                        use_container_width=use_container_width)
                return True
            else:
                self._display_fallback_logo()
                return False
        except Exception as e:
            st.error(f"Ошибка отображения прозрачного логотипа: {e}")
            return False
    
    def _display_fallback_logo(self):
        """Отображает резервный логотип."""
        st.markdown("### 🏥 MQEA")
        st.markdown("**Medical Quantum Entanglement Analysis**")
        st.markdown(f"*{self.motto}*")
    
    def get_logo_info(self):
        """Возвращает информацию о логотипах."""
        return {
            'fullscreen_logo': str(self.fullscreen_logo),
            'wide_logo': str(self.wide_logo),
            'header_logo': str(self.header_logo),
            'fullscreen_exists': self.fullscreen_logo.exists(),
            'wide_exists': self.wide_logo.exists(),
            'header_exists': self.header_logo.exists(),
            'motto': self.motto,
            'motto_en': self.motto_en,
            'project_info': self.project_info
        }

# Функции для удобного использования
def display_fullscreen_logo(width=None, use_container_width=True):
    """Отображает полноэкранный логотип."""
    displayer = FullscreenLogoDisplay()
    return displayer.display_fullscreen_logo(width, use_container_width)

def display_wide_logo(width=None, use_container_width=True):
    """Отображает широкий логотип."""
    displayer = FullscreenLogoDisplay()
    return displayer.display_wide_logo(width, use_container_width)

def display_header_logo(width=None, use_container_width=True):
    """Отображает логотип для заголовка."""
    displayer = FullscreenLogoDisplay()
    return displayer.display_header_logo(width, use_container_width)

def display_main_screen_logo(width=None):
    """Отображает логотип для главного экрана."""
    displayer = FullscreenLogoDisplay()
    return displayer.display_main_screen_logo(width)

def display_transparent_logo(logo_type='wide', width=None, use_container_width=True):
    """Отображает прозрачный логотип."""
    displayer = FullscreenLogoDisplay()
    return displayer.display_transparent_logo(logo_type, width, use_container_width)

def display_centered_logo(width=None, use_container_width=True):
    """Отображает центрированный логотип с текстом под ним."""
    displayer = FullscreenLogoDisplay()
    return displayer.display_centered_logo(width, use_container_width)

def display_minimal_logo(width=None, use_container_width=True):
    """Отображает минимальный логотип с очень маленьким топбаром."""
    displayer = FullscreenLogoDisplay()
    return displayer.display_minimal_logo(width, use_container_width)

def display_sidebar_logo(width=None, use_container_width=True):
    """Отображает логотип оптимизированный для боковой панели."""
    displayer = FullscreenLogoDisplay()
    return displayer.display_sidebar_logo(width, use_container_width)

def display_text_logo(width=200, use_container_width=False):
    """Отображает минимальный текстовый логотип."""
    displayer = FullscreenLogoDisplay()
    return displayer.display_text_logo(width, use_container_width)

def get_fullscreen_logo_info():
    """Возвращает информацию о полноэкранных логотипах."""
    displayer = FullscreenLogoDisplay()
    return displayer.get_logo_info()

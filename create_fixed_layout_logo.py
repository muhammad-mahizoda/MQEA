#!/usr/bin/env python3
"""
Создание логотипа MQEA с исправленной композицией - текст не перекрывает логотип.

Автор: Мухаммад Махизода
Таджикский национальный университет
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Circle, Rectangle, Polygon, FancyBboxPatch
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime

class FixedLayoutLogoGenerator:
    """Генератор логотипа MQEA с исправленной композицией."""
    
    def __init__(self):
        # Улучшенная цветовая палитра
        self.colors = {
            'primary_blue': '#0066CC',
            'light_blue': '#00CCFF',
            'accent_blue': '#4A90E2',
            'white': '#FFFFFF',
            'black': '#000000',
            'dark_gray': '#333333',
            'light_gray': '#666666',
            'transparent': 'none'
        }
        
        # Девиз проекта
        self.motto = "Спокойствие, доверие, стабильность"
        self.motto_en = "Calm, Trust, Stability"
        
        # Настройки качества
        self.dpi = 300
        self.antialiasing = True
        
    def create_fullscreen_logo_fixed(self, size=(1200, 400), color_scheme='blue'):
        """Создает полноэкранный логотип с исправленной композицией."""
        fig, ax = plt.subplots(figsize=(size[0]/100, size[1]/100), dpi=self.dpi)
        ax.set_xlim(0, 24)
        ax.set_ylim(0, 8)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Прозрачный фон
        fig.patch.set_alpha(0.0)
        ax.set_facecolor('none')
        
        # Цвета
        primary_color = self.colors['primary_blue']
        accent_color = self.colors['light_blue']
        
        # Сердце (смещено влево, чтобы освободить место для текста)
        heart_x = np.linspace(-1.5, 1.5, 150)
        heart_y = (np.sqrt(1 - heart_x**2) + np.sqrt(1 - heart_x**2) * np.sin(np.pi * heart_x)) / 2
        
        # Масштабирование и позиционирование сердца (смещено влево)
        heart_x = heart_x * 2.5 + 8  # Смещено влево с 12 до 8
        heart_y = heart_y * 2.5 + 4
        
        # Градиент для сердца
        ax.fill(heart_x, heart_y, color=primary_color, alpha=0.9)
        ax.plot(heart_x, heart_y, color=primary_color, linewidth=4)
        
        # Тень для сердца
        shadow_x = heart_x + 0.2
        shadow_y = heart_y - 0.2
        ax.fill(shadow_x, shadow_y, color='black', alpha=0.3)
        
        # Квантовые элементы вокруг сердца
        for i in range(8):
            angle = i * np.pi / 4
            radius = 2.8
            x = 8 + radius * np.cos(angle)
            y = 4 + radius * np.sin(angle)
            quantum_dot = Circle((x, y), 0.25, color=accent_color, alpha=0.8)
            ax.add_patch(quantum_dot)
            glow = Circle((x, y), 0.4, color=accent_color, alpha=0.3)
            ax.add_patch(glow)
        
        # Дополнительные квантовые элементы внутри сердца
        for i in range(4):
            angle = i * np.pi / 2
            radius = 1.2
            x = 8 + radius * np.cos(angle)
            y = 4 + radius * np.sin(angle)
            inner_dot = Circle((x, y), 0.15, color=accent_color, alpha=0.7)
            ax.add_patch(inner_dot)
        
        # Текст справа от логотипа (не перекрывает)
        text_x = 16  # Справа от логотипа
        
        # Название проекта (крупное)
        ax.text(text_x, 5.5, 'MQEA', fontsize=42, fontweight='bold', 
                ha='center', color=primary_color)
        
        # Полное название
        ax.text(text_x, 4.8, 'Medical Quantum', 
                fontsize=16, ha='center', color=self.colors['dark_gray'])
        ax.text(text_x, 4.4, 'Entanglement Analysis', 
                fontsize=16, ha='center', color=self.colors['dark_gray'])
        
        # Девиз (крупный)
        ax.text(text_x, 3.5, self.motto, 
                fontsize=18, fontweight='bold', ha='center', 
                color=primary_color, style='italic')
        
        # Девиз на английском
        ax.text(text_x, 3.0, self.motto_en, 
                fontsize=14, ha='center', 
                color=self.colors['light_gray'], style='italic')
        
        plt.tight_layout()
        filename = f"mqea_logo_fullscreen_fixed_layout.png"
        plt.savefig(filename, dpi=self.dpi, bbox_inches='tight', 
                   facecolor='none', edgecolor='none', 
                   pad_inches=0.1, transparent=True)
        plt.close()
        return filename
    
    def create_wide_logo_fixed(self, size=(1000, 300), color_scheme='blue'):
        """Создает широкий логотип с исправленной композицией."""
        fig, ax = plt.subplots(figsize=(size[0]/100, size[1]/100), dpi=self.dpi)
        ax.set_xlim(0, 20)
        ax.set_ylim(0, 6)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Прозрачный фон
        fig.patch.set_alpha(0.0)
        ax.set_facecolor('none')
        
        # Цвета
        primary_color = self.colors['primary_blue']
        accent_color = self.colors['light_blue']
        
        # Сердце (смещено влево)
        heart_x = np.linspace(-1.2, 1.2, 120)
        heart_y = (np.sqrt(1 - heart_x**2) + np.sqrt(1 - heart_x**2) * np.sin(np.pi * heart_x)) / 2
        
        # Масштабирование и позиционирование сердца
        heart_x = heart_x * 2.0 + 6  # Смещено влево
        heart_y = heart_y * 2.0 + 3.5
        
        ax.fill(heart_x, heart_y, color=primary_color, alpha=0.9)
        ax.plot(heart_x, heart_y, color=primary_color, linewidth=3)
        
        # Квантовые элементы
        for i in range(6):
            angle = i * np.pi / 3
            radius = 2.2
            x = 6 + radius * np.cos(angle)
            y = 3.5 + radius * np.sin(angle)
            quantum_dot = Circle((x, y), 0.2, color=accent_color, alpha=0.8)
            ax.add_patch(quantum_dot)
            glow = Circle((x, y), 0.35, color=accent_color, alpha=0.3)
            ax.add_patch(glow)
        
        # Дополнительные элементы внутри сердца
        for i in range(3):
            angle = i * 2 * np.pi / 3
            radius = 0.9
            x = 6 + radius * np.cos(angle)
            y = 3.5 + radius * np.sin(angle)
            inner_dot = Circle((x, y), 0.12, color=accent_color, alpha=0.7)
            ax.add_patch(inner_dot)
        
        # Текст справа от логотипа
        text_x = 14
        
        # Название проекта
        ax.text(text_x, 4.5, 'MQEA', fontsize=32, fontweight='bold', 
                ha='center', color=primary_color)
        
        # Полное название
        ax.text(text_x, 3.8, 'Medical Quantum', 
                fontsize=12, ha='center', color=self.colors['dark_gray'])
        ax.text(text_x, 3.4, 'Entanglement Analysis', 
                fontsize=12, ha='center', color=self.colors['dark_gray'])
        
        # Девиз
        ax.text(text_x, 2.8, self.motto, 
                fontsize=14, fontweight='bold', ha='center', 
                color=primary_color, style='italic')
        
        # Девиз на английском
        ax.text(text_x, 2.4, self.motto_en, 
                fontsize=10, ha='center', 
                color=self.colors['light_gray'], style='italic')
        
        plt.tight_layout()
        filename = f"mqea_logo_wide_fixed_layout.png"
        plt.savefig(filename, dpi=self.dpi, bbox_inches='tight', 
                   facecolor='none', edgecolor='none', 
                   pad_inches=0.05, transparent=True)
        plt.close()
        return filename
    
    def create_header_logo_fixed(self, size=(800, 200), color_scheme='blue'):
        """Создает логотип для заголовка с исправленной композицией."""
        fig, ax = plt.subplots(figsize=(size[0]/100, size[1]/100), dpi=self.dpi)
        ax.set_xlim(0, 16)
        ax.set_ylim(0, 4)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Прозрачный фон
        fig.patch.set_alpha(0.0)
        ax.set_facecolor('none')
        
        # Цвета
        primary_color = self.colors['primary_blue']
        accent_color = self.colors['light_blue']
        
        # Сердце (смещено влево)
        heart_x = np.linspace(-0.8, 0.8, 80)
        heart_y = (np.sqrt(1 - heart_x**2) + np.sqrt(1 - heart_x**2) * np.sin(np.pi * heart_x)) / 2
        
        # Масштабирование и позиционирование сердца
        heart_x = heart_x * 1.5 + 5  # Смещено влево
        heart_y = heart_y * 1.5 + 2.5
        
        ax.fill(heart_x, heart_y, color=primary_color, alpha=0.9)
        ax.plot(heart_x, heart_y, color=primary_color, linewidth=2.5)
        
        # Квантовые элементы
        for i in range(5):
            angle = i * 2 * np.pi / 5
            radius = 1.8
            x = 5 + radius * np.cos(angle)
            y = 2.5 + radius * np.sin(angle)
            quantum_dot = Circle((x, y), 0.15, color=accent_color, alpha=0.8)
            ax.add_patch(quantum_dot)
        
        # Дополнительные элементы внутри сердца
        for i in range(2):
            angle = i * np.pi
            radius = 0.6
            x = 5 + radius * np.cos(angle)
            y = 2.5 + radius * np.sin(angle)
            inner_dot = Circle((x, y), 0.1, color=accent_color, alpha=0.7)
            ax.add_patch(inner_dot)
        
        # Текст справа от логотипа
        text_x = 11
        
        # Название проекта
        ax.text(text_x, 2.8, 'MQEA', fontsize=24, fontweight='bold', 
                ha='center', color=primary_color)
        
        # Девиз
        ax.text(text_x, 2.2, self.motto, 
                fontsize=10, fontweight='bold', ha='center', 
                color=primary_color, style='italic')
        
        plt.tight_layout()
        filename = f"mqea_logo_header_fixed_layout.png"
        plt.savefig(filename, dpi=self.dpi, bbox_inches='tight', 
                   facecolor='none', edgecolor='none', 
                   pad_inches=0.03, transparent=True)
        plt.close()
        return filename
    
    def create_centered_logo_fixed(self, size=(800, 300), color_scheme='blue'):
        """Создает центрированный логотип с текстом под ним."""
        fig, ax = plt.subplots(figsize=(size[0]/100, size[1]/100), dpi=self.dpi)
        ax.set_xlim(0, 16)
        ax.set_ylim(0, 6)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Прозрачный фон
        fig.patch.set_alpha(0.0)
        ax.set_facecolor('none')
        
        # Цвета
        primary_color = self.colors['primary_blue']
        accent_color = self.colors['light_blue']
        
        # Сердце в центре
        heart_x = np.linspace(-1.2, 1.2, 120)
        heart_y = (np.sqrt(1 - heart_x**2) + np.sqrt(1 - heart_x**2) * np.sin(np.pi * heart_x)) / 2
        
        # Масштабирование и позиционирование сердца
        heart_x = heart_x * 2.0 + 8
        heart_y = heart_y * 2.0 + 4
        
        ax.fill(heart_x, heart_y, color=primary_color, alpha=0.9)
        ax.plot(heart_x, heart_y, color=primary_color, linewidth=3)
        
        # Квантовые элементы
        for i in range(8):
            angle = i * np.pi / 4
            radius = 2.5
            x = 8 + radius * np.cos(angle)
            y = 4 + radius * np.sin(angle)
            quantum_dot = Circle((x, y), 0.2, color=accent_color, alpha=0.8)
            ax.add_patch(quantum_dot)
            glow = Circle((x, y), 0.35, color=accent_color, alpha=0.3)
            ax.add_patch(glow)
        
        # Дополнительные элементы внутри сердца
        for i in range(4):
            angle = i * np.pi / 2
            radius = 1.0
            x = 8 + radius * np.cos(angle)
            y = 4 + radius * np.sin(angle)
            inner_dot = Circle((x, y), 0.12, color=accent_color, alpha=0.7)
            ax.add_patch(inner_dot)
        
        # Текст под логотипом
        text_y = 1.5
        
        # Название проекта
        ax.text(8, text_y, 'MQEA', fontsize=28, fontweight='bold', 
                ha='center', color=primary_color)
        
        # Полное название
        ax.text(8, text_y - 0.6, 'Medical Quantum Entanglement Analysis', 
                fontsize=12, ha='center', color=self.colors['dark_gray'])
        
        # Девиз
        ax.text(8, text_y - 1.2, self.motto, 
                fontsize=12, fontweight='bold', ha='center', 
                color=primary_color, style='italic')
        
        # Девиз на английском
        ax.text(8, text_y - 1.6, self.motto_en, 
                fontsize=10, ha='center', 
                color=self.colors['light_gray'], style='italic')
        
        plt.tight_layout()
        filename = f"mqea_logo_centered_fixed_layout.png"
        plt.savefig(filename, dpi=self.dpi, bbox_inches='tight', 
                   facecolor='none', edgecolor='none', 
                   pad_inches=0.05, transparent=True)
        plt.close()
        return filename
    
    def generate_all_fixed_layout_logos(self):
        """Генерирует все варианты логотипов с исправленной композицией."""
        print("🔧 Создание логотипов MQEA с исправленной композицией...")
        print("Автор: Мухаммад Махизода")
        print("Таджикский национальный университет")
        print("=" * 70)
        print(f"📝 Девиз: '{self.motto}'")
        print(f"🎯 Качество: {self.dpi} DPI")
        print(f"🎨 Фон: Прозрачный")
        print(f"❌ Медицинский крест: Убран")
        print(f"🔧 Композиция: Исправлена (текст не перекрывает логотип)")
        print("=" * 70)
        
        generated_files = []
        
        # Генерация всех вариантов
        logo_types = [
            ('create_fullscreen_logo_fixed', 'Полноэкранный логотип с исправленной композицией'),
            ('create_wide_logo_fixed', 'Широкий логотип с исправленной композицией'),
            ('create_header_logo_fixed', 'Логотип для заголовка с исправленной композицией'),
            ('create_centered_logo_fixed', 'Центрированный логотип с текстом под ним')
        ]
        
        for logo_type, description in logo_types:
            print(f"\n🔬 Создание: {description}")
            
            try:
                if logo_type == 'create_fullscreen_logo_fixed':
                    filename = self.create_fullscreen_logo_fixed()
                elif logo_type == 'create_wide_logo_fixed':
                    filename = self.create_wide_logo_fixed()
                elif logo_type == 'create_header_logo_fixed':
                    filename = self.create_header_logo_fixed()
                elif logo_type == 'create_centered_logo_fixed':
                    filename = self.create_centered_logo_fixed()
                
                generated_files.append(filename)
                print(f"  ✅ Создан: {filename}")
                
            except Exception as e:
                print(f"  ❌ Ошибка: {e}")
        
        print(f"\n🎉 Генерация завершена!")
        print(f"📁 Создано файлов: {len(generated_files)}")
        
        return generated_files

def main():
    """Основная функция."""
    generator = FixedLayoutLogoGenerator()
    generated_files = generator.generate_all_fixed_layout_logos()
    
    print("\n📋 Созданные логотипы с исправленной композицией:")
    for i, filename in enumerate(generated_files, 1):
        print(f"{i:2d}. {filename}")
    
    print("\n💡 Рекомендации:")
    print("• mqea_logo_fullscreen_fixed_layout.png - для полного экрана")
    print("• mqea_logo_wide_fixed_layout.png - для широких экранов")
    print("• mqea_logo_header_fixed_layout.png - для заголовков")
    print("• mqea_logo_centered_fixed_layout.png - центрированный вариант")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Создание компактных логотипов MQEA с уменьшенным топбаром.

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

class CompactLogoGenerator:
    """Генератор компактных логотипов MQEA с уменьшенным топбаром."""
    
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
        
    def create_compact_fullscreen_logo(self, size=(1000, 300), color_scheme='blue'):
        """Создает компактный полноэкранный логотип с уменьшенным топбаром."""
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
        
        # Сердце (компактное)
        heart_x = np.linspace(-1.2, 1.2, 120)
        heart_y = (np.sqrt(1 - heart_x**2) + np.sqrt(1 - heart_x**2) * np.sin(np.pi * heart_x)) / 2
        
        # Масштабирование и позиционирование сердца
        heart_x = heart_x * 1.8 + 6  # Компактное сердце
        heart_y = heart_y * 1.8 + 3.5
        
        # Градиент для сердца
        ax.fill(heart_x, heart_y, color=primary_color, alpha=0.9)
        ax.plot(heart_x, heart_y, color=primary_color, linewidth=3)
        
        # Тень для сердца
        shadow_x = heart_x + 0.15
        shadow_y = heart_y - 0.15
        ax.fill(shadow_x, shadow_y, color='black', alpha=0.2)
        
        # Квантовые элементы (компактные)
        for i in range(6):
            angle = i * np.pi / 3
            radius = 2.2
            x = 6 + radius * np.cos(angle)
            y = 3.5 + radius * np.sin(angle)
            quantum_dot = Circle((x, y), 0.2, color=accent_color, alpha=0.8)
            ax.add_patch(quantum_dot)
            glow = Circle((x, y), 0.3, color=accent_color, alpha=0.3)
            ax.add_patch(glow)
        
        # Дополнительные элементы внутри сердца
        for i in range(3):
            angle = i * 2 * np.pi / 3
            radius = 0.9
            x = 6 + radius * np.cos(angle)
            y = 3.5 + radius * np.sin(angle)
            inner_dot = Circle((x, y), 0.12, color=accent_color, alpha=0.7)
            ax.add_patch(inner_dot)
        
        # Текст справа от логотипа (компактный)
        text_x = 14
        
        # Название проекта (уменьшенное)
        ax.text(text_x, 4.2, 'MQEA', fontsize=28, fontweight='bold', 
                ha='center', color=primary_color)
        
        # Полное название (компактное)
        ax.text(text_x, 3.6, 'Medical Quantum', 
                fontsize=11, ha='center', color=self.colors['dark_gray'])
        ax.text(text_x, 3.3, 'Entanglement Analysis', 
                fontsize=11, ha='center', color=self.colors['dark_gray'])
        
        # Девиз (компактный)
        ax.text(text_x, 2.8, self.motto, 
                fontsize=12, fontweight='bold', ha='center', 
                color=primary_color, style='italic')
        
        # Девиз на английском (компактный)
        ax.text(text_x, 2.4, self.motto_en, 
                fontsize=9, ha='center', 
                color=self.colors['light_gray'], style='italic')
        
        plt.tight_layout()
        filename = f"mqea_logo_compact_fullscreen.png"
        plt.savefig(filename, dpi=self.dpi, bbox_inches='tight', 
                   facecolor='none', edgecolor='none', 
                   pad_inches=0.05, transparent=True)
        plt.close()
        return filename
    
    def create_compact_wide_logo(self, size=(800, 200), color_scheme='blue'):
        """Создает компактный широкий логотип."""
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
        
        # Сердце (компактное)
        heart_x = np.linspace(-0.8, 0.8, 80)
        heart_y = (np.sqrt(1 - heart_x**2) + np.sqrt(1 - heart_x**2) * np.sin(np.pi * heart_x)) / 2
        
        # Масштабирование и позиционирование сердца
        heart_x = heart_x * 1.5 + 5
        heart_y = heart_y * 1.5 + 2.5
        
        ax.fill(heart_x, heart_y, color=primary_color, alpha=0.9)
        ax.plot(heart_x, heart_y, color=primary_color, linewidth=2.5)
        
        # Квантовые элементы (компактные)
        for i in range(5):
            angle = i * 2 * np.pi / 5
            radius = 1.8
            x = 5 + radius * np.cos(angle)
            y = 2.5 + radius * np.sin(angle)
            quantum_dot = Circle((x, y), 0.15, color=accent_color, alpha=0.8)
            ax.add_patch(quantum_dot)
            glow = Circle((x, y), 0.25, color=accent_color, alpha=0.3)
            ax.add_patch(glow)
        
        # Дополнительные элементы внутри сердца
        for i in range(2):
            angle = i * np.pi
            radius = 0.6
            x = 5 + radius * np.cos(angle)
            y = 2.5 + radius * np.sin(angle)
            inner_dot = Circle((x, y), 0.1, color=accent_color, alpha=0.7)
            ax.add_patch(inner_dot)
        
        # Текст справа от логотипа (компактный)
        text_x = 11
        
        # Название проекта (компактное)
        ax.text(text_x, 3.0, 'MQEA', fontsize=22, fontweight='bold', 
                ha='center', color=primary_color)
        
        # Полное название (компактное)
        ax.text(text_x, 2.5, 'Medical Quantum', 
                fontsize=9, ha='center', color=self.colors['dark_gray'])
        ax.text(text_x, 2.2, 'Entanglement Analysis', 
                fontsize=9, ha='center', color=self.colors['dark_gray'])
        
        # Девиз (компактный)
        ax.text(text_x, 1.8, self.motto, 
                fontsize=10, fontweight='bold', ha='center', 
                color=primary_color, style='italic')
        
        # Девиз на английском (компактный)
        ax.text(text_x, 1.5, self.motto_en, 
                fontsize=8, ha='center', 
                color=self.colors['light_gray'], style='italic')
        
        plt.tight_layout()
        filename = f"mqea_logo_compact_wide.png"
        plt.savefig(filename, dpi=self.dpi, bbox_inches='tight', 
                   facecolor='none', edgecolor='none', 
                   pad_inches=0.03, transparent=True)
        plt.close()
        return filename
    
    def create_compact_header_logo(self, size=(600, 150), color_scheme='blue'):
        """Создает компактный логотип для заголовка."""
        fig, ax = plt.subplots(figsize=(size[0]/100, size[1]/100), dpi=self.dpi)
        ax.set_xlim(0, 12)
        ax.set_ylim(0, 3)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Прозрачный фон
        fig.patch.set_alpha(0.0)
        ax.set_facecolor('none')
        
        # Цвета
        primary_color = self.colors['primary_blue']
        accent_color = self.colors['light_blue']
        
        # Сердце (очень компактное)
        heart_x = np.linspace(-0.6, 0.6, 60)
        heart_y = (np.sqrt(1 - heart_x**2) + np.sqrt(1 - heart_x**2) * np.sin(np.pi * heart_x)) / 2
        
        # Масштабирование и позиционирование сердца
        heart_x = heart_x * 1.2 + 4
        heart_y = heart_y * 1.2 + 1.8
        
        ax.fill(heart_x, heart_y, color=primary_color, alpha=0.9)
        ax.plot(heart_x, heart_y, color=primary_color, linewidth=2)
        
        # Квантовые элементы (компактные)
        for i in range(4):
            angle = i * np.pi / 2
            radius = 1.4
            x = 4 + radius * np.cos(angle)
            y = 1.8 + radius * np.sin(angle)
            quantum_dot = Circle((x, y), 0.12, color=accent_color, alpha=0.8)
            ax.add_patch(quantum_dot)
        
        # Дополнительные элементы внутри сердца
        for i in range(2):
            angle = i * np.pi
            radius = 0.4
            x = 4 + radius * np.cos(angle)
            y = 1.8 + radius * np.sin(angle)
            inner_dot = Circle((x, y), 0.08, color=accent_color, alpha=0.7)
            ax.add_patch(inner_dot)
        
        # Текст справа от логотипа (компактный)
        text_x = 8.5
        
        # Название проекта (компактное)
        ax.text(text_x, 2.2, 'MQEA', fontsize=18, fontweight='bold', 
                ha='center', color=primary_color)
        
        # Девиз (компактный)
        ax.text(text_x, 1.6, self.motto, 
                fontsize=8, fontweight='bold', ha='center', 
                color=primary_color, style='italic')
        
        plt.tight_layout()
        filename = f"mqea_logo_compact_header.png"
        plt.savefig(filename, dpi=self.dpi, bbox_inches='tight', 
                   facecolor='none', edgecolor='none', 
                   pad_inches=0.02, transparent=True)
        plt.close()
        return filename
    
    def create_minimal_logo(self, size=(400, 100), color_scheme='blue'):
        """Создает минимальный логотип с очень маленьким топбаром."""
        fig, ax = plt.subplots(figsize=(size[0]/100, size[1]/100), dpi=self.dpi)
        ax.set_xlim(0, 8)
        ax.set_ylim(0, 2)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Прозрачный фон
        fig.patch.set_alpha(0.0)
        ax.set_facecolor('none')
        
        # Цвета
        primary_color = self.colors['primary_blue']
        accent_color = self.colors['light_blue']
        
        # Сердце (минимальное)
        heart_x = np.linspace(-0.4, 0.4, 40)
        heart_y = (np.sqrt(1 - heart_x**2) + np.sqrt(1 - heart_x**2) * np.sin(np.pi * heart_x)) / 2
        
        # Масштабирование и позиционирование сердца
        heart_x = heart_x * 0.8 + 3
        heart_y = heart_y * 0.8 + 1.2
        
        ax.fill(heart_x, heart_y, color=primary_color, alpha=0.9)
        ax.plot(heart_x, heart_y, color=primary_color, linewidth=1.5)
        
        # Квантовые элементы (минимальные)
        for i in range(3):
            angle = i * 2 * np.pi / 3
            radius = 1.0
            x = 3 + radius * np.cos(angle)
            y = 1.2 + radius * np.sin(angle)
            quantum_dot = Circle((x, y), 0.08, color=accent_color, alpha=0.8)
            ax.add_patch(quantum_dot)
        
        # Текст справа от логотипа (минимальный)
        text_x = 6
        
        # Название проекта (минимальное)
        ax.text(text_x, 1.4, 'MQEA', fontsize=12, fontweight='bold', 
                ha='center', color=primary_color)
        
        # Девиз (минимальный)
        ax.text(text_x, 0.8, self.motto, 
                fontsize=6, fontweight='bold', ha='center', 
                color=primary_color, style='italic')
        
        plt.tight_layout()
        filename = f"mqea_logo_minimal.png"
        plt.savefig(filename, dpi=self.dpi, bbox_inches='tight', 
                   facecolor='none', edgecolor='none', 
                   pad_inches=0.01, transparent=True)
        plt.close()
        return filename
    
    def generate_all_compact_logos(self):
        """Генерирует все варианты компактных логотипов."""
        print("📏 Создание компактных логотипов MQEA с уменьшенным топбаром...")
        print("Автор: Мухаммад Махизода")
        print("Таджикский национальный университет")
        print("=" * 70)
        print(f"📝 Девиз: '{self.motto}'")
        print(f"🎯 Качество: {self.dpi} DPI")
        print(f"🎨 Фон: Прозрачный")
        print(f"❌ Медицинский крест: Убран")
        print(f"🔧 Композиция: Исправлена")
        print(f"📏 Топбар: Уменьшен")
        print("=" * 70)
        
        generated_files = []
        
        # Генерация всех вариантов
        logo_types = [
            ('create_compact_fullscreen_logo', 'Компактный полноэкранный логотип'),
            ('create_compact_wide_logo', 'Компактный широкий логотип'),
            ('create_compact_header_logo', 'Компактный логотип для заголовка'),
            ('create_minimal_logo', 'Минимальный логотип')
        ]
        
        for logo_type, description in logo_types:
            print(f"\n🔬 Создание: {description}")
            
            try:
                if logo_type == 'create_compact_fullscreen_logo':
                    filename = self.create_compact_fullscreen_logo()
                elif logo_type == 'create_compact_wide_logo':
                    filename = self.create_compact_wide_logo()
                elif logo_type == 'create_compact_header_logo':
                    filename = self.create_compact_header_logo()
                elif logo_type == 'create_minimal_logo':
                    filename = self.create_minimal_logo()
                
                generated_files.append(filename)
                print(f"  ✅ Создан: {filename}")
                
            except Exception as e:
                print(f"  ❌ Ошибка: {e}")
        
        print(f"\n🎉 Генерация завершена!")
        print(f"📁 Создано файлов: {len(generated_files)}")
        
        return generated_files

def main():
    """Основная функция."""
    generator = CompactLogoGenerator()
    generated_files = generator.generate_all_compact_logos()
    
    print("\n📋 Созданные компактные логотипы:")
    for i, filename in enumerate(generated_files, 1):
        print(f"{i:2d}. {filename}")
    
    print("\n💡 Рекомендации:")
    print("• mqea_logo_compact_fullscreen.png - компактный для полного экрана")
    print("• mqea_logo_compact_wide.png - компактный для широких экранов")
    print("• mqea_logo_compact_header.png - компактный для заголовков")
    print("• mqea_logo_minimal.png - минимальный вариант")

if __name__ == "__main__":
    main()

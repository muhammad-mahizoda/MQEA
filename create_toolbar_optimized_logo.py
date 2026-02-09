#!/usr/bin/env python3
"""
Создание логотипов MQEA оптимизированных для работы с тулбаром.

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

class ToolbarOptimizedLogoGenerator:
    """Генератор логотипов MQEA оптимизированных для тулбара."""
    
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
        
    def create_toolbar_logo(self, size=(600, 120), color_scheme='blue'):
        """Создает логотип оптимизированный для тулбара."""
        fig, ax = plt.subplots(figsize=(size[0]/100, size[1]/100), dpi=self.dpi)
        ax.set_xlim(0, 12)
        ax.set_ylim(0, 2.4)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Прозрачный фон
        fig.patch.set_alpha(0.0)
        ax.set_facecolor('none')
        
        # Цвета
        primary_color = self.colors['primary_blue']
        accent_color = self.colors['light_blue']
        
        # Сердце (компактное для тулбара)
        heart_x = np.linspace(-0.5, 0.5, 50)
        heart_y = (np.sqrt(1 - heart_x**2) + np.sqrt(1 - heart_x**2) * np.sin(np.pi * heart_x)) / 2
        
        # Масштабирование и позиционирование сердца
        heart_x = heart_x * 0.8 + 3
        heart_y = heart_y * 0.8 + 1.2
        
        ax.fill(heart_x, heart_y, color=primary_color, alpha=0.9)
        ax.plot(heart_x, heart_y, color=primary_color, linewidth=1.5)
        
        # Квантовые элементы (компактные)
        for i in range(4):
            angle = i * np.pi / 2
            radius = 1.0
            x = 3 + radius * np.cos(angle)
            y = 1.2 + radius * np.sin(angle)
            quantum_dot = Circle((x, y), 0.08, color=accent_color, alpha=0.8)
            ax.add_patch(quantum_dot)
        
        # Дополнительные элементы внутри сердца
        for i in range(2):
            angle = i * np.pi
            radius = 0.3
            x = 3 + radius * np.cos(angle)
            y = 1.2 + radius * np.sin(angle)
            inner_dot = Circle((x, y), 0.05, color=accent_color, alpha=0.7)
            ax.add_patch(inner_dot)
        
        # Текст справа от логотипа (компактный)
        text_x = 8
        
        # Название проекта (компактное)
        ax.text(text_x, 1.6, 'MQEA', fontsize=14, fontweight='bold', 
                ha='center', color=primary_color)
        
        # Полное название (компактное)
        ax.text(text_x, 1.2, 'Medical Quantum', 
                fontsize=7, ha='center', color=self.colors['dark_gray'])
        ax.text(text_x, 1.0, 'Entanglement Analysis', 
                fontsize=7, ha='center', color=self.colors['dark_gray'])
        
        # Девиз (компактный)
        ax.text(text_x, 0.6, self.motto, 
                fontsize=8, fontweight='bold', ha='center', 
                color=primary_color, style='italic')
        
        plt.tight_layout()
        filename = f"mqea_logo_toolbar_optimized.png"
        plt.savefig(filename, dpi=self.dpi, bbox_inches='tight', 
                   facecolor='none', edgecolor='none', 
                   pad_inches=0.02, transparent=True)
        plt.close()
        return filename
    
    def create_header_toolbar_logo(self, size=(500, 100), color_scheme='blue'):
        """Создает логотип для заголовка с учетом тулбара."""
        fig, ax = plt.subplots(figsize=(size[0]/100, size[1]/100), dpi=self.dpi)
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 2)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Прозрачный фон
        fig.patch.set_alpha(0.0)
        ax.set_facecolor('none')
        
        # Цвета
        primary_color = self.colors['primary_blue']
        accent_color = self.colors['light_blue']
        
        # Сердце (очень компактное)
        heart_x = np.linspace(-0.4, 0.4, 40)
        heart_y = (np.sqrt(1 - heart_x**2) + np.sqrt(1 - heart_x**2) * np.sin(np.pi * heart_x)) / 2
        
        # Масштабирование и позиционирование сердца
        heart_x = heart_x * 0.6 + 2.5
        heart_y = heart_y * 0.6 + 1.0
        
        ax.fill(heart_x, heart_y, color=primary_color, alpha=0.9)
        ax.plot(heart_x, heart_y, color=primary_color, linewidth=1.2)
        
        # Квантовые элементы (минимальные)
        for i in range(3):
            angle = i * 2 * np.pi / 3
            radius = 0.8
            x = 2.5 + radius * np.cos(angle)
            y = 1.0 + radius * np.sin(angle)
            quantum_dot = Circle((x, y), 0.06, color=accent_color, alpha=0.8)
            ax.add_patch(quantum_dot)
        
        # Текст справа от логотипа (минимальный)
        text_x = 7
        
        # Название проекта (минимальное)
        ax.text(text_x, 1.3, 'MQEA', fontsize=12, fontweight='bold', 
                ha='center', color=primary_color)
        
        # Девиз (минимальный)
        ax.text(text_x, 0.7, self.motto, 
                fontsize=6, fontweight='bold', ha='center', 
                color=primary_color, style='italic')
        
        plt.tight_layout()
        filename = f"mqea_logo_header_toolbar.png"
        plt.savefig(filename, dpi=self.dpi, bbox_inches='tight', 
                   facecolor='none', edgecolor='none', 
                   pad_inches=0.01, transparent=True)
        plt.close()
        return filename
    
    def create_sidebar_toolbar_logo(self, size=(300, 80), color_scheme='blue'):
        """Создает логотип для боковой панели с учетом тулбара."""
        fig, ax = plt.subplots(figsize=(size[0]/100, size[1]/100), dpi=self.dpi)
        ax.set_xlim(0, 6)
        ax.set_ylim(0, 1.6)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Прозрачный фон
        fig.patch.set_alpha(0.0)
        ax.set_facecolor('none')
        
        # Цвета
        primary_color = self.colors['primary_blue']
        accent_color = self.colors['light_blue']
        
        # Сердце (минимальное)
        heart_x = np.linspace(-0.3, 0.3, 30)
        heart_y = (np.sqrt(1 - heart_x**2) + np.sqrt(1 - heart_x**2) * np.sin(np.pi * heart_x)) / 2
        
        # Масштабирование и позиционирование сердца
        heart_x = heart_x * 0.5 + 3
        heart_y = heart_y * 0.5 + 0.8
        
        ax.fill(heart_x, heart_y, color=primary_color, alpha=0.9)
        ax.plot(heart_x, heart_y, color=primary_color, linewidth=1)
        
        # Квантовые элементы (минимальные)
        for i in range(3):
            angle = i * 2 * np.pi / 3
            radius = 0.6
            x = 3 + radius * np.cos(angle)
            y = 0.8 + radius * np.sin(angle)
            quantum_dot = Circle((x, y), 0.04, color=accent_color, alpha=0.8)
            ax.add_patch(quantum_dot)
        
        # Текст под логотипом (минимальный)
        text_y = 0.3
        
        # Название проекта (минимальное)
        ax.text(3, text_y, 'MQEA', fontsize=10, fontweight='bold', 
                ha='center', color=primary_color)
        
        plt.tight_layout()
        filename = f"mqea_logo_sidebar_toolbar.png"
        plt.savefig(filename, dpi=self.dpi, bbox_inches='tight', 
                   facecolor='none', edgecolor='none', 
                   pad_inches=0.01, transparent=True)
        plt.close()
        return filename
    
    def create_ultra_compact_logo(self, size=(200, 60), color_scheme='blue'):
        """Создает ультра-компактный логотип для тулбара."""
        fig, ax = plt.subplots(figsize=(size[0]/100, size[1]/100), dpi=self.dpi)
        ax.set_xlim(0, 4)
        ax.set_ylim(0, 1.2)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Прозрачный фон
        fig.patch.set_alpha(0.0)
        ax.set_facecolor('none')
        
        # Цвета
        primary_color = self.colors['primary_blue']
        accent_color = self.colors['light_blue']
        
        # Сердце (ультра-компактное)
        heart_x = np.linspace(-0.2, 0.2, 20)
        heart_y = (np.sqrt(1 - heart_x**2) + np.sqrt(1 - heart_x**2) * np.sin(np.pi * heart_x)) / 2
        
        # Масштабирование и позиционирование сердца
        heart_x = heart_x * 0.3 + 2
        heart_y = heart_y * 0.3 + 0.6
        
        ax.fill(heart_x, heart_y, color=primary_color, alpha=0.9)
        ax.plot(heart_x, heart_y, color=primary_color, linewidth=0.8)
        
        # Квантовые элементы (ультра-компактные)
        for i in range(2):
            angle = i * np.pi
            radius = 0.4
            x = 2 + radius * np.cos(angle)
            y = 0.6 + radius * np.sin(angle)
            quantum_dot = Circle((x, y), 0.03, color=accent_color, alpha=0.8)
            ax.add_patch(quantum_dot)
        
        # Текст справа от логотипа (ультра-компактный)
        text_x = 3.2
        
        # Название проекта (ультра-компактное)
        ax.text(text_x, 0.7, 'MQEA', fontsize=8, fontweight='bold', 
                ha='center', color=primary_color)
        
        # Девиз (ультра-компактный)
        ax.text(text_x, 0.4, self.motto, 
                fontsize=4, fontweight='bold', ha='center', 
                color=primary_color, style='italic')
        
        plt.tight_layout()
        filename = f"mqea_logo_ultra_compact.png"
        plt.savefig(filename, dpi=self.dpi, bbox_inches='tight', 
                   facecolor='none', edgecolor='none', 
                   pad_inches=0.005, transparent=True)
        plt.close()
        return filename
    
    def generate_all_toolbar_logos(self):
        """Генерирует все варианты логотипов оптимизированных для тулбара."""
        print("🔧 Создание логотипов MQEA оптимизированных для тулбара...")
        print("Автор: Мухаммад Махизода")
        print("Таджикский национальный университет")
        print("=" * 70)
        print(f"📝 Девиз: '{self.motto}'")
        print(f"🎯 Качество: {self.dpi} DPI")
        print(f"🎨 Фон: Прозрачный")
        print(f"❌ Медицинский крест: Убран")
        print(f"🔧 Композиция: Исправлена")
        print(f"📏 Топбар: Уменьшен")
        print(f"🔧 Тулбар: Оптимизирован")
        print("=" * 70)
        
        generated_files = []
        
        # Генерация всех вариантов
        logo_types = [
            ('create_toolbar_logo', 'Логотип оптимизированный для тулбара'),
            ('create_header_toolbar_logo', 'Логотип заголовка с учетом тулбара'),
            ('create_sidebar_toolbar_logo', 'Логотип боковой панели с учетом тулбара'),
            ('create_ultra_compact_logo', 'Ультра-компактный логотип для тулбара')
        ]
        
        for logo_type, description in logo_types:
            print(f"\n🔬 Создание: {description}")
            
            try:
                if logo_type == 'create_toolbar_logo':
                    filename = self.create_toolbar_logo()
                elif logo_type == 'create_header_toolbar_logo':
                    filename = self.create_header_toolbar_logo()
                elif logo_type == 'create_sidebar_toolbar_logo':
                    filename = self.create_sidebar_toolbar_logo()
                elif logo_type == 'create_ultra_compact_logo':
                    filename = self.create_ultra_compact_logo()
                
                generated_files.append(filename)
                print(f"  ✅ Создан: {filename}")
                
            except Exception as e:
                print(f"  ❌ Ошибка: {e}")
        
        print(f"\n🎉 Генерация завершена!")
        print(f"📁 Создано файлов: {len(generated_files)}")
        
        return generated_files

def main():
    """Основная функция."""
    generator = ToolbarOptimizedLogoGenerator()
    generated_files = generator.generate_all_toolbar_logos()
    
    print("\n📋 Созданные логотипы оптимизированные для тулбара:")
    for i, filename in enumerate(generated_files, 1):
        print(f"{i:2d}. {filename}")
    
    print("\n💡 Рекомендации:")
    print("• mqea_logo_toolbar_optimized.png - основной для тулбара")
    print("• mqea_logo_header_toolbar.png - для заголовка с тулбаром")
    print("• mqea_logo_sidebar_toolbar.png - для боковой панели")
    print("• mqea_logo_ultra_compact.png - ультра-компактный для тулбара")

if __name__ == "__main__":
    main()

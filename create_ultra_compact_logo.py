#!/usr/bin/env python3
"""
Создание ультра-компактного логотипа MQEA для размещения под тулбаром.

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

class UltraCompactLogoGenerator:
    """Генератор ультра-компактного логотипа MQEA."""
    
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
        
    def create_ultra_compact_main_logo(self, size=(400, 80), color_scheme='blue'):
        """Создает ультра-компактный основной логотип."""
        fig, ax = plt.subplots(figsize=(size[0]/100, size[1]/100), dpi=self.dpi)
        ax.set_xlim(0, 8)
        ax.set_ylim(0, 1.6)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Прозрачный фон
        fig.patch.set_alpha(0.0)
        ax.set_facecolor('none')
        
        # Цвета
        primary_color = self.colors['primary_blue']
        accent_color = self.colors['light_blue']
        
        # Сердце (ультра-компактное)
        heart_x = np.linspace(-0.3, 0.3, 30)
        heart_y = (np.sqrt(1 - heart_x**2) + np.sqrt(1 - heart_x**2) * np.sin(np.pi * heart_x)) / 2
        
        # Масштабирование и позиционирование сердца
        heart_x = heart_x * 0.4 + 2
        heart_y = heart_y * 0.4 + 0.8
        
        ax.fill(heart_x, heart_y, color=primary_color, alpha=0.9)
        ax.plot(heart_x, heart_y, color=primary_color, linewidth=0.8)
        
        # Медицинский крест (ультра-компактный)
        cross_center = (2, 0.8)
        cross_vertical = Rectangle((cross_center[0]-0.06, cross_center[1]-0.24), 
                                 0.12, 0.48, color=self.colors['white'], alpha=0.95)
        cross_horizontal = Rectangle((cross_center[0]-0.24, cross_center[1]-0.06), 
                                   0.48, 0.12, color=self.colors['white'], alpha=0.95)
        ax.add_patch(cross_vertical)
        ax.add_patch(cross_horizontal)
        
        # Квантовые элементы (ультра-компактные)
        for i in range(3):
            angle = i * 2 * np.pi / 3
            radius = 0.4
            x = 2 + radius * np.cos(angle)
            y = 0.8 + radius * np.sin(angle)
            quantum_dot = Circle((x, y), 0.03, color=accent_color, alpha=0.8)
            ax.add_patch(quantum_dot)
        
        # Текст справа от логотипа (ультра-компактный)
        text_x = 5.5
        
        # Название проекта (ультра-компактное)
        ax.text(text_x, 1.1, 'MQEA', fontsize=8, fontweight='bold', 
                ha='center', color=primary_color)
        
        # Полное название (ультра-компактное)
        ax.text(text_x, 0.8, 'Medical Quantum', 
                fontsize=4, ha='center', color=self.colors['dark_gray'])
        ax.text(text_x, 0.6, 'Entanglement Analysis', 
                fontsize=4, ha='center', color=self.colors['dark_gray'])
        
        # Девиз (ультра-компактный)
        ax.text(text_x, 0.3, self.motto, 
                fontsize=5, fontweight='bold', ha='center', 
                color=primary_color, style='italic')
        
        plt.tight_layout()
        filename = f"mqea_logo_ultra_compact_main.png"
        plt.savefig(filename, dpi=self.dpi, bbox_inches='tight', 
                   facecolor='none', edgecolor='none', 
                   pad_inches=0.005, transparent=True)
        plt.close()
        return filename
    
    def create_ultra_compact_header_logo(self, size=(300, 60), color_scheme='blue'):
        """Создает ультра-компактный логотип для заголовка."""
        fig, ax = plt.subplots(figsize=(size[0]/100, size[1]/100), dpi=self.dpi)
        ax.set_xlim(0, 6)
        ax.set_ylim(0, 1.2)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Прозрачный фон
        fig.patch.set_alpha(0.0)
        ax.set_facecolor('none')
        
        # Цвета
        primary_color = self.colors['primary_blue']
        accent_color = self.colors['light_blue']
        
        # Сердце (микро-компактное)
        heart_x = np.linspace(-0.25, 0.25, 25)
        heart_y = (np.sqrt(1 - heart_x**2) + np.sqrt(1 - heart_x**2) * np.sin(np.pi * heart_x)) / 2
        
        # Масштабирование и позиционирование сердца
        heart_x = heart_x * 0.3 + 1.5
        heart_y = heart_y * 0.3 + 0.6
        
        ax.fill(heart_x, heart_y, color=primary_color, alpha=0.9)
        ax.plot(heart_x, heart_y, color=primary_color, linewidth=0.6)
        
        # Медицинский крест (микро-компактный)
        cross_center = (1.5, 0.6)
        cross_vertical = Rectangle((cross_center[0]-0.04, cross_center[1]-0.18), 
                                 0.08, 0.36, color=self.colors['white'], alpha=0.95)
        cross_horizontal = Rectangle((cross_center[0]-0.18, cross_center[1]-0.04), 
                                   0.36, 0.08, color=self.colors['white'], alpha=0.95)
        ax.add_patch(cross_vertical)
        ax.add_patch(cross_horizontal)
        
        # Квантовые элементы (микро-компактные)
        for i in range(2):
            angle = i * np.pi
            radius = 0.3
            x = 1.5 + radius * np.cos(angle)
            y = 0.6 + radius * np.sin(angle)
            quantum_dot = Circle((x, y), 0.02, color=accent_color, alpha=0.8)
            ax.add_patch(quantum_dot)
        
        # Текст справа от логотипа (микро-компактный)
        text_x = 4.5
        
        # Название проекта (микро-компактное)
        ax.text(text_x, 0.8, 'MQEA', fontsize=6, fontweight='bold', 
                ha='center', color=primary_color)
        
        # Девиз (микро-компактный)
        ax.text(text_x, 0.4, self.motto, 
                fontsize=3, fontweight='bold', ha='center', 
                color=primary_color, style='italic')
        
        plt.tight_layout()
        filename = f"mqea_logo_ultra_compact_header.png"
        plt.savefig(filename, dpi=self.dpi, bbox_inches='tight', 
                   facecolor='none', edgecolor='none', 
                   pad_inches=0.003, transparent=True)
        plt.close()
        return filename
    
    def create_ultra_compact_sidebar_logo(self, size=(200, 50), color_scheme='blue'):
        """Создает ультра-компактный логотип для боковой панели."""
        fig, ax = plt.subplots(figsize=(size[0]/100, size[1]/100), dpi=self.dpi)
        ax.set_xlim(0, 4)
        ax.set_ylim(0, 1)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Прозрачный фон
        fig.patch.set_alpha(0.0)
        ax.set_facecolor('none')
        
        # Цвета
        primary_color = self.colors['primary_blue']
        accent_color = self.colors['light_blue']
        
        # Сердце (нано-компактное)
        heart_x = np.linspace(-0.2, 0.2, 20)
        heart_y = (np.sqrt(1 - heart_x**2) + np.sqrt(1 - heart_x**2) * np.sin(np.pi * heart_x)) / 2
        
        # Масштабирование и позиционирование сердца
        heart_x = heart_x * 0.25 + 2
        heart_y = heart_y * 0.25 + 0.5
        
        ax.fill(heart_x, heart_y, color=primary_color, alpha=0.9)
        ax.plot(heart_x, heart_y, color=primary_color, linewidth=0.5)
        
        # Медицинский крест (нано-компактный)
        cross_center = (2, 0.5)
        cross_vertical = Rectangle((cross_center[0]-0.03, cross_center[1]-0.12), 
                                 0.06, 0.24, color=self.colors['white'], alpha=0.95)
        cross_horizontal = Rectangle((cross_center[0]-0.12, cross_center[1]-0.03), 
                                   0.24, 0.06, color=self.colors['white'], alpha=0.95)
        ax.add_patch(cross_vertical)
        ax.add_patch(cross_horizontal)
        
        # Квантовые элементы (нано-компактные)
        for i in range(2):
            angle = i * np.pi
            radius = 0.2
            x = 2 + radius * np.cos(angle)
            y = 0.5 + radius * np.sin(angle)
            quantum_dot = Circle((x, y), 0.015, color=accent_color, alpha=0.8)
            ax.add_patch(quantum_dot)
        
        # Текст под логотипом (нано-компактный)
        text_y = 0.2
        
        # Название проекта (нано-компактное)
        ax.text(2, text_y, 'MQEA', fontsize=4, fontweight='bold', 
                ha='center', color=primary_color)
        
        plt.tight_layout()
        filename = f"mqea_logo_ultra_compact_sidebar.png"
        plt.savefig(filename, dpi=self.dpi, bbox_inches='tight', 
                   facecolor='none', edgecolor='none', 
                   pad_inches=0.002, transparent=True)
        plt.close()
        return filename
    
    def create_minimal_text_logo(self, size=(300, 40), color_scheme='blue'):
        """Создает минимальный текстовый логотип."""
        fig, ax = plt.subplots(figsize=(size[0]/100, size[1]/100), dpi=self.dpi)
        ax.set_xlim(0, 6)
        ax.set_ylim(0, 0.8)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Прозрачный фон
        fig.patch.set_alpha(0.0)
        ax.set_facecolor('none')
        
        # Цвета
        primary_color = self.colors['primary_blue']
        
        # Минимальный медицинский символ
        cross_center = (1, 0.4)
        cross_vertical = Rectangle((cross_center[0]-0.05, cross_center[1]-0.2), 
                                 0.1, 0.4, color=primary_color, alpha=0.9)
        cross_horizontal = Rectangle((cross_center[0]-0.2, cross_center[1]-0.05), 
                                   0.4, 0.1, color=primary_color, alpha=0.9)
        ax.add_patch(cross_vertical)
        ax.add_patch(cross_horizontal)
        
        # Текст справа от символа
        text_x = 3
        
        # Название проекта (минимальное)
        ax.text(text_x, 0.5, 'MQEA', fontsize=6, fontweight='bold', 
                ha='center', color=primary_color)
        
        # Девиз (минимальный)
        ax.text(text_x, 0.2, self.motto, 
                fontsize=3, fontweight='bold', ha='center', 
                color=primary_color, style='italic')
        
        plt.tight_layout()
        filename = f"mqea_logo_minimal_text.png"
        plt.savefig(filename, dpi=self.dpi, bbox_inches='tight', 
                   facecolor='none', edgecolor='none', 
                   pad_inches=0.002, transparent=True)
        plt.close()
        return filename
    
    def generate_all_ultra_compact_logos(self):
        """Генерирует все варианты ультра-компактных логотипов."""
        print("📏 Создание ультра-компактных логотипов MQEA...")
        print("Автор: Мухаммад Махизода")
        print("Таджикский национальный университет")
        print("=" * 70)
        print(f"📝 Девиз: '{self.motto}'")
        print(f"🎯 Качество: {self.dpi} DPI")
        print(f"🎨 Фон: Прозрачный")
        print(f"❤️ Сердце: Восстановлено")
        print(f"➕ Медицинский крест: Добавлен")
        print(f"📏 Размер: Ультра-компактный")
        print(f"🔧 Тулбар: Не перекрывается")
        print("=" * 70)
        
        generated_files = []
        
        # Генерация всех вариантов
        logo_types = [
            ('create_ultra_compact_main_logo', 'Ультра-компактный основной логотип'),
            ('create_ultra_compact_header_logo', 'Ультра-компактный логотип для заголовка'),
            ('create_ultra_compact_sidebar_logo', 'Ультра-компактный логотип для боковой панели'),
            ('create_minimal_text_logo', 'Минимальный текстовый логотип')
        ]
        
        for logo_type, description in logo_types:
            print(f"\n🔬 Создание: {description}")
            
            try:
                if logo_type == 'create_ultra_compact_main_logo':
                    filename = self.create_ultra_compact_main_logo()
                elif logo_type == 'create_ultra_compact_header_logo':
                    filename = self.create_ultra_compact_header_logo()
                elif logo_type == 'create_ultra_compact_sidebar_logo':
                    filename = self.create_ultra_compact_sidebar_logo()
                elif logo_type == 'create_minimal_text_logo':
                    filename = self.create_minimal_text_logo()
                
                generated_files.append(filename)
                print(f"  ✅ Создан: {filename}")
                
            except Exception as e:
                print(f"  ❌ Ошибка: {e}")
        
        print(f"\n🎉 Генерация завершена!")
        print(f"📁 Создано файлов: {len(generated_files)}")
        
        return generated_files

def main():
    """Основная функция."""
    generator = UltraCompactLogoGenerator()
    generated_files = generator.generate_all_ultra_compact_logos()
    
    print("\n📋 Созданные ультра-компактные логотипы:")
    for i, filename in enumerate(generated_files, 1):
        print(f"{i:2d}. {filename}")
    
    print("\n💡 Рекомендации:")
    print("• mqea_logo_ultra_compact_main.png - ультра-компактный основной")
    print("• mqea_logo_ultra_compact_header.png - ультра-компактный заголовок")
    print("• mqea_logo_ultra_compact_sidebar.png - ультра-компактная боковая панель")
    print("• mqea_logo_minimal_text.png - минимальный текстовый")

if __name__ == "__main__":
    main()

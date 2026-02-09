#!/usr/bin/env python3
"""
Создание исправленного медицинского логотипа MQEA с правильным дизайном.

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

class CorrectedMedicalLogoGenerator:
    """Генератор исправленного медицинского логотипа MQEA."""
    
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
        
    def create_corrected_main_logo(self, size=(800, 200), color_scheme='blue'):
        """Создает исправленный основной медицинский логотип."""
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
        
        # Сердце (правильная форма)
        heart_x = np.linspace(-1, 1, 100)
        heart_y = (np.sqrt(1 - heart_x**2) + np.sqrt(1 - heart_x**2) * np.sin(np.pi * heart_x)) / 2
        
        # Масштабирование и позиционирование сердца
        heart_x = heart_x * 1.5 + 4
        heart_y = heart_y * 1.5 + 2.5
        
        # Градиент для сердца
        ax.fill(heart_x, heart_y, color=primary_color, alpha=0.9)
        ax.plot(heart_x, heart_y, color=primary_color, linewidth=2.5)
        
        # Тень для сердца
        shadow_x = heart_x + 0.1
        shadow_y = heart_y - 0.1
        ax.fill(shadow_x, shadow_y, color='black', alpha=0.2)
        
        # Медицинский крест (белый, четкий)
        cross_center = (4, 2.5)
        cross_vertical = Rectangle((cross_center[0]-0.2, cross_center[1]-0.8), 
                                 0.4, 1.6, color=self.colors['white'], alpha=0.95)
        cross_horizontal = Rectangle((cross_center[0]-0.8, cross_center[1]-0.2), 
                                   1.6, 0.4, color=self.colors['white'], alpha=0.95)
        ax.add_patch(cross_vertical)
        ax.add_patch(cross_horizontal)
        
        # Квантовые элементы вокруг сердца (медицинские)
        for i in range(6):
            angle = i * np.pi / 3
            radius = 2.0
            x = 4 + radius * np.cos(angle)
            y = 2.5 + radius * np.sin(angle)
            quantum_dot = Circle((x, y), 0.15, color=accent_color, alpha=0.8)
            ax.add_patch(quantum_dot)
            glow = Circle((x, y), 0.25, color=accent_color, alpha=0.3)
            ax.add_patch(glow)
        
        # Текст справа от логотипа
        text_x = 11
        
        # Название проекта
        ax.text(text_x, 3.0, 'MQEA', fontsize=20, fontweight='bold', 
                ha='center', color=primary_color)
        
        # Полное название
        ax.text(text_x, 2.5, 'Medical Quantum', 
                fontsize=10, ha='center', color=self.colors['dark_gray'])
        ax.text(text_x, 2.2, 'Entanglement Analysis', 
                fontsize=10, ha='center', color=self.colors['dark_gray'])
        
        # Девиз
        ax.text(text_x, 1.8, self.motto, 
                fontsize=10, fontweight='bold', ha='center', 
                color=primary_color, style='italic')
        
        # Девиз на английском
        ax.text(text_x, 1.5, self.motto_en, 
                fontsize=8, ha='center', 
                color=self.colors['light_gray'], style='italic')
        
        plt.tight_layout()
        filename = f"mqea_logo_corrected_main.png"
        plt.savefig(filename, dpi=self.dpi, bbox_inches='tight', 
                   facecolor='none', edgecolor='none', 
                   pad_inches=0.03, transparent=True)
        plt.close()
        return filename
    
    def create_corrected_header_logo(self, size=(600, 150), color_scheme='blue'):
        """Создает исправленный логотип для заголовка."""
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
        
        # Сердце (компактное)
        heart_x = np.linspace(-0.8, 0.8, 80)
        heart_y = (np.sqrt(1 - heart_x**2) + np.sqrt(1 - heart_x**2) * np.sin(np.pi * heart_x)) / 2
        
        # Масштабирование и позиционирование сердца
        heart_x = heart_x * 1.2 + 3
        heart_y = heart_y * 1.2 + 1.8
        
        ax.fill(heart_x, heart_y, color=primary_color, alpha=0.9)
        ax.plot(heart_x, heart_y, color=primary_color, linewidth=2)
        
        # Медицинский крест
        cross_center = (3, 1.8)
        cross_vertical = Rectangle((cross_center[0]-0.15, cross_center[1]-0.6), 
                                 0.3, 1.2, color=self.colors['white'], alpha=0.95)
        cross_horizontal = Rectangle((cross_center[0]-0.6, cross_center[1]-0.15), 
                                   1.2, 0.3, color=self.colors['white'], alpha=0.95)
        ax.add_patch(cross_vertical)
        ax.add_patch(cross_horizontal)
        
        # Квантовые элементы
        for i in range(4):
            angle = i * np.pi / 2
            radius = 1.5
            x = 3 + radius * np.cos(angle)
            y = 1.8 + radius * np.sin(angle)
            quantum_dot = Circle((x, y), 0.12, color=accent_color, alpha=0.8)
            ax.add_patch(quantum_dot)
        
        # Текст справа от логотипа
        text_x = 8.5
        
        # Название проекта
        ax.text(text_x, 2.2, 'MQEA', fontsize=16, fontweight='bold', 
                ha='center', color=primary_color)
        
        # Девиз
        ax.text(text_x, 1.6, self.motto, 
                fontsize=8, fontweight='bold', ha='center', 
                color=primary_color, style='italic')
        
        plt.tight_layout()
        filename = f"mqea_logo_corrected_header.png"
        plt.savefig(filename, dpi=self.dpi, bbox_inches='tight', 
                   facecolor='none', edgecolor='none', 
                   pad_inches=0.02, transparent=True)
        plt.close()
        return filename
    
    def create_corrected_sidebar_logo(self, size=(300, 80), color_scheme='blue'):
        """Создает исправленный логотип для боковой панели."""
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
        
        # Медицинский крест (маленький)
        cross_center = (3, 0.8)
        cross_vertical = Rectangle((cross_center[0]-0.08, cross_center[1]-0.3), 
                                 0.16, 0.6, color=self.colors['white'], alpha=0.95)
        cross_horizontal = Rectangle((cross_center[0]-0.3, cross_center[1]-0.08), 
                                   0.6, 0.16, color=self.colors['white'], alpha=0.95)
        ax.add_patch(cross_vertical)
        ax.add_patch(cross_horizontal)
        
        # Квантовые элементы
        for i in range(3):
            angle = i * 2 * np.pi / 3
            radius = 0.6
            x = 3 + radius * np.cos(angle)
            y = 0.8 + radius * np.sin(angle)
            quantum_dot = Circle((x, y), 0.04, color=accent_color, alpha=0.8)
            ax.add_patch(quantum_dot)
        
        # Текст под логотипом
        text_y = 0.3
        
        # Название проекта
        ax.text(3, text_y, 'MQEA', fontsize=10, fontweight='bold', 
                ha='center', color=primary_color)
        
        plt.tight_layout()
        filename = f"mqea_logo_corrected_sidebar.png"
        plt.savefig(filename, dpi=self.dpi, bbox_inches='tight', 
                   facecolor='none', edgecolor='none', 
                   pad_inches=0.01, transparent=True)
        plt.close()
        return filename
    
    def create_corrected_centered_logo(self, size=(800, 300), color_scheme='blue'):
        """Создает исправленный центрированный логотип."""
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
        
        # Медицинский крест (четкий)
        cross_center = (8, 4)
        cross_vertical = Rectangle((cross_center[0]-0.25, cross_center[1]-1.0), 
                                 0.5, 2.0, color=self.colors['white'], alpha=0.95)
        cross_horizontal = Rectangle((cross_center[0]-1.0, cross_center[1]-0.25), 
                                   2.0, 0.5, color=self.colors['white'], alpha=0.95)
        ax.add_patch(cross_vertical)
        ax.add_patch(cross_horizontal)
        
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
        filename = f"mqea_logo_corrected_centered.png"
        plt.savefig(filename, dpi=self.dpi, bbox_inches='tight', 
                   facecolor='none', edgecolor='none', 
                   pad_inches=0.05, transparent=True)
        plt.close()
        return filename
    
    def generate_all_corrected_logos(self):
        """Генерирует все варианты исправленных медицинских логотипов."""
        print("🏥 Создание исправленных медицинских логотипов MQEA...")
        print("Автор: Мухаммад Махизода")
        print("Таджикский национальный университет")
        print("=" * 70)
        print(f"📝 Девиз: '{self.motto}'")
        print(f"🎯 Качество: {self.dpi} DPI")
        print(f"🎨 Фон: Прозрачный")
        print(f"❤️ Сердце: Восстановлено")
        print(f"➕ Медицинский крест: Добавлен")
        print(f"🔧 Дизайн: Исправлен")
        print("=" * 70)
        
        generated_files = []
        
        # Генерация всех вариантов
        logo_types = [
            ('create_corrected_main_logo', 'Исправленный основной медицинский логотип'),
            ('create_corrected_header_logo', 'Исправленный логотип для заголовка'),
            ('create_corrected_sidebar_logo', 'Исправленный логотип для боковой панели'),
            ('create_corrected_centered_logo', 'Исправленный центрированный логотип')
        ]
        
        for logo_type, description in logo_types:
            print(f"\n🔬 Создание: {description}")
            
            try:
                if logo_type == 'create_corrected_main_logo':
                    filename = self.create_corrected_main_logo()
                elif logo_type == 'create_corrected_header_logo':
                    filename = self.create_corrected_header_logo()
                elif logo_type == 'create_corrected_sidebar_logo':
                    filename = self.create_corrected_sidebar_logo()
                elif logo_type == 'create_corrected_centered_logo':
                    filename = self.create_corrected_centered_logo()
                
                generated_files.append(filename)
                print(f"  ✅ Создан: {filename}")
                
            except Exception as e:
                print(f"  ❌ Ошибка: {e}")
        
        print(f"\n🎉 Генерация завершена!")
        print(f"📁 Создано файлов: {len(generated_files)}")
        
        return generated_files

def main():
    """Основная функция."""
    generator = CorrectedMedicalLogoGenerator()
    generated_files = generator.generate_all_corrected_logos()
    
    print("\n📋 Созданные исправленные медицинские логотипы:")
    for i, filename in enumerate(generated_files, 1):
        print(f"{i:2d}. {filename}")
    
    print("\n💡 Рекомендации:")
    print("• mqea_logo_corrected_main.png - основной исправленный")
    print("• mqea_logo_corrected_header.png - для заголовка")
    print("• mqea_logo_corrected_sidebar.png - для боковой панели")
    print("• mqea_logo_corrected_centered.png - центрированный")

if __name__ == "__main__":
    main()

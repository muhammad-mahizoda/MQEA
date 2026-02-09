#!/usr/bin/env python3
"""
Создание оптимизированного логотипа MQEA с улучшенным качеством и размещением.

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

class OptimizedLogoGenerator:
    """Генератор оптимизированного логотипа MQEA."""
    
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
            'background': '#F8F9FA'
        }
        
        # Девиз проекта
        self.motto = "Спокойствие, доверие, стабильность"
        self.motto_en = "Calm, Trust, Stability"
        
        # Настройки качества
        self.dpi = 300
        self.antialiasing = True
        
    def create_premium_logo(self, size=(600, 400), color_scheme='blue'):
        """Создает премиум версию логотипа с улучшенным качеством."""
        fig, ax = plt.subplots(figsize=(size[0]/100, size[1]/100), dpi=self.dpi)
        ax.set_xlim(0, 12)
        ax.set_ylim(0, 8)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Цвета
        primary_color = self.colors['primary_blue']
        accent_color = self.colors['light_blue']
        background_color = self.colors['background']
        
        # Фон с градиентом
        ax.add_patch(Rectangle((0, 0), 12, 8, color=background_color, alpha=0.1))
        
        # Сердце (улучшенное)
        heart_x = np.linspace(-1.2, 1.2, 120)
        heart_y = (np.sqrt(1 - heart_x**2) + np.sqrt(1 - heart_x**2) * np.sin(np.pi * heart_x)) / 2
        
        # Масштабирование и позиционирование сердца
        heart_x = heart_x * 2.5 + 6
        heart_y = heart_y * 2.5 + 5.5
        
        # Градиент для сердца
        ax.fill(heart_x, heart_y, color=primary_color, alpha=0.9)
        ax.plot(heart_x, heart_y, color=primary_color, linewidth=3)
        
        # Тень для сердца
        shadow_x = heart_x + 0.1
        shadow_y = heart_y - 0.1
        ax.fill(shadow_x, shadow_y, color='black', alpha=0.2)
        
        # Медицинский крест (улучшенный)
        cross_center = (6, 5.5)
        cross_vertical = Rectangle((cross_center[0]-0.3, cross_center[1]-1.2), 
                                 0.6, 2.4, color=self.colors['white'], alpha=0.95)
        cross_horizontal = Rectangle((cross_center[0]-1.2, cross_center[1]-0.3), 
                                   2.4, 0.6, color=self.colors['white'], alpha=0.95)
        ax.add_patch(cross_vertical)
        ax.add_patch(cross_horizontal)
        
        # Квантовые элементы (улучшенные)
        for i in range(8):
            angle = i * np.pi / 4
            radius = 2.2
            x = 6 + radius * np.cos(angle)
            y = 5.5 + radius * np.sin(angle)
            # Градиент для квантовых элементов
            quantum_dot = Circle((x, y), 0.2, color=accent_color, alpha=0.8)
            ax.add_patch(quantum_dot)
            # Свечение
            glow = Circle((x, y), 0.3, color=accent_color, alpha=0.3)
            ax.add_patch(glow)
        
        # Название проекта (улучшенное)
        ax.text(6, 3.8, 'MQEA', fontsize=32, fontweight='bold', 
                ha='center', color=primary_color, 
                bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
        
        # Полное название
        ax.text(6, 3.2, 'Medical Quantum Entanglement Analysis', 
                fontsize=14, ha='center', color=self.colors['dark_gray'],
                bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.7))
        
        # Девиз (улучшенный)
        ax.text(6, 2.6, self.motto, 
                fontsize=16, fontweight='bold', ha='center', 
                color=primary_color, style='italic',
                bbox=dict(boxstyle="round,pad=0.3", facecolor=accent_color, alpha=0.2))
        
        # Девиз на английском
        ax.text(6, 2.2, self.motto_en, 
                fontsize=12, ha='center', 
                color=self.colors['light_gray'], style='italic')
        
        # Информация об авторе (улучшенная)
        ax.text(6, 1.6, 'Автор: Мухаммад Махизода', 
                fontsize=12, ha='center', color=self.colors['dark_gray'],
                bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.6))
        
        ax.text(6, 1.2, 'Таджикский национальный университет', 
                fontsize=10, ha='center', color=self.colors['light_gray'])
        
        plt.tight_layout()
        filename = f"mqea_logo_premium.png"
        plt.savefig(filename, dpi=self.dpi, bbox_inches='tight', 
                   facecolor='white', edgecolor='none', 
                   pad_inches=0.1, transparent=False)
        plt.close()
        return filename
    
    def create_streamlit_logo(self, size=(400, 300), color_scheme='blue'):
        """Создает оптимизированный логотип для Streamlit."""
        fig, ax = plt.subplots(figsize=(size[0]/100, size[1]/100), dpi=self.dpi)
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 6)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Цвета
        primary_color = self.colors['primary_blue']
        accent_color = self.colors['light_blue']
        
        # Сердце (оптимизированное для веб)
        heart_x = np.linspace(-1, 1, 100)
        heart_y = (np.sqrt(1 - heart_x**2) + np.sqrt(1 - heart_x**2) * np.sin(np.pi * heart_x)) / 2
        
        # Масштабирование и позиционирование сердца
        heart_x = heart_x * 2 + 5
        heart_y = heart_y * 2 + 4
        
        ax.fill(heart_x, heart_y, color=primary_color, alpha=0.9)
        ax.plot(heart_x, heart_y, color=primary_color, linewidth=2.5)
        
        # Медицинский крест
        cross_center = (5, 4)
        cross_vertical = Rectangle((cross_center[0]-0.25, cross_center[1]-1.0), 
                                 0.5, 2.0, color=self.colors['white'], alpha=0.95)
        cross_horizontal = Rectangle((cross_center[0]-1.0, cross_center[1]-0.25), 
                                   2.0, 0.5, color=self.colors['white'], alpha=0.95)
        ax.add_patch(cross_vertical)
        ax.add_patch(cross_horizontal)
        
        # Квантовые элементы
        for i in range(6):
            angle = i * np.pi / 3
            radius = 1.8
            x = 5 + radius * np.cos(angle)
            y = 4 + radius * np.sin(angle)
            quantum_dot = Circle((x, y), 0.15, color=accent_color, alpha=0.8)
            ax.add_patch(quantum_dot)
        
        # Название проекта
        ax.text(5, 2.5, 'MQEA', fontsize=24, fontweight='bold', 
                ha='center', color=primary_color)
        
        # Девиз
        ax.text(5, 2.0, self.motto, 
                fontsize=12, fontweight='bold', ha='center', 
                color=primary_color, style='italic')
        
        # Информация об авторе
        ax.text(5, 1.3, 'Мухаммад Махизода', 
                fontsize=10, ha='center', color=self.colors['dark_gray'])
        
        ax.text(5, 1.0, 'Таджикский национальный университет', 
                fontsize=8, ha='center', color=self.colors['light_gray'])
        
        plt.tight_layout()
        filename = f"mqea_logo_streamlit_optimized.png"
        plt.savefig(filename, dpi=self.dpi, bbox_inches='tight', 
                   facecolor='white', edgecolor='none', 
                   pad_inches=0.05, transparent=False)
        plt.close()
        return filename
    
    def create_sidebar_logo(self, size=(250, 200), color_scheme='blue'):
        """Создает компактный логотип для сайдбара."""
        fig, ax = plt.subplots(figsize=(size[0]/100, size[1]/100), dpi=self.dpi)
        ax.set_xlim(0, 8)
        ax.set_ylim(0, 5)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Цвета
        primary_color = self.colors['primary_blue']
        accent_color = self.colors['light_blue']
        
        # Сердце (компактное)
        heart_x = np.linspace(-0.8, 0.8, 80)
        heart_y = (np.sqrt(1 - heart_x**2) + np.sqrt(1 - heart_x**2) * np.sin(np.pi * heart_x)) / 2
        
        # Масштабирование и позиционирование сердца
        heart_x = heart_x * 1.5 + 4
        heart_y = heart_y * 1.5 + 3.5
        
        ax.fill(heart_x, heart_y, color=primary_color, alpha=0.9)
        ax.plot(heart_x, heart_y, color=primary_color, linewidth=2)
        
        # Медицинский крест
        cross_center = (4, 3.5)
        cross_vertical = Rectangle((cross_center[0]-0.2, cross_center[1]-0.8), 
                                 0.4, 1.6, color=self.colors['white'], alpha=0.95)
        cross_horizontal = Rectangle((cross_center[0]-0.8, cross_center[1]-0.2), 
                                   1.6, 0.4, color=self.colors['white'], alpha=0.95)
        ax.add_patch(cross_vertical)
        ax.add_patch(cross_horizontal)
        
        # Квантовые элементы
        for i in range(4):
            angle = i * np.pi / 2
            radius = 1.3
            x = 4 + radius * np.cos(angle)
            y = 3.5 + radius * np.sin(angle)
            quantum_dot = Circle((x, y), 0.12, color=accent_color, alpha=0.8)
            ax.add_patch(quantum_dot)
        
        # Название проекта
        ax.text(4, 2.2, 'MQEA', fontsize=18, fontweight='bold', 
                ha='center', color=primary_color)
        
        # Девиз (сокращенный)
        ax.text(4, 1.7, 'Спокойствие • Доверие • Стабильность', 
                fontsize=8, ha='center', 
                color=primary_color, style='italic')
        
        # Информация об авторе
        ax.text(4, 1.2, 'Мухаммад Махизода', 
                fontsize=7, ha='center', color=self.colors['dark_gray'])
        
        plt.tight_layout()
        filename = f"mqea_logo_sidebar_optimized.png"
        plt.savefig(filename, dpi=self.dpi, bbox_inches='tight', 
                   facecolor='white', edgecolor='none', 
                   pad_inches=0.03, transparent=False)
        plt.close()
        return filename
    
    def create_card_logo(self, size=(350, 250), color_scheme='blue'):
        """Создает логотип для карточек с улучшенным дизайном."""
        fig, ax = plt.subplots(figsize=(size[0]/100, size[1]/100), dpi=self.dpi)
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 7)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Цвета
        primary_color = self.colors['primary_blue']
        accent_color = self.colors['light_blue']
        
        # Фон карточки
        card = FancyBboxPatch((0.5, 0.5), 9, 6, 
                             boxstyle="round,pad=0.3", 
                             facecolor='white', 
                             edgecolor=primary_color, 
                             linewidth=2, alpha=0.95)
        ax.add_patch(card)
        
        # Сердце
        heart_x = np.linspace(-1, 1, 100)
        heart_y = (np.sqrt(1 - heart_x**2) + np.sqrt(1 - heart_x**2) * np.sin(np.pi * heart_x)) / 2
        
        # Масштабирование и позиционирование сердца
        heart_x = heart_x * 1.8 + 5
        heart_y = heart_y * 1.8 + 4.5
        
        ax.fill(heart_x, heart_y, color=primary_color, alpha=0.9)
        ax.plot(heart_x, heart_y, color=primary_color, linewidth=2)
        
        # Медицинский крест
        cross_center = (5, 4.5)
        cross_vertical = Rectangle((cross_center[0]-0.2, cross_center[1]-0.7), 
                                 0.4, 1.4, color=self.colors['white'], alpha=0.95)
        cross_horizontal = Rectangle((cross_center[0]-0.7, cross_center[1]-0.2), 
                                   1.4, 0.4, color=self.colors['white'], alpha=0.95)
        ax.add_patch(cross_vertical)
        ax.add_patch(cross_horizontal)
        
        # Квантовые элементы
        for i in range(6):
            angle = i * np.pi / 3
            radius = 1.5
            x = 5 + radius * np.cos(angle)
            y = 4.5 + radius * np.sin(angle)
            quantum_dot = Circle((x, y), 0.12, color=accent_color, alpha=0.8)
            ax.add_patch(quantum_dot)
        
        # Название проекта
        ax.text(5, 3.2, 'MQEA', fontsize=20, fontweight='bold', 
                ha='center', color=primary_color)
        
        # Девиз
        ax.text(5, 2.7, self.motto, 
                fontsize=10, fontweight='bold', ha='center', 
                color=primary_color, style='italic')
        
        # Информация об авторе
        ax.text(5, 2.1, 'Мухаммад Махизода', 
                fontsize=9, ha='center', color=self.colors['dark_gray'])
        
        ax.text(5, 1.7, 'Таджикский национальный университет', 
                fontsize=7, ha='center', color=self.colors['light_gray'])
        
        plt.tight_layout()
        filename = f"mqea_logo_card_optimized.png"
        plt.savefig(filename, dpi=self.dpi, bbox_inches='tight', 
                   facecolor='white', edgecolor='none', 
                   pad_inches=0.05, transparent=False)
        plt.close()
        return filename
    
    def generate_all_optimized_logos(self):
        """Генерирует все оптимизированные варианты логотипов."""
        print("🎨 Создание оптимизированных логотипов MQEA...")
        print("Автор: Мухаммад Махизода")
        print("Таджикский национальный университет")
        print("=" * 60)
        print(f"📝 Девиз: '{self.motto}'")
        print(f"🎯 Качество: {self.dpi} DPI")
        print("=" * 60)
        
        generated_files = []
        
        # Генерация всех вариантов
        logo_types = [
            ('create_premium_logo', 'Премиум логотип'),
            ('create_streamlit_logo', 'Оптимизированный для Streamlit'),
            ('create_sidebar_logo', 'Компактный для сайдбара'),
            ('create_card_logo', 'Логотип для карточек')
        ]
        
        for logo_type, description in logo_types:
            print(f"\n🔬 Создание: {description}")
            
            try:
                if logo_type == 'create_premium_logo':
                    filename = self.create_premium_logo()
                elif logo_type == 'create_streamlit_logo':
                    filename = self.create_streamlit_logo()
                elif logo_type == 'create_sidebar_logo':
                    filename = self.create_sidebar_logo()
                elif logo_type == 'create_card_logo':
                    filename = self.create_card_logo()
                
                generated_files.append(filename)
                print(f"  ✅ Создан: {filename}")
                
            except Exception as e:
                print(f"  ❌ Ошибка: {e}")
        
        print(f"\n🎉 Генерация завершена!")
        print(f"📁 Создано файлов: {len(generated_files)}")
        
        return generated_files

def main():
    """Основная функция."""
    generator = OptimizedLogoGenerator()
    generated_files = generator.generate_all_optimized_logos()
    
    print("\n📋 Созданные оптимизированные логотипы:")
    for i, filename in enumerate(generated_files, 1):
        print(f"{i:2d}. {filename}")
    
    print("\n💡 Рекомендации:")
    print("• mqea_logo_premium.png - для презентаций и документов")
    print("• mqea_logo_streamlit_optimized.png - для веб-приложений")
    print("• mqea_logo_sidebar_optimized.png - для сайдбаров")
    print("• mqea_logo_card_optimized.png - для карточек и карточек")

if __name__ == "__main__":
    main()

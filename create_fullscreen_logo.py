#!/usr/bin/env python3
"""
Создание логотипа MQEA на полный экран с прозрачным фоном.

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

class FullscreenLogoGenerator:
    """Генератор логотипа на полный экран с прозрачным фоном."""
    
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
        
    def create_fullscreen_logo(self, size=(1200, 400), color_scheme='blue'):
        """Создает логотип на полный экран с прозрачным фоном."""
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
        
        # Сердце (увеличенное для полного экрана)
        heart_x = np.linspace(-2, 2, 200)
        heart_y = (np.sqrt(1 - heart_x**2) + np.sqrt(1 - heart_x**2) * np.sin(np.pi * heart_x)) / 2
        
        # Масштабирование и позиционирование сердца
        heart_x = heart_x * 3 + 12
        heart_y = heart_y * 3 + 4
        
        # Градиент для сердца
        ax.fill(heart_x, heart_y, color=primary_color, alpha=0.9)
        ax.plot(heart_x, heart_y, color=primary_color, linewidth=4)
        
        # Тень для сердца
        shadow_x = heart_x + 0.2
        shadow_y = heart_y - 0.2
        ax.fill(shadow_x, shadow_y, color='black', alpha=0.3)
        
        # Медицинский крест (увеличенный)
        cross_center = (12, 4)
        cross_vertical = Rectangle((cross_center[0]-0.4, cross_center[1]-1.5), 
                                 0.8, 3.0, color=self.colors['white'], alpha=0.95)
        cross_horizontal = Rectangle((cross_center[0]-1.5, cross_center[1]-0.4), 
                                   3.0, 0.8, color=self.colors['white'], alpha=0.95)
        ax.add_patch(cross_vertical)
        ax.add_patch(cross_horizontal)
        
        # Квантовые элементы (увеличенные)
        for i in range(12):
            angle = i * np.pi / 6
            radius = 3.5
            x = 12 + radius * np.cos(angle)
            y = 4 + radius * np.sin(angle)
            # Градиент для квантовых элементов
            quantum_dot = Circle((x, y), 0.3, color=accent_color, alpha=0.8)
            ax.add_patch(quantum_dot)
            # Свечение
            glow = Circle((x, y), 0.5, color=accent_color, alpha=0.4)
            ax.add_patch(glow)
        
        # Название проекта (крупное)
        ax.text(12, 1.5, 'MQEA', fontsize=48, fontweight='bold', 
                ha='center', color=primary_color)
        
        # Полное название
        ax.text(12, 1.0, 'Medical Quantum Entanglement Analysis', 
                fontsize=18, ha='center', color=self.colors['dark_gray'])
        
        # Девиз (крупный)
        ax.text(12, 0.5, self.motto, 
                fontsize=20, fontweight='bold', ha='center', 
                color=primary_color, style='italic')
        
        # Девиз на английском
        ax.text(12, 0.2, self.motto_en, 
                fontsize=14, ha='center', 
                color=self.colors['light_gray'], style='italic')
        
        plt.tight_layout()
        filename = f"mqea_logo_fullscreen_transparent.png"
        plt.savefig(filename, dpi=self.dpi, bbox_inches='tight', 
                   facecolor='none', edgecolor='none', 
                   pad_inches=0.1, transparent=True)
        plt.close()
        return filename
    
    def create_wide_logo(self, size=(1000, 300), color_scheme='blue'):
        """Создает широкий логотип для главного экрана."""
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
        
        # Сердце (широкое)
        heart_x = np.linspace(-1.5, 1.5, 150)
        heart_y = (np.sqrt(1 - heart_x**2) + np.sqrt(1 - heart_x**2) * np.sin(np.pi * heart_x)) / 2
        
        # Масштабирование и позиционирование сердца
        heart_x = heart_x * 2.5 + 10
        heart_y = heart_y * 2.5 + 3.5
        
        ax.fill(heart_x, heart_y, color=primary_color, alpha=0.9)
        ax.plot(heart_x, heart_y, color=primary_color, linewidth=3)
        
        # Медицинский крест
        cross_center = (10, 3.5)
        cross_vertical = Rectangle((cross_center[0]-0.3, cross_center[1]-1.2), 
                                 0.6, 2.4, color=self.colors['white'], alpha=0.95)
        cross_horizontal = Rectangle((cross_center[0]-1.2, cross_center[1]-0.3), 
                                   2.4, 0.6, color=self.colors['white'], alpha=0.95)
        ax.add_patch(cross_vertical)
        ax.add_patch(cross_horizontal)
        
        # Квантовые элементы
        for i in range(10):
            angle = i * np.pi / 5
            radius = 2.8
            x = 10 + radius * np.cos(angle)
            y = 3.5 + radius * np.sin(angle)
            quantum_dot = Circle((x, y), 0.25, color=accent_color, alpha=0.8)
            ax.add_patch(quantum_dot)
            glow = Circle((x, y), 0.4, color=accent_color, alpha=0.3)
            ax.add_patch(glow)
        
        # Название проекта
        ax.text(10, 2.0, 'MQEA', fontsize=36, fontweight='bold', 
                ha='center', color=primary_color)
        
        # Полное название
        ax.text(10, 1.5, 'Medical Quantum Entanglement Analysis', 
                fontsize=14, ha='center', color=self.colors['dark_gray'])
        
        # Девиз
        ax.text(10, 1.0, self.motto, 
                fontsize=16, fontweight='bold', ha='center', 
                color=primary_color, style='italic')
        
        # Девиз на английском
        ax.text(10, 0.6, self.motto_en, 
                fontsize=12, ha='center', 
                color=self.colors['light_gray'], style='italic')
        
        plt.tight_layout()
        filename = f"mqea_logo_wide_transparent.png"
        plt.savefig(filename, dpi=self.dpi, bbox_inches='tight', 
                   facecolor='none', edgecolor='none', 
                   pad_inches=0.05, transparent=True)
        plt.close()
        return filename
    
    def create_header_logo(self, size=(800, 200), color_scheme='blue'):
        """Создает логотип для заголовка с прозрачным фоном."""
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
        heart_x = np.linspace(-1, 1, 100)
        heart_y = (np.sqrt(1 - heart_x**2) + np.sqrt(1 - heart_x**2) * np.sin(np.pi * heart_x)) / 2
        
        # Масштабирование и позиционирование сердца
        heart_x = heart_x * 1.8 + 8
        heart_y = heart_y * 1.8 + 2.5
        
        ax.fill(heart_x, heart_y, color=primary_color, alpha=0.9)
        ax.plot(heart_x, heart_y, color=primary_color, linewidth=2.5)
        
        # Медицинский крест
        cross_center = (8, 2.5)
        cross_vertical = Rectangle((cross_center[0]-0.25, cross_center[1]-0.9), 
                                 0.5, 1.8, color=self.colors['white'], alpha=0.95)
        cross_horizontal = Rectangle((cross_center[0]-0.9, cross_center[1]-0.25), 
                                   1.8, 0.5, color=self.colors['white'], alpha=0.95)
        ax.add_patch(cross_vertical)
        ax.add_patch(cross_horizontal)
        
        # Квантовые элементы
        for i in range(8):
            angle = i * np.pi / 4
            radius = 2.2
            x = 8 + radius * np.cos(angle)
            y = 2.5 + radius * np.sin(angle)
            quantum_dot = Circle((x, y), 0.2, color=accent_color, alpha=0.8)
            ax.add_patch(quantum_dot)
        
        # Название проекта
        ax.text(8, 1.2, 'MQEA', fontsize=28, fontweight='bold', 
                ha='center', color=primary_color)
        
        # Девиз
        ax.text(8, 0.7, self.motto, 
                fontsize=12, fontweight='bold', ha='center', 
                color=primary_color, style='italic')
        
        plt.tight_layout()
        filename = f"mqea_logo_header_transparent.png"
        plt.savefig(filename, dpi=self.dpi, bbox_inches='tight', 
                   facecolor='none', edgecolor='none', 
                   pad_inches=0.03, transparent=True)
        plt.close()
        return filename
    
    def generate_all_fullscreen_logos(self):
        """Генерирует все варианты логотипов на полный экран."""
        print("🖥️ Создание логотипов MQEA на полный экран с прозрачным фоном...")
        print("Автор: Мухаммад Махизода")
        print("Таджикский национальный университет")
        print("=" * 70)
        print(f"📝 Девиз: '{self.motto}'")
        print(f"🎯 Качество: {self.dpi} DPI")
        print(f"🎨 Фон: Прозрачный")
        print("=" * 70)
        
        generated_files = []
        
        # Генерация всех вариантов
        logo_types = [
            ('create_fullscreen_logo', 'Полноэкранный логотип'),
            ('create_wide_logo', 'Широкий логотип'),
            ('create_header_logo', 'Логотип для заголовка')
        ]
        
        for logo_type, description in logo_types:
            print(f"\n🔬 Создание: {description}")
            
            try:
                if logo_type == 'create_fullscreen_logo':
                    filename = self.create_fullscreen_logo()
                elif logo_type == 'create_wide_logo':
                    filename = self.create_wide_logo()
                elif logo_type == 'create_header_logo':
                    filename = self.create_header_logo()
                
                generated_files.append(filename)
                print(f"  ✅ Создан: {filename}")
                
            except Exception as e:
                print(f"  ❌ Ошибка: {e}")
        
        print(f"\n🎉 Генерация завершена!")
        print(f"📁 Создано файлов: {len(generated_files)}")
        
        return generated_files

def main():
    """Основная функция."""
    generator = FullscreenLogoGenerator()
    generated_files = generator.generate_all_fullscreen_logos()
    
    print("\n📋 Созданные полноэкранные логотипы:")
    for i, filename in enumerate(generated_files, 1):
        print(f"{i:2d}. {filename}")
    
    print("\n💡 Рекомендации:")
    print("• mqea_logo_fullscreen_transparent.png - для полного экрана")
    print("• mqea_logo_wide_transparent.png - для широких экранов")
    print("• mqea_logo_header_transparent.png - для заголовков")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Добавление девиза к основному логотипу MQEA.

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

class LogoWithMottoGenerator:
    """Генератор логотипа с девизом."""
    
    def __init__(self):
        self.colors = {
            'blue': '#0066CC',
            'light_blue': '#00CCFF',
            'white': '#FFFFFF',
            'black': '#000000',
            'gray': '#666666'
        }
        
        # Девиз проекта
        self.motto = "Спокойствие, доверие, стабильность"
        self.motto_en = "Calm, Trust, Stability"
        
    def create_heart_medical_logo_with_motto(self, size=(500, 600), color_scheme='blue'):
        """Создает логотип с сердцем, медицинским символом и девизом."""
        fig, ax = plt.subplots(figsize=(size[0]/100, size[1]/100))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 12)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Цвета
        primary_color = self.colors[color_scheme]
        accent_color = self.colors['light_blue']
        
        # Сердце
        heart_x = np.linspace(-1, 1, 100)
        heart_y = (np.sqrt(1 - heart_x**2) + np.sqrt(1 - heart_x**2) * np.sin(np.pi * heart_x)) / 2
        
        # Масштабирование и позиционирование сердца
        heart_x = heart_x * 2 + 5
        heart_y = heart_y * 2 + 7
        
        ax.fill(heart_x, heart_y, color=primary_color, alpha=0.8)
        ax.plot(heart_x, heart_y, color=primary_color, linewidth=2)
        
        # Медицинский крест в центре сердца
        cross_center = (5, 7)
        cross_vertical = Rectangle((cross_center[0]-0.2, cross_center[1]-0.8), 
                                 0.4, 1.6, color=self.colors['white'])
        cross_horizontal = Rectangle((cross_center[0]-0.8, cross_center[1]-0.2), 
                                   1.6, 0.4, color=self.colors['white'])
        ax.add_patch(cross_vertical)
        ax.add_patch(cross_horizontal)
        
        # Квантовые элементы вокруг сердца
        for i in range(8):
            angle = i * np.pi / 4
            radius = 2.0
            x = 5 + radius * np.cos(angle)
            y = 7 + radius * np.sin(angle)
            quantum_dot = Circle((x, y), 0.15, color=accent_color)
            ax.add_patch(quantum_dot)
        
        # Название проекта
        ax.text(5, 4.5, 'MQEA', fontsize=28, fontweight='bold', 
                ha='center', color=primary_color)
        
        # Полное название
        ax.text(5, 4.0, 'Medical Quantum Entanglement Analysis', 
                fontsize=12, ha='center', color=self.colors['gray'])
        
        # Девиз на русском языке
        ax.text(5, 3.2, self.motto, 
                fontsize=14, fontweight='bold', ha='center', 
                color=primary_color, style='italic')
        
        # Девиз на английском языке
        ax.text(5, 2.8, self.motto_en, 
                fontsize=10, ha='center', 
                color=self.colors['gray'], style='italic')
        
        # Информация об авторе
        ax.text(5, 1.8, 'Автор: Мухаммад Махизода', 
                fontsize=10, ha='center', color=self.colors['gray'])
        
        ax.text(5, 1.4, 'Таджикский национальный университет', 
                fontsize=9, ha='center', color=self.colors['gray'])
        
        plt.tight_layout()
        filename = f"mqea_logo_with_motto.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        plt.close()
        return filename
    
    def create_compact_logo_with_motto(self, size=(400, 500), color_scheme='blue'):
        """Создает компактную версию логотипа с девизом."""
        fig, ax = plt.subplots(figsize=(size[0]/100, size[1]/100))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Цвета
        primary_color = self.colors[color_scheme]
        accent_color = self.colors['light_blue']
        
        # Сердце (меньше)
        heart_x = np.linspace(-0.8, 0.8, 80)
        heart_y = (np.sqrt(1 - heart_x**2) + np.sqrt(1 - heart_x**2) * np.sin(np.pi * heart_x)) / 2
        
        # Масштабирование и позиционирование сердца
        heart_x = heart_x * 1.5 + 5
        heart_y = heart_y * 1.5 + 6.5
        
        ax.fill(heart_x, heart_y, color=primary_color, alpha=0.8)
        ax.plot(heart_x, heart_y, color=primary_color, linewidth=2)
        
        # Медицинский крест в центре сердца
        cross_center = (5, 6.5)
        cross_vertical = Rectangle((cross_center[0]-0.15, cross_center[1]-0.6), 
                                 0.3, 1.2, color=self.colors['white'])
        cross_horizontal = Rectangle((cross_center[0]-0.6, cross_center[1]-0.15), 
                                   1.2, 0.3, color=self.colors['white'])
        ax.add_patch(cross_vertical)
        ax.add_patch(cross_horizontal)
        
        # Квантовые элементы вокруг сердца
        for i in range(6):
            angle = i * np.pi / 3
            radius = 1.5
            x = 5 + radius * np.cos(angle)
            y = 6.5 + radius * np.sin(angle)
            quantum_dot = Circle((x, y), 0.12, color=accent_color)
            ax.add_patch(quantum_dot)
        
        # Название проекта
        ax.text(5, 4.5, 'MQEA', fontsize=24, fontweight='bold', 
                ha='center', color=primary_color)
        
        # Девиз
        ax.text(5, 3.8, self.motto, 
                fontsize=12, fontweight='bold', ha='center', 
                color=primary_color, style='italic')
        
        # Информация об авторе
        ax.text(5, 2.8, 'Мухаммад Махизода', 
                fontsize=10, ha='center', color=self.colors['gray'])
        
        ax.text(5, 2.4, 'Таджикский национальный университет', 
                fontsize=8, ha='center', color=self.colors['gray'])
        
        plt.tight_layout()
        filename = f"mqea_logo_compact_with_motto.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        plt.close()
        return filename
    
    def create_sidebar_logo_with_motto(self, size=(300, 400), color_scheme='blue'):
        """Создает версию логотипа для сайдбара с девизом."""
        fig, ax = plt.subplots(figsize=(size[0]/100, size[1]/100))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 8)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Цвета
        primary_color = self.colors[color_scheme]
        accent_color = self.colors['light_blue']
        
        # Сердце (еще меньше)
        heart_x = np.linspace(-0.6, 0.6, 60)
        heart_y = (np.sqrt(1 - heart_x**2) + np.sqrt(1 - heart_x**2) * np.sin(np.pi * heart_x)) / 2
        
        # Масштабирование и позиционирование сердца
        heart_x = heart_x * 1.2 + 5
        heart_y = heart_y * 1.2 + 5.5
        
        ax.fill(heart_x, heart_y, color=primary_color, alpha=0.8)
        ax.plot(heart_x, heart_y, color=primary_color, linewidth=2)
        
        # Медицинский крест в центре сердца
        cross_center = (5, 5.5)
        cross_vertical = Rectangle((cross_center[0]-0.12, cross_center[1]-0.5), 
                                 0.24, 1.0, color=self.colors['white'])
        cross_horizontal = Rectangle((cross_center[0]-0.5, cross_center[1]-0.12), 
                                   1.0, 0.24, color=self.colors['white'])
        ax.add_patch(cross_vertical)
        ax.add_patch(cross_horizontal)
        
        # Квантовые элементы вокруг сердца
        for i in range(4):
            angle = i * np.pi / 2
            radius = 1.2
            x = 5 + radius * np.cos(angle)
            y = 5.5 + radius * np.sin(angle)
            quantum_dot = Circle((x, y), 0.1, color=accent_color)
            ax.add_patch(quantum_dot)
        
        # Название проекта
        ax.text(5, 3.8, 'MQEA', fontsize=18, fontweight='bold', 
                ha='center', color=primary_color)
        
        # Девиз (сокращенный)
        ax.text(5, 3.2, 'Спокойствие • Доверие • Стабильность', 
                fontsize=9, ha='center', 
                color=primary_color, style='italic')
        
        # Информация об авторе
        ax.text(5, 2.4, 'Мухаммад Махизода', 
                fontsize=8, ha='center', color=self.colors['gray'])
        
        plt.tight_layout()
        filename = f"mqea_logo_sidebar_with_motto.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        plt.close()
        return filename
    
    def generate_all_logos_with_motto(self):
        """Генерирует все варианты логотипов с девизом."""
        print("❤️ Генерация логотипов MQEA с девизом...")
        print("Автор: Мухаммад Махизода")
        print("Таджикский национальный университет")
        print("=" * 60)
        print(f"📝 Девиз: '{self.motto}'")
        print("=" * 60)
        
        generated_files = []
        
        # Генерация всех вариантов
        logo_types = [
            ('create_heart_medical_logo_with_motto', 'Полный логотип с девизом'),
            ('create_compact_logo_with_motto', 'Компактный логотип с девизом'),
            ('create_sidebar_logo_with_motto', 'Логотип для сайдбара с девизом')
        ]
        
        for logo_type, description in logo_types:
            print(f"\n🔬 Создание: {description}")
            
            try:
                if logo_type == 'create_heart_medical_logo_with_motto':
                    filename = self.create_heart_medical_logo_with_motto()
                elif logo_type == 'create_compact_logo_with_motto':
                    filename = self.create_compact_logo_with_motto()
                elif logo_type == 'create_sidebar_logo_with_motto':
                    filename = self.create_sidebar_logo_with_motto()
                
                generated_files.append(filename)
                print(f"  ✅ Создан: {filename}")
                
            except Exception as e:
                print(f"  ❌ Ошибка: {e}")
        
        print(f"\n🎉 Генерация завершена!")
        print(f"📁 Создано файлов: {len(generated_files)}")
        
        return generated_files

def main():
    """Основная функция."""
    generator = LogoWithMottoGenerator()
    generated_files = generator.generate_all_logos_with_motto()
    
    print("\n📋 Созданные логотипы с девизом:")
    for i, filename in enumerate(generated_files, 1):
        print(f"{i:2d}. {filename}")
    
    print("\n💡 Рекомендации:")
    print("• mqea_logo_with_motto.png - для заголовков и презентаций")
    print("• mqea_logo_compact_with_motto.png - для документов")
    print("• mqea_logo_sidebar_with_motto.png - для сайдбаров")

if __name__ == "__main__":
    main()

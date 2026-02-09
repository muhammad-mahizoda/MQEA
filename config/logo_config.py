"""
Конфигурация логотипов для MQEA.

Автор: Мухаммад Махизода
Таджикский национальный университет
"""

from pathlib import Path
from typing import Dict, List

class LogoConfig:
    """Конфигурация логотипов MQEA."""
    
    def __init__(self):
        self.logo_dir = Path("webapp/static/logos")
        self.default_logo = "heart_medical_blue.png"
        self.main_logo = "heart_medical_blue.png"  # Основной логотип проекта
        self.main_logo_path = Path("mqea_logo.png")  # Путь к основному логотипу
        
        # Основные логотипы
        self.main_logos = {
            "quantum_medical_cross": {
                "blue": "quantum_medical_cross_blue.png",
                "green": "quantum_medical_cross_green.png",
                "red": "quantum_medical_cross_red.png",
                "description": "Квантовый атом с медицинским крестом",
                "best_for": "Основной логотип, научные публикации"
            },
            "dna_medical": {
                "blue": "dna_medical_blue.png",
                "green": "dna_medical_green.png",
                "red": "dna_medical_red.png",
                "description": "ДНК спираль с медицинским символом",
                "best_for": "Биомедицинские исследования"
            },
            "quantum_entanglement": {
                "blue": "quantum_entanglement_blue.png",
                "green": "quantum_entanglement_green.png",
                "red": "quantum_entanglement_red.png",
                "description": "Квантовая запутанность",
                "best_for": "Техническая документация"
            },
            "medical_shield": {
                "blue": "medical_shield_blue.png",
                "green": "medical_shield_green.png",
                "red": "medical_shield_red.png",
                "description": "Медицинский щит",
                "best_for": "Клинические приложения"
            },
            "heart_medical": {
                "blue": "heart_medical_blue.png",
                "green": "heart_medical_green.png",
                "red": "heart_medical_red.png",
                "description": "Сердце с медицинским символом",
                "best_for": "Пользовательские интерфейсы"
            }
        }
        
        # Цветовые схемы
        self.color_schemes = {
            "blue": {
                "primary": "#0066CC",
                "accent": "#00CCFF",
                "meaning": "Доверие, стабильность, технологичность"
            },
            "green": {
                "primary": "#00AA44",
                "accent": "#00FF88",
                "meaning": "Здоровье, природа, рост"
            },
            "red": {
                "primary": "#CC0000",
                "accent": "#FF4444",
                "meaning": "Энергия, страсть, важность"
            }
        }
    
    def get_logo_path(self, logo_type: str, color: str) -> Path:
        """Получает путь к логотипу."""
        if logo_type in self.main_logos and color in self.main_logos[logo_type]:
            filename = self.main_logos[logo_type][color]
            return self.logo_dir / filename
        return self.logo_dir / self.default_logo
    
    def get_all_logos(self) -> List[Dict]:
        """Получает список всех логотипов."""
        logos = []
        for logo_type, variants in self.main_logos.items():
            for color, filename in variants.items():
                if isinstance(filename, str):
                    logos.append({
                        "type": logo_type,
                        "color": color,
                        "filename": filename,
                        "path": self.logo_dir / filename,
                        "description": variants.get("description", ""),
                        "best_for": variants.get("best_for", "")
                    })
        return logos
    
    def get_recommended_logo(self, use_case: str) -> str:
        """Получает рекомендуемый логотип для конкретного случая."""
        recommendations = {
            "main_logo": "heart_medical_blue.png",
            "scientific": "quantum_entanglement_blue.png",
            "clinical": "medical_shield_green.png",
            "user_interface": "heart_medical_blue.png",
            "biomedical": "dna_medical_green.png"
        }
        return recommendations.get(use_case, self.default_logo)
    
    def get_main_logo_path(self) -> Path:
        """Получает путь к основному логотипу проекта."""
        return self.main_logo_path
    
    def get_main_logo_filename(self) -> str:
        """Получает имя файла основного логотипа."""
        return self.main_logo
    
    def is_main_logo_available(self) -> bool:
        """Проверяет доступность основного логотипа."""
        return self.main_logo_path.exists()

# Глобальный экземпляр конфигурации
logo_config = LogoConfig()

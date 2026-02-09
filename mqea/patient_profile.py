"""
Профиль пациента для персонализированных медицинских рекомендаций.

Автор: Мухаммад Махизода
Таджикский национальный университет
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from datetime import datetime, date
from enum import Enum


class Gender(Enum):
    """Пол пациента."""
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class ActivityLevel(Enum):
    """Уровень физической активности."""
    SEDENTARY = "sedentary"  # Малоподвижный
    LIGHT = "light"  # Легкая активность
    MODERATE = "moderate"  # Умеренная активность
    HIGH = "high"  # Высокая активность
    VERY_HIGH = "very_high"  # Очень высокая активность


class MedicalHistory(Enum):
    """Медицинская история."""
    DIABETES = "diabetes"
    HYPERTENSION = "hypertension"
    HEART_DISEASE = "heart_disease"
    RESPIRATORY_DISEASE = "respiratory_disease"
    KIDNEY_DISEASE = "kidney_disease"
    LIVER_DISEASE = "liver_disease"
    THYROID_DISEASE = "thyroid_disease"
    CANCER = "cancer"
    AUTOIMMUNE = "autoimmune"
    NONE = "none"


@dataclass
class PatientProfile:
    """Профиль пациента для персонализированных рекомендаций."""
    
    # Основная информация
    patient_id: str
    name: str
    birth_date: date
    gender: Gender
    
    # Физические параметры
    height_cm: float  # Рост в см
    weight_kg: float  # Вес в кг
    
    # Медицинская история
    medical_history: List[MedicalHistory]
    current_medications: List[str]
    allergies: List[str]
    
    # Образ жизни
    activity_level: ActivityLevel
    smoking: bool
    alcohol_consumption: bool
    
    # Дополнительная информация
    occupation: Optional[str] = None
    notes: Optional[str] = None
    
    @property
    def age(self) -> int:
        """Вычисляет возраст пациента."""
        today = date.today()
        return today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )
    
    @property
    def bmi(self) -> float:
        """Вычисляет индекс массы тела (BMI)."""
        height_m = self.height_cm / 100
        return self.weight_kg / (height_m ** 2)
    
    @property
    def bmi_category(self) -> str:
        """Определяет категорию BMI."""
        if self.bmi < 18.5:
            return "Недостаточный вес"
        elif self.bmi < 25:
            return "Нормальный вес"
        elif self.bmi < 30:
            return "Избыточный вес"
        else:
            return "Ожирение"
    
    def get_age_adjusted_ranges(self, indicator: str) -> Dict[str, Tuple[float, float]]:
        """Возвращает возрастные нормы для медицинских показателей."""
        
        age = self.age
        
        # Базовые нормы
        ranges = {
            'heart_rate': {'normal': (60, 100), 'warning': (50, 120), 'critical': (40, 150)},
            'blood_pressure_systolic': {'normal': (90, 140), 'warning': (80, 160), 'critical': (70, 180)},
            'blood_pressure_diastolic': {'normal': (60, 90), 'warning': (50, 100), 'critical': (40, 110)},
            'temperature': {'normal': (36.1, 37.2), 'warning': (35.5, 38.0), 'critical': (35.0, 40.0)},
            'oxygen_saturation': {'normal': (95, 100), 'warning': (90, 95), 'critical': (85, 90)},
            'respiratory_rate': {'normal': (12, 20), 'warning': (10, 25), 'critical': (8, 30)},
            'glucose': {'normal': (3.9, 5.6), 'warning': (3.0, 7.8), 'critical': (2.5, 11.1)},
            'cholesterol': {'normal': (0, 200), 'warning': (200, 240), 'critical': (240, 300)}
        }
        
        if indicator not in ranges:
            return ranges.get('heart_rate', {'normal': (0, 100), 'warning': (0, 100), 'critical': (0, 100)})
        
        # Возрастные корректировки
        if indicator == 'heart_rate':
            if age >= 65:
                # Для пожилых людей нормальный пульс может быть ниже
                ranges[indicator]['normal'] = (55, 95)
                ranges[indicator]['warning'] = (45, 115)
            elif age < 18:
                # Для детей и подростков пульс выше
                ranges[indicator]['normal'] = (70, 120)
                ranges[indicator]['warning'] = (60, 140)
        
        elif indicator == 'blood_pressure_systolic':
            if age >= 65:
                # Для пожилых людей систолическое давление может быть выше
                ranges[indicator]['normal'] = (100, 150)
                ranges[indicator]['warning'] = (90, 170)
            elif age < 18:
                # Для детей давление ниже
                ranges[indicator]['normal'] = (80, 120)
                ranges[indicator]['warning'] = (70, 130)
        
        elif indicator == 'glucose':
            if age >= 65:
                # Для пожилых людей глюкоза может быть выше
                ranges[indicator]['normal'] = (4.0, 6.0)
                ranges[indicator]['warning'] = (3.5, 8.0)
            elif age < 18:
                # Для детей глюкоза может быть ниже
                ranges[indicator]['normal'] = (3.5, 5.5)
                ranges[indicator]['warning'] = (2.8, 7.5)
        
        elif indicator == 'cholesterol':
            if age >= 65:
                # Для пожилых людей холестерин может быть выше
                ranges[indicator]['normal'] = (0, 220)
                ranges[indicator]['warning'] = (220, 260)
            elif age < 18:
                # Для детей холестерин ниже
                ranges[indicator]['normal'] = (0, 170)
                ranges[indicator]['warning'] = (170, 200)
        
        return ranges[indicator]
    
    def get_risk_factors(self) -> List[str]:
        """Возвращает список факторов риска пациента."""
        risk_factors = []
        
        # Возрастные факторы риска
        if self.age >= 65:
            risk_factors.append("Пожилой возраст (65+)")
        elif self.age < 18:
            risk_factors.append("Детский/подростковый возраст")
        
        # BMI факторы риска
        if self.bmi >= 30:
            risk_factors.append("Ожирение")
        elif self.bmi >= 25:
            risk_factors.append("Избыточный вес")
        elif self.bmi < 18.5:
            risk_factors.append("Недостаточный вес")
        
        # Медицинская история
        if MedicalHistory.DIABETES in self.medical_history:
            risk_factors.append("Сахарный диабет")
        if MedicalHistory.HYPERTENSION in self.medical_history:
            risk_factors.append("Гипертония")
        if MedicalHistory.HEART_DISEASE in self.medical_history:
            risk_factors.append("Заболевания сердца")
        if MedicalHistory.RESPIRATORY_DISEASE in self.medical_history:
            risk_factors.append("Заболевания дыхательной системы")
        
        # Образ жизни
        if self.smoking:
            risk_factors.append("Курение")
        if self.alcohol_consumption:
            risk_factors.append("Употребление алкоголя")
        if self.activity_level == ActivityLevel.SEDENTARY:
            risk_factors.append("Малоподвижный образ жизни")
        
        return risk_factors
    
    def get_personalized_recommendations(self) -> List[str]:
        """Возвращает персонализированные рекомендации на основе профиля."""
        recommendations = []
        
        # Рекомендации по возрасту
        if self.age >= 65:
            recommendations.append("Регулярные медицинские осмотры каждые 6 месяцев")
            recommendations.append("Контроль артериального давления и уровня глюкозы")
            recommendations.append("Профилактика падений и переломов")
        elif self.age < 18:
            recommendations.append("Регулярные педиатрические осмотры")
            recommendations.append("Контроль роста и развития")
            recommendations.append("Вакцинация по календарю")
        
        # Рекомендации по весу
        if self.bmi >= 30:
            recommendations.append("Программа снижения веса под наблюдением врача")
            recommendations.append("Диетическое питание и физические упражнения")
        elif self.bmi < 18.5:
            recommendations.append("Консультация диетолога для набора веса")
            recommendations.append("Проверка на возможные заболевания")
        
        # Рекомендации по медицинской истории
        if MedicalHistory.DIABETES in self.medical_history:
            recommendations.append("Строгий контроль уровня глюкозы")
            recommendations.append("Регулярные консультации эндокринолога")
        if MedicalHistory.HYPERTENSION in self.medical_history:
            recommendations.append("Ежедневный контроль артериального давления")
            recommendations.append("Ограничение соли в рационе")
        if MedicalHistory.HEART_DISEASE in self.medical_history:
            recommendations.append("Регулярные кардиологические осмотры")
            recommendations.append("Контроль уровня холестерина")
        
        # Рекомендации по образу жизни
        if self.smoking:
            recommendations.append("Отказ от курения")
            recommendations.append("Консультация по методам отказа от курения")
        if self.activity_level == ActivityLevel.SEDENTARY:
            recommendations.append("Увеличение физической активности")
            recommendations.append("Начать с легких упражнений")
        
        return recommendations
    
    def to_dict(self) -> Dict:
        """Преобразует профиль в словарь для сериализации."""
        return {
            'patient_id': self.patient_id,
            'name': self.name,
            'birth_date': self.birth_date.isoformat(),
            'age': self.age,
            'gender': self.gender.value,
            'height_cm': self.height_cm,
            'weight_kg': self.weight_kg,
            'bmi': self.bmi,
            'bmi_category': self.bmi_category,
            'medical_history': [h.value for h in self.medical_history],
            'current_medications': self.current_medications,
            'allergies': self.allergies,
            'activity_level': self.activity_level.value,
            'smoking': self.smoking,
            'alcohol_consumption': self.alcohol_consumption,
            'occupation': self.occupation,
            'notes': self.notes,
            'risk_factors': self.get_risk_factors(),
            'personalized_recommendations': self.get_personalized_recommendations()
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'PatientProfile':
        """Создает профиль из словаря."""
        return cls(
            patient_id=data['patient_id'],
            name=data['name'],
            birth_date=datetime.fromisoformat(data['birth_date']).date(),
            gender=Gender(data['gender']),
            height_cm=data['height_cm'],
            weight_kg=data['weight_kg'],
            medical_history=[MedicalHistory(h) for h in data['medical_history']],
            current_medications=data['current_medications'],
            allergies=data['allergies'],
            activity_level=ActivityLevel(data['activity_level']),
            smoking=data['smoking'],
            alcohol_consumption=data['alcohol_consumption'],
            occupation=data.get('occupation'),
            notes=data.get('notes')
        )


def create_sample_patient_profiles() -> List[PatientProfile]:
    """Создает примеры профилей пациентов для тестирования."""
    
    profiles = [
        # Пожилой пациент с диабетом
        PatientProfile(
            patient_id="P001",
            name="Ахмед Каримов",
            birth_date=date(1955, 3, 15),
            gender=Gender.MALE,
            height_cm=175,
            weight_kg=85,
            medical_history=[MedicalHistory.DIABETES, MedicalHistory.HYPERTENSION],
            current_medications=["Метформин", "Эналаприл"],
            allergies=["Пенициллин"],
            activity_level=ActivityLevel.LIGHT,
            smoking=False,
            alcohol_consumption=False,
            occupation="Пенсионер",
            notes="Пациент с диабетом 2 типа, контролируемый"
        ),
        
        # Молодой спортсмен
        PatientProfile(
            patient_id="P002",
            name="Анна Петрова",
            birth_date=date(1990, 7, 22),
            gender=Gender.FEMALE,
            height_cm=165,
            weight_kg=55,
            medical_history=[MedicalHistory.NONE],
            current_medications=[],
            allergies=[],
            activity_level=ActivityLevel.VERY_HIGH,
            smoking=False,
            alcohol_consumption=False,
            occupation="Спортсменка",
            notes="Профессиональная бегунья"
        ),
        
        # Ребенок с астмой
        PatientProfile(
            patient_id="P003",
            name="Дмитрий Смирнов",
            birth_date=date(2015, 11, 8),
            gender=Gender.MALE,
            height_cm=120,
            weight_kg=25,
            medical_history=[MedicalHistory.RESPIRATORY_DISEASE],
            current_medications=["Сальбутамол"],
            allergies=["Пыльца", "Пыль"],
            activity_level=ActivityLevel.MODERATE,
            smoking=False,
            alcohol_consumption=False,
            occupation="Ученик",
            notes="Бронхиальная астма, контролируемая"
        ),
        
        # Пациент среднего возраста с ожирением
        PatientProfile(
            patient_id="P004",
            name="Елена Козлова",
            birth_date=date(1978, 12, 3),
            gender=Gender.FEMALE,
            height_cm=160,
            weight_kg=95,
            medical_history=[MedicalHistory.HYPERTENSION],
            current_medications=["Лозартан"],
            allergies=[],
            activity_level=ActivityLevel.SEDENTARY,
            smoking=True,
            alcohol_consumption=True,
            occupation="Офисный работник",
            notes="Требуется снижение веса"
        )
    ]
    
    return profiles

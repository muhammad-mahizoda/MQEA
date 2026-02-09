#!/usr/bin/env python3
"""
Демонстрация персонализированных медицинских рекомендаций на основе профилей пациентов.

Автор: Мухаммад Махизода
Таджикский национальный университет
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mqea import (
    MQEAAnalyzer, 
    PatientProfile, 
    Gender, 
    ActivityLevel, 
    MedicalHistory,
    create_sample_patient_profiles,
    MedicalRecommendationEngine
)
from mqea.data_processor import MedicalTimeSeries
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, date


def create_test_data_for_patient(patient_profile: PatientProfile) -> MedicalTimeSeries:
    """Создает тестовые данные для конкретного пациента с учетом его профиля."""
    
    # Генерируем временные метки (24 часа, каждые 15 минут)
    start_time = datetime.now() - timedelta(hours=24)
    timestamps = pd.date_range(start=start_time, periods=96, freq='15T')
    
    # Базовые значения в зависимости от возраста и пола
    age = patient_profile.age
    gender = patient_profile.gender
    
    # Настройки для разных возрастных групп
    if age >= 65:
        # Пожилые пациенты - более высокие значения
        base_heart_rate = np.random.normal(75, 10, 96)
        base_systolic = np.random.normal(140, 15, 96)
        base_diastolic = np.random.normal(85, 10, 96)
        base_glucose = np.random.normal(6.0, 1.0, 96)  # Выше для пожилых
        base_cholesterol = np.random.normal(220, 30, 96)
    elif age < 18:
        # Дети - более низкие значения
        base_heart_rate = np.random.normal(85, 15, 96)
        base_systolic = np.random.normal(100, 10, 96)
        base_diastolic = np.random.normal(65, 8, 96)
        base_glucose = np.random.normal(4.5, 0.8, 96)  # Ниже для детей
        base_cholesterol = np.random.normal(150, 20, 96)
    else:
        # Взрослые - средние значения
        base_heart_rate = np.random.normal(70, 12, 96)
        base_systolic = np.random.normal(120, 15, 96)
        base_diastolic = np.random.normal(80, 10, 96)
        base_glucose = np.random.normal(5.2, 0.9, 96)
        base_cholesterol = np.random.normal(180, 25, 96)
    
    # Корректировки на основе медицинской истории
    if MedicalHistory.DIABETES in patient_profile.medical_history:
        base_glucose += np.random.normal(2.0, 0.5, 96)  # Повышенная глюкоза
    
    if MedicalHistory.HYPERTENSION in patient_profile.medical_history:
        base_systolic += np.random.normal(20, 5, 96)  # Повышенное давление
        base_diastolic += np.random.normal(10, 3, 96)
    
    if MedicalHistory.HEART_DISEASE in patient_profile.medical_history:
        base_heart_rate += np.random.normal(15, 5, 96)  # Повышенный пульс
    
    # Корректировки на основе образа жизни
    if patient_profile.smoking:
        base_heart_rate += np.random.normal(10, 3, 96)
        base_systolic += np.random.normal(10, 3, 96)
    
    if patient_profile.activity_level == ActivityLevel.SEDENTARY:
        base_heart_rate += np.random.normal(5, 2, 96)
        base_cholesterol += np.random.normal(20, 5, 96)
    elif patient_profile.activity_level == ActivityLevel.VERY_HIGH:
        base_heart_rate -= np.random.normal(5, 2, 96)
        base_cholesterol -= np.random.normal(15, 5, 96)
    
    # Создаем DataFrame
    data = {
        'heart_rate': base_heart_rate,
        'blood_pressure_systolic': base_systolic,
        'blood_pressure_diastolic': base_diastolic,
        'temperature': np.random.normal(36.5, 0.3, 96),
        'oxygen_saturation': np.random.normal(97, 1.5, 96),
        'respiratory_rate': np.random.normal(16, 2, 96),
        'glucose': base_glucose,
        'cholesterol': base_cholesterol
    }
    
    df = pd.DataFrame(data, index=timestamps)
    missing_mask = df.isnull()
    
    return MedicalTimeSeries(
        data=df,
        indicators=list(df.columns),
        timestamps=df.index,
        missing_data_mask=missing_mask,
        quantum_states={},
        metadata={
            'source': 'patient_profile_test',
            'patient_id': patient_profile.patient_id,
            'patient_age': patient_profile.age,
            'missing_percentage': 0.0
        }
    )


def demonstrate_patient_profiles():
    """Демонстрирует персонализированные рекомендации для разных профилей пациентов."""
    
    print("🧬⚛️ MQEA - ДЕМОНСТРАЦИЯ ПЕРСОНАЛИЗИРОВАННЫХ РЕКОМЕНДАЦИЙ")
    print("=" * 60)
    print("Автор: Мухаммад Махизода")
    print("Таджикский национальный университет")
    print("=" * 60)
    
    # Создаем примеры профилей пациентов
    profiles = create_sample_patient_profiles()
    
    # Инициализируем анализатор
    analyzer = MQEAAnalyzer()
    
    for i, profile in enumerate(profiles, 1):
        print(f"\n{'='*60}")
        print(f"👤 ПАЦИЕНТ #{i}: {profile.name}")
        print(f"{'='*60}")
        
        # Показываем информацию о пациенте
        print(f"📋 **ИНФОРМАЦИЯ О ПАЦИЕНТЕ:**")
        print(f"• ID: {profile.patient_id}")
        print(f"• Возраст: {profile.age} лет")
        print(f"• Пол: {profile.gender.value}")
        print(f"• Рост: {profile.height_cm} см")
        print(f"• Вес: {profile.weight_kg} кг")
        print(f"• BMI: {profile.bmi:.1f} ({profile.bmi_category})")
        print(f"• Медицинская история: {', '.join([h.value for h in profile.medical_history])}")
        print(f"• Лекарства: {', '.join(profile.current_medications) if profile.current_medications else 'Нет'}")
        print(f"• Аллергии: {', '.join(profile.allergies) if profile.allergies else 'Нет'}")
        print(f"• Активность: {profile.activity_level.value}")
        print(f"• Курение: {'Да' if profile.smoking else 'Нет'}")
        print(f"• Алкоголь: {'Да' if profile.alcohol_consumption else 'Нет'}")
        
        # Показываем факторы риска
        risk_factors = profile.get_risk_factors()
        if risk_factors:
            print(f"• Факторы риска: {', '.join(risk_factors)}")
        
        # Создаем тестовые данные для пациента
        print(f"\n📊 **СОЗДАНИЕ ТЕСТОВЫХ ДАННЫХ...**")
        time_series = create_test_data_for_patient(profile)
        
        # Показываем последние значения
        latest_values = time_series.data.iloc[-1]
        print(f"📈 **ПОСЛЕДНИЕ ЗНАЧЕНИЯ ПОКАЗАТЕЛЕЙ:**")
        for indicator, value in latest_values.items():
            print(f"• {indicator}: {value:.2f}")
        
        # Выполняем квантовый анализ
        print(f"\n🔬 **ВЫПОЛНЕНИЕ КВАНТОВОГО АНАЛИЗА...**")
        analysis_results = analyzer.quantum_entanglement_analysis(
            time_series=time_series,
            quantum_threshold=0.3
        )
        
        print(f"✅ Анализ завершен:")
        print(f"  - Квантовая когерентность: {analysis_results['quantum_signatures']['quantum_coherence']:.3f}")
        print(f"  - Окон запутанности: {len(analysis_results['quantum_entanglements'])}")
        
        # Создаем движок рекомендаций с профилем пациента
        print(f"\n💊 **ГЕНЕРАЦИЯ ПЕРСОНАЛИЗИРОВАННЫХ РЕКОМЕНДАЦИЙ...**")
        recommendation_engine = MedicalRecommendationEngine(patient_profile=profile)
        recommendations = recommendation_engine.analyze_patient_data(
            current_data=time_series,
            analysis_results=analysis_results
        )
        
        print(f"✅ Рекомендации сгенерированы: {len(recommendations)} рекомендаций")
        
        # Показываем статистику рекомендаций
        urgent_count = len([r for r in recommendations if r.type.value == "urgent"])
        warning_count = len([r for r in recommendations if r.type.value == "warning"])
        caution_count = len([r for r in recommendations if r.type.value == "caution"])
        monitoring_count = len([r for r in recommendations if r.type.value == "monitoring"])
        
        print(f"\n📊 **СТАТИСТИКА РЕКОМЕНДАЦИЙ:**")
        print(f"  🚨 Срочные: {urgent_count}")
        print(f"  ⚠️ Предупреждения: {warning_count}")
        print(f"  🔶 Осторожность: {caution_count}")
        print(f"  👁️ Мониторинг: {monitoring_count}")
        
        # Показываем топ-5 рекомендаций
        print(f"\n💊 **ТОП-5 РЕКОМЕНДАЦИЙ:**")
        for j, rec in enumerate(recommendations[:5], 1):
            print(f"\n{j}. {rec.title}")
            print(f"   Тип: {rec.type.value.upper()}")
            print(f"   Уровень риска: {rec.risk_level.value.upper()}")
            print(f"   Приоритет: {rec.priority}/10")
            print(f"   Уверенность: {rec.confidence*100:.0f}%")
            print(f"   Описание: {rec.description}")
            print(f"   Действие: {rec.action_required}")
            print(f"   Временные рамки: {rec.timeframe}")
            print(f"   Обоснование: {rec.medical_justification}")
        
        # Показываем персонализированные рекомендации из профиля
        personalized_recs = profile.get_personalized_recommendations()
        if personalized_recs:
            print(f"\n🎯 **ПЕРСОНАЛИЗИРОВАННЫЕ РЕКОМЕНДАЦИИ ИЗ ПРОФИЛЯ:**")
            for j, rec in enumerate(personalized_recs, 1):
                print(f"{j}. {rec}")
        
        print(f"\n{'='*60}")
    
    print(f"\n🎉 **ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА!**")
    print("Система MQEA успешно продемонстрировала персонализированные")
    print("медицинские рекомендации на основе профилей пациентов разных возрастов!")


if __name__ == "__main__":
    demonstrate_patient_profiles()

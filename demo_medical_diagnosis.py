#!/usr/bin/env python3
"""
Демонстрация расширенной медицинской диагностической системы MQEA
для работы с большими объемами данных, персонализации лечения
и прогнозирования рисков заболеваний.

Автор: Мухаммад Махизода
Таджикский национальный университет
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import time
import json
from pathlib import Path

from mqea.medical_diagnostic_system import (
    MedicalDiagnosticSystem, PatientProfile, DiagnosticResult, 
    RiskLevel, DiagnosticCategory, TreatmentRecommendation
)
from mqea.big_data_processor import BigDataProcessor
from mqea.core import MQEAAnalyzer


def create_sample_patients(n_patients: int = 50) -> list:
    """Создание образцов пациентов для демонстрации."""
    patients = []
    
    # Различные профили пациентов
    profiles = [
        {
            'age_range': (25, 35),
            'gender': 'female',
            'weight_range': (50, 70),
            'height_range': (160, 175),
            'medical_history': [],
            'lifestyle': {'smoking': False, 'sedentary': False, 'alcohol': 'none'},
            'risk_factors': ['low']
        },
        {
            'age_range': (45, 65),
            'gender': 'male',
            'weight_range': (70, 90),
            'height_range': (170, 185),
            'medical_history': ['hypertension'],
            'lifestyle': {'smoking': True, 'sedentary': True, 'alcohol': 'moderate'},
            'risk_factors': ['high']
        },
        {
            'age_range': (65, 85),
            'gender': 'female',
            'weight_range': (60, 80),
            'height_range': (155, 170),
            'medical_history': ['diabetes', 'hypertension'],
            'lifestyle': {'smoking': False, 'sedentary': True, 'alcohol': 'none'},
            'risk_factors': ['critical']
        }
    ]
    
    for i in range(n_patients):
        profile_template = np.random.choice(profiles)
        
        age = np.random.randint(*profile_template['age_range'])
        weight = np.random.uniform(*profile_template['weight_range'])
        height = np.random.uniform(*profile_template['height_range'])
        
        patient = PatientProfile(
            patient_id=f"P{i+1:04d}",
            age=age,
            gender=profile_template['gender'],
            weight=weight,
            height=height,
            medical_history=profile_template['medical_history'].copy(),
            current_medications=[],
            allergies=[],
            lifestyle_factors=profile_template['lifestyle'].copy(),
            genetic_factors=None
        )
        
        patients.append(patient)
    
    return patients


def generate_medical_data(patient: PatientProfile, days: int = 30) -> pd.DataFrame:
    """Генерация медицинских данных для пациента."""
    n_records = days * 24  # Каждый час
    
    # Базовые значения на основе профиля пациента
    base_values = {
        'heart_rate': 75 if patient.age < 50 else 80,
        'blood_pressure_systolic': 120 if 'hypertension' not in patient.medical_history else 140,
        'blood_pressure_diastolic': 80 if 'hypertension' not in patient.medical_history else 90,
        'temperature': 36.6,
        'oxygen_saturation': 98,
        'respiratory_rate': 16,
        'glucose': 5.0 if 'diabetes' not in patient.medical_history else 7.5,
        'cholesterol': 180 if patient.age < 50 else 220
    }
    
    # Корректировка на основе факторов риска
    if patient.lifestyle_factors.get('smoking', False):
        base_values['oxygen_saturation'] -= 2
        base_values['respiratory_rate'] += 2
    
    if patient.lifestyle_factors.get('sedentary', False):
        base_values['heart_rate'] += 5
        base_values['glucose'] += 0.5
    
    if patient.bmi > 30:
        base_values['blood_pressure_systolic'] += 10
        base_values['glucose'] += 1.0
    
    # Генерация временных рядов
    data = []
    for i in range(n_records):
        timestamp = datetime.now() - timedelta(hours=n_records-i)
        
        record = {
            'patient_id': patient.patient_id,
            'timestamp': timestamp,
            'age': patient.age,
            'gender': patient.gender,
            'bmi': patient.bmi
        }
        
        # Добавление медицинских показателей с вариацией
        for indicator, base_value in base_values.items():
            # Суточные циклы
            daily_cycle = 0.1 * np.sin(2 * np.pi * i / 24)
            
            # Случайная вариация
            noise = np.random.normal(0, base_value * 0.05)
            
            # Тренды (ухудшение со временем для пациентов с рисками)
            trend = 0
            if patient.age > 65:
                trend = i * 0.001
            if 'diabetes' in patient.medical_history:
                trend += i * 0.002
            
            value = base_value + daily_cycle + noise + trend
            
            # Ограничение значений в разумных пределах
            if indicator == 'heart_rate':
                value = max(40, min(200, value))
            elif indicator in ['blood_pressure_systolic', 'blood_pressure_diastolic']:
                value = max(60, min(250, value))
            elif indicator == 'temperature':
                value = max(35, min(42, value))
            elif indicator == 'oxygen_saturation':
                value = max(70, min(100, value))
            elif indicator == 'respiratory_rate':
                value = max(8, min(40, value))
            elif indicator == 'glucose':
                value = max(2, min(20, value))
            elif indicator == 'cholesterol':
                value = max(100, min(400, value))
            
            record[indicator] = round(value, 1)
        
        data.append(record)
    
    return pd.DataFrame(data)


def main():
    """Основная демонстрация медицинской диагностической системы."""
    print("=" * 80)
    print("🏥 ДЕМОНСТРАЦИЯ МЕДИЦИНСКОЙ ДИАГНОСТИЧЕСКОЙ СИСТЕМЫ MQEA")
    print("=" * 80)
    print("Автор: Мухаммад Махизода")
    print("Таджикский национальный университет")
    print("=" * 80)
    
    # 1. Инициализация системы
    print("\n🔧 ШАГ 1: Инициализация медицинской диагностической системы")
    print("-" * 60)
    
    medical_system = MedicalDiagnosticSystem(
        max_workers=4,
        enable_parallel_processing=True,
        enable_ml_models=True,
        enable_real_time_monitoring=True
    )
    
    print("✅ Система инициализирована")
    
    # 2. Создание профилей пациентов
    print("\n👥 ШАГ 2: Создание профилей пациентов")
    print("-" * 60)
    
    patients = create_sample_patients(20)
    
    for patient in patients:
        medical_system.add_patient_profile(patient)
    
    print(f"✅ Создано {len(patients)} профилей пациентов")
    
    # 3. Генерация медицинских данных
    print("\n📊 ШАГ 3: Генерация медицинских данных")
    print("-" * 60)
    
    all_medical_data = []
    for patient in patients[:5]:  # Анализируем первых 5 пациентов
        print(f"   Генерация данных для {patient.patient_id}...")
        patient_data = generate_medical_data(patient, days=7)
        all_medical_data.append(patient_data)
    
    print(f"✅ Сгенерированы данные для {len(all_medical_data)} пациентов")
    
    # 4. Анализ медицинских данных
    print("\n🔍 ШАГ 4: Анализ медицинских данных")
    print("-" * 60)
    
    diagnostic_results = []
    
    for i, patient_data in enumerate(all_medical_data):
        patient_id = patients[i].patient_id
        print(f"   Анализ данных пациента {patient_id}...")
        
        # Создание MedicalTimeSeries
        indicators = ['heart_rate', 'blood_pressure_systolic', 'blood_pressure_diastolic',
                     'temperature', 'oxygen_saturation', 'respiratory_rate', 'glucose', 'cholesterol']
        
        time_series = pd.DataFrame({
            'timestamp': patient_data['timestamp'],
            **{indicator: patient_data[indicator] for indicator in indicators}
        })
        
        # Конвертация в MedicalTimeSeries (упрощенная версия)
        from mqea.data_processor import MedicalTimeSeries
        medical_time_series = MedicalTimeSeries(
            data=time_series.set_index('timestamp'),
            indicators=indicators,
            timestamps=time_series['timestamp'].tolist(),
            missing_data_mask=time_series[indicators].isnull(),
            quantum_states={},
            metadata={'patient_id': patient_id}
        )
        
        # Диагностика
        try:
            diagnostic = medical_system.analyze_patient_data(
                patient_id=patient_id,
                medical_data=medical_time_series
            )
            diagnostic_results.append(diagnostic)
            
            print(f"     ✅ Категория: {diagnostic.category.value}")
            print(f"     ✅ Уровень риска: {diagnostic.risk_level.value}")
            print(f"     ✅ Уверенность: {diagnostic.confidence:.3f}")
            
        except Exception as e:
            print(f"     ❌ Ошибка анализа: {e}")
    
    print(f"✅ Завершен анализ {len(diagnostic_results)} пациентов")
    
    # 5. Прогнозирование рисков
    print("\n🔮 ШАГ 5: Прогнозирование рисков заболеваний")
    print("-" * 60)
    
    for i, patient in enumerate(patients[:3]):  # Прогноз для первых 3 пациентов
        print(f"   Прогноз рисков для {patient.patient_id}...")
        
        try:
            risk_predictions = medical_system.predict_disease_risk(
                patient_id=patient.patient_id,
                time_horizon_days=30
            )
            
            print(f"     Прогноз на 30 дней:")
            for category, risk in risk_predictions.items():
                risk_level = "низкий" if risk < 0.3 else "средний" if risk < 0.6 else "высокий" if risk < 0.8 else "критический"
                print(f"       - {category}: {risk:.3f} ({risk_level})")
                
        except Exception as e:
            print(f"     ❌ Ошибка прогнозирования: {e}")
    
    # 6. Генерация планов лечения
    print("\n💊 ШАГ 6: Генерация планов лечения")
    print("-" * 60)
    
    for diagnostic in diagnostic_results[:3]:  # Планы для первых 3 диагнозов
        print(f"   План лечения для {diagnostic.patient_id}...")
        
        try:
            treatment_plan = medical_system.generate_treatment_plan(
                patient_id=diagnostic.patient_id,
                diagnostic_result=diagnostic
            )
            
            print(f"     Создано {len(treatment_plan)} рекомендаций:")
            for j, treatment in enumerate(treatment_plan):
                print(f"       {j+1}. {treatment.description}")
                print(f"          Приоритет: {treatment.priority}, Эффективность: {treatment.expected_effectiveness:.2f}")
                
        except Exception as e:
            print(f"     ❌ Ошибка генерации плана: {e}")
    
    # 7. Демонстрация работы с большими данными
    print("\n📈 ШАГ 7: Демонстрация работы с большими данными")
    print("-" * 60)
    
    # Создание большого набора данных
    print("   Создание большого набора данных...")
    big_data = []
    
    for patient in patients:
        patient_data = generate_medical_data(patient, days=1)  # 1 день данных
        big_data.append(patient_data)
    
    big_dataframe = pd.concat(big_data, ignore_index=True)
    print(f"   ✅ Создан набор данных: {len(big_dataframe):,} записей")
    
    # Инициализация процессора больших данных
    big_data_processor = BigDataProcessor(
        chunk_size=1000,
        max_workers=2,
        enable_dask=False,  # Отключаем Dask для демонстрации
        memory_limit_gb=4.0
    )
    
    # Обработка данных
    print("   Обработка больших данных...")
    start_time = time.time()
    
    results = big_data_processor.process_large_dataset(
        data_source=big_dataframe,
        output_format="json",
        output_path="output/medical_analysis"
    )
    
    processing_time = time.time() - start_time
    
    print(f"   ✅ Обработка завершена за {processing_time:.2f} секунд")
    print(f"   ✅ Обработано чанков: {results['successful_chunks']}/{results['total_chunks']}")
    print(f"   ✅ Проанализировано пациентов: {results['total_patients']}")
    print(f"   ✅ Скорость: {results['total_patients']/processing_time:.1f} пациентов/сек")
    
    # 8. Статистика и сводка
    print("\n📊 ШАГ 8: Статистика и сводка")
    print("-" * 60)
    
    # Статистика диагностики
    risk_levels = [d.risk_level for d in diagnostic_results]
    risk_counts = {level.value: risk_levels.count(level) for level in RiskLevel}
    
    categories = [d.category for d in diagnostic_results]
    category_counts = {cat.value: categories.count(cat) for cat in DiagnosticCategory}
    
    print("📈 Статистика диагностики:")
    print(f"   Уровни риска:")
    for level, count in risk_counts.items():
        print(f"     - {level}: {count} пациентов")
    
    print(f"   Категории заболеваний:")
    for category, count in category_counts.items():
        print(f"     - {category}: {count} пациентов")
    
    # Статистика обработки больших данных
    stats = big_data_processor.get_processing_statistics()
    print(f"\n📈 Статистика обработки больших данных:")
    print(f"   - Всего чанков: {stats['total_chunks_processed']}")
    print(f"   - Пациентов проанализировано: {stats['total_patients_analyzed']}")
    print(f"   - Время обработки: {stats['total_processing_time']:.2f} сек")
    print(f"   - Скорость: {stats['average_patients_per_second']:.1f} пациентов/сек")
    print(f"   - Успешность: {stats['success_rate']:.1%}")
    
    # 9. Сохранение результатов
    print("\n💾 ШАГ 9: Сохранение результатов")
    print("-" * 60)
    
    # Создание директории для результатов
    output_dir = Path("output/medical_diagnosis_demo")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Сохранение диагностических результатов
    diagnostic_data = []
    for diagnostic in diagnostic_results:
        diagnostic_data.append({
            'patient_id': diagnostic.patient_id,
            'timestamp': diagnostic.timestamp.isoformat(),
            'category': diagnostic.category.value,
            'risk_level': diagnostic.risk_level.value,
            'confidence': diagnostic.confidence,
            'indicators': diagnostic.indicators,
            'recommendations': diagnostic.recommendations,
            'urgency_score': diagnostic.urgency_score,
            'follow_up_required': diagnostic.follow_up_required
        })
    
    with open(output_dir / "diagnostic_results.json", 'w', encoding='utf-8') as f:
        json.dump(diagnostic_data, f, indent=2, ensure_ascii=False)
    
    # Сохранение статистики
    with open(output_dir / "statistics.json", 'w', encoding='utf-8') as f:
        json.dump({
            'risk_levels': risk_counts,
            'categories': category_counts,
            'processing_stats': stats,
            'total_patients': len(patients),
            'analyzed_patients': len(diagnostic_results)
        }, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Результаты сохранены в {output_dir}")
    
    # 10. Заключение
    print("\n" + "=" * 80)
    print("🎉 ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА УСПЕШНО!")
    print("=" * 80)
    print("Система MQEA продемонстрировала:")
    print("✅ Анализ больших объемов медицинских данных")
    print("✅ Персонализированную диагностику")
    print("✅ Прогнозирование рисков заболеваний")
    print("✅ Генерацию планов лечения")
    print("✅ Параллельную обработку")
    print("✅ Масштабируемость")
    print("\n🌐 Для интерактивной работы откройте: http://127.0.0.1:8501")
    print("📚 Изучите код в папке mqea/ для глубокого понимания")
    print("=" * 80)
    
    # Закрытие процессора
    big_data_processor.close()


if __name__ == "__main__":
    main()

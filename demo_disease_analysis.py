#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Демонстрация квантового анализа признаков заболеваний MQEA.

Автор: Мухаммад Махизода
Таджикский национальный университет
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mqea import MQEAAnalyzer, DiseasePatternAnalyzer
from mqea.data_processor import MedicalTimeSeries
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def create_sample_medical_data():
    """Создание примерных медицинских данных."""
    # Генерируем временные метки
    start_date = datetime.now() - timedelta(days=30)
    timestamps = [start_date + timedelta(days=i) for i in range(30)]
    
    # Создаем данные с признаками ВИЧ
    data = {
        'cd4_count': np.random.normal(300, 50, 30),  # Низкий CD4 (признак ВИЧ)
        'cd4_percentage': np.random.normal(15, 3, 30),  # Низкий процент
        'viral_load': np.random.normal(50000, 10000, 30),  # Высокая вирусная нагрузка
        'white_blood_cells': np.random.normal(3000, 500, 30),  # Низкие лейкоциты
        'lymphocytes': np.random.normal(800, 200, 30),  # Низкие лимфоциты
        'hemoglobin': np.random.normal(10, 1, 30),  # Низкий гемоглобин
        'platelets': np.random.normal(120000, 20000, 30),  # Низкие тромбоциты
        'temperature': np.random.normal(37.5, 0.5, 30),  # Повышенная температура
        'heart_rate': np.random.normal(90, 10, 30)
    }
    
    df = pd.DataFrame(data, index=timestamps)
    
    # Создание маски пропущенных данных
    missing_mask = pd.DataFrame(False, index=df.index, columns=df.columns)
    
    # Создание квантовых состояний
    quantum_states = {}
    for indicator in df.columns:
        quantum_states[indicator] = np.zeros(len(df))
    
    # Расчет процента пропущенных данных
    total_cells = len(df) * len(df.columns)
    missing_cells = missing_mask.sum().sum()
    missing_percentage = (missing_cells / total_cells * 100) if total_cells > 0 else 0.0
    
    return MedicalTimeSeries(
        data=df,
        indicators=list(data.keys()),
        timestamps=pd.DatetimeIndex(timestamps),
        missing_data_mask=missing_mask,
        quantum_states=quantum_states,
        metadata={
            'source': 'synthetic',
            'total_points': len(df),
            'missing_percentage': missing_percentage
        }
    )


def demo_hiv_analysis():
    """Демонстрация анализа ВИЧ."""
    print("=" * 70)
    print("🔬 ДЕМОНСТРАЦИЯ КВАНТОВОГО АНАЛИЗА ПРИЗНАКОВ ВИЧ/СПИД")
    print("=" * 70)
    
    # Создание анализатора
    analyzer = DiseasePatternAnalyzer()
    
    # Создание примерных данных
    print("\n📊 Создание примерных медицинских данных...")
    medical_data = create_sample_medical_data()
    print(f"✅ Данные созданы: {len(medical_data.indicators)} показателей, {len(medical_data.timestamps)} точек")
    
    # Симптомы пациента
    patient_symptoms = [
        'fever',
        'fatigue',
        'weight_loss',
        'night_sweats',
        'swollen_lymph_nodes',
        'recurrent_infections'
    ]
    
    # Факторы риска
    risk_factors = [
        'unprotected_sex',
        'iv_drug_use'
    ]
    
    print(f"\n📋 Симптомы пациента: {', '.join(patient_symptoms)}")
    print(f"⚠️  Факторы риска: {', '.join(risk_factors)}")
    
    # Анализ заболеваний
    print("\n⚛️  Выполнение квантового анализа признаков заболеваний...")
    results = analyzer.analyze_disease_patterns(
        medical_data=medical_data,
        patient_symptoms=patient_symptoms,
        risk_factors=risk_factors
    )
    
    # Вывод результатов
    print("\n" + "=" * 70)
    print("📊 РЕЗУЛЬТАТЫ АНАЛИЗА")
    print("=" * 70)
    
    for i, result in enumerate(results[:5], 1):  # Показываем топ-5
        print(f"\n{i}. {result.disease_name} ({result.disease_code})")
        print(f"   Категория: {result.category.value}")
        print(f"   Вероятность: {result.probability:.1%}")
        print(f"   Уверенность: {result.confidence:.1%}")
        print(f"   Уровень срочности: {result.urgency_level.upper()}")
        
        if result.matched_indicators:
            print(f"   📈 Совпавшие показатели:")
            for indicator in result.matched_indicators[:5]:
                print(f"      - {indicator}")
        
        if result.matched_symptoms:
            print(f"   🦠 Совпавшие симптомы:")
            for symptom in result.matched_symptoms[:5]:
                print(f"      - {symptom}")
        
        if result.risk_factors_present:
            print(f"   ⚠️  Факторы риска:")
            for risk in result.risk_factors_present:
                print(f"      - {risk}")
        
        if result.recommendations:
            print(f"   💡 Рекомендации:")
            for rec in result.recommendations[:3]:
                print(f"      {rec}")
        
        if result.diagnostic_tests_recommended:
            print(f"   🧪 Рекомендуемые тесты:")
            for test in result.diagnostic_tests_recommended[:3]:
                print(f"      - {test}")
    
    # Детальный анализ ВИЧ
    if results and results[0].disease_code.startswith('B20'):
        print("\n" + "=" * 70)
        print("🔍 ДЕТАЛЬНЫЙ АНАЛИЗ ВИЧ/СПИД")
        print("=" * 70)
        
        hiv_result = results[0]
        print(f"\nВероятность наличия признаков ВИЧ: {hiv_result.probability:.1%}")
        print(f"Уверенность в анализе: {hiv_result.confidence:.1%}")
        
        print(f"\n📊 Квантовая подпись:")
        for indicator, value in hiv_result.quantum_signature.items():
            print(f"   {indicator}: {value:.2f}")
        
        print(f"\n⚠️  КРИТИЧЕСКИЕ РЕКОМЕНДАЦИИ:")
        for rec in hiv_result.recommendations:
            print(f"   {rec}")


def demo_cancer_analysis():
    """Демонстрация анализа рака."""
    print("\n" + "=" * 70)
    print("🔬 ДЕМОНСТРАЦИЯ КВАНТОВОГО АНАЛИЗА ПРИЗНАКОВ РАКА")
    print("=" * 70)
    
    analyzer = DiseasePatternAnalyzer()
    
    # Данные с признаками рака
    start_date = datetime.now() - timedelta(days=30)
    timestamps = [start_date + timedelta(days=i) for i in range(30)]
    
    data = {
        'tumor_markers': np.random.normal(25, 5, 30),  # Повышенные онкомаркеры
        'white_blood_cells': np.random.normal(15000, 2000, 30),  # Повышенные лейкоциты
        'hemoglobin': np.random.normal(9, 1, 30),  # Низкий гемоглобин
        'platelets': np.random.normal(100000, 15000, 30),  # Низкие тромбоциты
        'lactate_dehydrogenase': np.random.normal(400, 50, 30),  # Повышенный ЛДГ
        'c_reactive_protein': np.random.normal(15, 3, 30),  # Повышенный СРБ
        'temperature': np.random.normal(37.8, 0.5, 30)
    }
    
    df = pd.DataFrame(data, index=timestamps)
    
    # Создание маски пропущенных данных
    missing_mask = pd.DataFrame(False, index=df.index, columns=df.columns)
    
    # Создание квантовых состояний
    quantum_states = {}
    for indicator in df.columns:
        quantum_states[indicator] = np.zeros(len(df))
    
    # Расчет процента пропущенных данных
    total_cells = len(df) * len(df.columns)
    missing_cells = missing_mask.sum().sum()
    missing_percentage = (missing_cells / total_cells * 100) if total_cells > 0 else 0.0
    
    medical_data = MedicalTimeSeries(
        data=df,
        indicators=list(data.keys()),
        timestamps=pd.DatetimeIndex(timestamps),
        missing_data_mask=missing_mask,
        quantum_states=quantum_states,
        metadata={
            'source': 'synthetic_cancer',
            'total_points': len(df),
            'missing_percentage': missing_percentage
        }
    )
    
    patient_symptoms = [
        'unexplained_weight_loss',
        'fatigue',
        'fever',
        'pain',
        'night_sweats'
    ]
    
    risk_factors = [
        'age_over_50',
        'smoking',
        'family_history'
    ]
    
    print(f"\n📋 Симптомы: {', '.join(patient_symptoms)}")
    print(f"⚠️  Факторы риска: {', '.join(risk_factors)}")
    
    print("\n⚛️  Выполнение квантового анализа...")
    results = analyzer.analyze_disease_patterns(
        medical_data=medical_data,
        patient_symptoms=patient_symptoms,
        risk_factors=risk_factors
    )
    
    # Поиск результатов по раку
    cancer_results = [r for r in results if r.category.value == 'oncological']
    
    if cancer_results:
        print("\n" + "=" * 70)
        print("📊 РЕЗУЛЬТАТЫ АНАЛИЗА РАКА")
        print("=" * 70)
        
        for result in cancer_results[:3]:
            print(f"\n{result.disease_name} ({result.disease_code})")
            print(f"   Вероятность: {result.probability:.1%}")
            print(f"   Уровень срочности: {result.urgency_level.upper()}")
            
            if result.recommendations:
                print(f"   💡 Рекомендации:")
                for rec in result.recommendations[:2]:
                    print(f"      {rec}")


def main():
    """Основная функция."""
    print("🏥 MQEA - Квантовый анализ признаков заболеваний")
    print("Автор: Мухаммад Махизода")
    print("Таджикский национальный университет")
    
    try:
        # Анализ ВИЧ
        demo_hiv_analysis()
        
        # Анализ рака
        demo_cancer_analysis()
        
        print("\n" + "=" * 70)
        print("✅ ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")
        print("=" * 70)
        print("\n💡 Важно: Этот анализ предназначен для демонстрации возможностей системы.")
        print("   Для реальной диагностики необходимо обратиться к врачу.")
        
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

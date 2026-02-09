"""
Демонстрация системы медицинских рекомендаций MQEA.

Автор: Мухаммад Махизода
Таджикский национальный университет
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mqea import MQEAAnalyzer, MedicalRecommendationEngine
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def create_test_patient_data():
    """Создает тестовые данные пациента с различными патологиями."""
    
    # Создаем временные метки (24 часа, каждые 15 минут)
    start_time = datetime.now() - timedelta(hours=24)
    timestamps = pd.date_range(
        start=start_time,
        periods=96,  # 24 часа * 4 (каждые 15 минут)
        freq='15T'
    )
    
    # Создаем данные с различными патологиями
    data = {
        'heart_rate': np.random.normal(95, 10, 96),  # Тахикардия
        'blood_pressure_systolic': np.random.normal(150, 15, 96),  # Гипертония
        'blood_pressure_diastolic': np.random.normal(95, 10, 96),  # Гипертония
        'temperature': np.random.normal(37.5, 0.3, 96),  # Лихорадка
        'oxygen_saturation': np.random.normal(92, 2, 96),  # Гипоксемия
        'respiratory_rate': np.random.normal(22, 3, 96),  # Тахипноэ
        'glucose': np.random.normal(6.7, 1.1, 96),  # Гипергликемия (6.7 ммоль/л ≈ 120 мг/дл)
        'cholesterol': np.random.normal(250, 30, 96)  # Гиперхолестеринемия
    }
    
    # Создаем DataFrame
    df = pd.DataFrame(data, index=timestamps)
    
    # Создаем объект MedicalTimeSeries
    from mqea.data_processor import MedicalTimeSeries
    missing_mask = df.isnull()
    
    return MedicalTimeSeries(
        data=df,
        indicators=list(df.columns),
        timestamps=df.index,
        missing_data_mask=missing_mask,
        quantum_states={},
        metadata={
            'source': 'test_patient', 
            'patient_id': 'TEST001',
            'missing_percentage': 0.0
        }
    )


def main():
    """Главная функция демонстрации."""
    
    print("🧬⚛️ MQEA - ДЕМОНСТРАЦИЯ МЕДИЦИНСКИХ РЕКОМЕНДАЦИЙ")
    print("=" * 60)
    print("Автор: Мухаммад Махизода")
    print("Таджикский национальный университет")
    print("=" * 60)
    
    # Инициализация
    print("\n🔧 Инициализация системы...")
    analyzer = MQEAAnalyzer()
    recommendation_engine = MedicalRecommendationEngine()
    
    # Создание тестовых данных
    print("\n📊 Создание тестовых данных пациента...")
    patient_data = create_test_patient_data()
    
    print(f"✅ Данные созданы:")
    print(f"   - Показателей: {len(patient_data.indicators)}")
    print(f"   - Точек данных: {len(patient_data.timestamps)}")
    print(f"   - Период: {patient_data.timestamps.min()} - {patient_data.timestamps.max()}")
    
    # Показываем последние значения
    print(f"\n📈 Последние значения показателей:")
    latest_values = patient_data.data.iloc[-1]
    for indicator, value in latest_values.items():
        print(f"   - {indicator}: {value:.2f}")
    
    # Выполнение анализа
    print("\n🔬 Выполнение квантового анализа...")
    analysis_results = analyzer.quantum_entanglement_analysis(
        patient_data, 
        quantum_threshold=0.3
    )
    
    print(f"✅ Анализ завершен:")
    print(f"   - Квантовая когерентность: {analysis_results['quantum_signatures']['quantum_coherence']:.3f}")
    print(f"   - Окон запутанности: {len(analysis_results['quantum_entanglements'])}")
    
    # Генерация рекомендаций
    print("\n💊 Генерация медицинских рекомендаций...")
    recommendations = recommendation_engine.analyze_patient_data(
        patient_data,
        analysis_results
    )
    
    print(f"✅ Рекомендации сгенерированы: {len(recommendations)} рекомендаций")
    
    # Группировка по типам
    urgent = [r for r in recommendations if r.type.value == "urgent"]
    warnings = [r for r in recommendations if r.type.value == "warning"]
    cautions = [r for r in recommendations if r.type.value == "caution"]
    monitoring = [r for r in recommendations if r.type.value == "monitoring"]
    
    print(f"\n📊 Статистика рекомендаций:")
    print(f"   🚨 Срочные: {len(urgent)}")
    print(f"   ⚠️ Предупреждения: {len(warnings)}")
    print(f"   🔶 Осторожность: {len(cautions)}")
    print(f"   👁️ Мониторинг: {len(monitoring)}")
    
    # Показываем рекомендации
    print(f"\n💊 ДЕТАЛЬНЫЕ РЕКОМЕНДАЦИИ:")
    print("=" * 60)
    
    for i, rec in enumerate(recommendations, 1):
        print(f"\n{i}. {rec.title}")
        print(f"   Тип: {rec.type.value.upper()}")
        print(f"   Уровень риска: {rec.risk_level.value.upper()}")
        print(f"   Приоритет: {rec.priority}/10")
        print(f"   Уверенность: {rec.confidence:.1%}")
        print(f"   Описание: {rec.description}")
        print(f"   Действие: {rec.action_required}")
        print(f"   Временные рамки: {rec.timeframe}")
        print(f"   Обоснование: {rec.medical_justification}")
        print(f"   Показатели: {', '.join(rec.indicators)}")
        print("-" * 40)
    
    # Генерация сводного отчета
    print(f"\n📋 СВОДНЫЙ ОТЧЕТ:")
    print("=" * 60)
    report = recommendation_engine.generate_summary_report(recommendations)
    print(report)
    
    # Сохранение в файл
    print(f"\n💾 Сохранение рекомендаций в файл...")
    rec_data = []
    for rec in recommendations:
        rec_data.append({
            'Тип': rec.type.value,
            'Уровень_риска': rec.risk_level.value,
            'Заголовок': rec.title,
            'Описание': rec.description,
            'Действие': rec.action_required,
            'Временные_рамки': rec.timeframe,
            'Приоритет': rec.priority,
            'Уверенность': f"{rec.confidence:.1%}",
            'Показатели': ', '.join(rec.indicators)
        })
    
    df_recs = pd.DataFrame(rec_data)
    filename = f"medical_recommendations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df_recs.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"✅ Рекомендации сохранены в файл: {filename}")
    
    print(f"\n🎉 Демонстрация завершена!")
    print(f"Система MQEA успешно проанализировала данные пациента и сгенерировала персонализированные медицинские рекомендации.")


if __name__ == "__main__":
    main()

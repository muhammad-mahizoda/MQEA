#!/usr/bin/env python3
"""
Отладка отфильтрованных данных MQEA
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
import pandas as pd
import numpy as np

def debug_filtered_data():
    """Отладка отфильтрованных данных MQEA"""
    print("🔍 Отладка отфильтрованных данных MQEA...")
    print("=" * 60)
    
    # Импортируем необходимые модули
    try:
        from mqea.core import MQEAAnalyzer
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        return False
    
    # Создаем анализатор
    analyzer = MQEAAnalyzer()
    
    # Тестовый профиль пациента
    test_profile = {
        'heart_rate': 80,
        'blood_pressure_systolic': 130,
        'blood_pressure_diastolic': 85,
        'temperature': 36.8,
        'oxygen_saturation': 96,
        'respiratory_rate': 18,
        'glucose': 6.5,
        'cholesterol': 220
    }
    
    # Генерируем данные и выполняем анализ
    data = analyzer.generate_synthetic_data(
        duration_hours=24,
        sampling_rate_minutes=15,
        add_noise=True,
        add_missing_data=True,
        patient_profile=test_profile
    )
    
    analysis_results = analyzer.quantum_entanglement_analysis(
        data, quantum_threshold=0.3
    )
    
    print("📊 ИСХОДНЫЕ ДАННЫЕ:")
    print("-" * 50)
    for key, value in analysis_results.items():
        print(f"• {key}: {type(value)}")
        if isinstance(value, dict):
            for sub_key, sub_value in value.items():
                print(f"  - {sub_key}: {sub_value} ({type(sub_value)})")
    
    # Импортируем функцию фильтрации
    sys.path.append('webapp')
    from modern_medical_app import _filter_mqea_data
    
    filtered_data = _filter_mqea_data(analysis_results)
    
    print(f"\n📊 ОТФИЛЬТРОВАННЫЕ ДАННЫЕ:")
    print("-" * 50)
    for key, value in filtered_data.items():
        print(f"• {key}: {type(value)}")
        if isinstance(value, dict):
            for sub_key, sub_value in value.items():
                print(f"  - {sub_key}: {sub_value} ({type(sub_value)})")
        else:
            print(f"  Значение: {value}")
    
    # Проверяем ключевые метрики
    print(f"\n🔍 ПРОВЕРКА КЛЮЧЕВЫХ МЕТРИК:")
    print("-" * 50)
    
    # Исходные метрики
    original_coherence = analysis_results.get('quantum_signatures', {}).get('quantum_coherence', 0)
    original_pairs = analysis_results.get('quantum_signatures', {}).get('entangled_pairs_count', 0)
    original_max_ent = analysis_results.get('quantum_signatures', {}).get('average_entanglement', 0)
    
    print(f"Исходные метрики:")
    print(f"• Когерентность: {original_coherence}")
    print(f"• Запутанных пар: {original_pairs}")
    print(f"• Макс. запутанность: {original_max_ent}")
    
    # Отфильтрованные метрики
    filtered_coherence = filtered_data.get('quantum_coherence', 0)
    filtered_pairs = filtered_data.get('entangled_pairs', 0)
    filtered_max_ent = filtered_data.get('max_entanglement', 0)
    
    print(f"\nОтфильтрованные метрики:")
    print(f"• Когерентность: {filtered_coherence}")
    print(f"• Запутанных пар: {filtered_pairs}")
    print(f"• Макс. запутанность: {filtered_max_ent}")
    
    # Проверяем, что метрики сохранились
    print(f"\n✅ ПРОВЕРКА СОХРАНЕНИЯ:")
    print("-" * 50)
    
    if abs(original_coherence - filtered_coherence) < 0.001:
        print("✅ Когерентность сохранилась")
    else:
        print(f"❌ Когерентность изменилась: {original_coherence} → {filtered_coherence}")
    
    if original_pairs == filtered_pairs:
        print("✅ Количество запутанных пар сохранилось")
    else:
        print(f"❌ Количество запутанных пар изменилось: {original_pairs} → {filtered_pairs}")
    
    if abs(original_max_ent - filtered_max_ent) < 0.001:
        print("✅ Максимальная запутанность сохранилась")
    else:
        print(f"❌ Максимальная запутанность изменилась: {original_max_ent} → {filtered_max_ent}")
    
    # Проверяем сериализацию
    print(f"\n💾 ПРОВЕРКА СЕРИАЛИЗАЦИИ:")
    print("-" * 50)
    
    try:
        import json
        json_str = json.dumps(filtered_data)
        print("✅ Данные успешно сериализованы")
        print(f"Размер JSON: {len(json_str)} символов")
    except Exception as e:
        print(f"❌ Ошибка сериализации: {e}")

if __name__ == "__main__":
    debug_filtered_data()

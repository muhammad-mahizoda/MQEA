"""
Тесты для MQEA - Medical Quantum Entanglement Analysis.

Проверяет корректность работы основных компонентов системы.
"""

import unittest
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import sys
import os

# Добавляем путь к модулю
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mqea import MQEAAnalyzer, QuantumEntanglementEngine, MedicalDataProcessor, MQEAVisualizer


class TestQuantumEntanglementEngine(unittest.TestCase):
    """Тесты для движка квантовой запутанности."""
    
    def setUp(self):
        """Настройка тестов."""
        self.engine = QuantumEntanglementEngine(hbar=1.0)
    
    def test_create_quantum_state(self):
        """Тест создания квантового состояния."""
        state = self.engine.create_quantum_state('heart_rate', 75.0, 0.1)
        
        self.assertIsNotNone(state)
        self.assertEqual(state.phase, 75.0 * np.pi / 2)  # Проверяем фазу
        self.assertGreater(state.energy, 0)  # Энергия должна быть положительной
    
    def test_calculate_entanglement(self):
        """Тест вычисления запутанности."""
        # Создаем два квантовых состояния
        self.engine.create_quantum_state('heart_rate', 75.0, 0.1)
        self.engine.create_quantum_state('blood_pressure', 120.0, 0.15)
        
        # Вычисляем запутанность
        entangled_pair = self.engine.calculate_entanglement('heart_rate', 'blood_pressure')
        
        self.assertIsNotNone(entangled_pair)
        self.assertGreaterEqual(entangled_pair.entanglement_strength, 0)
        self.assertLessEqual(entangled_pair.entanglement_strength, 1)
    
    def test_quantum_measurement(self):
        """Тест квантового измерения."""
        self.engine.create_quantum_state('heart_rate', 75.0, 0.1)
        
        measured_value, uncertainty = self.engine.quantum_measurement('heart_rate')
        
        self.assertIsInstance(measured_value, float)
        self.assertIsInstance(uncertainty, float)
        self.assertGreaterEqual(measured_value, 0)
        self.assertGreater(uncertainty, 0)
    
    def test_entanglement_network(self):
        """Тест построения сети запутанности."""
        # Создаем несколько состояний
        self.engine.create_quantum_state('indicator1', 50.0, 0.1)
        self.engine.create_quantum_state('indicator2', 60.0, 0.1)
        self.engine.create_quantum_state('indicator3', 70.0, 0.1)
        
        # Вычисляем запутанности
        self.engine.calculate_entanglement('indicator1', 'indicator2')
        self.engine.calculate_entanglement('indicator2', 'indicator3')
        
        network = self.engine.get_entanglement_network()
        
        self.assertIsInstance(network, dict)
        self.assertIn('indicator1', network)
        self.assertIn('indicator2', network)


class TestMedicalDataProcessor(unittest.TestCase):
    """Тесты для процессора медицинских данных."""
    
    def setUp(self):
        """Настройка тестов."""
        self.processor = MedicalDataProcessor()
    
    def test_generate_synthetic_data(self):
        """Тест генерации синтетических данных."""
        time_series = self.processor.generate_synthetic_medical_data(
            duration_hours=1,
            sampling_rate_minutes=5,
            add_noise=True,
            add_missing_data=True
        )
        
        self.assertIsNotNone(time_series)
        self.assertGreater(len(time_series.indicators), 0)
        self.assertGreater(len(time_series.timestamps), 0)
        self.assertIsInstance(time_series.data, pd.DataFrame)
    
    def test_quantum_imputation(self):
        """Тест квантового заполнения пропусков."""
        # Создаем данные с пропусками
        time_series = self.processor.generate_synthetic_medical_data(
            duration_hours=2,
            sampling_rate_minutes=10,
            add_missing_data=True
        )
        
        # Заполняем пропуски
        filled_data = self.processor.quantum_imputation(time_series, max_iterations=10)
        
        self.assertIsNotNone(filled_data)
        self.assertEqual(filled_data.missing_data_mask.sum().sum(), 0)  # Не должно быть пропусков
    
    def test_detect_temporal_patterns(self):
        """Тест обнаружения временных паттернов."""
        time_series = self.processor.generate_synthetic_medical_data(
            duration_hours=6,
            sampling_rate_minutes=15
        )
        
        patterns = self.processor.detect_temporal_patterns(time_series)
        
        self.assertIsInstance(patterns, list)
        for pattern in patterns:
            self.assertIn(pattern.pattern_type, ['periodic', 'trend_increasing', 'trend_decreasing', 'anomaly', 'quantum_entangled'])


class TestMQEAAnalyzer(unittest.TestCase):
    """Тесты для основного анализатора MQEA."""
    
    def setUp(self):
        """Настройка тестов."""
        self.analyzer = MQEAAnalyzer()
    
    def test_initialization(self):
        """Тест инициализации анализатора."""
        self.assertIsNotNone(self.analyzer.quantum_engine)
        self.assertIsNotNone(self.analyzer.data_processor)
        self.assertTrue(self.analyzer.enable_quantum_imputation)
        self.assertTrue(self.analyzer.enable_pattern_detection)
    
    def test_generate_synthetic_data(self):
        """Тест генерации синтетических данных."""
        time_series = self.analyzer.generate_synthetic_data(
            duration_hours=1,
            sampling_rate_minutes=10
        )
        
        self.assertIsNotNone(time_series)
        self.assertIsNotNone(self.analyzer.current_data)
    
    def test_quantum_entanglement_analysis(self):
        """Тест квантового анализа запутанности."""
        # Генерируем данные
        time_series = self.analyzer.generate_synthetic_data(
            duration_hours=2,
            sampling_rate_minutes=15
        )
        
        # Выполняем анализ
        results = self.analyzer.quantum_entanglement_analysis(time_series)
        
        self.assertIsNotNone(results)
        self.assertIn('quantum_entanglements', results)
        self.assertIn('quantum_signatures', results)
        self.assertIn('temporal_analysis', results)
    
    def test_fill_missing_data(self):
        """Тест заполнения пропущенных данных."""
        # Генерируем данные с пропусками
        time_series = self.analyzer.generate_synthetic_data(
            duration_hours=1,
            sampling_rate_minutes=10,
            add_missing_data=True
        )
        
        # Заполняем пропуски
        filled_data = self.analyzer.fill_missing_data(time_series, method='quantum')
        
        self.assertIsNotNone(filled_data)
        self.assertEqual(filled_data.missing_data_mask.sum().sum(), 0)
    
    def test_detect_patterns(self):
        """Тест обнаружения паттернов."""
        # Генерируем данные
        time_series = self.analyzer.generate_synthetic_data(
            duration_hours=3,
            sampling_rate_minutes=20
        )
        
        # Обнаруживаем паттерны
        patterns = self.analyzer.detect_patterns(time_series)
        
        self.assertIsInstance(patterns, list)
        self.assertIsNotNone(self.analyzer.detected_patterns)
    
    def test_get_analysis_summary(self):
        """Тест получения сводки анализа."""
        # Генерируем данные и выполняем анализ
        time_series = self.analyzer.generate_synthetic_data(duration_hours=1)
        self.analyzer.quantum_entanglement_analysis(time_series)
        self.analyzer.detect_patterns(time_series)
        
        summary = self.analyzer.get_analysis_summary()
        
        self.assertIsNotNone(summary)
        self.assertIn('data_info', summary)
        self.assertIn('quantum_analysis', summary)
        self.assertIn('patterns_detected', summary)
    
    def test_reset(self):
        """Тест сброса анализатора."""
        # Генерируем данные
        self.analyzer.generate_synthetic_data(duration_hours=1)
        
        # Сбрасываем
        self.analyzer.reset()
        
        self.assertIsNone(self.analyzer.current_data)
        self.assertEqual(len(self.analyzer.analysis_results), 0)
        self.assertEqual(len(self.analyzer.detected_patterns), 0)


class TestMQEAVisualizer(unittest.TestCase):
    """Тесты для визуализатора MQEA."""
    
    def setUp(self):
        """Настройка тестов."""
        self.visualizer = MQEAVisualizer()
        self.analyzer = MQEAAnalyzer()
    
    def test_initialization(self):
        """Тест инициализации визуализатора."""
        self.assertIsNotNone(self.visualizer.colors)
        self.assertEqual(self.visualizer.theme, 'plotly_white')
    
    def test_plot_time_series(self):
        """Тест создания графика временных рядов."""
        # Генерируем данные
        time_series = self.analyzer.generate_synthetic_data(
            duration_hours=1,
            sampling_rate_minutes=10
        )
        
        # Создаем график
        fig = self.visualizer.plot_time_series(time_series, interactive=True)
        
        self.assertIsNotNone(fig)
        self.assertIsInstance(fig, dict)  # Plotly figure is a dict
    
    def test_plot_entanglement_heatmap(self):
        """Тест создания тепловой карты запутанности."""
        indicators = ['heart_rate', 'blood_pressure', 'temperature']
        entanglement_matrix = np.random.rand(3, 3)
        
        fig = self.visualizer.plot_entanglement_heatmap(
            entanglement_matrix, indicators
        )
        
        self.assertIsNotNone(fig)
        self.assertIsInstance(fig, dict)
    
    def test_plot_entanglement_network(self):
        """Тест создания графа сети запутанности."""
        network = {
            'indicator1': ['indicator2', 'indicator3'],
            'indicator2': ['indicator1'],
            'indicator3': ['indicator1']
        }
        
        fig = self.visualizer.plot_entanglement_network(network)
        
        self.assertIsNotNone(fig)
        self.assertIsInstance(fig, dict)


class TestIntegration(unittest.TestCase):
    """Интеграционные тесты."""
    
    def test_full_workflow(self):
        """Тест полного рабочего процесса MQEA."""
        # 1. Инициализация
        analyzer = MQEAAnalyzer()
        visualizer = MQEAVisualizer()
        
        # 2. Генерация данных
        time_series = analyzer.generate_synthetic_data(
            duration_hours=2,
            sampling_rate_minutes=15,
            add_missing_data=True
        )
        
        # 3. Квантовый анализ
        quantum_results = analyzer.quantum_entanglement_analysis(time_series)
        
        # 4. Заполнение пропусков
        filled_data = analyzer.fill_missing_data(time_series, method='quantum')
        
        # 5. Обнаружение паттернов
        patterns = analyzer.detect_patterns(filled_data)
        
        # 6. Визуализация
        time_series_fig = visualizer.plot_time_series(filled_data)
        
        # 7. Проверки
        self.assertIsNotNone(quantum_results)
        self.assertIsNotNone(filled_data)
        self.assertIsInstance(patterns, list)
        self.assertIsNotNone(time_series_fig)
        
        # 8. Сводка
        summary = analyzer.get_analysis_summary()
        self.assertIsNotNone(summary)


def run_tests():
    """Запуск всех тестов."""
    print("Запуск тестов MQEA...")
    
    # Создаем тестовый набор
    test_suite = unittest.TestSuite()
    
    # Добавляем тесты
    test_classes = [
        TestQuantumEntanglementEngine,
        TestMedicalDataProcessor,
        TestMQEAAnalyzer,
        TestMQEAVisualizer,
        TestIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Запускаем тесты
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Выводим результаты
    print(f"\nРезультаты тестирования:")
    print(f"  - Всего тестов: {result.testsRun}")
    print(f"  - Успешно: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"  - Ошибок: {len(result.failures) + len(result.errors)}")
    
    if result.failures:
        print(f"\nНеудачные тесты:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")
    
    if result.errors:
        print(f"\nОшибки:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)

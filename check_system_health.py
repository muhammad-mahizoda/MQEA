#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт проверки работоспособности системы MQEA.

Автор: Мухаммад Махизода
Таджикский национальный университет
"""

import sys
import os
import time
import socket
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime

# Добавляем путь к модулям
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class SystemHealthChecker:
    """Проверка работоспособности системы MQEA."""
    
    def __init__(self):
        self.results = {
            'passed': [],
            'failed': [],
            'warnings': []
        }
        self.start_time = time.time()
    
    def check(self, name: str, condition: bool, message: str = ""):
        """Добавить результат проверки."""
        if condition:
            self.results['passed'].append((name, message))
            print(f"✅ {name}: {message if message else 'OK'}")
        else:
            self.results['failed'].append((name, message))
            print(f"❌ {name}: {message if message else 'FAILED'}")
    
    def warn(self, name: str, message: str):
        """Добавить предупреждение."""
        self.results['warnings'].append((name, message))
        print(f"⚠️  {name}: {message}")
    
    def check_files(self) -> bool:
        """Проверка наличия важных файлов."""
        print("\n📁 ПРОВЕРКА ФАЙЛОВ")
        print("=" * 50)
        
        important_files = [
            ("mqea/__init__.py", "Основной модуль MQEA"),
            ("mqea/core.py", "Ядро системы"),
            ("mqea/quantum_entanglement.py", "Квантовый движок"),
            ("webapp/modern_medical_app.py", "Веб-приложение"),
            ("api/main.py", "API сервер"),
            ("config/settings.py", "Конфигурация"),
            ("requirements.txt", "Зависимости"),
            ("start_modern.py", "Скрипт запуска")
        ]
        
        all_ok = True
        for file_path, description in important_files:
            exists = Path(file_path).exists()
            self.check(f"{description} ({file_path})", exists)
            if not exists:
                all_ok = False
        
        return all_ok
    
    def check_imports(self) -> bool:
        """Проверка импортов основных модулей."""
        print("\n📦 ПРОВЕРКА ИМПОРТОВ")
        print("=" * 50)
        
        modules_to_check = [
            ("mqea", "MQEA модуль"),
            ("mqea.core", "MQEAAnalyzer"),
            ("mqea.quantum_entanglement", "QuantumEntanglementEngine"),
            ("mqea.data_processor", "MedicalDataProcessor"),
            ("streamlit", "Streamlit"),
            ("pandas", "Pandas"),
            ("numpy", "NumPy"),
            ("plotly", "Plotly")
        ]
        
        all_ok = True
        for module_name, description in modules_to_check:
            try:
                __import__(module_name)
                self.check(f"{description}", True)
            except ImportError as e:
                self.check(f"{description}", False, f"Ошибка импорта: {e}")
                all_ok = False
        
        return all_ok
    
    def check_ports(self) -> bool:
        """Проверка доступности портов."""
        print("\n🌐 ПРОВЕРКА ПОРТОВ")
        print("=" * 50)
        
        ports_to_check = [
            (8501, "Streamlit"),
            (8000, "FastAPI")
        ]
        
        all_ok = True
        for port, service in ports_to_check:
            is_open = self._check_port(port)
            if is_open:
                self.warn(f"Порт {port} ({service})", "Порт уже занят")
            else:
                self.check(f"Порт {port} ({service})", True, "Порт свободен")
        
        return True  # Порты могут быть заняты, это не ошибка
    
    def _check_port(self, port: int) -> bool:
        """Проверить, открыт ли порт."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('127.0.0.1', port))
            sock.close()
            return result == 0
        except:
            return False
    
    def check_dependencies(self) -> bool:
        """Проверка зависимостей."""
        print("\n📚 ПРОВЕРКА ЗАВИСИМОСТЕЙ")
        print("=" * 50)
        
        try:
            import pkg_resources
            requirements_file = Path("requirements.txt")
            
            if not requirements_file.exists():
                self.check("requirements.txt", False, "Файл не найден")
                return False
            
            with open(requirements_file, 'r', encoding='utf-8') as f:
                requirements = f.readlines()
            
            installed_packages = {pkg.key: pkg.version for pkg in pkg_resources.working_set}
            
            all_ok = True
            for req in requirements:
                req = req.strip()
                if not req or req.startswith('#'):
                    continue
                
                # Парсим requirement (простая версия)
                if '>=' in req:
                    package_name = req.split('>=')[0].strip()
                elif '==' in req:
                    package_name = req.split('==')[0].strip()
                else:
                    package_name = req.split()[0].strip()
                
                package_key = package_name.lower().replace('-', '_')
                
                if package_key in installed_packages:
                    self.check(f"{package_name}", True, f"v{installed_packages[package_key]}")
                else:
                    self.check(f"{package_name}", False, "Не установлен")
                    all_ok = False
            
            return all_ok
            
        except Exception as e:
            self.warn("Проверка зависимостей", f"Не удалось проверить: {e}")
            return True  # Не критично
    
    def check_mqea_functionality(self) -> bool:
        """Проверка функциональности MQEA."""
        print("\n⚛️  ПРОВЕРКА ФУНКЦИОНАЛЬНОСТИ MQEA")
        print("=" * 50)
        
        try:
            from mqea import MQEAAnalyzer
            
            # Инициализация
            analyzer = MQEAAnalyzer()
            self.check("Инициализация MQEAAnalyzer", analyzer is not None)
            
            # Генерация данных
            time_series = analyzer.generate_synthetic_data(
                duration_hours=1,
                sampling_rate_minutes=10
            )
            self.check("Генерация синтетических данных", time_series is not None)
            
            # Квантовый анализ
            results = analyzer.quantum_entanglement_analysis(time_series)
            self.check("Квантовый анализ", results is not None and 'quantum_entanglements' in results)
            
            # Заполнение пропусков
            filled_data = analyzer.fill_missing_data(time_series, method='quantum')
            self.check("Заполнение пропусков", filled_data is not None)
            
            return True
            
        except Exception as e:
            self.check("Функциональность MQEA", False, f"Ошибка: {e}")
            return False
    
    def check_database(self) -> bool:
        """Проверка базы данных."""
        print("\n💾 ПРОВЕРКА БАЗЫ ДАННЫХ")
        print("=" * 50)
        
        try:
            from config.settings import get_settings
            settings = get_settings()
            
            db_url = settings.database.url
            self.check("Конфигурация БД", db_url is not None, f"URL: {db_url}")
            
            # Попытка подключения (для SQLite просто проверяем файл)
            if db_url.startswith('sqlite'):
                db_path = db_url.replace('sqlite:///', '')
                if db_path.startswith('/'):
                    # Абсолютный путь
                    exists = Path(db_path).exists()
                else:
                    # Относительный путь
                    exists = Path(db_path).exists()
                
                if exists:
                    self.check("Файл БД", True, f"Существует: {db_path}")
                else:
                    self.warn("Файл БД", f"Не существует (будет создан): {db_path}")
            
            return True
            
        except Exception as e:
            self.warn("База данных", f"Не удалось проверить: {e}")
            return True  # Не критично для первого запуска
    
    def check_configuration(self) -> bool:
        """Проверка конфигурации."""
        print("\n⚙️  ПРОВЕРКА КОНФИГУРАЦИИ")
        print("=" * 50)
        
        try:
            from config.settings import get_settings
            settings = get_settings()
            
            self.check("Настройки приложения", settings is not None)
            self.check("Название приложения", settings.app_name == "MQEA")
            self.check("Версия", settings.api.version is not None)
            self.check("Окружение", settings.environment in ['development', 'testing', 'staging', 'production'])
            
            return True
            
        except Exception as e:
            self.check("Конфигурация", False, f"Ошибка: {e}")
            return False
    
    def check_tests(self) -> bool:
        """Проверка наличия тестов."""
        print("\n🧪 ПРОВЕРКА ТЕСТОВ")
        print("=" * 50)
        
        test_files = [
            ("tests/test_mqea.py", "Основные тесты"),
            ("test_complete_system.py", "Системный тест")
        ]
        
        all_ok = True
        for test_file, description in test_files:
            exists = Path(test_file).exists()
            self.check(f"{description} ({test_file})", exists)
            if not exists:
                all_ok = False
        
        return all_ok
    
    def run_all_checks(self) -> Dict:
        """Запустить все проверки."""
        print("🔍 ПРОВЕРКА РАБОТОСПОСОБНОСТИ СИСТЕМЫ MQEA")
        print("=" * 70)
        print(f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        checks = [
            ("Файлы", self.check_files),
            ("Импорты", self.check_imports),
            ("Зависимости", self.check_dependencies),
            ("Конфигурация", self.check_configuration),
            ("База данных", self.check_database),
            ("Порты", self.check_ports),
            ("Функциональность MQEA", self.check_mqea_functionality),
            ("Тесты", self.check_tests)
        ]
        
        results = {}
        for name, check_func in checks:
            try:
                results[name] = check_func()
            except Exception as e:
                self.warn(name, f"Ошибка при проверке: {e}")
                results[name] = False
        
        return results
    
    def print_summary(self):
        """Вывести итоговую сводку."""
        elapsed_time = time.time() - self.start_time
        
        print("\n" + "=" * 70)
        print("📊 ИТОГОВАЯ СВОДКА")
        print("=" * 70)
        
        total_checks = len(self.results['passed']) + len(self.results['failed'])
        passed = len(self.results['passed'])
        failed = len(self.results['failed'])
        warnings_count = len(self.results['warnings'])
        
        print(f"✅ Пройдено: {passed}")
        print(f"❌ Не пройдено: {failed}")
        print(f"⚠️  Предупреждений: {warnings_count}")
        print(f"⏱️  Время проверки: {elapsed_time:.2f} сек")
        
        if failed == 0:
            print("\n🎉 ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ УСПЕШНО!")
            print("✅ Система готова к работе")
        else:
            print(f"\n⚠️  ОБНАРУЖЕНЫ ПРОБЛЕМЫ: {failed} проверок не пройдено")
            print("❌ Рекомендуется исправить проблемы перед использованием")
        
        if warnings_count > 0:
            print(f"\n💡 Предупреждения (не критично): {warnings_count}")
        
        print("=" * 70)
        
        return failed == 0


def main():
    """Основная функция."""
    checker = SystemHealthChecker()
    
    try:
        # Запуск всех проверок
        results = checker.run_all_checks()
        
        # Вывод сводки
        success = checker.print_summary()
        
        # Возврат кода выхода
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Проверка прервана пользователем")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

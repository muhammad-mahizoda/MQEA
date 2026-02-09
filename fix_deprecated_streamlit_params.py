#!/usr/bin/env python3
"""
Исправление устаревших параметров Streamlit в проекте MQEA.

Автор: Мухаммад Махизода
Таджикский национальный университет
"""

import os
import re
from pathlib import Path

class StreamlitDeprecationFixer:
    """Класс для исправления устаревших параметров Streamlit."""
    
    def __init__(self):
        self.deprecated_params = {
            'use_column_width': 'use_container_width'
        }
        
        # Файлы для проверки
        self.files_to_check = [
            'webapp/modern_medical_app.py',
            'webapp/ai_chat_app.py',
            'webapp/enhanced_medical_app.py',
            'webapp/unified_main_app.py',
            'webapp/streamlit_app.py',
            'utils/logo_utils.py',
            'utils/optimized_logo_display.py'
        ]
    
    def fix_file(self, file_path: str) -> bool:
        """
        Исправляет устаревшие параметры в файле.
        
        Args:
            file_path: Путь к файлу
            
        Returns:
            bool: True если файл был изменен
        """
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                print(f"⚠️ Файл не найден: {file_path}")
                return False
            
            # Читаем содержимое файла
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            changes_made = False
            
            # Исправляем устаревшие параметры
            for deprecated, replacement in self.deprecated_params.items():
                pattern = rf'{deprecated}\s*=\s*(True|False)'
                matches = re.findall(pattern, content)
                
                if matches:
                    for match in matches:
                        old_param = f'{deprecated}={match}'
                        new_param = f'{replacement}={match}'
                        content = content.replace(old_param, new_param)
                        changes_made = True
                        print(f"  ✅ Исправлено: {old_param} → {new_param}")
            
            # Сохраняем изменения
            if changes_made:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"📝 Файл обновлен: {file_path}")
                return True
            else:
                print(f"✅ Файл уже актуален: {file_path}")
                return False
                
        except Exception as e:
            print(f"❌ Ошибка при обработке {file_path}: {e}")
            return False
    
    def check_all_files(self):
        """Проверяет и исправляет все файлы."""
        print("🔧 Исправление устаревших параметров Streamlit...")
        print("Автор: Мухаммад Махизода")
        print("Таджикский национальный университет")
        print("=" * 60)
        
        fixed_count = 0
        total_count = len(self.files_to_check)
        
        for file_path in self.files_to_check:
            print(f"\n📁 Проверка: {file_path}")
            
            if self.fix_file(file_path):
                fixed_count += 1
        
        print(f"\n🎉 Исправление завершено!")
        print(f"📊 Статистика:")
        print(f"   Проверено файлов: {total_count}")
        print(f"   Исправлено файлов: {fixed_count}")
        print(f"   Уже актуальных: {total_count - fixed_count}")
        
        return fixed_count > 0
    
    def search_deprecated_usage(self):
        """Ищет использование устаревших параметров в проекте."""
        print("\n🔍 Поиск устаревших параметров в проекте...")
        
        deprecated_found = False
        
        for file_path in self.files_to_check:
            try:
                file_path = Path(file_path)
                
                if not file_path.exists():
                    continue
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                for deprecated in self.deprecated_params.keys():
                    if deprecated in content:
                        print(f"⚠️ Найден устаревший параметр в {file_path}: {deprecated}")
                        deprecated_found = True
                        
            except Exception as e:
                print(f"❌ Ошибка при проверке {file_path}: {e}")
        
        if not deprecated_found:
            print("✅ Устаревшие параметры не найдены!")
        
        return deprecated_found

def main():
    """Основная функция."""
    fixer = StreamlitDeprecationFixer()
    
    # Проверяем наличие устаревших параметров
    has_deprecated = fixer.search_deprecated_usage()
    
    if has_deprecated:
        # Исправляем устаревшие параметры
        fixer.check_all_files()
        
        print("\n💡 Рекомендации:")
        print("• Перезапустите Streamlit приложения")
        print("• Проверьте работу логотипов")
        print("• Убедитесь, что предупреждения исчезли")
    else:
        print("\n🎉 Все параметры актуальны!")
        print("✅ Проект готов к использованию")

if __name__ == "__main__":
    main()

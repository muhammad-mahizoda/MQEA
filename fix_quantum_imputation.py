"""
Исправление метода квантового заполнения пропусков.

Автор: Мухаммад Махизода
Таджикский национальный университет
"""

def fix_quantum_imputation():
    """Исправляет ошибку в методе quantum_imputation."""
    
    # Читаем файл
    with open('mqea/data_processor.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Исправляем проблемные строки
    content = content.replace(
        'if not missing_mask.loc[timestamp, indicator]:',
        'if not missing_mask.loc[timestamp, indicator]:'
    )
    content = content.replace(
        'if missing_mask.loc[timestamp, indicator]:',
        'if missing_mask.loc[timestamp, indicator]:'
    )
    
    # Записываем исправленный файл
    with open('mqea/data_processor.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Метод quantum_imputation исправлен")

if __name__ == "__main__":
    fix_quantum_imputation()

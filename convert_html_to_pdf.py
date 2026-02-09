"""
Конвертер HTML в PDF с помощью браузера.
Создает высококачественный PDF из HTML отчета.

Автор: Мухаммад Махизода
Таджикский национальный университет
"""

import os
import sys
import subprocess
import time
from pathlib import Path


def check_dependencies():
    """Проверка наличия необходимых зависимостей."""
    
    dependencies = {
        'weasyprint': 'pip install weasyprint',
        'wkhtmltopdf': 'wkhtmltopdf (установить отдельно)',
        'playwright': 'pip install playwright'
    }
    
    available = {}
    
    # Проверка weasyprint
    try:
        import weasyprint
        available['weasyprint'] = True
        print("✅ WeasyPrint доступен")
    except ImportError:
        available['weasyprint'] = False
        print("❌ WeasyPrint не установлен")
    
    # Проверка playwright
    try:
        import playwright
        available['playwright'] = True
        print("✅ Playwright доступен")
    except ImportError:
        available['playwright'] = False
        print("❌ Playwright не установлен")
    
    return available


def convert_with_weasyprint(html_file, output_file):
    """Конвертация с помощью WeasyPrint."""
    
    try:
        from weasyprint import HTML, CSS
        
        print("🔄 Конвертация с помощью WeasyPrint...")
        
        # Создание PDF
        html_doc = HTML(filename=html_file)
        html_doc.write_pdf(output_file)
        
        print(f"✅ PDF создан с помощью WeasyPrint: {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка WeasyPrint: {e}")
        return False


def convert_with_playwright(html_file, output_file):
    """Конвертация с помощью Playwright."""
    
    try:
        from playwright.sync_api import sync_playwright
        
        print("🔄 Конвертация с помощью Playwright...")
        
        with sync_playwright() as p:
            # Запуск браузера
            browser = p.chromium.launch()
            page = browser.new_page()
            
            # Загрузка HTML файла
            html_path = os.path.abspath(html_file)
            page.goto(f"file://{html_path}")
            
            # Ожидание загрузки
            page.wait_for_load_state('networkidle')
            
            # Создание PDF
            page.pdf(
                path=output_file,
                format='A4',
                print_background=True,
                margin={
                    'top': '1cm',
                    'right': '1cm',
                    'bottom': '1cm',
                    'left': '1cm'
                }
            )
            
            browser.close()
        
        print(f"✅ PDF создан с помощью Playwright: {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка Playwright: {e}")
        return False


def convert_with_wkhtmltopdf(html_file, output_file):
    """Конвертация с помощью wkhtmltopdf."""
    
    try:
        print("🔄 Конвертация с помощью wkhtmltopdf...")
        
        # Команда для wkhtmltopdf
        cmd = [
            'wkhtmltopdf',
            '--page-size', 'A4',
            '--margin-top', '1cm',
            '--margin-right', '1cm',
            '--margin-bottom', '1cm',
            '--margin-left', '1cm',
            '--enable-local-file-access',
            '--print-media-type',
            html_file,
            output_file
        ]
        
        # Выполнение команды
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ PDF создан с помощью wkhtmltopdf: {output_file}")
            return True
        else:
            print(f"❌ Ошибка wkhtmltopdf: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("❌ wkhtmltopdf не найден в системе")
        return False
    except Exception as e:
        print(f"❌ Ошибка wkhtmltopdf: {e}")
        return False


def convert_html_to_pdf(html_file="MQEA_Technical_Report.html", output_file="MQEA_Technical_Report_Enhanced.pdf"):
    """Основная функция конвертации HTML в PDF."""
    
    print("🧬⚛️ Конвертер HTML в PDF для MQEA")
    print("=" * 50)
    
    # Проверка наличия HTML файла
    if not os.path.exists(html_file):
        print(f"❌ HTML файл не найден: {html_file}")
        return False
    
    print(f"📄 Исходный файл: {html_file}")
    print(f"📄 Выходной файл: {output_file}")
    
    # Проверка зависимостей
    available = check_dependencies()
    
    # Попытка конвертации с разными методами
    success = False
    
    # Метод 1: WeasyPrint (лучшее качество)
    if available.get('weasyprint', False):
        success = convert_with_weasyprint(html_file, output_file)
        if success:
            return True
    
    # Метод 2: Playwright (хорошее качество)
    if not success and available.get('playwright', False):
        success = convert_with_playwright(html_file, output_file)
        if success:
            return True
    
    # Метод 3: wkhtmltopdf (базовое качество)
    if not success:
        success = convert_with_wkhtmltopdf(html_file, output_file)
        if success:
            return True
    
    # Если ничего не сработало
    if not success:
        print("\n❌ Не удалось конвертировать HTML в PDF")
        print("💡 Рекомендации:")
        print("   1. Установите WeasyPrint: pip install weasyprint")
        print("   2. Или установите Playwright: pip install playwright && playwright install")
        print("   3. Или установите wkhtmltopdf отдельно")
        print(f"\n📄 HTML файл доступен для просмотра: {os.path.abspath(html_file)}")
        return False
    
    return True


def install_weasyprint():
    """Установка WeasyPrint."""
    
    print("📦 Установка WeasyPrint...")
    
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'weasyprint'])
        print("✅ WeasyPrint установлен успешно")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка установки WeasyPrint: {e}")
        return False


def main():
    """Основная функция."""
    
    # Проверка аргументов командной строки
    if len(sys.argv) > 1 and sys.argv[1] == '--install':
        return install_weasyprint()
    
    # Конвертация
    success = convert_html_to_pdf()
    
    if success:
        output_file = "MQEA_Technical_Report_Enhanced.pdf"
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"\n📄 Размер PDF файла: {file_size:,} байт")
            print(f"📁 Путь к файлу: {os.path.abspath(output_file)}")
            print("\n🎉 Конвертация завершена успешно!")
        else:
            print("\n❌ PDF файл не был создан")
            return 1
    else:
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())

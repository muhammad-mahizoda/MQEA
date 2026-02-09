"""
Создание PDF презентации из всех графиков MQEA
Порядок: титульная страница -> основные графики -> графики для инвесторов -> дополнительные
"""

from PIL import Image
import os

def create_pdf_presentation():
    """Создание PDF презентации из всех графиков"""
    
    # Определяем порядок графиков
    charts_order = [
        # Титульная страница
        'mqea_title_page.png',
        
        # Основные графики (7)
        'mqea_revenue_growth.png',
        'mqea_ebitda_monthly.png',
        'mqea_financial_model_part1.png',
        'mqea_financial_model_part2.png',
        'mqea_growth_singularity.png',
        'mqea_team_growth.png',
        'mqea_development_roadmap.png',
        
        # Графики для инвесторов (7)
        'mqea_investment_allocation.png',
        'mqea_roi_projection.png',
        'mqea_company_valuation.png',
        'mqea_why_invest.png',
        'mqea_investment_timeline.png',
        'mqea_competitive_advantage.png',
        'mqea_risk_reward.png',
        
        # Дополнительные графики (4)
        'mqea_technology_stack.png',
        'mqea_customer_acquisition.png',
        'mqea_detailed_investment.png',
        'mqea_trust_indicators.png',
        
        # Финальная страница
        'mqea_final_page.png',
    ]
    
    charts_dir = 'charts'
    output_pdf = 'MQEA_Investor_Presentation.pdf'
    
    # Проверяем наличие всех файлов
    images = []
    missing_files = []
    
    print("=" * 60)
    print("Создание PDF презентации MQEA для инвесторов")
    print("=" * 60)
    print()
    
    for chart_file in charts_order:
        file_path = os.path.join(charts_dir, chart_file)
        if os.path.exists(file_path):
            try:
                img = Image.open(file_path)
                # Конвертируем RGBA в RGB если нужно
                if img.mode == 'RGBA':
                    # Создаем белый фон для прозрачных изображений
                    rgb_img = Image.new('RGB', img.size, (10, 10, 10))  # Темный фон
                    rgb_img.paste(img, mask=img.split()[3])  # Используем альфа-канал как маску
                    img = rgb_img
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Конвертируем в RGB формат для PDF
                images.append(img)
                print(f"[OK] Добавлен: {chart_file}")
            except Exception as e:
                print(f"[ERROR] Ошибка при открытии {chart_file}: {e}")
                missing_files.append(chart_file)
        else:
            print(f"[WARNING] Файл не найден: {chart_file}")
            missing_files.append(chart_file)
    
    if missing_files:
        print(f"\n[WARNING] Не найдено файлов: {len(missing_files)}")
        for file in missing_files:
            print(f"  - {file}")
    
    if not images:
        print("\n[ERROR] Нет изображений для создания PDF!")
        return
    
    # Сохраняем все изображения в PDF
    try:
        if images:
            # Сохраняем первое изображение и добавляем остальные
            images[0].save(
                output_pdf,
                "PDF",
                resolution=300.0,
                save_all=True,
                append_images=images[1:] if len(images) > 1 else []
            )
            print()
            print("=" * 60)
            print(f"[SUCCESS] PDF презентация создана: {output_pdf}")
            print("=" * 60)
            print(f"\nВсего страниц: {len(images)}")
            print(f"\nПорядок страниц:")
            for i, chart_file in enumerate(charts_order, 1):
                if chart_file not in missing_files:
                    print(f"  {i}. {chart_file}")
        else:
            print("\n[ERROR] Нет изображений для сохранения!")
    except Exception as e:
        print(f"\n[ERROR] Ошибка при создании PDF: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    create_pdf_presentation()


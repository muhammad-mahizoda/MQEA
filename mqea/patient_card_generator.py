#!/usr/bin/env python3
"""
Генератор карточек пациентов для печати MQEA.

Автор: Мухаммад Махизода
Таджикский национальный университет
"""

from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
import io
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import os

class WatermarkCanvas:
    """Класс для добавления водяного знака в PDF."""
    
    def __init__(self, canvas, doc):
        self.canvas = canvas
        self.doc = doc
    
    def draw_watermark(self):
        """Рисует водяной знак на странице."""
        # Сохраняем текущее состояние
        self.canvas.saveState()
        
        # Устанавливаем прозрачность
        self.canvas.setFillAlpha(0.1)
        
        # Поворачиваем текст на 45 градусов
        self.canvas.rotate(45)
        
        # Устанавливаем шрифт и размер (используем стандартные шрифты reportlab)
        try:
            # Пробуем использовать Helvetica (стандартный шрифт reportlab)
            self.canvas.setFont("Helvetica-Bold", 48)
        except:
            # Если не работает, используем базовый Helvetica
            self.canvas.setFont("Helvetica", 48)
        
        # Рисуем водяной знак в центре страницы
        self.canvas.drawCentredString(0, 0, "MQEA")
        self.canvas.drawCentredString(0, -60, "MEDICAL")
        self.canvas.drawCentredString(0, -120, "SECURITY")
        
        # Добавляем дату и время
        try:
            self.canvas.setFont("Helvetica", 24)
        except:
            self.canvas.setFont("Helvetica-Bold", 24)
        current_time = datetime.now().strftime("%d.%m.%Y %H:%M")
        self.canvas.drawCentredString(0, -200, current_time)
        
        # Восстанавливаем состояние
        self.canvas.restoreState()

class PatientCardGenerator:
    """Генератор карточек пациентов."""
    
    def __init__(self):
        """Инициализация генератора."""
        self._register_fonts()
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _register_fonts(self):
        """Регистрация шрифтов с поддержкой кириллицы."""
        try:
            # Используем встроенные шрифты ReportLab с поддержкой кириллицы
            from reportlab.pdfbase.cidfonts import UnicodeCIDFont
            from reportlab.pdfbase import pdfmetrics
            
            # Регистрируем встроенные шрифты с поддержкой кириллицы
            pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
            pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light-Bold'))
            self.font_name = 'STSong-Light'
            self.bold_font_name = 'STSong-Light-Bold'
            print("✅ Используется встроенный шрифт STSong-Light с поддержкой кириллицы")
        except Exception as e:
            print(f"⚠️ Не удалось загрузить STSong-Light: {e}")
            try:
                # Альтернативный подход - используем системные шрифты
                import os
                if os.name == 'nt':  # Windows
                    # Пробуем разные пути к Arial
                    arial_paths = [
                        'C:/Windows/Fonts/arial.ttf',
                        'C:/Windows/Fonts/ARIAL.TTF',
                        'C:/Windows/Fonts/arial.ttc'
                    ]
                    arial_loaded = False
                    for path in arial_paths:
                        try:
                            if os.path.exists(path):
                                pdfmetrics.registerFont(TTFont('Arial', path))
                                pdfmetrics.registerFont(TTFont('Arial-Bold', path.replace('.ttf', 'bd.ttf').replace('.ttc', 'bd.ttf')))
                                self.font_name = 'Arial'
                                self.bold_font_name = 'Arial-Bold'
                                arial_loaded = True
                                print(f"✅ Загружен Arial из {path}")
                                break
                        except:
                            continue
                    
                    if not arial_loaded:
                        raise Exception("Arial не найден")
                else:  # Linux/Mac
                    pdfmetrics.registerFont(TTFont('DejaVuSans', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
                    pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
                    self.font_name = 'DejaVuSans'
                    self.bold_font_name = 'DejaVuSans-Bold'
            except Exception as e2:
                print(f"⚠️ Не удалось загрузить системные шрифты: {e2}")
                # Если ничего не работает, используем встроенный шрифт
                self.font_name = 'Helvetica'
                self.bold_font_name = 'Helvetica-Bold'
                print("⚠️ Предупреждение: Кириллические символы могут отображаться некорректно")
    
    def _setup_custom_styles(self):
        """Настройка пользовательских стилей."""
        # Заголовок карточки
        self.styles.add(ParagraphStyle(
            name='CardTitle',
            parent=self.styles['Heading1'],
            fontName=self.font_name,
            fontSize=18,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        ))
        
        # Заголовок секции
        self.styles.add(ParagraphStyle(
            name='SectionTitle',
            parent=self.styles['Heading2'],
            fontName=self.font_name,
            fontSize=14,
            spaceAfter=10,
            spaceBefore=15,
            textColor=colors.darkgreen
        ))
        
        # Информация о пациенте
        self.styles.add(ParagraphStyle(
            name='PatientInfo',
            parent=self.styles['Normal'],
            fontName=self.font_name,
            fontSize=11,
            spaceAfter=5,
            leftIndent=20
        ))
        
        # Медицинские данные
        self.styles.add(ParagraphStyle(
            name='MedicalData',
            parent=self.styles['Normal'],
            fontName=self.font_name,
            fontSize=10,
            spaceAfter=3,
            leftIndent=15
        ))
        
        # Компактный стиль для таблиц
        self.styles.add(ParagraphStyle(
            name='TableData',
            parent=self.styles['Normal'],
            fontName=self.font_name,
            fontSize=8,
            spaceAfter=2,
            spaceBefore=2,
            leading=10  # Межстрочный интервал
        ))
    
    def generate_patient_card(self, patient_data: Dict, output_path: str = "patient_card.pdf"):
        """Генерация карточки пациента с водяным знаком."""
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        story = []
        
        # Заголовок
        story.append(Paragraph("МЕДИЦИНСКАЯ КАРТОЧКА ПАЦИЕНТА", self.styles['CardTitle']))
        story.append(Paragraph("MQEA - Medical Quantum Entanglement Analysis", self.styles['MedicalData']))
        story.append(Spacer(1, 20))
        
        # Информация о пациенте
        story.extend(self._create_patient_info_section(patient_data))
        story.append(Spacer(1, 15))
        
        # Медицинские показатели
        story.extend(self._create_vital_signs_section(patient_data))
        story.append(Spacer(1, 15))
        
        # Результаты MQEA анализа
        story.extend(self._create_mqea_analysis_section(patient_data))
        story.append(Spacer(1, 15))
        
        # Диагнозы и рекомендации
        story.extend(self._create_diagnosis_section(patient_data))
        story.append(Spacer(1, 15))
        
        # Графики (если есть данные)
        if 'mqea_data' in patient_data:
            story.extend(self._create_charts_section(patient_data))
            story.append(Spacer(1, 15))
        
        # Подпись врача
        story.extend(self._create_signature_section())
        
        # Создаем PDF с водяным знаком
        def add_watermark(canvas, doc):
            watermark = WatermarkCanvas(canvas, doc)
            watermark.draw_watermark()
        
        doc.build(story, onFirstPage=add_watermark, onLaterPages=add_watermark)
        return output_path
    
    def _create_patient_info_section(self, patient_data: Dict) -> List:
        """Создание секции информации о пациенте."""
        elements = []
        
        elements.append(Paragraph("ИНФОРМАЦИЯ О ПАЦИЕНТЕ", self.styles['SectionTitle']))
        
        # Основная информация
        info_data = [
            ['ID пациента:', patient_data.get('patient_id', 'N/A')],
            ['ФИО:', patient_data.get('name', 'N/A')],
            ['Возраст:', f"{patient_data.get('age', 'N/A')} лет"],
            ['Пол:', patient_data.get('gender', 'N/A')],
            ['Дата рождения:', patient_data.get('birth_date', 'N/A')],
            ['Контактный телефон:', patient_data.get('phone', 'N/A')],
            ['Адрес:', patient_data.get('address', 'N/A')]
        ]
        
        info_table = Table(info_data, colWidths=[4*cm, 7*cm])
        info_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), self.bold_font_name),
            ('FONTNAME', (1, 0), (1, -1), self.font_name),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        elements.append(info_table)
        return elements
    
    def _create_vital_signs_section(self, patient_data: Dict) -> List:
        """Создание секции жизненных показателей."""
        elements = []
        
        elements.append(Paragraph("ЖИЗНЕННЫЕ ПОКАЗАТЕЛИ", self.styles['SectionTitle']))
        
        # Текущие показатели
        vital_signs = patient_data.get('vital_signs', {})
        current_date = datetime.now().strftime("%d.%m.%Y %H:%M")
        
        signs_data = [
            ['Показатель', 'Значение', 'Норма', 'Статус'],
            ['Частота пульса', f"{vital_signs.get('heart_rate', 'N/A')} уд/мин", '60-100', self._get_status('heart_rate', vital_signs)],
            ['АД систолическое', f"{vital_signs.get('blood_pressure_systolic', 'N/A')} мм рт.ст.", '<140', self._get_status('blood_pressure_systolic', vital_signs)],
            ['АД диастолическое', f"{vital_signs.get('blood_pressure_diastolic', 'N/A')} мм рт.ст.", '<90', self._get_status('blood_pressure_diastolic', vital_signs)],
            ['Температура тела', f"{vital_signs.get('temperature', 'N/A')} °C", '36.0-37.0', self._get_status('temperature', vital_signs)],
            ['Насыщение O₂', f"{vital_signs.get('oxygen_saturation', 'N/A')}%", '95-100', self._get_status('oxygen_saturation', vital_signs)],
            ['Частота дыхания', f"{vital_signs.get('respiratory_rate', 'N/A')} в мин", '12-20', self._get_status('respiratory_rate', vital_signs)],
            ['Глюкоза', f"{vital_signs.get('glucose', 'N/A')} ммоль/л", '3.9-5.9', self._get_status('glucose', vital_signs)],
            ['Холестерин', f"{vital_signs.get('cholesterol', 'N/A')} мг/дл", '<200', self._get_status('cholesterol', vital_signs)]
        ]
        
        signs_table = Table(signs_data, colWidths=[4.5*cm, 2.5*cm, 2*cm, 2*cm])
        signs_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), self.bold_font_name),
            ('FONTNAME', (0, 1), (-1, -1), self.font_name),  # Добавляем шрифт для всех строк данных
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        elements.append(signs_table)
        elements.append(Paragraph(f"<i>Дата измерения: {current_date}</i>", self.styles['MedicalData']))
        
        return elements
    
    def _get_status(self, indicator: str, vital_signs: Dict) -> str:
        """Получение статуса показателя."""
        value = vital_signs.get(indicator)
        if value is None:
            return "N/A"
        
        try:
            val = float(value)
            if indicator == 'heart_rate':
                return "Норма" if 60 <= val <= 100 else "Отклонение"
            elif indicator == 'blood_pressure_systolic':
                return "Норма" if val < 140 else "Отклонение"
            elif indicator == 'blood_pressure_diastolic':
                return "Норма" if val < 90 else "Отклонение"
            elif indicator == 'temperature':
                return "Норма" if 36.0 <= val <= 37.0 else "Отклонение"
            elif indicator == 'oxygen_saturation':
                return "Норма" if val >= 95 else "Отклонение"
            elif indicator == 'respiratory_rate':
                return "Норма" if 12 <= val <= 20 else "Отклонение"
            elif indicator == 'glucose':
                return "Норма" if 3.9 <= val <= 5.9 else "Отклонение"
            elif indicator == 'cholesterol':
                return "Норма" if val < 200 else "Отклонение"
        except (ValueError, TypeError):
            pass
        
        return "N/A"
    
    def _create_mqea_analysis_section(self, patient_data: Dict) -> List:
        """Создание секции MQEA анализа."""
        elements = []
        
        elements.append(Paragraph("РЕЗУЛЬТАТЫ MQEA АНАЛИЗА", self.styles['SectionTitle']))
        
        mqea_data = patient_data.get('mqea_analysis', {})
        
        # Извлекаем данные из разных источников (для совместимости)
        quantum_signatures = mqea_data.get('quantum_signatures', {})
        entanglement_stats = mqea_data.get('entanglement_statistics', {})
        
        # Функция перевода названий показателей на русский
        def translate_indicator(indicator_name: str) -> str:
            """Переводит название показателя на русский язык."""
            translations = {
                'heart_rate': 'ЧСС',
                'blood_pressure_systolic': 'АД сист.',
                'blood_pressure_diastolic': 'АД диаст.',
                'temperature': 'Температура',
                'oxygen_saturation': 'SpO2',
                'respiratory_rate': 'ЧДД',
                'glucose': 'Глюкоза',
                'cholesterol': 'Холестерин',
                # Дополнительные показатели
                'bmi': 'ИМТ',
                'age': 'Возраст',
                'weight': 'Вес',
                'height': 'Рост',
                'blood_pressure': 'Артериальное давление',
                'systolic_pressure': 'Систолическое давление',
                'diastolic_pressure': 'Диастолическое давление'
            }
            # Если название уже на русском или не найдено, возвращаем как есть
            return translations.get(indicator_name.lower(), indicator_name.replace('_', ' ').title())
        
        # Функция перевода типа паттерна на русский
        def translate_pattern_type(pattern_type: str) -> str:
            """Переводит тип паттерна на русский язык."""
            translations = {
                'quantum_entangled': 'Квантовая запутанность',
                'quantum_coherence': 'Квантовая когерентность',
                'temporal_pattern': 'Временной паттерн',
                'correlation_pattern': 'Корреляционный паттерн',
                'anomaly_pattern': 'Аномальный паттерн',
                'trend_pattern': 'Трендовый паттерн',
                'cyclic_pattern': 'Циклический паттерн',
                'seasonal_pattern': 'Сезонный паттерн',
                'unknown': 'Неизвестный',
                'неизвестный': 'Неизвестный'
            }
            # Если тип уже на русском или не найден, возвращаем с заглавной буквы
            return translations.get(pattern_type.lower(), pattern_type.replace('_', ' ').title())
        
        # Вспомогательная функция для безопасного преобразования в число
        def safe_float(value, default=0.0):
            """Безопасное преобразование значения в float."""
            if value is None:
                return default
            # Обрабатываем numpy типы
            if hasattr(value, 'item'):
                try:
                    return float(value.item())
                except (ValueError, TypeError, AttributeError):
                    pass
            # Обрабатываем numpy скаляры напрямую
            try:
                if isinstance(value, (np.integer, np.floating, np.complexfloating)):
                    if isinstance(value, np.complexfloating):
                        return float(abs(value))  # Используем модуль для комплексных чисел
                    return float(value)
            except (TypeError, AttributeError):
                pass
            if isinstance(value, (int, float)):
                return float(value)
            if isinstance(value, dict):
                # Обрабатываем сериализованные комплексные числа
                # Приоритет: magnitude > real > imag
                if 'magnitude' in value:
                    return float(value['magnitude'])
                elif 'real' in value:
                    return float(value['real'])
                elif 'imag' in value:
                    return float(value['imag'])
                else:
                    # Пробуем преобразовать все значения словаря
                    for key in ['value', 'strength', 'confidence']:
                        if key in value:
                            return safe_float(value[key], default)
                    return default
            if isinstance(value, str):
                try:
                    return float(value)
                except (ValueError, TypeError):
                    return default
            # Обрабатываем комплексные числа напрямую
            if hasattr(value, 'real') and hasattr(value, 'imag'):
                return float(abs(value))  # Используем модуль комплексного числа
            return default
        
        def safe_int(value, default=0):
            """Безопасное преобразование значения в int."""
            if value is None:
                return default
            if isinstance(value, (int, float)):
                return int(value)
            if isinstance(value, str):
                try:
                    return int(float(value))
                except (ValueError, TypeError):
                    return default
            return default
        
        # Основные параметры с безопасным преобразованием
        coherence = safe_float(quantum_signatures.get('quantum_coherence') or mqea_data.get('quantum_coherence'), 0)
        
        entangled_pairs_val = (quantum_signatures.get('entangled_pairs_count') or 
                               entanglement_stats.get('entangled_pairs') or 
                               mqea_data.get('entanglement_pairs'))
        entangled_pairs = safe_int(entangled_pairs_val, 0)
        
        max_entanglement_val = (entanglement_stats.get('max_entanglement') or 
                               quantum_signatures.get('average_entanglement') or 
                               mqea_data.get('max_entanglement'))
        max_entanglement = safe_float(max_entanglement_val, 0)
        
        avg_entanglement_val = (quantum_signatures.get('average_entanglement') or 
                                entanglement_stats.get('average_entanglement'))
        avg_entanglement = safe_float(avg_entanglement_val, 0)
        
        entanglement_entropy = safe_float(quantum_signatures.get('entanglement_entropy'), 0)
        total_states = safe_int(quantum_signatures.get('total_quantum_states'), 0)
        
        # Паттерны
        patterns = mqea_data.get('patterns', [])
        if not isinstance(patterns, list):
            patterns = []
        quantum_patterns = mqea_data.get('quantum_patterns', [])
        if not isinstance(quantum_patterns, list):
            quantum_patterns = []
        total_patterns = len(patterns) + len(quantum_patterns)
        
        # Временной анализ
        temporal_analysis = mqea_data.get('temporal_analysis', {})
        if not isinstance(temporal_analysis, dict):
            temporal_analysis = {}
        duration_hours = safe_float(temporal_analysis.get('total_duration_hours'), 0)
        data_completeness = safe_float(temporal_analysis.get('data_completeness'), 0)
        
        # Основная таблица результатов
        # Используем Paragraph для лучшего переноса текста с компактным стилем
        analysis_data = [
            [
                Paragraph("<b>Параметр</b>", self.styles['TableData']),
                Paragraph("<b>Значение</b>", self.styles['TableData']),
                Paragraph("<b>Интерпретация</b>", self.styles['TableData'])
            ],
            [
                Paragraph("Квантовая когерентность", self.styles['TableData']),
                Paragraph(f"{coherence:.3f}", self.styles['TableData']),
                Paragraph(self._interpret_coherence(coherence), self.styles['TableData'])
            ],
            [
                Paragraph("Запутанных пар", self.styles['TableData']),
                Paragraph(f"{entangled_pairs}", self.styles['TableData']),
                Paragraph(self._interpret_entanglement(entangled_pairs), self.styles['TableData'])
            ],
            [
                Paragraph("Максимальная запутанность", self.styles['TableData']),
                Paragraph(f"{max_entanglement:.3f}", self.styles['TableData']),
                Paragraph(self._interpret_max_entanglement(max_entanglement), self.styles['TableData'])
            ],
            [
                Paragraph("Средняя запутанность", self.styles['TableData']),
                Paragraph(f"{avg_entanglement:.3f}", self.styles['TableData']),
                Paragraph(self._interpret_avg_entanglement(avg_entanglement), self.styles['TableData'])
            ],
            [
                Paragraph("Энтропия запутанности", self.styles['TableData']),
                Paragraph(f"{entanglement_entropy:.3f}", self.styles['TableData']),
                Paragraph(self._interpret_entropy(entanglement_entropy), self.styles['TableData'])
            ],
            [
                Paragraph("Всего квантовых состояний", self.styles['TableData']),
                Paragraph(f"{total_states}", self.styles['TableData']),
                Paragraph(self._interpret_states(total_states), self.styles['TableData'])
            ],
            [
                Paragraph("Обнаруженные паттерны", self.styles['TableData']),
                Paragraph(f"{total_patterns}", self.styles['TableData']),
                Paragraph(self._interpret_patterns(total_patterns), self.styles['TableData'])
            ],
            [
                Paragraph("Продолжительность анализа", self.styles['TableData']),
                Paragraph(f"{duration_hours:.1f} ч", self.styles['TableData']),
                Paragraph(self._interpret_duration(duration_hours), self.styles['TableData'])
            ],
            [
                Paragraph("Полнота данных", self.styles['TableData']),
                Paragraph(f"{data_completeness*100:.1f}%", self.styles['TableData']),
                Paragraph(self._interpret_completeness(data_completeness), self.styles['TableData'])
            ]
        ]
        
        # Увеличиваем ширину колонок для лучшего отображения
        # A4 ширина ~21см, оставляем отступы по 1см с каждой стороны = 19см для таблицы
        analysis_table = Table(analysis_data, colWidths=[6.5*cm, 3.5*cm, 5*cm])
        analysis_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 1), (1, -1), 'CENTER'),  # Значения по центру
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 3),
            ('RIGHTPADDING', (0, 0), (-1, -1), 3),
            # Paragraph сам обрабатывает перенос текста, поэтому WORDWRAP не нужен
        ]))
        
        elements.append(analysis_table)
        elements.append(Spacer(1, 10))
        
        # Детальная информация о паттернах
        if total_patterns > 0:
            elements.append(Paragraph("<b>Детальная информация о паттернах:</b>", self.styles['MedicalData']))
            
            # Показываем первые 5 паттернов
            all_patterns = patterns + quantum_patterns
            for i, pattern in enumerate(all_patterns[:5], 1):
                if not isinstance(pattern, dict):
                    continue
                    
                pattern_type_raw = str(pattern.get('type', 'Неизвестный'))
                # Переводим тип паттерна на русский
                pattern_type = translate_pattern_type(pattern_type_raw)
                confidence = safe_float(pattern.get('confidence'), 0)
                
                # Всегда пытаемся извлечь confidence из quantum_signature, если он доступен
                quantum_sig = pattern.get('quantum_signature', {})
                if isinstance(quantum_sig, dict):
                    total_strength = quantum_sig.get('total_entanglement_strength')
                    if total_strength is not None:
                        extracted_confidence = safe_float(total_strength, 0)
                        # Используем значение из quantum_signature, если оно больше или если confidence = 0
                        if extracted_confidence > 0:
                            confidence = extracted_confidence
                
                # Форматируем описание паттерна
                description = pattern.get('description')
                if not description and isinstance(quantum_sig, dict):
                    # Форматируем quantum_signature в читаемый вид
                    desc_parts = []
                    if 'entangled_pairs' in quantum_sig:
                        desc_parts.append(f"запутанных пар: {quantum_sig['entangled_pairs']}")
                    if 'average_phase' in quantum_sig:
                        phase_val = quantum_sig['average_phase']
                        # Обрабатываем numpy типы и обычные числа
                        if hasattr(phase_val, 'item'):
                            phase_val = phase_val.item()
                        elif isinstance(phase_val, dict):
                            phase_val = safe_float(phase_val, 0)
                        desc_parts.append(f"средняя фаза: {float(phase_val):.3f}")
                    if desc_parts:
                        description = ", ".join(desc_parts)
                
                if not description:
                    description = 'Нет описания'
                
                pattern_text = f"{i}. <b>{pattern_type}</b> (уверенность: {confidence:.1%})"
                if description and description != 'Нет описания':
                    # Экранируем специальные символы для HTML
                    description = description.replace('<', '&lt;').replace('>', '&gt;')
                    pattern_text += f" - {description}"
                
                elements.append(Paragraph(pattern_text, self.styles['MedicalData']))
            
            if total_patterns > 5:
                elements.append(Paragraph(f"... и еще {total_patterns - 5} паттернов", self.styles['MedicalData']))
            
            elements.append(Spacer(1, 10))
        
        # Информация о значимых запутанных парах
        if entangled_pairs > 0:
            elements.append(Paragraph("<b>Наиболее значимые взаимосвязи:</b>", self.styles['MedicalData']))
            
            # Получаем информацию о запутанных парах из quantum_entanglements
            quantum_entanglements = mqea_data.get('quantum_entanglements', [])
            if not isinstance(quantum_entanglements, list):
                quantum_entanglements = []
                
            significant_pairs = []
            
            for window_result in quantum_entanglements:
                if not isinstance(window_result, dict):
                    continue
                if 'significant_pairs' in window_result:
                    pairs_list = window_result['significant_pairs']
                    if isinstance(pairs_list, list):
                        significant_pairs.extend(pairs_list)
            
            # Сортируем по силе запутанности
            significant_pairs.sort(key=lambda x: safe_float(x.get('strength') if isinstance(x, dict) else 0, 0), reverse=True)
            
            # Показываем топ-5 пар
            for i, pair in enumerate(significant_pairs[:5], 1):
                if not isinstance(pair, dict):
                    continue
                    
                indicators = pair.get('indicators', [])
                if not isinstance(indicators, list):
                    indicators = []
                    
                # Извлекаем strength с улучшенной обработкой
                strength = safe_float(pair.get('strength'), 0)
                
                # Если strength = 0, пытаемся найти альтернативные источники
                if strength == 0:
                    # Проверяем другие возможные ключи
                    for alt_key in ['entanglement_strength', 'avg_entanglement', 'value']:
                        alt_value = pair.get(alt_key)
                        if alt_value is not None:
                            alt_strength = safe_float(alt_value, 0)
                            if alt_strength > 0:
                                strength = alt_strength
                                break
                
                significance = str(pair.get('significance', 'medium'))
                # Переводим значимость на русский
                significance_ru = {
                    'high': 'высокая',
                    'medium': 'средняя',
                    'low': 'низкая',
                    'very_high': 'очень высокая',
                    'very_low': 'очень низкая'
                }.get(significance.lower(), significance)
                
                if len(indicators) >= 2:
                    # Переводим названия показателей на русский
                    indicator1 = translate_indicator(str(indicators[0]))
                    indicator2 = translate_indicator(str(indicators[1]))
                    pair_text = f"{i}. <b>{indicator1}</b> ↔ <b>{indicator2}</b> "
                    pair_text += f"(сила: {strength:.3f}, значимость: {significance_ru})"
                    elements.append(Paragraph(pair_text, self.styles['MedicalData']))
            
            if len(significant_pairs) > 5:
                elements.append(Paragraph(f"... и еще {len(significant_pairs) - 5} взаимосвязей", self.styles['MedicalData']))
            
            elements.append(Spacer(1, 10))
        
        # Заключение MQEA
        conclusion = self._generate_mqea_conclusion(mqea_data, coherence, entangled_pairs, max_entanglement, total_patterns)
        elements.append(Paragraph(f"<b>Заключение MQEA:</b>", self.styles['MedicalData']))
        elements.append(Paragraph(conclusion, self.styles['MedicalData']))
        elements.append(Spacer(1, 10))
        
        # Рекомендации на основе анализа
        recommendations = self._generate_mqea_recommendations(coherence, entangled_pairs, max_entanglement, total_patterns)
        if recommendations:
            elements.append(Paragraph("<b>Рекомендации на основе MQEA анализа:</b>", self.styles['MedicalData']))
            for i, rec in enumerate(recommendations, 1):
                elements.append(Paragraph(f"{i}. {rec}", self.styles['MedicalData']))
        
        return elements
    
    def _interpret_coherence(self, coherence: float) -> str:
        """Интерпретация квантовой когерентности."""
        try:
            coherence = float(coherence) if coherence is not None else 0.0
            if coherence > 0.7:
                return "Высокая стабильность"
            elif coherence > 0.4:
                return "Умеренная стабильность"
            else:
                return "Низкая стабильность"
        except (ValueError, TypeError):
            return "Не определено"
    
    def _interpret_entanglement(self, pairs: int) -> str:
        """Интерпретация количества запутанных пар."""
        try:
            pairs = int(pairs) if pairs is not None else 0
            if pairs > 20:
                return "Сильная взаимосвязь"
            elif pairs > 10:
                return "Умеренная взаимосвязь"
            else:
                return "Слабая взаимосвязь"
        except (ValueError, TypeError):
            return "Не определено"
    
    def _interpret_max_entanglement(self, max_ent: float) -> str:
        """Интерпретация максимальной запутанности."""
        try:
            max_ent = float(max_ent) if max_ent is not None else 0.0
            if max_ent > 0.7:
                return "Очень сильная"
            elif max_ent > 0.4:
                return "Сильная"
            else:
                return "Слабая"
        except (ValueError, TypeError):
            return "Не определено"
    
    def _interpret_patterns(self, count: int) -> str:
        """Интерпретация количества паттернов."""
        try:
            count = int(count) if count is not None else 0
            if count > 5:
                return "Много паттернов"
            elif count > 2:
                return "Несколько паттернов"
            else:
                return "Мало паттернов"
        except (ValueError, TypeError):
            return "Не определено"
    
    def _interpret_correlation(self, corr: float) -> str:
        """Интерпретация временной корреляции."""
        if corr > 0.7:
            return "Высокая"
        elif corr > 0.4:
            return "Умеренная"
        else:
            return "Низкая"
    
    def _generate_mqea_conclusion(self, mqea_data: Dict, coherence: float, pairs: int, 
                                  max_ent: float, patterns: int) -> str:
        """Генерация заключения MQEA."""
        conclusion_parts = []
        
        # Безопасное преобразование значений
        coherence = float(coherence) if coherence is not None else 0.0
        pairs = int(pairs) if pairs is not None else 0
        max_ent = float(max_ent) if max_ent is not None else 0.0
        patterns = int(patterns) if patterns is not None else 0
        
        # Оценка квантовой когерентности
        if coherence > 0.7:
            conclusion_parts.append("Высокая квантовая когерентность указывает на стабильное состояние системы.")
        elif coherence > 0.4:
            conclusion_parts.append("Умеренная квантовая когерентность свидетельствует о нормальном функционировании.")
        else:
            conclusion_parts.append("Низкая квантовая когерентность может указывать на нестабильность системы.")
        
        # Оценка запутанности
        if pairs > 20:
            conclusion_parts.append(f"Обнаружено {pairs} значимых взаимосвязей между показателями, что указывает на сильную корреляцию.")
        elif pairs > 10:
            conclusion_parts.append(f"Обнаружено {pairs} взаимосвязей между показателями, что соответствует умеренной корреляции.")
        elif pairs > 0:
            conclusion_parts.append(f"Обнаружено {pairs} взаимосвязей, что указывает на слабую корреляцию между показателями.")
        else:
            conclusion_parts.append("Не обнаружено значимых взаимосвязей между показателями.")
        
        # Оценка максимальной запутанности
        if max_ent > 0.7:
            conclusion_parts.append("Максимальная запутанность очень высокая, что указывает на сильные взаимосвязи.")
        elif max_ent > 0.4:
            conclusion_parts.append("Максимальная запутанность умеренная.")
        else:
            conclusion_parts.append("Максимальная запутанность низкая.")
        
        # Оценка паттернов
        if patterns > 5:
            conclusion_parts.append(f"Обнаружено {patterns} паттернов в данных, что указывает на сложную структуру.")
        elif patterns > 0:
            conclusion_parts.append(f"Обнаружено {patterns} паттернов в данных.")
        else:
            conclusion_parts.append("Паттерны в данных не обнаружены.")
        
        return " ".join(conclusion_parts)
    
    def _generate_mqea_recommendations(self, coherence: float, pairs: int, 
                                      max_ent: float, patterns: int) -> List[str]:
        """Генерация рекомендаций на основе MQEA анализа."""
        recommendations = []
        
        # Безопасное преобразование значений
        try:
            coherence = float(coherence) if coherence is not None else 0.0
            pairs = int(pairs) if pairs is not None else 0
            max_ent = float(max_ent) if max_ent is not None else 0.0
            patterns = int(patterns) if patterns is not None else 0
        except (ValueError, TypeError):
            recommendations.append("Рекомендуется провести повторный анализ для получения корректных данных.")
            return recommendations
        
        if coherence < 0.4 or pairs < 10:
            recommendations.append("Провести дополнительные лабораторные исследования для уточнения состояния.")
            recommendations.append("Усилить мониторинг жизненных показателей.")
            recommendations.append("Рассмотреть возможность консультации с профильным специалистом.")
        elif coherence < 0.6 or pairs < 20:
            recommendations.append("Увеличить частоту наблюдений за состоянием пациента.")
            recommendations.append("Провести дополнительные диагностические тесты.")
        else:
            recommendations.append("Продолжить текущий режим мониторинга.")
            recommendations.append("Следующий анализ рекомендуется через 24-48 часов.")
        
        if max_ent < 0.3:
            recommendations.append("Обратить внимание на слабые взаимосвязи между показателями - возможны скрытые проблемы.")
        
        if patterns == 0:
            recommendations.append("Рекомендуется провести более детальный анализ для выявления паттернов.")
        
        return recommendations
    
    def _interpret_avg_entanglement(self, avg_ent: float) -> str:
        """Интерпретация средней запутанности."""
        try:
            avg_ent = float(avg_ent) if avg_ent is not None else 0.0
            if avg_ent > 0.6:
                return "Высокая"
            elif avg_ent > 0.3:
                return "Умеренная"
            else:
                return "Низкая"
        except (ValueError, TypeError):
            return "Не определено"
    
    def _interpret_entropy(self, entropy: float) -> str:
        """Интерпретация энтропии запутанности."""
        try:
            entropy = float(entropy) if entropy is not None else 0.0
            if entropy > 0.7:
                return "Высокая неопределенность"
            elif entropy > 0.4:
                return "Умеренная неопределенность"
            else:
                return "Низкая неопределенность"
        except (ValueError, TypeError):
            return "Не определено"
    
    def _interpret_states(self, states: int) -> str:
        """Интерпретация количества квантовых состояний."""
        try:
            states = int(states) if states is not None else 0
            if states > 100:
                return "Много состояний"
            elif states > 50:
                return "Умеренное количество"
            else:
                return "Мало состояний"
        except (ValueError, TypeError):
            return "Не определено"
    
    def _interpret_duration(self, duration: float) -> str:
        """Интерпретация продолжительности анализа."""
        try:
            duration = float(duration) if duration is not None else 0.0
            if duration > 48:
                return "Длительный анализ"
            elif duration > 24:
                return "Средний анализ"
            else:
                return "Краткий анализ"
        except (ValueError, TypeError):
            return "Не определено"
    
    def _interpret_completeness(self, completeness: float) -> str:
        """Интерпретация полноты данных."""
        try:
            completeness = float(completeness) if completeness is not None else 0.0
            if completeness > 0.9:
                return "Полные данные"
            elif completeness > 0.7:
                return "Достаточные данные"
            else:
                return "Неполные данные"
        except (ValueError, TypeError):
            return "Не определено"
    
    def _create_diagnosis_section(self, patient_data: Dict) -> List:
        """Создание секции диагнозов и рекомендаций."""
        elements = []
        
        elements.append(Paragraph("ДИАГНОЗЫ И РЕКОМЕНДАЦИИ", self.styles['SectionTitle']))
        
        diagnoses = patient_data.get('diagnoses', [])
        recommendations = patient_data.get('recommendations', [])
        
        if diagnoses:
            elements.append(Paragraph("<b>Диагнозы:</b>", self.styles['MedicalData']))
            for i, diagnosis in enumerate(diagnoses, 1):
                elements.append(Paragraph(f"{i}. {diagnosis.get('condition', 'N/A')} - {diagnosis.get('severity', 'N/A')} (уверенность: {diagnosis.get('confidence', 0):.1%})", self.styles['MedicalData']))
        
        if recommendations:
            elements.append(Paragraph("<b>Рекомендации:</b>", self.styles['MedicalData']))
            for i, rec in enumerate(recommendations, 1):
                elements.append(Paragraph(f"{i}. {rec.get('title', 'N/A')}: {rec.get('description', 'N/A')}", self.styles['MedicalData']))
        
        return elements
    
    def _create_charts_section(self, patient_data: Dict) -> List:
        """Создание секции с графиками."""
        elements = []
        
        elements.append(Paragraph("📈 ГРАФИКИ АНАЛИЗА", self.styles['SectionTitle']))
        
        # Здесь можно добавить генерацию графиков
        # Пока что добавляем заглушку
        elements.append(Paragraph("Графики временных рядов и квантовых показателей", self.styles['MedicalData']))
        
        return elements
    
    def _create_signature_section(self) -> List:
        """Создание секции подписи."""
        elements = []
        
        elements.append(Spacer(1, 30))
        elements.append(Paragraph("Подпись врача: _________________", self.styles['MedicalData']))
        elements.append(Paragraph(f"Дата: {datetime.now().strftime('%d.%m.%Y')}", self.styles['MedicalData']))
        elements.append(Spacer(1, 20))
        elements.append(Paragraph("MQEA - Medical Quantum Entanglement Analysis", self.styles['MedicalData']))
        elements.append(Paragraph("Автор: Мухаммад Махизода, Таджикский национальный университет", self.styles['MedicalData']))
        
        return elements
    
    def generate_summary_report(self, patients_data: List[Dict], output_path: str = "summary_report.pdf"):
        """Генерация сводного отчета по всем пациентам."""
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        story = []
        
        # Заголовок отчета
        story.append(Paragraph("СВОДНЫЙ ОТЧЕТ MQEA", self.styles['CardTitle']))
        story.append(Paragraph(f"Дата генерации: {datetime.now().strftime('%d.%m.%Y %H:%M')}", self.styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Статистика
        story.append(self._create_statistics_section(patients_data))
        story.append(Spacer(1, 15))
        
        # Список пациентов
        story.append(self._create_patients_list_section(patients_data))
        
        # Создаем PDF с водяным знаком
        def add_watermark(canvas, doc):
            watermark = WatermarkCanvas(canvas, doc)
            watermark.draw_watermark()
        
        doc.build(story, onFirstPage=add_watermark, onLaterPages=add_watermark)
        return output_path
    
    def _create_statistics_section(self, patients_data: List[Dict]) -> List:
        """Создание секции статистики."""
        elements = []
        
        elements.append(Paragraph("📈 СТАТИСТИКА", self.styles['SectionTitle']))
        
        total_patients = len(patients_data)
        avg_age = sum(p.get('age', 0) for p in patients_data) / total_patients if total_patients > 0 else 0
        
        stats_data = [
            ['Параметр', 'Значение'],
            ['Всего пациентов', str(total_patients)],
            ['Средний возраст', f"{avg_age:.1f} лет"],
            ['Мужчин', str(sum(1 for p in patients_data if p.get('gender') == 'Мужской'))],
            ['Женщин', str(sum(1 for p in patients_data if p.get('gender') == 'Женский'))],
            ['С диагнозами', str(sum(1 for p in patients_data if p.get('diagnoses')))],
        ]
        
        stats_table = Table(stats_data, colWidths=[6*cm, 4*cm])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), self.bold_font_name),
            ('FONTNAME', (0, 1), (-1, -1), self.font_name),  # Добавляем шрифт для всех строк данных
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        elements.append(stats_table)
        return elements
    
    def _create_patients_list_section(self, patients_data: List[Dict]) -> List:
        """Создание секции списка пациентов."""
        elements = []
        
        elements.append(Paragraph("👥 СПИСОК ПАЦИЕНТОВ", self.styles['SectionTitle']))
        
        if not patients_data:
            elements.append(Paragraph("Нет данных о пациентах", self.styles['MedicalData']))
            return elements
        
        # Заголовок таблицы
        header_data = [['ID', 'ФИО', 'Возраст', 'Пол', 'Последний визит', 'Статус']]
        
        # Данные пациентов
        for patient in patients_data[:20]:  # Показываем первых 20
            last_visit = patient.get('last_visit', 'N/A')
            if isinstance(last_visit, datetime):
                last_visit = last_visit.strftime('%d.%m.%Y')
            
            status = "Активен" if patient.get('is_active', True) else "Неактивен"
            
            header_data.append([
                patient.get('patient_id', 'N/A'),
                patient.get('name', 'N/A'),
                str(patient.get('age', 'N/A')),
                patient.get('gender', 'N/A'),
                last_visit,
                status
            ])
        
        patients_table = Table(header_data, colWidths=[2*cm, 4*cm, 1.5*cm, 1.5*cm, 2*cm, 2*cm])
        patients_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), self.bold_font_name),
            ('FONTNAME', (0, 1), (-1, -1), self.font_name),  # Добавляем шрифт для всех строк данных
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        elements.append(patients_table)
        
        if len(patients_data) > 20:
            elements.append(Paragraph(f"... и еще {len(patients_data) - 20} пациентов", self.styles['MedicalData']))
        
        return elements

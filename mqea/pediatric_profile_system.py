"""
Система профилей детей с историей развития и прогнозированием.

Функции:
- Создание и управление профилями детей
- Сохранение истории всех анализов
- Сравнение текущих и предыдущих анализов
- Отслеживание динамики развития
- Прогнозирование развития
- Выявление слабых и сильных сторон
- Персонализированные рекомендации
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
import numpy as np

from .pediatric_quantum_system import (
    DetailedAnthropometry,
    PediatricVitalSigns,
    PediatricQuantumEngine
)


@dataclass
class ChildProfile:
    """Профиль ребенка."""
    child_id: str
    name: str
    date_of_birth: str  # YYYY-MM-DD
    gender: str  # male/female
    blood_type: Optional[str] = None
    allergies: List[str] = None
    chronic_conditions: List[str] = None
    parents_info: Dict[str, str] = None
    created_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
        if self.allergies is None:
            self.allergies = []
        if self.chronic_conditions is None:
            self.chronic_conditions = []
        if self.parents_info is None:
            self.parents_info = {}


@dataclass
class DevelopmentRecord:
    """Запись о развитии ребенка."""
    record_id: str
    child_id: str
    date: str  # YYYY-MM-DD
    age_months: int
    vital_signs: Dict[str, Any]
    anthropometry: Optional[Dict[str, Any]] = None
    quantum_analysis: Optional[Dict[str, Any]] = None
    development_report: Optional[Dict[str, Any]] = None
    notes: str = ""
    
    def __post_init__(self):
        if self.date is None:
            self.date = datetime.now().strftime("%Y-%m-%d")


class PediatricProfileManager:
    """Менеджер профилей детей."""
    
    def __init__(self, data_dir: str = "data/pediatric_profiles"):
        self.data_dir = data_dir
        self.engine = PediatricQuantumEngine()
        os.makedirs(data_dir, exist_ok=True)
    
    def create_child_profile(self, name: str, date_of_birth: str, gender: str, **kwargs) -> ChildProfile:
        """Создает новый профиль ребенка."""
        child_id = f"child_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        profile = ChildProfile(
            child_id=child_id,
            name=name,
            date_of_birth=date_of_birth,
            gender=gender,
            **kwargs
        )
        
        self._save_profile(profile)
        return profile
    
    def get_child_profile(self, child_id: str) -> Optional[ChildProfile]:
        """Получает профиль ребенка."""
        profile_path = os.path.join(self.data_dir, f"{child_id}_profile.json")
        
        if not os.path.exists(profile_path):
            return None
        
        with open(profile_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return ChildProfile(**data)
    
    def list_all_profiles(self) -> List[ChildProfile]:
        """Возвращает список всех профилей."""
        profiles = []
        
        for filename in os.listdir(self.data_dir):
            if filename.endswith('_profile.json'):
                child_id = filename.replace('_profile.json', '')
                profile = self.get_child_profile(child_id)
                if profile:
                    profiles.append(profile)
        
        return profiles
    
    def update_profile(self, profile: ChildProfile):
        """Обновляет профиль ребенка."""
        self._save_profile(profile)
    
    def _save_profile(self, profile: ChildProfile):
        """Сохраняет профиль в файл."""
        profile_path = os.path.join(self.data_dir, f"{profile.child_id}_profile.json")
        
        with open(profile_path, 'w', encoding='utf-8') as f:
            json.dump(asdict(profile), f, ensure_ascii=False, indent=2)
    
    def add_development_record(self,
                              child_id: str,
                              vital_signs: PediatricVitalSigns,
                              anthropometry: Optional[DetailedAnthropometry] = None,
                              notes: str = "") -> DevelopmentRecord:
        """Добавляет новую запись о развитии."""
        profile = self.get_child_profile(child_id)
        if not profile:
            raise ValueError(f"Профиль {child_id} не найден")
        
        # Вычисляем возраст в месяцах
        birth_date = datetime.strptime(profile.date_of_birth, "%Y-%m-%d")
        current_date = datetime.now()
        age_months = (current_date.year - birth_date.year) * 12 + (current_date.month - birth_date.month)
        
        # Создаем запись
        record_id = f"record_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Сериализуем данные для записи
        vital_signs_dict = asdict(vital_signs)
        anthropometry_dict = None
        if anthropometry:
            anthropometry_dict = asdict(anthropometry)
            # Конвертируем datetime в строку для JSON сериализации
            if 'timestamp' in anthropometry_dict and anthropometry_dict['timestamp']:
                if hasattr(anthropometry_dict['timestamp'], 'isoformat'):
                    anthropometry_dict['timestamp'] = anthropometry_dict['timestamp'].isoformat()
                else:
                    anthropometry_dict['timestamp'] = str(anthropometry_dict['timestamp'])
        
        record = DevelopmentRecord(
            record_id=record_id,
            child_id=child_id,
            date=current_date.strftime("%Y-%m-%d"),
            age_months=age_months,
            vital_signs=vital_signs_dict,
            anthropometry=anthropometry_dict,
            notes=notes
        )
        
        # Выполняем анализ
        if anthropometry:
            detailed_analysis = self.engine.analyze_detailed_anthropometry(anthropometry, age_months)
            comprehensive_report = self.engine.generate_comprehensive_development_report(
                anthropometry, age_months, detailed_analysis
            )
            
            record.quantum_analysis = detailed_analysis
            record.development_report = comprehensive_report
        else:
            # Базовый анализ только по жизненным показателям
            detected_conditions = self.engine.detect_pediatric_conditions(vital_signs)
            quantum_report = self.engine.generate_pediatric_quantum_report(vital_signs, detected_conditions)
            
            record.quantum_analysis = {
                'detected_conditions': detected_conditions
            }
            record.development_report = quantum_report
        
        # Сохраняем запись
        self._save_record(record)
        
        return record
    
    def get_development_history(self, child_id: str) -> List[DevelopmentRecord]:
        """Получает историю развития ребенка."""
        history_path = os.path.join(self.data_dir, f"{child_id}_history.json")
        
        if not os.path.exists(history_path):
            return []
        
        try:
            with open(history_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError, IOError) as e:
            print(f"Ошибка при загрузке истории для {child_id}: {e}")
            # Создаем резервную копию поврежденного файла
            backup_path = f"{history_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            try:
                if os.path.exists(history_path):
                    os.rename(history_path, backup_path)
                    print(f"Создана резервная копия: {backup_path}")
            except:
                pass
            return []
        
        try:
            records = [DevelopmentRecord(**record_data) for record_data in data]
            return sorted(records, key=lambda x: x.date)
        except Exception as e:
            print(f"Ошибка при создании записей для {child_id}: {e}")
            return []
    
    def _save_record(self, record: DevelopmentRecord):
        """Сохраняет запись о развитии."""
        history_path = os.path.join(self.data_dir, f"{record.child_id}_history.json")
        
        # Загружаем существующую историю
        history = []
        if os.path.exists(history_path):
            try:
                with open(history_path, 'r', encoding='utf-8') as f:
                    history = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError, IOError) as e:
                print(f"Ошибка при загрузке истории для {record.child_id}: {e}")
                # Создаем резервную копию поврежденного файла
                backup_path = f"{history_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                try:
                    os.rename(history_path, backup_path)
                    print(f"Создана резервная копия: {backup_path}")
                except:
                    pass
                history = []
        
        # Добавляем новую запись с правильной сериализацией
        try:
            record_dict = self._serialize_record(record)
            history.append(record_dict)
            
            # Сохраняем
            with open(history_path, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка при сохранении записи для {record.child_id}: {e}")
            raise
    
    def _serialize_record(self, record: DevelopmentRecord) -> Dict[str, Any]:
        """Сериализует запись о развитии для JSON."""
        record_dict = asdict(record)
        
        # Обрабатываем антропометрию, если она есть
        if record_dict.get('anthropometry'):
            anthropometry_dict = record_dict['anthropometry']
            # Конвертируем datetime в строку
            if 'timestamp' in anthropometry_dict and anthropometry_dict['timestamp']:
                if hasattr(anthropometry_dict['timestamp'], 'isoformat'):
                    anthropometry_dict['timestamp'] = anthropometry_dict['timestamp'].isoformat()
                else:
                    anthropometry_dict['timestamp'] = str(anthropometry_dict['timestamp'])
        
        return record_dict
    
    def compare_records(self, child_id: str, record1_id: str, record2_id: str) -> Dict[str, Any]:
        """Сравнивает две записи о развитии."""
        history = self.get_development_history(child_id)
        
        record1 = next((r for r in history if r.record_id == record1_id), None)
        record2 = next((r for r in history if r.record_id == record2_id), None)
        
        if not record1 or not record2:
            raise ValueError("Одна или обе записи не найдены")
        
        return self._analyze_development_progress(record1, record2)
    
    def analyze_latest_progress(self, child_id: str) -> Optional[Dict[str, Any]]:
        """Анализирует прогресс с момента последнего осмотра."""
        history = self.get_development_history(child_id)
        
        if len(history) < 2:
            return None
        
        # Берем две последние записи
        previous_record = history[-2]
        current_record = history[-1]
        
        return self._analyze_development_progress(previous_record, current_record)
    
    def _analyze_development_progress(self, old_record: DevelopmentRecord, new_record: DevelopmentRecord) -> Dict[str, Any]:
        """Анализирует прогресс развития между двумя записями."""
        
        analysis = {
            'period': {
                'from_date': old_record.date,
                'to_date': new_record.date,
                'from_age_months': old_record.age_months,
                'to_age_months': new_record.age_months,
                'time_diff_days': (datetime.strptime(new_record.date, "%Y-%m-%d") - 
                                  datetime.strptime(old_record.date, "%Y-%m-%d")).days
            },
            'vital_signs_changes': {},
            'anthropometry_changes': {},
            'strong_areas': [],
            'weak_areas': [],
            'recommendations': [],
            'predictions': {},
            'overall_assessment': ''
        }
        
        # Анализ изменений жизненных показателей
        old_vs = old_record.vital_signs
        new_vs = new_record.vital_signs
        
        vital_changes = {}
        for key in ['heart_rate', 'respiratory_rate', 'blood_pressure_systolic', 
                    'blood_pressure_diastolic', 'temperature', 'oxygen_saturation',
                    'weight_kg', 'height_cm', 'head_circumference_cm']:
            if key in old_vs and key in new_vs:
                old_val = old_vs[key]
                new_val = new_vs[key]
                if old_val and new_val:
                    change = new_val - old_val
                    percent_change = (change / old_val * 100) if old_val != 0 else 0
                    vital_changes[key] = {
                        'old': old_val,
                        'new': new_val,
                        'change': change,
                        'percent_change': percent_change,
                        'status': self._evaluate_change(key, change, percent_change, new_record.age_months)
                    }
        
        analysis['vital_signs_changes'] = vital_changes
        
        # Анализ антропометрических изменений
        if old_record.anthropometry and new_record.anthropometry:
            analysis['anthropometry_changes'] = self._compare_anthropometry(
                old_record.anthropometry, 
                new_record.anthropometry,
                new_record.age_months
            )
        
        # Определение сильных и слабых зон
        analysis['strong_areas'] = self._identify_strong_areas(vital_changes, analysis['anthropometry_changes'])
        analysis['weak_areas'] = self._identify_weak_areas(vital_changes, analysis['anthropometry_changes'])
        
        # Генерация рекомендаций
        analysis['recommendations'] = self._generate_progress_recommendations(
            analysis['weak_areas'],
            new_record.age_months
        )
        
        # Прогнозирование
        analysis['predictions'] = self._predict_future_development(
            child_id=new_record.child_id,
            current_age_months=new_record.age_months,
            vital_changes=vital_changes,
            anthropometry_changes=analysis['anthropometry_changes']
        )
        
        # Общая оценка
        analysis['overall_assessment'] = self._generate_progress_assessment(
            analysis['strong_areas'],
            analysis['weak_areas'],
            analysis['predictions']
        )
        
        return analysis
    
    def _evaluate_change(self, indicator: str, change: float, percent_change: float, age_months: int) -> str:
        """Оценивает изменение показателя."""
        # Показатели, которые должны расти
        growth_indicators = ['weight_kg', 'height_cm', 'head_circumference_cm']
        
        if indicator in growth_indicators:
            if change > 0:
                if percent_change < 2:
                    return "медленный рост"
                elif percent_change < 10:
                    return "нормальный рост"
                else:
                    return "быстрый рост"
            else:
                return "отсутствие роста ⚠️"
        
        # Для других показателей - стабильность это хорошо
        if abs(percent_change) < 5:
            return "стабильно"
        elif abs(percent_change) < 15:
            return "умеренные изменения"
        else:
            return "значительные изменения ⚠️"
    
    def _compare_anthropometry(self, old_anthro: Dict, new_anthro: Dict, age_months: int) -> Dict[str, Any]:
        """Сравнивает антропометрические данные."""
        changes = {}
        
        for key in new_anthro.keys():
            if key in old_anthro and key != 'timestamp':
                old_val = old_anthro[key]
                new_val = new_anthro[key]
                
                if old_val and new_val and isinstance(old_val, (int, float)) and isinstance(new_val, (int, float)):
                    change = new_val - old_val
                    percent_change = (change / old_val * 100) if old_val != 0 else 0
                    
                    changes[key] = {
                        'old': old_val,
                        'new': new_val,
                        'change': change,
                        'percent_change': percent_change,
                        'status': self._evaluate_anthropometry_change(key, percent_change)
                    }
        
        return changes
    
    def _evaluate_anthropometry_change(self, indicator: str, percent_change: float) -> str:
        """Оценивает изменение антропометрического показателя."""
        # Все размеры должны расти
        if percent_change > 0:
            if percent_change < 2:
                return "медленное развитие"
            elif percent_change < 10:
                return "нормальное развитие ✓"
            else:
                return "активное развитие ✓✓"
        elif percent_change < 0:
            return "уменьшение ⚠️"
        else:
            return "без изменений"
    
    def _identify_strong_areas(self, vital_changes: Dict, anthro_changes: Dict) -> List[Dict[str, str]]:
        """Определяет сильные стороны развития."""
        strong = []
        
        # Анализ жизненных показателей
        for key, data in vital_changes.items():
            if 'нормальный рост' in data['status'] or 'быстрый рост' in data['status']:
                strong.append({
                    'area': self._translate_indicator(key),
                    'status': data['status'],
                    'change': f"+{data['percent_change']:.1f}%"
                })
        
        # Анализ антропометрии
        for key, data in anthro_changes.items():
            if 'нормальное развитие' in data['status'] or 'активное развитие' in data['status']:
                if len(strong) < 10:  # Ограничиваем количество
                    strong.append({
                        'area': self._translate_indicator(key),
                        'status': data['status'],
                        'change': f"+{data['percent_change']:.1f}%"
                    })
        
        return strong
    
    def _identify_weak_areas(self, vital_changes: Dict, anthro_changes: Dict) -> List[Dict[str, str]]:
        """Определяет слабые стороны развития."""
        weak = []
        
        # Анализ жизненных показателей
        for key, data in vital_changes.items():
            if '⚠️' in data['status'] or 'медленный' in data['status']:
                weak.append({
                    'area': self._translate_indicator(key),
                    'status': data['status'],
                    'change': f"{data['percent_change']:+.1f}%",
                    'concern_level': 'высокий' if '⚠️' in data['status'] else 'средний'
                })
        
        # Анализ антропометрии
        for key, data in anthro_changes.items():
            if '⚠️' in data['status'] or 'медленное' in data['status']:
                weak.append({
                    'area': self._translate_indicator(key),
                    'status': data['status'],
                    'change': f"{data['percent_change']:+.1f}%",
                    'concern_level': 'высокий' if '⚠️' in data['status'] else 'средний'
                })
        
        return weak
    
    def _translate_indicator(self, key: str) -> str:
        """Переводит название показателя на русский."""
        translations = {
            'weight_kg': 'Вес',
            'height_cm': 'Рост',
            'head_circumference_cm': 'Окружность головы',
            'chest_circumference_cm': 'Окружность груди',
            'heart_rate': 'Частота сердцебиения',
            'respiratory_rate': 'Частота дыхания',
            'blood_pressure_systolic': 'Систолическое давление',
            'blood_pressure_diastolic': 'Диастолическое давление',
            'arm_span_cm': 'Размах рук',
            'leg_length_cm': 'Длина ног',
            'foot_length_cm': 'Длина стопы',
            'thumb_length_mm': 'Большой палец руки',
            'index_finger_length_mm': 'Указательный палец',
            'middle_finger_length_mm': 'Средний палец',
            'big_toe_length_mm': 'Большой палец ноги'
        }
        return translations.get(key, key)
    
    def _generate_progress_recommendations(self, weak_areas: List[Dict], age_months: int) -> List[str]:
        """Генерирует рекомендации на основе слабых зон."""
        recommendations = []
        
        for weak in weak_areas:
            area = weak['area'].lower()
            
            if 'вес' in area:
                recommendations.extend([
                    "💊 Консультация диетолога для оптимизации питания",
                    "🍽️ Увеличение калорийности рациона - больше белка и полезных жиров",
                    "📊 Еженедельный контроль набора веса"
                ])
            
            elif 'рост' in area:
                recommendations.extend([
                    "💊 Витамин D3 + Кальций для стимуляции роста костей",
                    "🏃‍♂️ Физические упражнения для стимуляции роста",
                    "😴 Обеспечить достаточный сон (гормон роста вырабатывается во сне)"
                ])
            
            elif 'голов' in area:
                recommendations.extend([
                    "🧠 Консультация невролога обязательна",
                    "👐 Массаж головы и шеи для улучшения кровообращения",
                    "🎮 Развивающие игры для стимуляции мозговой активности"
                ])
            
            elif 'палец' in area or 'рук' in area or 'ног' in area:
                recommendations.extend([
                    "👐 Ежедневный массаж конечностей (15 минут)",
                    "🤸 Упражнения для развития мелкой моторики",
                    "💊 Омега-3 для развития нервной системы и координации"
                ])
            
            elif 'грудь' in area or 'дыхание' in area:
                recommendations.extend([
                    "🫁 Дыхательная гимнастика",
                    "🏊 Плавание для развития грудной клетки",
                    "🚶 Больше прогулок на свежем воздухе"
                ])
        
        # Удаляем дубликаты
        return list(dict.fromkeys(recommendations))
    
    def _predict_future_development(self, 
                                   child_id: str,
                                   current_age_months: int,
                                   vital_changes: Dict,
                                   anthropometry_changes: Dict) -> Dict[str, Any]:
        """Прогнозирует будущее развитие."""
        history = self.get_development_history(child_id)
        
        predictions = {
            'next_month': {},
            'next_3_months': {},
            'potential_issues': [],
            'positive_trends': []
        }
        
        # Прогноз веса
        if 'weight_kg' in vital_changes:
            weight_data = vital_changes['weight_kg']
            current_weight = weight_data['new']
            monthly_growth = weight_data['change'] / max(1, (current_age_months - vital_changes.get('age_diff', 1)))
            
            predictions['next_month']['weight_kg'] = {
                'predicted': current_weight + monthly_growth,
                'confidence': 'высокая' if abs(weight_data['percent_change']) < 20 else 'средняя'
            }
            
            predictions['next_3_months']['weight_kg'] = {
                'predicted': current_weight + (monthly_growth * 3),
                'confidence': 'средняя'
            }
            
            if monthly_growth < 0.1:
                predictions['potential_issues'].append(
                    "⚠️ Медленный набор веса - возможна задержка физического развития"
                )
            elif monthly_growth > 0.5 and current_age_months > 12:
                predictions['potential_issues'].append(
                    "⚠️ Быстрый набор веса - риск избыточного веса"
                )
            else:
                predictions['positive_trends'].append(
                    "✓ Вес набирается в нормальном темпе"
                )
        
        # Прогноз роста
        if 'height_cm' in vital_changes:
            height_data = vital_changes['height_cm']
            current_height = height_data['new']
            monthly_growth = height_data['change'] / max(1, (current_age_months - vital_changes.get('age_diff', 1)))
            
            predictions['next_month']['height_cm'] = {
                'predicted': current_height + monthly_growth,
                'confidence': 'высокая'
            }
            
            predictions['next_3_months']['height_cm'] = {
                'predicted': current_height + (monthly_growth * 3),
                'confidence': 'средняя'
            }
            
            if monthly_growth > 0.3:
                predictions['positive_trends'].append(
                    "✓ Активный рост - ребенок развивается хорошо"
                )
        
        # Анализ тенденций антропометрии
        slow_development_count = sum(1 for v in anthropometry_changes.values() 
                                    if 'медленное' in v.get('status', ''))
        
        if slow_development_count > 3:
            predictions['potential_issues'].append(
                f"⚠️ Обнаружено {slow_development_count} зон с медленным развитием - требуется комплексная коррекция"
            )
        
        return predictions
    
    def _generate_progress_assessment(self, 
                                     strong_areas: List[Dict],
                                     weak_areas: List[Dict],
                                     predictions: Dict) -> str:
        """Генерирует общую оценку прогресса."""
        assessment = ""
        
        if len(strong_areas) > len(weak_areas) * 2:
            assessment = "✅ **ОТЛИЧНЫЙ ПРОГРЕСС**\n\n"
            assessment += f"Ребенок развивается гармонично. Выявлено {len(strong_areas)} зон активного развития. "
            if weak_areas:
                assessment += f"Есть {len(weak_areas)} зон, требующих внимания, но общая динамика положительная."
        
        elif len(strong_areas) > len(weak_areas):
            assessment = "📋 **ХОРОШИЙ ПРОГРЕСС**\n\n"
            assessment += f"Развитие идет в правильном направлении. {len(strong_areas)} зон развиваются хорошо. "
            if weak_areas:
                assessment += f"Необходимо уделить внимание {len(weak_areas)} зонам для оптимального развития."
        
        elif len(weak_areas) > len(strong_areas):
            assessment = "⚠️ **ТРЕБУЕТСЯ ВНИМАНИЕ**\n\n"
            assessment += f"Выявлено {len(weak_areas)} зон с замедленным развитием. "
            assessment += "Рекомендуется усиленный контроль и выполнение всех назначений. "
            if strong_areas:
                assessment += f"Положительная динамика наблюдается в {len(strong_areas)} зонах."
        
        else:
            assessment = "📊 **СТАБИЛЬНОЕ РАЗВИТИЕ**\n\n"
            assessment += "Развитие идет планомерно. Продолжайте текущий режим ухода и наблюдения."
        
        # Добавляем прогноз
        potential_issues = predictions.get('potential_issues', [])
        if potential_issues:
            assessment += "\n\n**⚠️ Потенциальные риски:**\n"
            for issue in potential_issues[:3]:  # Показываем только топ-3
                assessment += f"\n{issue}"
        
        positive_trends = predictions.get('positive_trends', [])
        if positive_trends:
            assessment += "\n\n**✓ Положительные тенденции:**\n"
            for trend in positive_trends[:3]:
                assessment += f"\n{trend}"
        
        return assessment


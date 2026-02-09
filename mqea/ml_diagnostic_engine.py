#!/usr/bin/env python3
"""
Система машинного обучения для диагностики MQEA.

Автор: Мухаммад Махизода
Таджикский национальный университет
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
import os
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class MLDiagnosticEngine:
    """Движок машинного обучения для диагностики."""
    
    def __init__(self, model_path: str = "mqea_models/"):
        """Инициализация движка ML."""
        self.model_path = model_path
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.models = {}
        self.feature_importance = {}
        
        # Создаем директорию для моделей
        os.makedirs(model_path, exist_ok=True)
        
        # Инициализируем модели
        self._init_models()
        
        # Загружаем предобученные модели если есть
        self._load_models()
    
    def _init_models(self):
        """Инициализация моделей машинного обучения."""
        self.models = {
            'cardiovascular': RandomForestClassifier(n_estimators=100, random_state=42),
            'diabetes': GradientBoostingClassifier(n_estimators=100, random_state=42),
            'hypertension': LogisticRegression(random_state=42, max_iter=1000),
            'respiratory': SVC(kernel='rbf', probability=True, random_state=42),
            'general_health': RandomForestClassifier(n_estimators=150, random_state=42)
        }
    
    def _load_models(self):
        """Загрузка предобученных моделей."""
        for condition, model in self.models.items():
            model_file = os.path.join(self.model_path, f"{condition}_model.pkl")
            scaler_file = os.path.join(self.model_path, f"{condition}_scaler.pkl")
            
            if os.path.exists(model_file):
                try:
                    self.models[condition] = joblib.load(model_file)
                    if condition in ['cardiovascular', 'diabetes', 'hypertension', 'general_health']:
                        # Загружаем скейлер только для моделей, которые его используют
                        if os.path.exists(scaler_file):
                            self.scaler = joblib.load(scaler_file)
                            print(f"✅ Scaler для {condition} загружен")
                    print(f"✅ Модель {condition} загружена")
                except Exception as e:
                    print(f"❌ Ошибка загрузки модели {condition}: {e}")
    
    def _save_models(self):
        """Сохранение моделей."""
        for condition, model in self.models.items():
            model_file = os.path.join(self.model_path, f"{condition}_model.pkl")
            scaler_file = os.path.join(self.model_path, f"{condition}_scaler.pkl")
            
            try:
                joblib.dump(model, model_file)
                if condition in ['cardiovascular', 'diabetes', 'hypertension', 'general_health']:
                    joblib.dump(self.scaler, scaler_file)
                print(f"✅ Модель {condition} сохранена")
            except Exception as e:
                print(f"❌ Ошибка сохранения модели {condition}: {e}")
    
    def prepare_training_data(self, data: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray, List[str]]:
        """Подготовка данных для обучения."""
        # Медицинские показатели
        medical_features = [
            'heart_rate', 'blood_pressure_systolic', 'blood_pressure_diastolic',
            'temperature', 'oxygen_saturation', 'respiratory_rate',
            'glucose', 'cholesterol', 'bmi', 'age'
        ]
        
        # Демографические данные
        demographic_features = ['age', 'gender', 'bmi']
        
        # Факторы риска
        risk_factors = [
            'smoking', 'alcohol', 'sedentary_lifestyle', 'family_history',
            'stress_level', 'sleep_hours', 'exercise_frequency'
        ]
        
        # Квантовые показатели
        quantum_features = [
            'quantum_coherence', 'entanglement_pairs', 'max_entanglement',
            'pattern_complexity', 'temporal_correlation'
        ]
        
        # Объединяем все признаки
        all_features = medical_features + risk_factors + quantum_features
        
        # Фильтруем только существующие колонки
        available_features = [f for f in all_features if f in data.columns]
        
        # Подготавливаем X (признаки)
        X = data[available_features].copy()
        
        # Обрабатываем категориальные переменные
        for col in X.select_dtypes(include=['object']).columns:
            if col not in self.label_encoders:
                self.label_encoders[col] = LabelEncoder()
            X[col] = self.label_encoders[col].fit_transform(X[col].astype(str))
        
        # Заполняем пропущенные значения
        X = X.fillna(X.median())
        
        # Подготавливаем y (целевая переменная)
        if 'diagnosis' in data.columns:
            y = data['diagnosis']
        else:
            # Если нет диагноза, создаем синтетические метки на основе показателей
            y = self._generate_synthetic_labels(X)
        
        return X.values, y.values, available_features
    
    def _generate_synthetic_labels(self, X: pd.DataFrame) -> pd.Series:
        """Генерация синтетических меток для обучения."""
        labels = []
        
        for _, row in X.iterrows():
            # Простая логика для генерации меток на основе медицинских показателей
            if 'heart_rate' in row and row['heart_rate'] > 100:
                labels.append('cardiovascular_risk')
            elif 'glucose' in row and row['glucose'] > 7.0:
                labels.append('diabetes_risk')
            elif 'blood_pressure_systolic' in row and row['blood_pressure_systolic'] > 140:
                labels.append('hypertension_risk')
            elif 'oxygen_saturation' in row and row['oxygen_saturation'] < 95:
                labels.append('respiratory_risk')
            else:
                labels.append('healthy')
        
        return pd.Series(labels)
    
    def train_models(self, data: pd.DataFrame) -> Dict[str, float]:
        """Обучение всех моделей."""
        X, y, features = self.prepare_training_data(data)
        
        # Разделяем данные
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Масштабируем данные
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        results = {}
        
        for condition, model in self.models.items():
            try:
                # Обучаем модель
                if condition in ['cardiovascular', 'diabetes', 'hypertension', 'general_health']:
                    model.fit(X_train_scaled, y_train)
                    y_pred = model.predict(X_test_scaled)
                else:
                    model.fit(X_train, y_train)
                    y_pred = model.predict(X_test)
                
                # Оцениваем точность
                accuracy = accuracy_score(y_test, y_pred)
                results[condition] = accuracy
                
                # Сохраняем важность признаков для RandomForest
                if hasattr(model, 'feature_importances_'):
                    self.feature_importance[condition] = dict(zip(features, model.feature_importances_))
                
                print(f"✅ Модель {condition} обучена. Точность: {accuracy:.3f}")
                
            except Exception as e:
                print(f"❌ Ошибка обучения модели {condition}: {e}")
                results[condition] = 0.0
        
        # Сохраняем модели
        self._save_models()
        
        return results
    
    def predict_diagnosis(self, patient_data: Dict) -> Dict[str, Dict]:
        """Предсказание диагноза для пациента."""
        predictions = {}
        
        # Подготавливаем данные пациента
        patient_df = pd.DataFrame([patient_data])
        
        # Обрабатываем категориальные переменные
        for col in patient_df.select_dtypes(include=['object']).columns:
            if col in self.label_encoders:
                try:
                    patient_df[col] = self.label_encoders[col].transform(patient_df[col].astype(str))
                except ValueError:
                    # Если значение не было в обучающих данных, используем 0
                    patient_df[col] = 0
        
        # Заполняем пропущенные значения
        patient_df = patient_df.fillna(0)
        
        for condition, model in self.models.items():
            try:
                # Проверяем, обучена ли модель
                if not hasattr(model, 'predict'):
                    raise ValueError(f"Модель {condition} не обучена")
                
                # Проверяем, есть ли у модели атрибут classes_ (признак обученной модели)
                if not hasattr(model, 'classes_'):
                    # Модель не обучена, возвращаем значения по умолчанию
                    predictions[condition] = {
                        'prediction': 'unknown',
                        'confidence': 0.0,
                        'probabilities': {}
                    }
                    continue
                
                # Получаем признаки для данной модели
                if condition in ['cardiovascular', 'diabetes', 'hypertension', 'general_health']:
                    # Проверяем, обучен ли scaler
                    if hasattr(self.scaler, 'mean_') and self.scaler.mean_ is not None:
                        # Используем масштабированные данные
                        patient_scaled = self.scaler.transform(patient_df.values)
                        proba = model.predict_proba(patient_scaled)[0]
                        prediction = model.predict(patient_scaled)[0]
                    else:
                        # Если scaler не обучен, пытаемся использовать данные без масштабирования
                        # или обучаем scaler на фиктивных данных
                        try:
                            # Пробуем использовать данные без масштабирования
                            proba = model.predict_proba(patient_df.values)[0]
                            prediction = model.predict(patient_df.values)[0]
                        except Exception:
                            # Если не работает, создаем фиктивные данные для обучения scaler
                            # Используем те же размеры, что и у patient_df
                            dummy_data = np.random.rand(10, patient_df.shape[1])
                            # Нормализуем фиктивные данные к разумным значениям
                            for i in range(patient_df.shape[1]):
                                col_mean = patient_df.iloc[:, i].mean() if patient_df.shape[0] > 0 else 0
                                col_std = patient_df.iloc[:, i].std() if patient_df.shape[0] > 0 else 1
                                dummy_data[:, i] = dummy_data[:, i] * col_std + col_mean
                            
                            self.scaler.fit(dummy_data)
                            patient_scaled = self.scaler.transform(patient_df.values)
                            proba = model.predict_proba(patient_scaled)[0]
                            prediction = model.predict(patient_scaled)[0]
                else:
                    proba = model.predict_proba(patient_df.values)[0]
                    prediction = model.predict(patient_df.values)[0]
                
                # Получаем уверенность в предсказании
                confidence = max(proba) if len(proba) > 0 else 0.0
                
                predictions[condition] = {
                    'prediction': prediction,
                    'confidence': confidence,
                    'probabilities': dict(zip(model.classes_, proba)) if hasattr(model, 'classes_') else {}
                }
                
            except Exception as e:
                print(f"❌ Ошибка предсказания для {condition}: {e}")
                import traceback
                traceback.print_exc()
                # Если модель не обучена, возвращаем значения по умолчанию
                predictions[condition] = {
                    'prediction': 'unknown',
                    'confidence': 0.0,
                    'probabilities': {}
                }
        
        return predictions
    
    def get_feature_importance(self, condition: str) -> Dict[str, float]:
        """Получение важности признаков для модели."""
        return self.feature_importance.get(condition, {})
    
    def generate_medical_recommendations(self, predictions: Dict[str, Dict], patient_data: Dict) -> List[Dict]:
        """Генерация медицинских рекомендаций на основе предсказаний."""
        recommendations = []
        
        for condition, pred_data in predictions.items():
            if pred_data['confidence'] > 0.7:  # Высокая уверенность
                if 'risk' in pred_data['prediction']:
                    recommendations.append({
                        'type': 'warning',
                        'condition': condition,
                        'title': f'Риск {condition}',
                        'description': f'Обнаружен высокий риск {condition} с уверенностью {pred_data["confidence"]:.1%}',
                        'confidence': pred_data['confidence'],
                        'priority': 'high' if pred_data['confidence'] > 0.8 else 'medium',
                        'recommendations': self._get_condition_recommendations(condition, patient_data)
                    })
                elif pred_data['prediction'] == 'healthy':
                    recommendations.append({
                        'type': 'positive',
                        'condition': condition,
                        'title': f'Здоровье {condition}',
                        'description': f'Показатели {condition} в норме',
                        'confidence': pred_data['confidence'],
                        'priority': 'low',
                        'recommendations': self._get_health_maintenance_recommendations(condition)
                    })
        
        return recommendations
    
    def _get_condition_recommendations(self, condition: str, patient_data: Dict) -> List[str]:
        """Получение рекомендаций для конкретного состояния."""
        recommendations = {
            'cardiovascular': [
                'Регулярно контролируйте артериальное давление (ежедневно)',
                'Соблюдайте диету с низким содержанием соли (< 5г в день)',
                'Увеличьте физическую активность (минимум 150 мин в неделю)',
                'Избегайте стрессовых ситуаций, практикуйте релаксацию',
                'Принимайте назначенные врачом препараты строго по схеме',
                'Контролируйте уровень холестерина в крови',
                'Избегайте курения и ограничьте употребление алкоголя',
                'Поддерживайте здоровый вес (ИМТ 18.5-24.9)',
                'Регулярно посещайте кардиолога (раз в 6 месяцев)',
                'Следите за пульсом и его регулярностью'
            ],
            'diabetes': [
                'Контролируйте уровень глюкозы в крови (4-6 раз в день)',
                'Соблюдайте диабетическую диету с низким гликемическим индексом',
                'Регулярно занимайтесь физическими упражнениями',
                'Следите за весом и ИМТ',
                'Регулярно посещайте эндокринолога (каждые 3 месяца)',
                'Контролируйте уровень HbA1c (цель < 7%)',
                'Следите за состоянием ног и кожи',
                'Избегайте гипогликемии - всегда носите с собой глюкозу',
                'Контролируйте артериальное давление и холестерин',
                'Ведите дневник показателей глюкозы'
            ],
            'hypertension': [
                'Ограничьте потребление соли (< 2г в день)',
                'Контролируйте артериальное давление ежедневно',
                'Принимайте антигипертензивные препараты строго по времени',
                'Избегайте курения и алкоголя',
                'Соблюдайте режим сна (7-8 часов)',
                'Снизьте потребление кофеина',
                'Увеличьте потребление калия (бананы, картофель)',
                'Регулярно занимайтесь аэробными упражнениями',
                'Избегайте стресса и практикуйте медитацию',
                'Контролируйте вес и окружность талии'
            ],
            'respiratory': [
                'Избегайте курения и пассивного курения',
                'Улучшите качество воздуха в помещении (очистители воздуха)',
                'Выполняйте дыхательные упражнения ежедневно',
                'Избегайте аллергенов и раздражителей',
                'Регулярно проветривайте помещения',
                'Поддерживайте оптимальную влажность воздуха (40-60%)',
                'Избегайте загрязненного воздуха и пыли',
                'Регулярно делайте ингаляции с физраствором',
                'Контролируйте уровень кислорода в крови',
                'При ухудшении дыхания немедленно обращайтесь к врачу'
            ],
            'metabolic': [
                'Контролируйте уровень глюкозы и инсулина',
                'Соблюдайте низкоуглеводную диету',
                'Регулярно занимайтесь силовыми упражнениями',
                'Контролируйте уровень гормонов щитовидной железы',
                'Избегайте стресса и недосыпания',
                'Контролируйте уровень кортизола',
                'Принимайте витамины группы B и магний',
                'Регулярно посещайте эндокринолога',
                'Следите за весом и составом тела',
                'Избегайте переедания и нерегулярного питания'
            ]
        }
        
        return recommendations.get(condition, [
            'Проконсультируйтесь с врачом для уточнения диагноза',
            'Следите за общим состоянием здоровья',
            'Ведите здоровый образ жизни',
            'Регулярно проходите медицинские осмотры',
            'При ухудшении состояния немедленно обращайтесь к врачу'
        ])
    
    def _get_health_maintenance_recommendations(self, condition: str) -> List[str]:
        """Получение рекомендаций для поддержания здоровья."""
        return [
            'Продолжайте вести здоровый образ жизни',
            'Регулярно проходите медицинские осмотры (раз в год)',
            'Соблюдайте сбалансированную диету с достаточным количеством овощей и фруктов',
            'Поддерживайте физическую активность (минимум 150 мин в неделю)',
            'Избегайте вредных привычек (курение, алкоголь)',
            'Контролируйте стресс и высыпайтесь (7-8 часов)',
            'Следите за весом и ИМТ',
            'Пейте достаточное количество воды (1.5-2 л в день)',
            'Избегайте длительного сидения - делайте перерывы каждые час',
            'Регулярно измеряйте основные показатели (давление, пульс, температура)'
        ]
    
    def update_model_with_feedback(self, condition: str, patient_data: Dict, 
                                 actual_diagnosis: str, model_performance: float):
        """Обновление модели на основе обратной связи."""
        # Здесь можно реализовать инкрементальное обучение
        # или сохранение данных для переобучения
        print(f"📝 Получена обратная связь для {condition}: {actual_diagnosis} (точность: {model_performance:.3f})")
        
        # В реальной системе здесь бы происходило:
        # 1. Сохранение новых данных
        # 2. Периодическое переобучение модели
        # 3. Валидация на новых данных
    
    def get_model_statistics(self) -> Dict:
        """Получение статистики моделей."""
        stats = {}
        
        for condition, model in self.models.items():
            if hasattr(model, 'n_estimators'):
                stats[condition] = {
                    'type': 'RandomForest',
                    'n_estimators': model.n_estimators,
                    'feature_importance_available': hasattr(model, 'feature_importances_')
                }
            elif hasattr(model, 'n_estimators'):
                stats[condition] = {
                    'type': 'GradientBoosting',
                    'n_estimators': model.n_estimators
                }
            else:
                stats[condition] = {
                    'type': type(model).__name__,
                    'parameters': model.get_params()
                }
        
        return stats

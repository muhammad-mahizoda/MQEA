#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Квантовый анализатор признаков заболеваний MQEA.

Анализирует медицинские данные для выявления признаков различных заболеваний,
включая ВИЧ/СПИД, рак и другие, используя принципы квантовой запутанности.

Автор: Мухаммад Махизода
Таджикский национальный университет
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any, Set
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import json
from pathlib import Path

from .core import MQEAAnalyzer
from .quantum_entanglement import QuantumEntanglementEngine
from .data_processor import MedicalTimeSeries


class DiseaseCategory(Enum):
    """Категории заболеваний."""
    INFECTIOUS = "infectious"  # Инфекционные (ВИЧ, гепатит, туберкулез)
    ONCOLOGICAL = "oncological"  # Онкологические (рак)
    CARDIOVASCULAR = "cardiovascular"  # Сердечно-сосудистые
    RESPIRATORY = "respiratory"  # Дыхательные
    METABOLIC = "metabolic"  # Метаболические
    NEUROLOGICAL = "neurological"  # Неврологические
    AUTOIMMUNE = "autoimmune"  # Аутоиммунные
    ENDOCRINE = "endocrine"  # Эндокринные


@dataclass
class DiseasePattern:
    """Паттерн признаков заболевания."""
    disease_name: str
    disease_code: str  # ICD-10 код
    category: DiseaseCategory
    indicators: Dict[str, Dict[str, Any]]  # Показатели и их нормальные/патологические значения
    quantum_weights: Dict[str, float]  # Веса для квантового анализа
    risk_factors: List[str]  # Факторы риска
    symptoms: List[str]  # Симптомы
    diagnostic_tests: List[str]  # Диагностические тесты
    description: str = ""


@dataclass
class DiseaseAnalysisResult:
    """Результат анализа заболевания."""
    disease_name: str
    disease_code: str
    category: DiseaseCategory
    probability: float  # Вероятность наличия заболевания (0-1)
    confidence: float  # Уверенность в диагнозе (0-1)
    matched_indicators: List[str]  # Совпавшие показатели
    matched_symptoms: List[str]  # Совпавшие симптомы
    risk_factors_present: List[str]  # Присутствующие факторы риска
    quantum_signature: Dict[str, float]  # Квантовая подпись
    recommendations: List[str]  # Рекомендации
    urgency_level: str  # Уровень срочности
    diagnostic_tests_recommended: List[str]  # Рекомендуемые тесты
    timestamp: datetime = field(default_factory=datetime.now)


class DiseasePatternAnalyzer:
    """
    Квантовый анализатор признаков заболеваний.
    
    Использует принципы квантовой запутанности для выявления
    скрытых паттернов, указывающих на различные заболевания.
    """
    
    def __init__(self):
        """Инициализация анализатора."""
        self.mqea_analyzer = MQEAAnalyzer()
        self.quantum_engine = QuantumEntanglementEngine()
        self.disease_patterns: Dict[str, DiseasePattern] = {}
        self._load_disease_patterns()
    
    def _load_disease_patterns(self):
        """Загрузка паттернов заболеваний."""
        # ВИЧ/СПИД
        self.disease_patterns['hiv'] = DiseasePattern(
            disease_name="ВИЧ (Вирус иммунодефицита человека)",
            disease_code="B20-B24",
            category=DiseaseCategory.INFECTIOUS,
            indicators={
                'cd4_count': {
                    'normal_range': (500, 1200),
                    'warning_range': (200, 500),
                    'critical_range': (0, 200),
                    'unit': 'cells/μL'
                },
                'cd4_percentage': {
                    'normal_range': (30, 60),
                    'warning_range': (14, 30),
                    'critical_range': (0, 14),
                    'unit': '%'
                },
                'viral_load': {
                    'normal_range': (0, 50),
                    'warning_range': (50, 10000),
                    'critical_range': (10000, float('inf')),
                    'unit': 'copies/mL'
                },
                'white_blood_cells': {
                    'normal_range': (4000, 11000),
                    'warning_range': (2000, 4000),
                    'critical_range': (0, 2000),
                    'unit': 'cells/μL'
                },
                'lymphocytes': {
                    'normal_range': (1000, 4800),
                    'warning_range': (500, 1000),
                    'critical_range': (0, 500),
                    'unit': 'cells/μL'
                },
                'hemoglobin': {
                    'normal_range': (12, 18),
                    'warning_range': (8, 12),
                    'critical_range': (0, 8),
                    'unit': 'g/dL'
                },
                'platelets': {
                    'normal_range': (150000, 450000),
                    'warning_range': (50000, 150000),
                    'critical_range': (0, 50000),
                    'unit': 'cells/μL'
                }
            },
            quantum_weights={
                'cd4_count': 0.35,
                'cd4_percentage': 0.25,
                'viral_load': 0.20,
                'white_blood_cells': 0.10,
                'lymphocytes': 0.05,
                'hemoglobin': 0.03,
                'platelets': 0.02
            },
            risk_factors=[
                'unprotected_sex',
                'iv_drug_use',
                'blood_transfusion',
                'occupational_exposure',
                'mother_to_child_transmission'
            ],
            symptoms=[
                'fever',
                'fatigue',
                'weight_loss',
                'night_sweats',
                'swollen_lymph_nodes',
                'sore_throat',
                'rash',
                'muscle_aches',
                'headache',
                'diarrhea',
                'oral_thrush',
                'recurrent_infections'
            ],
            diagnostic_tests=[
                'HIV_antibody_test',
                'HIV_antigen_test',
                'HIV_RNA_test',
                'CD4_count',
                'Viral_load',
                'Complete_blood_count',
                'Liver_function_tests',
                'Kidney_function_tests'
            ],
            description="ВИЧ - вирус, который атакует иммунную систему, разрушая CD4+ Т-клетки"
        )
        
        # Рак (общие признаки)
        self.disease_patterns['cancer_general'] = DiseasePattern(
            disease_name="Онкологическое заболевание (общие признаки)",
            disease_code="C00-C97",
            category=DiseaseCategory.ONCOLOGICAL,
            indicators={
                'tumor_markers': {
                    'normal_range': (0, 5),
                    'warning_range': (5, 20),
                    'critical_range': (20, float('inf')),
                    'unit': 'ng/mL'
                },
                'white_blood_cells': {
                    'normal_range': (4000, 11000),
                    'warning_range': (11000, 20000),
                    'critical_range': (20000, float('inf')),
                    'unit': 'cells/μL'
                },
                'hemoglobin': {
                    'normal_range': (12, 18),
                    'warning_range': (8, 12),
                    'critical_range': (0, 8),
                    'unit': 'g/dL'
                },
                'platelets': {
                    'normal_range': (150000, 450000),
                    'warning_range': (50000, 150000),
                    'critical_range': (0, 50000),
                    'unit': 'cells/μL'
                },
                'lactate_dehydrogenase': {
                    'normal_range': (140, 280),
                    'warning_range': (280, 500),
                    'critical_range': (500, float('inf')),
                    'unit': 'U/L'
                },
                'alkaline_phosphatase': {
                    'normal_range': (44, 147),
                    'warning_range': (147, 300),
                    'critical_range': (300, float('inf')),
                    'unit': 'U/L'
                },
                'c_reactive_protein': {
                    'normal_range': (0, 3),
                    'warning_range': (3, 10),
                    'critical_range': (10, float('inf')),
                    'unit': 'mg/L'
                },
                'erythrocyte_sedimentation_rate': {
                    'normal_range': (0, 20),
                    'warning_range': (20, 50),
                    'critical_range': (50, float('inf')),
                    'unit': 'mm/h'
                }
            },
            quantum_weights={
                'tumor_markers': 0.30,
                'white_blood_cells': 0.15,
                'hemoglobin': 0.12,
                'platelets': 0.10,
                'lactate_dehydrogenase': 0.12,
                'alkaline_phosphatase': 0.10,
                'c_reactive_protein': 0.06,
                'erythrocyte_sedimentation_rate': 0.05
            },
            risk_factors=[
                'age_over_50',
                'family_history',
                'smoking',
                'alcohol_consumption',
                'obesity',
                'exposure_to_carcinogens',
                'chronic_inflammation',
                'immunosuppression'
            ],
            symptoms=[
                'unexplained_weight_loss',
                'fatigue',
                'fever',
                'pain',
                'lump_or_thickening',
                'changes_in_skin',
                'persistent_cough',
                'difficulty_swallowing',
                'changes_in_bowel_habits',
                'unusual_bleeding',
                'night_sweats'
            ],
            diagnostic_tests=[
                'Biopsy',
                'CT_scan',
                'MRI',
                'PET_scan',
                'Tumor_markers',
                'Complete_blood_count',
                'Liver_function_tests',
                'Genetic_testing'
            ],
            description="Онкологические заболевания характеризуются неконтролируемым ростом клеток"
        )
        
        # Рак легких
        self.disease_patterns['lung_cancer'] = DiseasePattern(
            disease_name="Рак легких",
            disease_code="C34",
            category=DiseaseCategory.ONCOLOGICAL,
            indicators={
                'carcinoembryonic_antigen': {
                    'normal_range': (0, 3),
                    'warning_range': (3, 10),
                    'critical_range': (10, float('inf')),
                    'unit': 'ng/mL'
                },
                'neuron_specific_enolase': {
                    'normal_range': (0, 16.3),
                    'warning_range': (16.3, 50),
                    'critical_range': (50, float('inf')),
                    'unit': 'ng/mL'
                },
                'oxygen_saturation': {
                    'normal_range': (95, 100),
                    'warning_range': (90, 95),
                    'critical_range': (0, 90),
                    'unit': '%'
                },
                'respiratory_rate': {
                    'normal_range': (12, 20),
                    'warning_range': (20, 30),
                    'critical_range': (30, float('inf')),
                    'unit': 'breaths/min'
                }
            },
            quantum_weights={
                'carcinoembryonic_antigen': 0.40,
                'neuron_specific_enolase': 0.30,
                'oxygen_saturation': 0.20,
                'respiratory_rate': 0.10
            },
            risk_factors=[
                'smoking',
                'secondhand_smoke',
                'radon_exposure',
                'asbestos_exposure',
                'air_pollution',
                'family_history',
                'age_over_65'
            ],
            symptoms=[
                'persistent_cough',
                'chest_pain',
                'shortness_of_breath',
                'wheezing',
                'hoarseness',
                'weight_loss',
                'fatigue',
                'coughing_up_blood',
                'recurrent_pneumonia'
            ],
            diagnostic_tests=[
                'Chest_X_ray',
                'CT_scan',
                'PET_scan',
                'Bronchoscopy',
                'Biopsy',
                'Sputum_cytology',
                'Tumor_markers'
            ],
            description="Рак легких - злокачественная опухоль, развивающаяся из эпителия бронхов"
        )
        
        # Гепатит B
        self.disease_patterns['hepatitis_b'] = DiseasePattern(
            disease_name="Гепатит B",
            disease_code="B16",
            category=DiseaseCategory.INFECTIOUS,
            indicators={
                'alt': {
                    'normal_range': (7, 56),
                    'warning_range': (56, 200),
                    'critical_range': (200, float('inf')),
                    'unit': 'U/L'
                },
                'ast': {
                    'normal_range': (10, 40),
                    'warning_range': (40, 150),
                    'critical_range': (150, float('inf')),
                    'unit': 'U/L'
                },
                'bilirubin_total': {
                    'normal_range': (0.2, 1.2),
                    'warning_range': (1.2, 3.0),
                    'critical_range': (3.0, float('inf')),
                    'unit': 'mg/dL'
                },
                'albumin': {
                    'normal_range': (3.5, 5.0),
                    'warning_range': (2.5, 3.5),
                    'critical_range': (0, 2.5),
                    'unit': 'g/dL'
                }
            },
            quantum_weights={
                'alt': 0.30,
                'ast': 0.25,
                'bilirubin_total': 0.25,
                'albumin': 0.20
            },
            risk_factors=[
                'unprotected_sex',
                'iv_drug_use',
                'blood_transfusion',
                'occupational_exposure',
                'mother_to_child_transmission',
                'tattoos_piercings'
            ],
            symptoms=[
                'fatigue',
                'nausea',
                'vomiting',
                'abdominal_pain',
                'jaundice',
                'dark_urine',
                'clay_colored_stools',
                'fever',
                'joint_pain'
            ],
            diagnostic_tests=[
                'HBsAg',
                'Anti_HBc',
                'HBV_DNA',
                'Liver_function_tests',
                'Liver_ultrasound',
                'Liver_biopsy'
            ],
            description="Гепатит B - вирусное заболевание печени"
        )
        
        # Туберкулез
        self.disease_patterns['tuberculosis'] = DiseasePattern(
            disease_name="Туберкулез",
            disease_code="A15-A19",
            category=DiseaseCategory.INFECTIOUS,
            indicators={
                'white_blood_cells': {
                    'normal_range': (4000, 11000),
                    'warning_range': (3000, 4000),
                    'critical_range': (0, 3000),
                    'unit': 'cells/μL'
                },
                'lymphocytes': {
                    'normal_range': (1000, 4800),
                    'warning_range': (500, 1000),
                    'critical_range': (0, 500),
                    'unit': 'cells/μL'
                },
                'hemoglobin': {
                    'normal_range': (12, 18),
                    'warning_range': (8, 12),
                    'critical_range': (0, 8),
                    'unit': 'g/dL'
                },
                'erythrocyte_sedimentation_rate': {
                    'normal_range': (0, 20),
                    'warning_range': (20, 50),
                    'critical_range': (50, float('inf')),
                    'unit': 'mm/h'
                }
            },
            quantum_weights={
                'white_blood_cells': 0.25,
                'lymphocytes': 0.25,
                'hemoglobin': 0.25,
                'erythrocyte_sedimentation_rate': 0.25
            },
            risk_factors=[
                'close_contact_with_tb',
                'immunosuppression',
                'hiv_infection',
                'diabetes',
                'malnutrition',
                'crowded_living_conditions',
                'healthcare_worker'
            ],
            symptoms=[
                'persistent_cough',
                'coughing_up_blood',
                'chest_pain',
                'weight_loss',
                'fatigue',
                'fever',
                'night_sweats',
                'loss_of_appetite'
            ],
            diagnostic_tests=[
                'Tuberculin_skin_test',
                'Interferon_gamma_release_assay',
                'Chest_X_ray',
                'Sputum_culture',
                'Sputum_AFB_smear',
                'CT_scan',
                'Biopsy'
            ],
            description="Туберкулез - инфекционное заболевание, вызываемое микобактериями"
        )
        
        # Диабет
        self.disease_patterns['diabetes'] = DiseasePattern(
            disease_name="Сахарный диабет",
            disease_code="E10-E14",
            category=DiseaseCategory.METABOLIC,
            indicators={
                'glucose_fasting': {
                    'normal_range': (70, 100),
                    'warning_range': (100, 126),
                    'critical_range': (126, float('inf')),
                    'unit': 'mg/dL'
                },
                'glucose_random': {
                    'normal_range': (70, 140),
                    'warning_range': (140, 200),
                    'critical_range': (200, float('inf')),
                    'unit': 'mg/dL'
                },
                'hba1c': {
                    'normal_range': (0, 5.7),
                    'warning_range': (5.7, 6.5),
                    'critical_range': (6.5, float('inf')),
                    'unit': '%'
                },
                'insulin': {
                    'normal_range': (2, 25),
                    'warning_range': (0, 2),
                    'critical_range': (25, float('inf')),
                    'unit': 'μU/mL'
                }
            },
            quantum_weights={
                'glucose_fasting': 0.35,
                'glucose_random': 0.25,
                'hba1c': 0.30,
                'insulin': 0.10
            },
            risk_factors=[
                'family_history',
                'obesity',
                'sedentary_lifestyle',
                'age_over_45',
                'gestational_diabetes',
                'polycystic_ovary_syndrome',
                'high_blood_pressure'
            ],
            symptoms=[
                'increased_thirst',
                'frequent_urination',
                'extreme_hunger',
                'unexplained_weight_loss',
                'fatigue',
                'blurred_vision',
                'slow_healing_wounds',
                'frequent_infections'
            ],
            diagnostic_tests=[
                'Fasting_blood_glucose',
                'Oral_glucose_tolerance_test',
                'HbA1c',
                'Random_blood_glucose',
                'Insulin_levels',
                'C_peptide'
            ],
            description="Сахарный диабет - нарушение обмена глюкозы"
        )
        
        # Гепатит C
        self.disease_patterns['hepatitis_c'] = DiseasePattern(
            disease_name="Гепатит C",
            disease_code="B17.1",
            category=DiseaseCategory.INFECTIOUS,
            indicators={
                'alt': {
                    'normal_range': (7, 56),
                    'warning_range': (56, 200),
                    'critical_range': (200, float('inf')),
                    'unit': 'U/L'
                },
                'ast': {
                    'normal_range': (10, 40),
                    'warning_range': (40, 150),
                    'critical_range': (150, float('inf')),
                    'unit': 'U/L'
                },
                'bilirubin_total': {
                    'normal_range': (0.2, 1.2),
                    'warning_range': (1.2, 3.0),
                    'critical_range': (3.0, float('inf')),
                    'unit': 'mg/dL'
                },
                'albumin': {
                    'normal_range': (3.5, 5.0),
                    'warning_range': (2.5, 3.5),
                    'critical_range': (0, 2.5),
                    'unit': 'g/dL'
                }
            },
            quantum_weights={
                'alt': 0.30,
                'ast': 0.25,
                'bilirubin_total': 0.25,
                'albumin': 0.20
            },
            risk_factors=[
                'iv_drug_use',
                'blood_transfusion',
                'unprotected_sex',
                'tattoos_piercings',
                'occupational_exposure'
            ],
            symptoms=[
                'fatigue',
                'nausea',
                'vomiting',
                'abdominal_pain',
                'jaundice',
                'dark_urine',
                'loss_of_appetite',
                'joint_pain'
            ],
            diagnostic_tests=[
                'HCV_antibody_test',
                'HCV_RNA_test',
                'Liver_function_tests',
                'Liver_ultrasound',
                'Liver_biopsy'
            ],
            description="Гепатит C - вирусное заболевание печени"
        )
        
        # Рак молочной железы
        self.disease_patterns['breast_cancer'] = DiseasePattern(
            disease_name="Рак молочной железы",
            disease_code="C50",
            category=DiseaseCategory.ONCOLOGICAL,
            indicators={
                'ca_15_3': {
                    'normal_range': (0, 30),
                    'warning_range': (30, 50),
                    'critical_range': (50, float('inf')),
                    'unit': 'U/mL'
                },
                'ca_27_29': {
                    'normal_range': (0, 38),
                    'warning_range': (38, 60),
                    'critical_range': (60, float('inf')),
                    'unit': 'U/mL'
                },
                'cea': {
                    'normal_range': (0, 3),
                    'warning_range': (3, 10),
                    'critical_range': (10, float('inf')),
                    'unit': 'ng/mL'
                }
            },
            quantum_weights={
                'ca_15_3': 0.40,
                'ca_27_29': 0.35,
                'cea': 0.25
            },
            risk_factors=[
                'age_over_50',
                'family_history',
                'genetic_mutations',
                'hormone_replacement_therapy',
                'alcohol_consumption',
                'obesity',
                'early_menarche',
                'late_menopause'
            ],
            symptoms=[
                'breast_lump',
                'breast_pain',
                'nipple_discharge',
                'skin_changes',
                'nipple_retraction',
                'swollen_lymph_nodes',
                'breast_swelling'
            ],
            diagnostic_tests=[
                'Mammography',
                'Breast_ultrasound',
                'MRI',
                'Biopsy',
                'Tumor_markers',
                'Genetic_testing'
            ],
            description="Рак молочной железы - злокачественная опухоль молочной железы"
        )
        
        # Рак простаты
        self.disease_patterns['prostate_cancer'] = DiseasePattern(
            disease_name="Рак простаты",
            disease_code="C61",
            category=DiseaseCategory.ONCOLOGICAL,
            indicators={
                'psa': {
                    'normal_range': (0, 4),
                    'warning_range': (4, 10),
                    'critical_range': (10, float('inf')),
                    'unit': 'ng/mL'
                },
                'free_psa': {
                    'normal_range': (0, 1),
                    'warning_range': (1, 2),
                    'critical_range': (2, float('inf')),
                    'unit': 'ng/mL'
                },
                'psa_ratio': {
                    'normal_range': (0.15, 1.0),
                    'warning_range': (0.10, 0.15),
                    'critical_range': (0, 0.10),
                    'unit': 'ratio'
                }
            },
            quantum_weights={
                'psa': 0.50,
                'free_psa': 0.30,
                'psa_ratio': 0.20
            },
            risk_factors=[
                'age_over_50',
                'family_history',
                'african_ancestry',
                'obesity',
                'high_fat_diet'
            ],
            symptoms=[
                'difficulty_urinating',
                'frequent_urination',
                'weak_urine_stream',
                'blood_in_urine',
                'erectile_dysfunction',
                'pain_in_pelvis',
                'bone_pain'
            ],
            diagnostic_tests=[
                'PSA_test',
                'Digital_rectal_exam',
                'Prostate_biopsy',
                'MRI',
                'CT_scan',
                'Bone_scan'
            ],
            description="Рак простаты - злокачественная опухоль предстательной железы"
        )
        
        # Гипертония
        self.disease_patterns['hypertension'] = DiseasePattern(
            disease_name="Артериальная гипертония",
            disease_code="I10-I16",
            category=DiseaseCategory.CARDIOVASCULAR,
            indicators={
                'blood_pressure_systolic': {
                    'normal_range': (90, 120),
                    'warning_range': (120, 140),
                    'critical_range': (140, float('inf')),
                    'unit': 'mmHg'
                },
                'blood_pressure_diastolic': {
                    'normal_range': (60, 80),
                    'warning_range': (80, 90),
                    'critical_range': (90, float('inf')),
                    'unit': 'mmHg'
                },
                'heart_rate': {
                    'normal_range': (60, 100),
                    'warning_range': (100, 120),
                    'critical_range': (120, float('inf')),
                    'unit': 'bpm'
                }
            },
            quantum_weights={
                'blood_pressure_systolic': 0.50,
                'blood_pressure_diastolic': 0.40,
                'heart_rate': 0.10
            },
            risk_factors=[
                'age_over_40',
                'family_history',
                'obesity',
                'sedentary_lifestyle',
                'smoking',
                'alcohol_consumption',
                'high_salt_diet',
                'stress'
            ],
            symptoms=[
                'headache',
                'dizziness',
                'shortness_of_breath',
                'chest_pain',
                'visual_changes',
                'fatigue',
                'irregular_heartbeat'
            ],
            diagnostic_tests=[
                'Blood_pressure_monitoring',
                'ECG',
                'Echocardiography',
                'Blood_tests',
                'Urine_tests',
                'Eye_examination'
            ],
            description="Артериальная гипертония - стойкое повышение артериального давления"
        )
        
        # Ишемическая болезнь сердца
        self.disease_patterns['coronary_heart_disease'] = DiseasePattern(
            disease_name="Ишемическая болезнь сердца",
            disease_code="I20-I25",
            category=DiseaseCategory.CARDIOVASCULAR,
            indicators={
                'cholesterol_total': {
                    'normal_range': (0, 200),
                    'warning_range': (200, 240),
                    'critical_range': (240, float('inf')),
                    'unit': 'mg/dL'
                },
                'ldl_cholesterol': {
                    'normal_range': (0, 100),
                    'warning_range': (100, 160),
                    'critical_range': (160, float('inf')),
                    'unit': 'mg/dL'
                },
                'hdl_cholesterol': {
                    'normal_range': (40, float('inf')),
                    'warning_range': (35, 40),
                    'critical_range': (0, 35),
                    'unit': 'mg/dL'
                },
                'triglycerides': {
                    'normal_range': (0, 150),
                    'warning_range': (150, 200),
                    'critical_range': (200, float('inf')),
                    'unit': 'mg/dL'
                }
            },
            quantum_weights={
                'cholesterol_total': 0.25,
                'ldl_cholesterol': 0.35,
                'hdl_cholesterol': 0.25,
                'triglycerides': 0.15
            },
            risk_factors=[
                'age_over_45',
                'family_history',
                'smoking',
                'diabetes',
                'hypertension',
                'obesity',
                'sedentary_lifestyle',
                'high_cholesterol'
            ],
            symptoms=[
                'chest_pain',
                'shortness_of_breath',
                'fatigue',
                'heart_palpitations',
                'dizziness',
                'nausea',
                'sweating'
            ],
            diagnostic_tests=[
                'ECG',
                'Stress_test',
                'Echocardiography',
                'Coronary_angiography',
                'CT_angiography',
                'Blood_tests'
            ],
            description="Ишемическая болезнь сердца - заболевание, вызванное недостаточным кровоснабжением сердца"
        )
        
        # Астма
        self.disease_patterns['asthma'] = DiseasePattern(
            disease_name="Бронхиальная астма",
            disease_code="J45",
            category=DiseaseCategory.RESPIRATORY,
            indicators={
                'oxygen_saturation': {
                    'normal_range': (95, 100),
                    'warning_range': (90, 95),
                    'critical_range': (0, 90),
                    'unit': '%'
                },
                'respiratory_rate': {
                    'normal_range': (12, 20),
                    'warning_range': (20, 30),
                    'critical_range': (30, float('inf')),
                    'unit': 'breaths/min'
                },
                'peak_expiratory_flow': {
                    'normal_range': (80, 100),
                    'warning_range': (50, 80),
                    'critical_range': (0, 50),
                    'unit': '% predicted'
                }
            },
            quantum_weights={
                'oxygen_saturation': 0.40,
                'respiratory_rate': 0.35,
                'peak_expiratory_flow': 0.25
            },
            risk_factors=[
                'family_history',
                'allergies',
                'smoking',
                'environmental_factors',
                'obesity',
                'respiratory_infections'
            ],
            symptoms=[
                'wheezing',
                'shortness_of_breath',
                'chest_tightness',
                'coughing',
                'difficulty_breathing',
                'rapid_breathing'
            ],
            diagnostic_tests=[
                'Spirometry',
                'Peak_flow_measurement',
                'Allergy_testing',
                'Chest_X_ray',
                'Blood_tests',
                'Methacholine_challenge'
            ],
            description="Бронхиальная астма - хроническое воспалительное заболевание дыхательных путей"
        )
        
        # Пневмония
        self.disease_patterns['pneumonia'] = DiseasePattern(
            disease_name="Пневмония",
            disease_code="J12-J18",
            category=DiseaseCategory.RESPIRATORY,
            indicators={
                'white_blood_cells': {
                    'normal_range': (4000, 11000),
                    'warning_range': (11000, 20000),
                    'critical_range': (20000, float('inf')),
                    'unit': 'cells/μL'
                },
                'temperature': {
                    'normal_range': (36.1, 37.2),
                    'warning_range': (37.3, 38.5),
                    'critical_range': (38.5, float('inf')),
                    'unit': '°C'
                },
                'oxygen_saturation': {
                    'normal_range': (95, 100),
                    'warning_range': (90, 95),
                    'critical_range': (0, 90),
                    'unit': '%'
                },
                'c_reactive_protein': {
                    'normal_range': (0, 3),
                    'warning_range': (3, 10),
                    'critical_range': (10, float('inf')),
                    'unit': 'mg/L'
                }
            },
            quantum_weights={
                'white_blood_cells': 0.30,
                'temperature': 0.25,
                'oxygen_saturation': 0.25,
                'c_reactive_protein': 0.20
            },
            risk_factors=[
                'age_over_65',
                'chronic_lung_disease',
                'smoking',
                'immunosuppression',
                'recent_surgery',
                'hospitalization',
                'ventilator_use'
            ],
            symptoms=[
                'cough',
                'fever',
                'chills',
                'shortness_of_breath',
                'chest_pain',
                'fatigue',
                'sweating',
                'nausea',
                'vomiting'
            ],
            diagnostic_tests=[
                'Chest_X_ray',
                'Blood_tests',
                'Sputum_culture',
                'CT_scan',
                'Pulse_oximetry',
                'Blood_culture'
            ],
            description="Пневмония - воспаление легких, обычно вызванное инфекцией"
        )
    
    def analyze_disease_patterns(self,
                                medical_data: MedicalTimeSeries,
                                patient_symptoms: Optional[List[str]] = None,
                                risk_factors: Optional[List[str]] = None) -> List[DiseaseAnalysisResult]:
        """
        Анализ медицинских данных для выявления признаков заболеваний.
        
        Args:
            medical_data: Медицинские временные ряды
            patient_symptoms: Симптомы пациента
            risk_factors: Факторы риска пациента
            
        Returns:
            List[DiseaseAnalysisResult]: Список результатов анализа заболеваний
        """
        results = []
        
        # Квантовый анализ данных
        quantum_results = self.mqea_analyzer.quantum_entanglement_analysis(
            time_series=medical_data,
            quantum_threshold=0.3
        )
        
        # Анализ каждого заболевания
        for disease_code, pattern in self.disease_patterns.items():
            analysis = self._analyze_single_disease(
                pattern=pattern,
                medical_data=medical_data,
                quantum_results=quantum_results,
                patient_symptoms=patient_symptoms or [],
                risk_factors=risk_factors or []
            )
            
            if analysis.probability > 0.1:  # Порог для включения в результаты
                results.append(analysis)
        
        # Сортировка по вероятности
        results.sort(key=lambda x: x.probability, reverse=True)
        
        return results
    
    def _analyze_single_disease(self,
                               pattern: DiseasePattern,
                               medical_data: MedicalTimeSeries,
                               quantum_results: Dict[str, Any],
                               patient_symptoms: List[str],
                               risk_factors: List[str]) -> DiseaseAnalysisResult:
        """Анализ одного заболевания."""
        
        matched_indicators = []
        indicator_scores = []
        quantum_signature = {}
        
        # Анализ показателей
        for indicator_name, indicator_config in pattern.indicators.items():
            if indicator_name in medical_data.indicators:
                values = medical_data.data[indicator_name].dropna()
                
                if len(values) > 0:
                    current_value = values.iloc[-1]
                    normal_range = indicator_config['normal_range']
                    warning_range = indicator_config['warning_range']
                    critical_range = indicator_config['critical_range']
                    weight = pattern.quantum_weights.get(indicator_name, 0.1)
                    
                    # Определение уровня отклонения
                    if critical_range[0] <= current_value <= critical_range[1]:
                        score = 1.0
                        matched_indicators.append(f"{indicator_name} (критическое отклонение)")
                    elif warning_range[0] <= current_value <= warning_range[1]:
                        score = 0.6
                        matched_indicators.append(f"{indicator_name} (предупреждение)")
                    elif normal_range[0] <= current_value <= normal_range[1]:
                        score = 0.0
                    else:
                        # Вне нормального диапазона
                        score = 0.8
                        matched_indicators.append(f"{indicator_name} (отклонение)")
                    
                    indicator_scores.append(score * weight)
                    
                    # Квантовая подпись
                    quantum_signature[indicator_name] = float(current_value)
        
        # Анализ симптомов
        matched_symptoms = []
        symptom_score = 0.0
        if patient_symptoms:
            matched_symptoms = [s for s in patient_symptoms if s.lower() in [sym.lower() for sym in pattern.symptoms]]
            symptom_score = len(matched_symptoms) / max(len(pattern.symptoms), 1) * 0.3
        
        # Анализ факторов риска
        risk_factors_present = []
        risk_score = 0.0
        if risk_factors:
            risk_factors_present = [rf for rf in risk_factors if rf.lower() in [r.lower() for r in pattern.risk_factors]]
            risk_score = len(risk_factors_present) / max(len(pattern.risk_factors), 1) * 0.2
        
        # Расчет вероятности
        indicator_probability = sum(indicator_scores) if indicator_scores else 0.0
        total_probability = min(1.0, indicator_probability + symptom_score + risk_score)
        
        # Расчет уверенности
        confidence = min(1.0, (len(matched_indicators) / max(len(pattern.indicators), 1)) * 0.6 +
                            (len(matched_symptoms) / max(len(pattern.symptoms), 1)) * 0.2 +
                            (len(risk_factors_present) / max(len(pattern.risk_factors), 1)) * 0.2)
        
        # Определение уровня срочности
        if total_probability > 0.7:
            urgency_level = "критический"
        elif total_probability > 0.4:
            urgency_level = "высокий"
        elif total_probability > 0.2:
            urgency_level = "средний"
        else:
            urgency_level = "низкий"
        
        # Генерация рекомендаций
        recommendations = self._generate_recommendations(
            pattern=pattern,
            probability=total_probability,
            matched_indicators=matched_indicators,
            matched_symptoms=matched_symptoms,
            risk_factors_present=risk_factors_present
        )
        
        return DiseaseAnalysisResult(
            disease_name=pattern.disease_name,
            disease_code=pattern.disease_code,
            category=pattern.category,
            probability=total_probability,
            confidence=confidence,
            matched_indicators=matched_indicators,
            matched_symptoms=matched_symptoms,
            risk_factors_present=risk_factors_present,
            quantum_signature=quantum_signature,
            recommendations=recommendations,
            urgency_level=urgency_level,
            diagnostic_tests_recommended=pattern.diagnostic_tests
        )
    
    def _generate_recommendations(self,
                                 pattern: DiseasePattern,
                                 probability: float,
                                 matched_indicators: List[str],
                                 matched_symptoms: List[str],
                                 risk_factors_present: List[str]) -> List[str]:
        """Генерация рекомендаций."""
        recommendations = []
        
        if probability > 0.7:
            recommendations.append(f"⚠️ КРИТИЧЕСКО: Немедленно обратитесь к врачу для диагностики {pattern.disease_name}")
            recommendations.append(f"Рекомендуется пройти следующие тесты: {', '.join(pattern.diagnostic_tests[:3])}")
        elif probability > 0.4:
            recommendations.append(f"⚠️ Высокая вероятность наличия признаков {pattern.disease_name}")
            recommendations.append(f"Рекомендуется консультация специалиста и прохождение диагностических тестов")
        elif probability > 0.2:
            recommendations.append(f"⚠️ Обнаружены некоторые признаки, указывающие на возможное наличие {pattern.disease_name}")
            recommendations.append(f"Рекомендуется наблюдение и повторное обследование")
        
        if matched_symptoms:
            recommendations.append(f"Обнаружены симптомы: {', '.join(matched_symptoms[:3])}")
        
        if risk_factors_present:
            recommendations.append(f"Присутствуют факторы риска: {', '.join(risk_factors_present[:3])}")
        
        return recommendations
    
    def get_disease_info(self, disease_code: str) -> Optional[DiseasePattern]:
        """Получить информацию о заболевании."""
        return self.disease_patterns.get(disease_code)
    
    def list_all_diseases(self) -> List[str]:
        """Получить список всех поддерживаемых заболеваний."""
        return list(self.disease_patterns.keys())

#!/usr/bin/env python3
"""
Система базы данных для истории пациентов MQEA.

Автор: Мухаммад Махизода
Таджикский национальный университет
"""

import sqlite3
import json
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import uuid
import os
from dataclasses import dataclass, asdict
from enum import Enum

class DiagnosisStatus(Enum):
    """Статус диагноза."""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    REJECTED = "rejected"
    MONITORING = "monitoring"

class TreatmentStatus(Enum):
    """Статус лечения."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    DISCONTINUED = "discontinued"

@dataclass
class PatientRecord:
    """Запись о пациенте."""
    patient_id: str
    name: str
    age: int
    gender: str
    contact_info: Dict
    medical_history: Dict
    created_at: datetime
    updated_at: datetime
    is_active: bool = True

@dataclass
class MedicalVisit:
    """Медицинский визит."""
    visit_id: str
    patient_id: str
    visit_date: datetime
    symptoms: List[str]
    vital_signs: Dict
    diagnosis: Optional[str] = None
    treatment_plan: Optional[str] = None
    notes: Optional[str] = None
    doctor_name: Optional[str] = None
    status: str = "completed"

@dataclass
class DiagnosisRecord:
    """Запись о диагнозе."""
    diagnosis_id: str
    patient_id: str
    visit_id: str
    condition: str
    severity: str
    confidence: float
    symptoms: List[str]
    risk_factors: List[str]
    treatment_recommendations: List[str]
    created_at: datetime
    status: DiagnosisStatus = DiagnosisStatus.PENDING

@dataclass
class TreatmentRecord:
    """Запись о лечении."""
    treatment_id: str
    patient_id: str
    diagnosis_id: str
    medication: str
    dosage: str
    frequency: str
    duration: str
    start_date: datetime
    end_date: Optional[datetime] = None
    status: TreatmentStatus = TreatmentStatus.NOT_STARTED
    effectiveness: Optional[float] = None

class PatientDatabase:
    """База данных пациентов."""
    
    def __init__(self, db_path: str = "mqea_patients.db"):
        """Инициализация базы данных."""
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Создание таблиц базы данных."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Таблица пациентов
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS patients (
                    patient_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    gender TEXT NOT NULL,
                    contact_info TEXT,
                    medical_history TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1
                )
            """)
            
            # Таблица визитов
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS visits (
                    visit_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    visit_date TIMESTAMP NOT NULL,
                    symptoms TEXT,
                    vital_signs TEXT,
                    diagnosis TEXT,
                    treatment_plan TEXT,
                    notes TEXT,
                    doctor_name TEXT,
                    status TEXT DEFAULT 'completed',
                    FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
                )
            """)
            
            # Таблица диагнозов
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS diagnoses (
                    diagnosis_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    visit_id TEXT NOT NULL,
                    condition TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    symptoms TEXT,
                    risk_factors TEXT,
                    treatment_recommendations TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'pending',
                    FOREIGN KEY (patient_id) REFERENCES patients (patient_id),
                    FOREIGN KEY (visit_id) REFERENCES visits (visit_id)
                )
            """)
            
            # Таблица лечения
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS treatments (
                    treatment_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    diagnosis_id TEXT NOT NULL,
                    medication TEXT NOT NULL,
                    dosage TEXT NOT NULL,
                    frequency TEXT NOT NULL,
                    duration TEXT NOT NULL,
                    start_date TIMESTAMP NOT NULL,
                    end_date TIMESTAMP,
                    status TEXT DEFAULT 'not_started',
                    effectiveness REAL,
                    FOREIGN KEY (patient_id) REFERENCES patients (patient_id),
                    FOREIGN KEY (diagnosis_id) REFERENCES diagnoses (diagnosis_id)
                )
            """)
            
            # Таблица анализов MQEA
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS mqea_analyses (
                    analysis_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    visit_id TEXT NOT NULL,
                    analysis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    quantum_coherence REAL,
                    entanglement_pairs INTEGER,
                    max_entanglement REAL,
                    patterns_detected TEXT,
                    recommendations TEXT,
                    raw_data TEXT,
                    FOREIGN KEY (patient_id) REFERENCES patients (patient_id),
                    FOREIGN KEY (visit_id) REFERENCES visits (visit_id)
                )
            """)
            
            conn.commit()
    
    def add_patient(self, patient: PatientRecord) -> bool:
        """Добавление нового пациента."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO patients 
                    (patient_id, name, age, gender, contact_info, medical_history, created_at, updated_at, is_active)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    patient.patient_id,
                    patient.name,
                    patient.age,
                    patient.gender,
                    json.dumps(patient.contact_info),
                    json.dumps(patient.medical_history),
                    patient.created_at,
                    patient.updated_at,
                    patient.is_active
                ))
                conn.commit()
                return True
        except Exception as e:
            print(f"Ошибка добавления пациента: {e}")
            return False
    
    def get_patient(self, patient_id: str) -> Optional[PatientRecord]:
        """Получение пациента по ID."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM patients WHERE patient_id = ?", (patient_id,))
                row = cursor.fetchone()
                
                if row:
                    return PatientRecord(
                        patient_id=row[0],
                        name=row[1],
                        age=row[2],
                        gender=row[3],
                        contact_info=json.loads(row[4]) if row[4] else {},
                        medical_history=json.loads(row[5]) if row[5] else {},
                        created_at=datetime.fromisoformat(row[6]),
                        updated_at=datetime.fromisoformat(row[7]),
                        is_active=bool(row[8])
                    )
                return None
        except Exception as e:
            print(f"Ошибка получения пациента: {e}")
            return None
    
    def get_all_patients(self) -> List[PatientRecord]:
        """Получение всех пациентов."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM patients WHERE is_active = 1 ORDER BY created_at DESC")
                rows = cursor.fetchall()
                
                patients = []
                for row in rows:
                    patients.append(PatientRecord(
                        patient_id=row[0],
                        name=row[1],
                        age=row[2],
                        gender=row[3],
                        contact_info=json.loads(row[4]) if row[4] else {},
                        medical_history=json.loads(row[5]) if row[5] else {},
                        created_at=datetime.fromisoformat(row[6]),
                        updated_at=datetime.fromisoformat(row[7]),
                        is_active=bool(row[8])
                    ))
                return patients
        except Exception as e:
            print(f"Ошибка получения пациентов: {e}")
            return []

    def update_patient(self, patient_id: str, *, name: Optional[str] = None, age: Optional[int] = None,
                       gender: Optional[str] = None, contact_info: Optional[Dict] = None,
                       medical_history: Optional[Dict] = None, is_active: Optional[bool] = None) -> bool:
        """Обновление данных пациента.

        Обновляет только переданные поля и проставляет updated_at = NOW.
        Возвращает True при успешном обновлении.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                fields = []
                values = []

                if name is not None:
                    fields.append("name = ?")
                    values.append(name)
                if age is not None:
                    fields.append("age = ?")
                    values.append(age)
                if gender is not None:
                    fields.append("gender = ?")
                    values.append(gender)
                if contact_info is not None:
                    fields.append("contact_info = ?")
                    values.append(json.dumps(contact_info))
                if medical_history is not None:
                    fields.append("medical_history = ?")
                    values.append(json.dumps(medical_history))
                if is_active is not None:
                    fields.append("is_active = ?")
                    values.append(1 if is_active else 0)

                # Всегда обновляем updated_at
                fields.append("updated_at = ?")
                values.append(datetime.now())

                if not fields:
                    return True

                set_clause = ", ".join(fields)
                values.append(patient_id)
                cursor.execute(f"UPDATE patients SET {set_clause} WHERE patient_id = ?", tuple(values))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Ошибка обновления пациента: {e}")
            return False

    def delete_patient(self, patient_id: str, *, hard: bool = False) -> bool:
        """Удаление пациента.

        По умолчанию мягкое удаление (is_active = 0). При hard=True удаляет запись из БД.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                if hard:
                    cursor.execute("DELETE FROM patients WHERE patient_id = ?", (patient_id,))
                else:
                    cursor.execute(
                        "UPDATE patients SET is_active = 0, updated_at = ? WHERE patient_id = ?",
                        (datetime.now(), patient_id),
                    )
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Ошибка удаления пациента: {e}")
            return False
    
    def add_visit(self, visit: MedicalVisit) -> bool:
        """Добавление визита."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO visits 
                    (visit_id, patient_id, visit_date, symptoms, vital_signs, diagnosis, 
                     treatment_plan, notes, doctor_name, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    visit.visit_id,
                    visit.patient_id,
                    visit.visit_date,
                    json.dumps(visit.symptoms),
                    json.dumps(visit.vital_signs),
                    visit.diagnosis,
                    visit.treatment_plan,
                    visit.notes,
                    visit.doctor_name,
                    visit.status
                ))
                conn.commit()
                return True
        except Exception as e:
            print(f"Ошибка добавления визита: {e}")
            return False
    
    def get_patient_visits(self, patient_id: str) -> List[MedicalVisit]:
        """Получение визитов пациента."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM visits 
                    WHERE patient_id = ? 
                    ORDER BY visit_date DESC
                """, (patient_id,))
                rows = cursor.fetchall()
                
                visits = []
                for row in rows:
                    visits.append(MedicalVisit(
                        visit_id=row[0],
                        patient_id=row[1],
                        visit_date=datetime.fromisoformat(row[2]),
                        symptoms=json.loads(row[3]) if row[3] else [],
                        vital_signs=json.loads(row[4]) if row[4] else {},
                        diagnosis=row[5],
                        treatment_plan=row[6],
                        notes=row[7],
                        doctor_name=row[8],
                        status=row[9]
                    ))
                return visits
        except Exception as e:
            print(f"Ошибка получения визитов: {e}")
            return []
    
    def add_diagnosis(self, diagnosis: DiagnosisRecord) -> bool:
        """Добавление диагноза."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO diagnoses 
                    (diagnosis_id, patient_id, visit_id, condition, severity, confidence,
                     symptoms, risk_factors, treatment_recommendations, created_at, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    diagnosis.diagnosis_id,
                    diagnosis.patient_id,
                    diagnosis.visit_id,
                    diagnosis.condition,
                    diagnosis.severity,
                    diagnosis.confidence,
                    json.dumps(diagnosis.symptoms),
                    json.dumps(diagnosis.risk_factors),
                    json.dumps(diagnosis.treatment_recommendations),
                    diagnosis.created_at,
                    diagnosis.status.value
                ))
                conn.commit()
                return True
        except Exception as e:
            print(f"Ошибка добавления диагноза: {e}")
            return False
    
    def get_patient_diagnoses(self, patient_id: str) -> List[DiagnosisRecord]:
        """Получение диагнозов пациента."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM diagnoses 
                    WHERE patient_id = ? 
                    ORDER BY created_at DESC
                """, (patient_id,))
                rows = cursor.fetchall()
                
                diagnoses = []
                for row in rows:
                    diagnoses.append(DiagnosisRecord(
                        diagnosis_id=row[0],
                        patient_id=row[1],
                        visit_id=row[2],
                        condition=row[3],
                        severity=row[4],
                        confidence=row[5],
                        symptoms=json.loads(row[6]) if row[6] else [],
                        risk_factors=json.loads(row[7]) if row[7] else [],
                        treatment_recommendations=json.loads(row[8]) if row[8] else [],
                        created_at=datetime.fromisoformat(row[9]),
                        status=DiagnosisStatus(row[10])
                    ))
                return diagnoses
        except Exception as e:
            print(f"Ошибка получения диагнозов: {e}")
            return []
    
    def add_mqea_analysis(self, analysis_data: Dict) -> bool:
        """Добавление анализа MQEA."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO mqea_analyses 
                    (analysis_id, patient_id, visit_id, analysis_date, quantum_coherence,
                     entanglement_pairs, max_entanglement, patterns_detected, recommendations, raw_data)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    analysis_data.get('analysis_id', str(uuid.uuid4())),
                    analysis_data.get('patient_id'),
                    analysis_data.get('visit_id'),
                    analysis_data.get('analysis_date', datetime.now()),
                    analysis_data.get('quantum_coherence', 0.0),
                    analysis_data.get('entanglement_pairs', 0),
                    analysis_data.get('max_entanglement', 0.0),
                    json.dumps(analysis_data.get('patterns_detected', [])),
                    json.dumps(analysis_data.get('recommendations', [])),
                    json.dumps(analysis_data.get('raw_data', {}))
                ))
                conn.commit()
                return True
        except Exception as e:
            print(f"Ошибка добавления анализа MQEA: {e}")
            return False
    
    def get_patient_analyses(self, patient_id: str) -> List[Dict]:
        """Получение анализов MQEA пациента."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM mqea_analyses 
                    WHERE patient_id = ? 
                    ORDER BY analysis_date DESC
                """, (patient_id,))
                rows = cursor.fetchall()
                
                analyses = []
                for row in rows:
                    analyses.append({
                        'analysis_id': row[0],
                        'patient_id': row[1],
                        'visit_id': row[2],
                        'analysis_date': datetime.fromisoformat(row[3]),
                        'quantum_coherence': row[4],
                        'entanglement_pairs': row[5],
                        'max_entanglement': row[6],
                        'patterns_detected': json.loads(row[7]) if row[7] else [],
                        'recommendations': json.loads(row[8]) if row[8] else [],
                        'raw_data': json.loads(row[9]) if row[9] else {}
                    })
                return analyses
        except Exception as e:
            print(f"Ошибка получения анализов: {e}")
            return []
    
    def get_statistics(self) -> Dict:
        """Получение статистики базы данных."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Общее количество пациентов
                cursor.execute("SELECT COUNT(*) FROM patients WHERE is_active = 1")
                total_patients = cursor.fetchone()[0]
                
                # Количество визитов
                cursor.execute("SELECT COUNT(*) FROM visits")
                total_visits = cursor.fetchone()[0]
                
                # Количество диагнозов
                cursor.execute("SELECT COUNT(*) FROM diagnoses")
                total_diagnoses = cursor.fetchone()[0]
                
                # Количество анализов MQEA
                cursor.execute("SELECT COUNT(*) FROM mqea_analyses")
                total_analyses = cursor.fetchone()[0]
                
                # Средняя квантовая когерентность
                cursor.execute("SELECT AVG(quantum_coherence) FROM mqea_analyses")
                avg_coherence = cursor.fetchone()[0] or 0.0
                
                return {
                    'total_patients': total_patients,
                    'total_visits': total_visits,
                    'total_diagnoses': total_diagnoses,
                    'total_analyses': total_analyses,
                    'average_coherence': round(avg_coherence, 3)
                }
        except Exception as e:
            print(f"Ошибка получения статистики: {e}")
            return {}
    
    def search_patients(self, query: str) -> List[PatientRecord]:
        """Поиск пациентов по имени или ID."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM patients 
                    WHERE (name LIKE ? OR patient_id LIKE ?) AND is_active = 1
                    ORDER BY name
                """, (f"%{query}%", f"%{query}%"))
                rows = cursor.fetchall()
                
                patients = []
                for row in rows:
                    patients.append(PatientRecord(
                        patient_id=row[0],
                        name=row[1],
                        age=row[2],
                        gender=row[3],
                        contact_info=json.loads(row[4]) if row[4] else {},
                        medical_history=json.loads(row[5]) if row[5] else {},
                        created_at=datetime.fromisoformat(row[6]),
                        updated_at=datetime.fromisoformat(row[7]),
                        is_active=bool(row[8])
                    ))
                return patients
        except Exception as e:
            print(f"Ошибка поиска пациентов: {e}")
            return []

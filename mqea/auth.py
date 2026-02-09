#!/usr/bin/env python3
"""
Система аутентификации для MQEA.

Автор: Мухаммад Махизода
Таджикский национальный университет
"""

import sqlite3
import json
import uuid
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Tuple, List
from dataclasses import dataclass
from passlib.context import CryptContext
import hashlib

# Контекст для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@dataclass
class User:
    """Пользователь системы."""
    user_id: str
    username: str
    email: str
    password_hash: str
    full_name: str
    role: str = "user"  # user, admin, doctor
    is_active: bool = True
    is_verified: bool = False
    created_at: datetime = None
    last_login: Optional[datetime] = None
    reset_token: Optional[str] = None
    reset_token_expires: Optional[datetime] = None


class AuthManager:
    """Менеджер аутентификации."""
    
    def __init__(self, db_path: str = "mqea_patients.db"):
        """Инициализация менеджера аутентификации."""
        self.db_path = db_path
        self.init_auth_tables()
    
    def init_auth_tables(self):
        """Создание таблиц для аутентификации."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Таблица пользователей
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    full_name TEXT NOT NULL,
                    role TEXT DEFAULT 'user',
                    is_active BOOLEAN DEFAULT 1,
                    is_verified BOOLEAN DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP,
                    reset_token TEXT,
                    reset_token_expires TIMESTAMP
                )
            """)
            
            # Таблица сессий
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_sessions (
                    session_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP NOT NULL,
                    ip_address TEXT,
                    user_agent TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            """)
            
            # Индексы для быстрого поиска
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_username ON users(username)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_email ON users(email)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_reset_token ON users(reset_token)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_session_user ON user_sessions(user_id)
            """)
            
            conn.commit()
    
    def hash_password(self, password: str) -> str:
        """Хеширование пароля."""
        return pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Проверка пароля."""
        return pwd_context.verify(plain_password, hashed_password)
    
    def register_user(
        self,
        username: str,
        email: str,
        password: str,
        full_name: str,
        role: str = "user"
    ) -> Tuple[bool, str]:
        """
        Регистрация нового пользователя.
        
        Returns:
            (success: bool, message: str)
        """
        try:
            # Валидация данных
            if not username or len(username) < 3:
                return False, "Имя пользователя должно содержать минимум 3 символа"
            
            if not email or "@" not in email:
                return False, "Некорректный email адрес"
            
            if not password or len(password) < 6:
                return False, "Пароль должен содержать минимум 6 символов"
            
            # Проверка существования пользователя
            if self.get_user_by_username(username):
                return False, "Пользователь с таким именем уже существует"
            
            if self.get_user_by_email(email):
                return False, "Пользователь с таким email уже существует"
            
            # Создание пользователя
            user_id = str(uuid.uuid4())
            password_hash = self.hash_password(password)
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO users 
                    (user_id, username, email, password_hash, full_name, role, is_active, is_verified, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    user_id,
                    username.lower(),
                    email.lower(),
                    password_hash,
                    full_name,
                    role,
                    True,
                    False,  # Требуется верификация email
                    datetime.now()
                ))
                conn.commit()
            
            return True, "Пользователь успешно зарегистрирован"
            
        except sqlite3.IntegrityError as e:
            return False, f"Ошибка регистрации: пользователь уже существует"
        except Exception as e:
            return False, f"Ошибка регистрации: {str(e)}"
    
    def authenticate_user(self, username: str, password: str) -> Tuple[bool, Optional[User], str]:
        """
        Аутентификация пользователя.
        
        Returns:
            (success: bool, user: User | None, message: str)
        """
        try:
            user = self.get_user_by_username(username)
            
            if not user:
                return False, None, "Неверное имя пользователя или пароль"
            
            if not user.is_active:
                return False, None, "Аккаунт деактивирован"
            
            if not self.verify_password(password, user.password_hash):
                return False, None, "Неверное имя пользователя или пароль"
            
            # Обновление времени последнего входа
            self.update_last_login(user.user_id)
            
            return True, user, "Успешный вход"
            
        except Exception as e:
            return False, None, f"Ошибка аутентификации: {str(e)}"
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Получение пользователя по имени."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM users WHERE username = ? COLLATE NOCASE
                """, (username.lower(),))
                row = cursor.fetchone()
                
                if row:
                    return self._row_to_user(row)
                return None
        except Exception:
            return None
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Получение пользователя по email."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM users WHERE email = ? COLLATE NOCASE
                """, (email.lower(),))
                row = cursor.fetchone()
                
                if row:
                    return self._row_to_user(row)
                return None
        except Exception:
            return None
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Получение пользователя по ID."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
                row = cursor.fetchone()
                
                if row:
                    return self._row_to_user(row)
                return None
        except Exception:
            return None
    
    def _row_to_user(self, row: sqlite3.Row) -> User:
        """Преобразование строки БД в объект User."""
        return User(
            user_id=row['user_id'],
            username=row['username'],
            email=row['email'],
            password_hash=row['password_hash'],
            full_name=row['full_name'],
            role=row['role'],
            is_active=bool(row['is_active']),
            is_verified=bool(row['is_verified']),
            created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None,
            last_login=datetime.fromisoformat(row['last_login']) if row['last_login'] else None,
            reset_token=row['reset_token'],
            reset_token_expires=datetime.fromisoformat(row['reset_token_expires']) if row['reset_token_expires'] else None
        )
    
    def update_last_login(self, user_id: str):
        """Обновление времени последнего входа."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE users SET last_login = ? WHERE user_id = ?
                """, (datetime.now(), user_id))
                conn.commit()
        except Exception:
            pass
    
    def create_reset_token(self, email: str) -> Tuple[bool, Optional[str], str]:
        """
        Создание токена для восстановления пароля.
        
        Returns:
            (success: bool, token: str | None, message: str)
        """
        try:
            user = self.get_user_by_email(email)
            
            if not user:
                # Не раскрываем, существует ли пользователь
                return True, None, "Если email существует, инструкция отправлена"
            
            # Генерация токена
            token = secrets.token_urlsafe(32)
            expires_at = datetime.now() + timedelta(hours=1)  # Токен действителен 1 час
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE users 
                    SET reset_token = ?, reset_token_expires = ?
                    WHERE user_id = ?
                """, (token, expires_at, user.user_id))
                conn.commit()
            
            return True, token, "Токен восстановления создан"
            
        except Exception as e:
            return False, None, f"Ошибка создания токена: {str(e)}"
    
    def verify_reset_token(self, token: str) -> Tuple[bool, Optional[User], str]:
        """
        Проверка токена восстановления пароля.
        
        Returns:
            (valid: bool, user: User | None, message: str)
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM users 
                    WHERE reset_token = ? AND reset_token_expires > ?
                """, (token, datetime.now()))
                row = cursor.fetchone()
                
                if row:
                    user = self._row_to_user(row)
                    return True, user, "Токен действителен"
                else:
                    return False, None, "Токен недействителен или истек"
                    
        except Exception as e:
            return False, None, f"Ошибка проверки токена: {str(e)}"
    
    def reset_password(self, token: str, new_password: str) -> Tuple[bool, str]:
        """
        Сброс пароля по токену.
        
        Returns:
            (success: bool, message: str)
        """
        try:
            if not new_password or len(new_password) < 6:
                return False, "Пароль должен содержать минимум 6 символов"
            
            valid, user, message = self.verify_reset_token(token)
            
            if not valid or not user:
                return False, message
            
            # Хеширование нового пароля
            password_hash = self.hash_password(new_password)
            
            # Обновление пароля и очистка токена
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE users 
                    SET password_hash = ?, reset_token = NULL, reset_token_expires = NULL
                    WHERE user_id = ?
                """, (password_hash, user.user_id))
                conn.commit()
            
            return True, "Пароль успешно изменен"
            
        except Exception as e:
            return False, f"Ошибка сброса пароля: {str(e)}"
    
    def change_password(self, user_id: str, old_password: str, new_password: str) -> Tuple[bool, str]:
        """
        Изменение пароля пользователя.
        
        Returns:
            (success: bool, message: str)
        """
        try:
            user = self.get_user_by_id(user_id)
            
            if not user:
                return False, "Пользователь не найден"
            
            if not self.verify_password(old_password, user.password_hash):
                return False, "Неверный текущий пароль"
            
            if not new_password or len(new_password) < 6:
                return False, "Пароль должен содержать минимум 6 символов"
            
            password_hash = self.hash_password(new_password)
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE users SET password_hash = ? WHERE user_id = ?
                """, (password_hash, user_id))
                conn.commit()
            
            return True, "Пароль успешно изменен"
            
        except Exception as e:
            return False, f"Ошибка изменения пароля: {str(e)}"
    
    def create_session(self, user_id: str, ip_address: str = None, user_agent: str = None) -> str:
        """Создание сессии пользователя."""
        try:
            session_id = str(uuid.uuid4())
            expires_at = datetime.now() + timedelta(days=30)  # Сессия на 30 дней
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO user_sessions 
                    (session_id, user_id, expires_at, ip_address, user_agent)
                    VALUES (?, ?, ?, ?, ?)
                """, (session_id, user_id, expires_at, ip_address, user_agent))
                conn.commit()
            
            return session_id
        except Exception:
            return ""
    
    def get_session(self, session_id: str) -> Optional[User]:
        """Получение пользователя по ID сессии."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT u.* FROM users u
                    INNER JOIN user_sessions s ON u.user_id = s.user_id
                    WHERE s.session_id = ? AND s.expires_at > ? AND u.is_active = 1
                """, (session_id, datetime.now()))
                row = cursor.fetchone()
                
                if row:
                    return self._row_to_user(row)
                return None
        except Exception:
            return None
    
    def delete_session(self, session_id: str):
        """Удаление сессии."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM user_sessions WHERE session_id = ?", (session_id,))
                conn.commit()
        except Exception:
            pass
    
    def get_all_users(self) -> List[User]:
        """Получение всех пользователей."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users ORDER BY created_at DESC")
                rows = cursor.fetchall()
                
                return [self._row_to_user(row) for row in rows]
        except Exception:
            return []
    
    def update_user_role(self, user_id: str, new_role: str) -> Tuple[bool, str]:
        """
        Изменение роли пользователя.
        
        Returns:
            (success: bool, message: str)
        """
        try:
            valid_roles = ['user', 'doctor', 'admin']
            if new_role not in valid_roles:
                return False, f"Некорректная роль. Допустимые: {', '.join(valid_roles)}"
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE users SET role = ? WHERE user_id = ?
                """, (new_role, user_id))
                conn.commit()
            
            return True, f"Роль успешно изменена на {new_role}"
        except Exception as e:
            return False, f"Ошибка изменения роли: {str(e)}"
    
    def update_user_status(self, user_id: str, is_active: bool) -> Tuple[bool, str]:
        """
        Изменение статуса активности пользователя.
        
        Returns:
            (success: bool, message: str)
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE users SET is_active = ? WHERE user_id = ?
                """, (is_active, user_id))
                conn.commit()
            
            status = "активирован" if is_active else "деактивирован"
            return True, f"Пользователь успешно {status}"
        except Exception as e:
            return False, f"Ошибка изменения статуса: {str(e)}"
    
    def create_doctor(
        self,
        username: str,
        email: str,
        password: str,
        full_name: str
    ) -> Tuple[bool, str]:
        """
        Создание нового доктора администратором.
        
        Returns:
            (success: bool, message: str)
        """
        return self.register_user(
            username=username,
            email=email,
            password=password,
            full_name=full_name,
            role="doctor"
        )
    
    def delete_user(self, user_id: str) -> Tuple[bool, str]:
        """
        Удаление пользователя (деактивация).
        
        Returns:
            (success: bool, message: str)
        """
        try:
            # Вместо физического удаления деактивируем пользователя
            return self.update_user_status(user_id, False)
        except Exception as e:
            return False, f"Ошибка удаления пользователя: {str(e)}"

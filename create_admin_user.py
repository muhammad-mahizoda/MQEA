#!/usr/bin/env python3
"""
Скрипт для создания администратора в базе данных PostgreSQL.

Автор: Мухаммад Махизода
Таджикский национальный университет
"""

import sys
import uuid
from datetime import datetime
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
import hashlib

# Попытка использовать bcrypt, если не работает - используем альтернативу
try:
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    USE_BCRYPT = True
except Exception as e:
    print(f"⚠️  Предупреждение: bcrypt недоступен ({e}), будет использован SHA256")
    USE_BCRYPT = False

def hash_password(password: str) -> str:
    """Хеширование пароля."""
    if USE_BCRYPT:
        try:
            # Ограничиваем длину пароля до 72 байт для bcrypt
            if len(password.encode('utf-8')) > 72:
                password = password[:72]
                print(f"⚠️  Пароль обрезан до 72 байт")
            return pwd_context.hash(password)
        except Exception as e:
            print(f"⚠️  Ошибка bcrypt: {e}, используется SHA256")
            # Fallback на SHA256
            return hashlib.sha256(password.encode('utf-8')).hexdigest()
    else:
        # Используем SHA256 как альтернативу
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

def get_db_connection():
    """Получить подключение к базе данных."""
    # Попробуем несколько способов подключения
    
    # Способ 1: Из переменной окружения DATABASE_URL
    db_url = os.getenv('DATABASE_URL')
    if db_url and 'postgresql://' in db_url:
        try:
            return psycopg2.connect(db_url)
        except Exception as e:
            print(f"⚠️  Не удалось подключиться через DATABASE_URL: {e}")
    
    # Способ 2: Через пользователя postgres с паролем из переменной окружения
    postgres_password = os.getenv('POSTGRES_PASSWORD')
    if postgres_password:
        try:
            conn = psycopg2.connect(
                host='localhost',
                database='mqea_db',
                user='postgres',
                password=postgres_password
            )
            return conn
        except Exception as e:
            print(f"⚠️  Не удалось подключиться с POSTGRES_PASSWORD: {e}")
    
    # Способ 3: Через пользователя mqea_user с паролем
    mqea_password = os.getenv('MQEA_DB_PASSWORD', os.getenv('DB_PASSWORD'))
    if mqea_password:
        try:
            conn = psycopg2.connect(
                host='localhost',
                database='mqea_db',
                user='mqea_user',
                password=mqea_password
            )
            return conn
        except Exception as e:
            print(f"⚠️  Не удалось подключиться с mqea_user: {e}")
    
    # Способ 4: Запросить пароль интерактивно
    print("\n📝 Требуется пароль для подключения к PostgreSQL")
    print("Выберите пользователя:")
    print("1. postgres (суперпользователь)")
    print("2. mqea_user (пользователь БД)")
    choice = input("Выберите (1 или 2, по умолчанию 1): ").strip() or "1"
    
    user = 'postgres' if choice == "1" else 'mqea_user'
    password = input(f"Введите пароль для пользователя {user}: ").strip()
    
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='mqea_db',
            user=user,
            password=password
        )
        return conn
    except Exception as e:
        print(f"❌ Ошибка подключения к базе данных: {e}")
        print("\n💡 Возможные решения:")
        print("1. Установите переменную окружения: export POSTGRES_PASSWORD='ваш_пароль'")
        print("2. Или установите: export DATABASE_URL='postgresql://postgres:пароль@localhost/mqea_db'")
        print("3. Или используйте sudo -u postgres psql для создания пользователя через SQL")
        sys.exit(1)

def create_user(username, email, password, full_name, role='admin'):
    """Создать пользователя в базе данных."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Генерируем user_id
        user_id = str(uuid.uuid4())
        
        # Хешируем пароль
        password_hash = hash_password(password)
        
        # Проверяем, существует ли пользователь
        cursor.execute("SELECT user_id FROM users WHERE username = %s OR email = %s", (username, email))
        existing = cursor.fetchone()
        
        if existing:
            print(f"❌ Пользователь с username '{username}' или email '{email}' уже существует!")
            conn.close()
            return False
        
        # Создаем пользователя
        cursor.execute("""
            INSERT INTO users 
            (user_id, username, email, password_hash, full_name, role, is_active, is_verified, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            user_id,
            username.lower(),
            email.lower(),
            password_hash,
            full_name,
            role,
            True,  # is_active
            True,  # is_verified (для админа автоматически)
            datetime.now()
        ))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"✅ Пользователь '{username}' успешно создан!")
        print(f"   User ID: {user_id}")
        print(f"   Email: {email}")
        print(f"   Роль: {role}")
        print(f"   Полное имя: {full_name}")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка создания пользователя: {e}")
        if conn:
            conn.close()
        return False

def main():
    """Основная функция."""
    print("=" * 70)
    print("🔧 СОЗДАНИЕ АДМИНИСТРАТОРА В БАЗЕ ДАННЫХ MQEA")
    print("=" * 70)
    
    # Получаем данные от пользователя
    print("\nВведите данные администратора:")
    username = input("Username (имя пользователя): ").strip()
    email = input("Email: ").strip()
    password = input("Password (пароль): ").strip()
    full_name = input("Full Name (полное имя): ").strip()
    
    if not username or not email or not password or not full_name:
        print("❌ Все поля обязательны!")
        sys.exit(1)
    
    # Создаем пользователя
    if create_user(username, email, password, full_name, role='admin'):
        print("\n✅ Администратор успешно создан!")
        print("\nВы можете войти в систему используя:")
        print(f"   Username: {username}")
        print(f"   Password: {password}")
    else:
        print("\n❌ Не удалось создать администратора!")
        sys.exit(1)

if __name__ == "__main__":
    main()

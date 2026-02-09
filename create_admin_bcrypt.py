#!/usr/bin/env python3
"""
Скрипт для создания администратора в PostgreSQL с правильным bcrypt хешем.

Автор: Мухаммад Махизода
Таджикский национальный университет
"""

import sys
import uuid
import subprocess
from datetime import datetime

def hash_password_bcrypt(password: str) -> str:
    """Хеширование пароля через bcrypt."""
    try:
        import bcrypt
        # Генерируем соль и хешируем пароль
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
        return password_hash
    except ImportError:
        print("❌ bcrypt не установлен!")
        print("Установите: pip install bcrypt")
        sys.exit(1)

def main():
    print("=" * 70)
    print("🔧 СОЗДАНИЕ АДМИНИСТРАТОРА С BCRYPT ХЕШЕМ")
    print("=" * 70)
    
    # Получаем данные
    print("\nВведите данные администратора:")
    username = input("Username: ").strip()
    email = input("Email: ").strip()
    password = input("Password: ").strip()
    full_name = input("Full Name: ").strip()
    
    if not all([username, email, password, full_name]):
        print("❌ Все поля обязательны!")
        sys.exit(1)
    
    # Генерируем user_id и хеш пароля
    user_id = str(uuid.uuid4())
    password_hash = hash_password_bcrypt(password)
    
    print(f"\n📋 Генерируем хеш пароля...")
    print(f"   User ID: {user_id}")
    print(f"   Username: {username.lower()}")
    print(f"   Email: {email.lower()}")
    
    # Создаем SQL команду
    sql = f"""
INSERT INTO users 
(user_id, username, email, password_hash, full_name, role, is_active, is_verified, created_at)
VALUES 
('{user_id}', '{username.lower()}', '{email.lower()}', '{password_hash.replace("'", "''")}', '{full_name.replace("'", "''")}', 'admin', TRUE, TRUE, '{datetime.now()}')
ON CONFLICT (username) DO UPDATE 
SET password_hash = EXCLUDED.password_hash,
    email = EXCLUDED.email,
    full_name = EXCLUDED.full_name,
    role = 'admin',
    is_active = TRUE;
"""
    
    print(f"\n📤 Выполняю SQL команду через PostgreSQL...")
    
    # Выполняем через sudo -u postgres psql
    try:
        result = subprocess.run(
            ['sudo', '-u', 'postgres', 'psql', 'mqea_db', '-c', sql],
            capture_output=True,
            text=True,
            check=True
        )
        
        print("✅ Пользователь успешно создан/обновлен!")
        print(f"\n📋 Данные для входа:")
        print(f"   Username: {username}")
        print(f"   Password: {password}")
        print(f"   Email: {email}")
        print(f"   Роль: admin")
        
    except subprocess.CalledProcessError as e:
        if "duplicate key" in e.stderr.lower() or "already exists" in e.stderr.lower():
            print("✅ Пользователь обновлен!")
            print(f"\n📋 Данные для входа:")
            print(f"   Username: {username}")
            print(f"   Password: {password}")
        else:
            print(f"❌ Ошибка создания пользователя: {e.stderr}")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

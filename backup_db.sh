#!/bin/bash
# Скрипт резервного копирования базы данных PostgreSQL

set -e

# Настройки
DB_NAME="mqea_db"
DB_USER="mqea_user"
BACKUP_DIR="/home/mqea/edino/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/mqea_db_backup_$DATE.sql.gz"
RETENTION_DAYS=30

# Создание директории для бэкапов
mkdir -p $BACKUP_DIR

# Резервное копирование
echo "Создание резервной копии базы данных $DB_NAME..."
PGPASSWORD=$(grep -oP 'DB_PASSWORD=\K[^ ]+' /root/mqea_db_password.txt 2>/dev/null || echo "")

if [ -z "$PGPASSWORD" ]; then
    echo "Ошибка: Пароль БД не найден. Используйте переменную окружения PGPASSWORD."
    exit 1
fi

export PGPASSWORD
pg_dump -U $DB_USER -h localhost $DB_NAME | gzip > $BACKUP_FILE

# Проверка успешности
if [ $? -eq 0 ]; then
    echo "Резервная копия создана: $BACKUP_FILE"
    
    # Удаление старых бэкапов
    find $BACKUP_DIR -name "mqea_db_backup_*.sql.gz" -mtime +$RETENTION_DAYS -delete
    echo "Старые резервные копии (старше $RETENTION_DAYS дней) удалены"
else
    echo "Ошибка при создании резервной копии!"
    exit 1
fi

# Опционально: отправка на удаленное хранилище
# rsync -avz $BACKUP_FILE user@remote-server:/backups/mqea/



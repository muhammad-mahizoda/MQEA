#!/bin/bash
# Скрипт автоматического развертывания MQEA на Ubuntu 22.04

set -e

echo "=========================================="
echo "Развертывание MQEA на Ubuntu 22.04"
echo "=========================================="

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Проверка прав root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}Пожалуйста, запустите скрипт с правами sudo${NC}"
    exit 1
fi

# Переменные
APP_USER="mqea"
APP_DIR="/home/$APP_USER/edino"
DB_NAME="mqea_db"
DB_USER="mqea_user"

echo -e "${GREEN}[1/10] Обновление системы...${NC}"
apt update
apt upgrade -y

echo -e "${GREEN}[2/10] Установка необходимых пакетов...${NC}"
apt install -y python3.11 python3.11-venv python3-pip nginx postgresql postgresql-contrib git curl ufw

echo -e "${GREEN}[3/10] Создание пользователя приложения...${NC}"
if ! id "$APP_USER" &>/dev/null; then
    adduser --disabled-password --gecos "" $APP_USER
    usermod -aG sudo $APP_USER
    echo -e "${GREEN}Пользователь $APP_USER создан${NC}"
else
    echo -e "${YELLOW}Пользователь $APP_USER уже существует${NC}"
fi

echo -e "${GREEN}[4/10] Настройка PostgreSQL...${NC}"
# Генерация пароля БД
DB_PASSWORD=$(openssl rand -base64 32 | tr -d "=+/" | cut -c1-25)
echo "Пароль БД: $DB_PASSWORD" > /root/mqea_db_password.txt
chmod 600 /root/mqea_db_password.txt

sudo -u postgres psql <<EOF
CREATE DATABASE $DB_NAME;
CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
ALTER ROLE $DB_USER SET client_encoding TO 'utf8';
ALTER ROLE $DB_USER SET default_transaction_isolation TO 'read committed';
ALTER ROLE $DB_USER SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
\q
EOF

echo -e "${GREEN}[5/10] Настройка директорий...${NC}"
mkdir -p $APP_DIR
mkdir -p $APP_DIR/logs
mkdir -p $APP_DIR/staticfiles
mkdir -p $APP_DIR/media
chown -R $APP_USER:$APP_USER $APP_DIR

echo -e "${YELLOW}[6/10] ВАЖНО: Скопируйте файлы проекта в $APP_DIR${NC}"
echo -e "${YELLOW}Вы можете использовать:${NC}"
echo -e "${YELLOW}  - git clone${NC}"
echo -e "${YELLOW}  - scp/rsync${NC}"
echo -e "${YELLOW}  - или скопируйте вручную${NC}"
read -p "Нажмите Enter после копирования файлов..."

echo -e "${GREEN}[7/10] Настройка виртуального окружения...${NC}"
sudo -u $APP_USER bash <<EOF
cd $APP_DIR
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
else
    echo -e "${YELLOW}requirements.txt не найден, устанавливаю базовые пакеты...${NC}"
    pip install streamlit gunicorn psycopg2-binary sqlalchemy pandas numpy
fi
pip install gunicorn
EOF

echo -e "${GREEN}[8/10] Создание systemd сервиса...${NC}"
cat > /etc/systemd/system/mqea.service <<EOF
[Unit]
Description=MQEA Gunicorn daemon
After=network.target postgresql.service

[Service]
User=$APP_USER
Group=$APP_USER
WorkingDirectory=$APP_DIR
Environment="PATH=$APP_DIR/venv/bin"
ExecStart=$APP_DIR/venv/bin/gunicorn \\
    --workers 3 \\
    --bind 127.0.0.1:8000 \\
    --timeout 120 \\
    --access-logfile $APP_DIR/logs/access.log \\
    --error-logfile $APP_DIR/logs/error.log \\
    webapp.modern_medical_app:app

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable mqea

echo -e "${GREEN}[9/10] Настройка Nginx...${NC}"
read -p "Введите доменное имя (или IP адрес): " DOMAIN_NAME

cat > /etc/nginx/sites-available/mqea <<EOF
server {
    listen 80;
    server_name $DOMAIN_NAME;

    client_max_body_size 100M;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_redirect off;
    }

    location /static/ {
        alias $APP_DIR/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias $APP_DIR/media/;
    }
}
EOF

ln -sf /etc/nginx/sites-available/mqea /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl restart nginx

echo -e "${GREEN}[10/10] Настройка файрвола...${NC}"
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable

echo -e "${GREEN}=========================================="
echo "Развертывание завершено!"
echo "=========================================="
echo -e "${YELLOW}Важная информация:${NC}"
echo "Пароль БД сохранен в: /root/mqea_db_password.txt"
echo "Доменное имя: $DOMAIN_NAME"
echo ""
echo -e "${GREEN}Следующие шаги:${NC}"
echo "1. Настройте config.py с правильными параметрами БД"
echo "2. Запустите: sudo systemctl start mqea"
echo "3. Проверьте статус: sudo systemctl status mqea"
echo "4. Для SSL: sudo certbot --nginx -d $DOMAIN_NAME"
echo ""
echo -e "${YELLOW}Проверка логов:${NC}"
echo "sudo journalctl -u mqea -f"
echo "tail -f $APP_DIR/logs/error.log"
echo "=========================================="



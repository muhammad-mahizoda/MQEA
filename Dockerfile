# MQEA - Medical Quantum Entanglement Analysis
# Автор: Мухаммад Махизода
# Таджикский национальный университет

FROM python:3.11-slim

# Метаданные
LABEL maintainer="muhammad.mahizoda@tnu.tj"
LABEL description="MQEA - Medical Quantum Entanglement Analysis"
LABEL version="1.0.0"
LABEL founder="Мухаммад Махизода"
LABEL university="Таджикский национальный университет"

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    gfortran \
    libopenblas-dev \
    liblapack-dev \
    libhdf5-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Создание пользователя для безопасности
RUN useradd --create-home --shell /bin/bash mqea

# Установка рабочей директории
WORKDIR /app

# Копирование файлов зависимостей
COPY requirements.txt .

# Установка Python зависимостей
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода
COPY . .

# Создание необходимых директорий
RUN mkdir -p /app/data /app/logs /app/temp && \
    chown -R mqea:mqea /app

# Переключение на пользователя mqea
USER mqea

# Переменные окружения
ENV PYTHONPATH=/app
ENV MQEA_ENVIRONMENT=production
ENV MQEA_DEBUG=false

# Открытие портов
EXPOSE 8000 9090

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Команда по умолчанию
CMD ["python", "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]

"""
FastAPI веб-сервер для MQEA.

Автор: Мухаммад Махизода
Таджикский национальный университет
"""

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import time
import asyncio
from datetime import datetime
from typing import List, Optional
import uuid
import os
from pathlib import Path

from config import get_settings, settings
from models.schemas import (
    QuantumAnalysisRequestSchema,
    QuantumAnalysisResultSchema,
    ImputationRequestSchema,
    ImputationResultSchema,
    PatternDetectionRequestSchema,
    PatternDetectionResultSchema,
    HealthCheckSchema,
    ErrorResponseSchema,
    SuccessResponseSchema,
    AnalysisJobSchema
)
from services.quantum_service import QuantumAnalysisService
from services.imputation_service import ImputationService
from services.pattern_service import PatternDetectionService
from utils.logging import get_logger
from utils.monitoring import setup_monitoring

# Инициализация логгера
logger = get_logger(__name__)

# Создание FastAPI приложения
app = FastAPI(
    title=settings.api.title,
    description=settings.api.description,
    version=settings.api.version,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.api.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Настройка доверенных хостов
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"] if settings.debug else ["localhost", "127.0.0.1"]
)

# Подключение статических файлов
if settings.debug:
    app.mount("/static", StaticFiles(directory="webapp/static"), name="static")

# Инициализация сервисов
quantum_service = QuantumAnalysisService()
imputation_service = ImputationService()
pattern_service = PatternDetectionService()

# Хранилище задач
analysis_jobs: dict[str, AnalysisJobSchema] = {}


@app.on_event("startup")
async def startup_event():
    """Инициализация при запуске."""
    logger.info("Запуск MQEA API сервера...")
    
    # Настройка мониторинга
    if settings.monitoring.enabled:
        setup_monitoring()
    
    # Создание необходимых директорий
    settings.data_dir.mkdir(exist_ok=True)
    settings.logs_dir.mkdir(exist_ok=True)
    settings.temp_dir.mkdir(exist_ok=True)
    
    logger.info("MQEA API сервер успешно запущен")


@app.on_event("shutdown")
async def shutdown_event():
    """Очистка при завершении."""
    logger.info("Завершение работы MQEA API сервера...")


@app.get("/", response_model=SuccessResponseSchema)
async def root():
    """Корневой эндпоинт."""
    return SuccessResponseSchema(
        message="Добро пожаловать в MQEA API!",
        data={
            "version": settings.api.version,
            "founder": "Мухаммад Махизода",
            "university": "Таджикский национальный университет",
            "docs": "/docs" if settings.debug else "Документация недоступна в production"
        }
    )


@app.get("/health", response_model=HealthCheckSchema)
async def health_check():
    """Проверка здоровья системы."""
    import psutil
    
    return HealthCheckSchema(
        status="healthy",
        version=settings.api.version,
        uptime=time.time() - start_time,
        quantum_engine_status="active",
        database_status="connected",
        redis_status="connected",
        memory_usage={
            "total": psutil.virtual_memory().total,
            "available": psutil.virtual_memory().available,
            "percent": psutil.virtual_memory().percent
        },
        cpu_usage=psutil.cpu_percent()
    )


@app.post("/api/v1/quantum/analyze", response_model=QuantumAnalysisResultSchema)
async def analyze_quantum_entanglement(
    request: QuantumAnalysisRequestSchema,
    background_tasks: BackgroundTasks
):
    """Выполнить квантовый анализ запутанности."""
    try:
        logger.info("Начало квантового анализа запутанности")
        
        start_time = time.time()
        
        # Выполнение анализа
        result = await quantum_service.analyze_entanglement(
            time_series=request.time_series,
            quantum_threshold=request.quantum_threshold,
            time_windows=request.time_windows,
            enable_pattern_detection=request.enable_pattern_detection,
            enable_quantum_imputation=request.enable_quantum_imputation
        )
        
        analysis_duration = time.time() - start_time
        
        logger.info(f"Квантовый анализ завершен за {analysis_duration:.2f} секунд")
        
        return QuantumAnalysisResultSchema(
            **result,
            analysis_duration=analysis_duration
        )
        
    except Exception as e:
        logger.error(f"Ошибка при квантовом анализе: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/imputation/fill", response_model=ImputationResultSchema)
async def fill_missing_data(request: ImputationRequestSchema):
    """Заполнить пропущенные данные."""
    try:
        logger.info("Начало заполнения пропущенных данных")
        
        start_time = time.time()
        
        # Выполнение заполнения
        result = await imputation_service.fill_missing_data(
            time_series=request.time_series,
            method=request.method,
            max_iterations=request.max_iterations
        )
        
        processing_time = time.time() - start_time
        
        logger.info(f"Заполнение данных завершено за {processing_time:.2f} секунд")
        
        return ImputationResultSchema(
            **result,
            processing_time=processing_time
        )
        
    except Exception as e:
        logger.error(f"Ошибка при заполнении данных: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/patterns/detect", response_model=PatternDetectionResultSchema)
async def detect_patterns(request: PatternDetectionRequestSchema):
    """Обнаружить паттерны в данных."""
    try:
        logger.info("Начало обнаружения паттернов")
        
        start_time = time.time()
        
        # Выполнение обнаружения паттернов
        result = await pattern_service.detect_patterns(
            time_series=request.time_series,
            pattern_types=request.pattern_types,
            min_pattern_length=request.min_pattern_length,
            quantum_threshold=request.quantum_threshold
        )
        
        processing_time = time.time() - start_time
        
        logger.info(f"Обнаружение паттернов завершено за {processing_time:.2f} секунд")
        
        return PatternDetectionResultSchema(
            **result,
            processing_time=processing_time
        )
        
    except Exception as e:
        logger.error(f"Ошибка при обнаружении паттернов: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/upload", response_model=SuccessResponseSchema)
async def upload_file(file: UploadFile = File(...)):
    """Загрузить файл с медицинскими данными."""
    try:
        # Проверка размера файла
        if file.size > settings.max_file_size:
            raise HTTPException(
                status_code=413,
                detail=f"Файл слишком большой. Максимальный размер: {settings.max_file_size} байт"
            )
        
        # Проверка типа файла
        if not file.filename.endswith(('.csv', '.xlsx', '.json')):
            raise HTTPException(
                status_code=400,
                detail="Поддерживаются только файлы CSV, XLSX и JSON"
            )
        
        # Сохранение файла
        file_path = settings.temp_dir / f"{uuid.uuid4()}_{file.filename}"
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        logger.info(f"Файл {file.filename} успешно загружен")
        
        return SuccessResponseSchema(
            message="Файл успешно загружен",
            data={
                "filename": file.filename,
                "file_id": str(uuid.uuid4()),
                "file_path": str(file_path),
                "size": file.size
            }
        )
        
    except Exception as e:
        logger.error(f"Ошибка при загрузке файла: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/analysis/start", response_model=AnalysisJobSchema)
async def start_analysis_job(
    request: QuantumAnalysisRequestSchema,
    background_tasks: BackgroundTasks
):
    """Запустить фоновую задачу анализа."""
    job_id = str(uuid.uuid4())
    
    job = AnalysisJobSchema(
        job_id=job_id,
        status="queued",
        progress=0
    )
    
    analysis_jobs[job_id] = job
    
    # Запуск фоновой задачи
    background_tasks.add_task(
        run_analysis_job,
        job_id,
        request
    )
    
    logger.info(f"Запущена задача анализа {job_id}")
    
    return job


@app.get("/api/v1/analysis/{job_id}", response_model=AnalysisJobSchema)
async def get_analysis_job(job_id: str):
    """Получить статус задачи анализа."""
    if job_id not in analysis_jobs:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    
    return analysis_jobs[job_id]


async def run_analysis_job(job_id: str, request: QuantumAnalysisRequestSchema):
    """Выполнить задачу анализа в фоне."""
    try:
        job = analysis_jobs[job_id]
        job.status = "running"
        job.started_at = datetime.now()
        job.progress = 10
        
        # Выполнение анализа
        result = await quantum_service.analyze_entanglement(
            time_series=request.time_series,
            quantum_threshold=request.quantum_threshold,
            time_windows=request.time_windows,
            enable_pattern_detection=request.enable_pattern_detection,
            enable_quantum_imputation=request.enable_quantum_imputation
        )
        
        job.progress = 100
        job.status = "completed"
        job.completed_at = datetime.now()
        job.result = result
        
        logger.info(f"Задача анализа {job_id} завершена успешно")
        
    except Exception as e:
        job = analysis_jobs[job_id]
        job.status = "failed"
        job.error = str(e)
        job.completed_at = datetime.now()
        
        logger.error(f"Ошибка в задаче анализа {job_id}: {str(e)}")


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Обработчик HTTP исключений."""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponseSchema(
            error="HTTP Error",
            message=exc.detail,
            details={"status_code": exc.status_code}
        ).dict()
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Обработчик общих исключений."""
    logger.error(f"Необработанная ошибка: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content=ErrorResponseSchema(
            error="Internal Server Error",
            message="Произошла внутренняя ошибка сервера",
            details={"error_type": type(exc).__name__}
        ).dict()
    )


# Глобальная переменная для времени запуска
start_time = time.time()


if __name__ == "__main__":
    uvicorn.run(
        "api.main:app",
        host=settings.api.host,
        port=settings.api.port,
        reload=settings.debug,
        log_level=settings.logging.level.lower()
    )

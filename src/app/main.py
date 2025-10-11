from fastapi import FastAPI, Request
from prometheus_fastapi_instrumentator import Instrumentator
from src.app.lifespan import lifespan
from src.app.dependencies.db_session import get_db_session
from src.app.routers.order_router import router as order_router
from src.app.routers.health_router import router as health_router
from src.app.core.metrics import metrics

app = FastAPI(
    title="Order API",
    description="API для заказов",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

app.include_router(order_router)
app.include_router(health_router)

# Инициализация Prometheus instrumentator
instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

# Эндпоинт для метрик
@app.get("/metrics")
async def get_metrics():
    """Эндпоинт для получения метрик Prometheus"""
    return metrics.get_metrics()

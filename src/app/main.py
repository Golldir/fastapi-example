from fastapi import FastAPI, Request
from prometheus_fastapi_instrumentator import Instrumentator
from src.app.lifespan import lifespan
from src.app.routers.order_router import router as order_router
from src.app.routers.metric_router import router as metric_router

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
app.include_router(metric_router)

# Инициализация Prometheus instrumentator
instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

# Примечание: метрики экспонируются через Instrumentator на /metrics

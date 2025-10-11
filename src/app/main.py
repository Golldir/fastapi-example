from fastapi import FastAPI, Request
from src.app.lifespan import lifespan
from src.app.dependencies.db_session import get_db_session
from src.app.routers.order_router import router as order_router

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

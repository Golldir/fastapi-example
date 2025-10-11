from fastapi import APIRouter, Request
from typing import Dict, Any

router = APIRouter()


@router.get("/health")
async def health_check(request: Request) -> Dict[str, Any]:
    """Health check эндпоинт для проверки состояния приложения"""
    
    # Получаем состояние из app.state
    database = getattr(request.app.state, 'database', None)
    redis = getattr(request.app.state, 'redis', None)
    
    health_status = {
        "status": "healthy",
        "timestamp": None,
        "services": {}
    }
    
    # Проверяем подключение к базе данных
    if database:
        try:
            db_connected = await database.check_connection()
            health_status["services"]["database"] = {
                "status": "healthy" if db_connected else "unhealthy",
                "connected": db_connected
            }
        except Exception as e:
            health_status["services"]["database"] = {
                "status": "unhealthy",
                "error": str(e),
                "connected": False
            }
    else:
        health_status["services"]["database"] = {
            "status": "unavailable",
            "connected": False
        }
    
    # Проверяем подключение к Redis
    if redis:
        try:
            redis_connected = await redis.check_connection()
            health_status["services"]["redis"] = {
                "status": "healthy" if redis_connected else "unhealthy",
                "connected": redis_connected
            }
        except Exception as e:
            health_status["services"]["redis"] = {
                "status": "unhealthy",
                "error": str(e),
                "connected": False
            }
    else:
        health_status["services"]["redis"] = {
            "status": "unavailable",
            "connected": False
        }
    
    # Общий статус приложения
    all_healthy = all(
        service.get("status") == "healthy" 
        for service in health_status["services"].values()
    )
    
    if not all_healthy:
        health_status["status"] = "degraded"
    
    # Добавляем timestamp
    import datetime
    health_status["timestamp"] = datetime.datetime.utcnow().isoformat()
    
    return health_status

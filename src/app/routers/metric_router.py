from fastapi import APIRouter
from prometheus_client import generate_latest
from src.app.core.metrics import DB_STATUS
from fastapi import Response
from prometheus_client import CONTENT_TYPE_LATEST
from src.app.core.redis import RedisConnection
from src.app.core.database import DatabaseConnection
from src.app.dependencies.redis import get_redis_connection
from src.app.dependencies.database import get_database_connection
from fastapi import Depends

router = APIRouter()

@router.get("/metrics")
async def metrics(
    redis_connection: RedisConnection = Depends(get_redis_connection),
    database_connection: DatabaseConnection = Depends(get_database_connection),
):
    redis_status = await redis_connection.check_connection()   
    database_status = await database_connection.check_connection()
    DB_STATUS.labels(db="postgres").set(1 if database_status else 0)
    DB_STATUS.labels(db="redis").set(1 if redis_status else 0)
  
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
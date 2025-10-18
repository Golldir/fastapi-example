from fastapi import Request
from src.app.core.database import DatabaseConnection
from src.app.core.config import settings

def get_database_connection(request: Request) -> DatabaseConnection:
    """Получить подключение к БД"""
    if request and hasattr(request.app.state, 'database'):
        return request.app.state.database

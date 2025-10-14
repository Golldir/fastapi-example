from fastapi import Request
from src.app.core.database import DatabaseConnection

def get_database_connection(request: Request) -> DatabaseConnection:
    """FastAPI автоматически передает Request сюда!"""
    return request.app.state.database
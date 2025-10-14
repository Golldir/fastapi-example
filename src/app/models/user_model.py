from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer
from src.app.models.base_model import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)

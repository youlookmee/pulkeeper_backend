# app/database.py

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker
)
from sqlalchemy.orm import declarative_base
from app.config import DATABASE_URL

# SQLAlchemy Base
Base = declarative_base()

# ---------------------------------------------------------
# Создаём асинхронный движок PostgreSQL
# ---------------------------------------------------------
# Railway выдаёт обычный postgres:// — надо заменить на postgresql+asyncpg://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://")

engine = create_async_engine(
    DATABASE_URL,
    echo=False,          # включить True если хочешь видеть SQL запросы
    future=True
)

# ---------------------------------------------------------
# Асинхронная фабрика сессий
# ---------------------------------------------------------
async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

# ---------------------------------------------------------
# Генератор получения сессии для роутеров
# ---------------------------------------------------------
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


# ---------------------------------------------------------
# ИНИЦИАЛИЗАЦИЯ БД (создание таблиц)
# ---------------------------------------------------------
async def init_db():
    """
    Создаёт таблицы, если их нет.
    Вызывается один раз при старте backend.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

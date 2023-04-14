from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.config import settings

engine = create_async_engine(settings.database_url, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    """Base model."""

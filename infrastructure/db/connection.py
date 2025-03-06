from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine
from sqlalchemy.orm import DeclarativeBase
from tg_bot.config import DB


def create_engine(db: DB) -> AsyncEngine:
    pool = create_async_engine(
        db.create_database_url(),
        echo=True,
        pool_size=5,
        max_overflow=10
    )
    return pool


def create_session(engine: AsyncEngine):
    session_pool = async_sessionmaker(engine)
    return session_pool


class Base(DeclarativeBase):
    pass

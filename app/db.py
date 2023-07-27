from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm.decl_api import DeclarativeMeta

from app.settings.settings import Settings

Base: DeclarativeMeta = declarative_base()


def build_connection_url(s: Settings, sync: bool = False) -> str:
    if s.mode == "test":
        db_name = s.test_db_name
    else:
        db_name = s.db_name

    if sync:
        schema = "postgresql"
    else:
        schema = "postgresql+asyncpg"

    return f"{schema}://{s.db_user}:{s.db_password}@{s.db_host}:{s.db_port}/{db_name}"


def get_connection_url() -> str:
    s = Settings()
    return build_connection_url(s)


def build_engine(s: Settings) -> AsyncEngine:
    return create_async_engine(
        build_connection_url(s),
        pool_size=20,
        max_overflow=10,
    )


def build_sync_engine(s: Settings) -> Engine:
    return create_engine(build_connection_url(s, sync=True))


def create_session(s: Settings) -> async_sessionmaker[AsyncSession]:
    engine = build_engine(s)
    return async_sessionmaker(engine, expire_on_commit=False, autoflush=False)

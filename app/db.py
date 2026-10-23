"""Database engine and session management."""

from collections.abc import Generator

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.settings import settings


class Base(DeclarativeBase):
    """Declarative base class for every ORM model in this application."""


def _make_engine(database_url: str) -> Engine:
    connect_args = {"check_same_thread": False} if database_url.startswith("sqlite") else {}
    return create_engine(database_url, connect_args=connect_args)


engine = _make_engine(settings.database_url)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db() -> Generator[Session, None, None]:
    """Yields a database session for a single request.

    FastAPI overrides this dependency in tests to point at an isolated
    in-memory database instead of the configured one.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

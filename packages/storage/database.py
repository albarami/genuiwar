"""SQLAlchemy engine and session management."""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from packages.shared.config import get_settings


class Base(DeclarativeBase):
    """SQLAlchemy declarative base for all ORM models."""


def get_engine(database_url: str | None = None):  # type: ignore[no-untyped-def]
    """Create a SQLAlchemy engine from the given or configured URL."""
    url = database_url or get_settings().database_url
    return create_engine(url, echo=get_settings().database_echo)


def get_session_factory(
    database_url: str | None = None,
) -> sessionmaker[Session]:
    """Create a session factory bound to the engine."""
    engine = get_engine(database_url)
    return sessionmaker(bind=engine, expire_on_commit=False)

from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError


def _build_url_from_parts(  # pylint: disable=too-many-arguments,too-many-positional-arguments
    db_user: str,
    db_password: str,
    db_host: str,
    db_port: int,
    db_name: str,
    sslmode: Optional[str] = None,
) -> str:
    """Build a SQLAlchemy URL from explicit connection parts.

    This function does not read environment variables — main.py passes the values.
    """
    auth = f"{db_user}:{db_password}" if db_password else f"{db_user}"
    url = f"postgresql+psycopg2://{auth}@{db_host}:{db_port}/{db_name}"
    if sslmode:
        url = url + f"?sslmode={sslmode}"
    return url


def DB_Connect(  # pylint: disable=too-many-arguments,too-many-positional-arguments
    db_host: str,
    db_user: str,
    db_password: str,
    db_name: str,
    db_port: int,
    db_sslmode: Optional[str] = None,
) -> Engine:
    """Create and return a SQLAlchemy Engine using the provided connection parameters.

    Signature kept similar to the previous `DB_Connect(... )`
    so `main.py` can continue calling it.
    Returns a SQLAlchemy Engine which callers can use to create sessions or execute SQL.
    """
    url = _build_url_from_parts(
        db_user, db_password, db_host, db_port, db_name, sslmode=db_sslmode
    )
    engine = create_engine(url, future=True)
    return engine


def get_session(
    engine: Engine, autoflush: bool = True, autocommit: bool = False
) -> Session:
    """Return a SQLAlchemy Session bound to the provided engine."""
    session_local = sessionmaker(
        bind=engine, autoflush=autoflush, autocommit=autocommit, future=True
    )
    return session_local()


def DB_Close(engine: Engine) -> None:
    """Dispose the SQLAlchemy engine (close all pooled connections)."""
    try:
        engine.dispose()
    except SQLAlchemyError:
        # Best-effort disposal; ignore engine disposal errors
        pass

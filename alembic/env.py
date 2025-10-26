from logging.config import fileConfig
import os
from urllib.parse import quote_plus

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Load environment variables from a .env file when available
# (optional) so developers can run alembic locally without exporting vars.
try:
    from dotenv import load_dotenv

    # load .env if present in repository root
    load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))
except Exception:
    # python-dotenv is optional for runtime; env vars may come from the env
    pass

# Read DB connection info from environment (match .env.example variable names)
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "chmgruser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "channel-manager")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_SSLMODE = os.getenv("DB_SSLMODE", "disable")

# Build SQLAlchemy URL and set it into the alembic config so both offline
# and online modes use the same connection string.
# Use psycopg2 driver.
if DB_PASSWORD:
    password = quote_plus(DB_PASSWORD)
else:
    password = ""

sqlalchemy_url = (
    f"postgresql+psycopg2://{DB_USER}:{password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
if DB_SSLMODE:
    sqlalchemy_url = sqlalchemy_url + f"?sslmode={DB_SSLMODE}"

# configparser treats '%' specially for interpolation. Escape '%' so passwords
# containing '%' don't break set_main_option (double the percent signs).
config.set_main_option("sqlalchemy.url", sqlalchemy_url.replace("%", "%%"))

# Attempt to import project's MetaData for autogenerate support. If your
# models live in another module, adjust the import path accordingly.
target_metadata = None
try:
    # prefer a top-level models.py exposing `metadata`
    from models import metadata as target_metadata  # type: ignore
except Exception:
    try:
        # fallback: package-style import
        from database.models import base  # type: ignore

        target_metadata = [base.metadata]
    except Exception:
        # no metadata available; autogenerate won't work until you provide it
        target_metadata = None


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    # Wait for DB to be available (useful when DB is starting in docker-compose).
    wait_seconds = int(os.getenv("ALEMBIC_DB_WAIT_SECONDS", "30"))
    attempt = 0
    last_err = None
    import time

    while attempt < wait_seconds:
        try:
            with connectable.connect() as connection:
                context.configure(
                    connection=connection, target_metadata=target_metadata
                )

                with context.begin_transaction():
                    context.run_migrations()
            # success
            return
        except Exception as exc:  # pragma: no cover - retry logic
            last_err = exc
            attempt += 1
            time.sleep(1)

    # If we exit the loop, raise the last seen exception to surface the original error
    raise last_err


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

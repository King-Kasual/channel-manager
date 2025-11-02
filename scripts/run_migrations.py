import os
from alembic.config import Config
from alembic import command


def run_migrations():
    """Run Alembic migrations (upgrade to head)."""
    here = os.path.dirname(__file__)
    project_root = os.path.abspath(os.path.join(here, ".."))
    alembic_ini = os.path.join(project_root, "alembic.ini")

    cfg = Config(alembic_ini)
    # Example: set sqlalchemy.url via code if needed
    # cfg.set_main_option(
    #     'sqlalchemy.url',
    #     'postgresql+psycopg2://user:pass@host:port/db',
    # )
    command.upgrade(cfg, "head")


if __name__ == "__main__":
    run_migrations()

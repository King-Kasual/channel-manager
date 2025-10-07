from sqlalchemy import MetaData

# Shared MetaData for all models so alembic can import models.metadata
metadata = MetaData()

__all__ = ["metadata"]

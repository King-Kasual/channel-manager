from sqlalchemy import Table, Column, Integer, String, DateTime
from . import metadata

channel_dynamic = Table(
    "channel_dynamic",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("discord_channel_id", String(64), nullable=False, unique=True),
    Column("created_at", DateTime(timezone=True)),
)

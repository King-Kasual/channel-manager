from sqlalchemy import MetaData, Table, Column, Integer, String, Boolean

metadata = MetaData()

channel_static = Table(
    "channel_static",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("discord_channel_id", String(64), nullable=False, unique=True),
    Column("created_at", String(64)),  # or use DateTime with timezone
)
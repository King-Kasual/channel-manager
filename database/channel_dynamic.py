from sqlalchemy import BigInteger, Column, DateTime, String, Integer, func
from database import base


class channel_dynamic(base):
    __tablename__ = "channel_dynamic"

    id = Column(Integer, primary_key=True, autoincrement=True)
    channel_id = Column(BigInteger, nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    guild_id = Column(BigInteger, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)

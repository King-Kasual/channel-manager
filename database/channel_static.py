from sqlalchemy import BigInteger, Column, DateTime, String, Integer, func
from database import base


class channel_static(base):
    __tablename__ = "channel_static"

    id = Column(Integer, primary_key=True, autoincrement=True)
    channel_id = Column(BigInteger, nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    guild_id = Column(BigInteger, nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False  # pylint: disable=not-callable
    )

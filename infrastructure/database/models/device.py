from sqlalchemy import (
    UUID,
    Column,
    ForeignKey,
    Index,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from application.api.dependencies.db import Base
from infrastructure.database.utils import TimestampsMixin


class Device(Base, TimestampsMixin):
    __tablename__ = "devices"

    __table_args__ = (Index("idx_device_player", "player_id"),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(
        UUID(as_uuid=True),
        ForeignKey("players.player_id", ondelete="CASCADE"),
        index=True,
    )
    model = Column(String, nullable=False)
    carrier = Column(String)
    firmware = Column(String)
    player = relationship("Player", back_populates="devices")

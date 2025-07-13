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


class Inventory(Base, TimestampsMixin):
    __tablename__ = "inventory"

    __table_args__ = (
        Index("idx_inventory_player_item", "player_id", "item_key"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(
        UUID(as_uuid=True),
        ForeignKey("players.player_id", ondelete="CASCADE"),
        index=True,
    )
    item_key = Column(String, nullable=False, index=True)
    item_count = Column(Integer, default=0)
    player = relationship("Player", back_populates="inventory")

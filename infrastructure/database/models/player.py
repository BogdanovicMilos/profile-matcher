from __future__ import annotations

import uuid
from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from application.api.dependencies.db import Base
from infrastructure.database.utils import TimestampsMixin


class Player(Base, TimestampsMixin):
    """
    Model class for a Player object
    """

    __tablename__ = "players"

    __table_args__ = (
        Index("idx_players_level", "level"),
        Index("idx_players_country", "country"),
        Index("idx_players_clan_id", "clan_id"),
        Index(
            "idx_players_active_campaigns_gin",
            "active_campaigns",
            postgresql_using="gin",
        ),
    )

    player_id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    credential = Column(String, nullable=False)
    last_session = Column(DateTime(timezone=True), nullable=False)
    last_purchase = Column(DateTime(timezone=True), nullable=False)
    total_spent = Column(Float, default=0.0)
    total_refund = Column(Float, default=0.0)
    total_transactions = Column(Integer, default=0)
    total_playtime = Column(Float, default=0.0)
    level = Column(Integer, default=0.0)
    xp = Column(Float, default=0.0)
    country = Column(String, nullable=False)
    language = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    birthdate = Column(DateTime(timezone=True), nullable=False)
    active_campaigns = Column(JSONB, default=[])

    clan_id = Column(
        String, ForeignKey("clans.id", ondelete="SET NULL"), nullable=True
    )
    clan = relationship("Clan", back_populates="players")
    devices = relationship(
        "Device", back_populates="player", cascade="all, delete-orphan"
    )
    inventory = relationship(
        "Inventory", back_populates="player", cascade="all, delete-orphan"
    )

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

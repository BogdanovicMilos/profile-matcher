from sqlalchemy import (
    Column,
    Index,
    String,
)
from sqlalchemy.orm import relationship

from application.api.dependencies.db import Base
from infrastructure.database.utils import TimestampsMixin


class Clan(Base, TimestampsMixin):
    __tablename__ = "clans"

    __table_args__ = (Index("idx_clan_name", "name"),)

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    players = relationship("Player", back_populates="clan")

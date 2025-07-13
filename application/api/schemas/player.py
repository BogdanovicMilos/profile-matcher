from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, ConfigDict
from uuid import UUID


class Inventory(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    item_key: str
    item_count: int


class Device(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    model: str
    carrier: str
    firmware: str


class Clan(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str


class Player(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    player_id: UUID
    credential: str
    created: datetime | None
    modified: datetime | None
    last_session: datetime | None
    total_spent: float
    total_refund: float
    total_transactions: int
    last_purchase: datetime | None
    active_campaigns: list[str]
    devices: list[Device]
    level: int
    xp: int
    total_playtime: float
    country: str
    language: str
    birthdate: datetime | None
    gender: str
    inventory: list[Inventory]
    clan: Clan

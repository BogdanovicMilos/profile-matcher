from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel
from typing import Any


class MatcherRange(BaseModel):
    min: int
    max: int


class CampaignMatchers(BaseModel):
    level: MatcherRange
    has: dict[str, list[Any]]
    does_not_have: dict[str, list[Any]]


class Campaign(BaseModel):
    game: str
    name: str
    priority: float
    matchers: CampaignMatchers
    start_date: datetime
    end_date: datetime
    enabled: bool
    last_updated: datetime

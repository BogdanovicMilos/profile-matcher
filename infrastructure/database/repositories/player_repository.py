from __future__ import annotations

from dataclasses import dataclass

import logging
from datetime import UTC, datetime
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette import status
from uuid import UUID

from infrastructure.database.models.player import Player


log = logging.getLogger("repository.player")


@dataclass
class PlayerRepository:
    session: AsyncSession

    async def get_player_profile(self, player_id: UUID) -> Player:
        """Retrieve player profile by player_id"""

        try:
            query = (
                select(Player)
                .where(Player.player_id == player_id)
                .options(
                    selectinload(Player.devices),
                    selectinload(Player.inventory),
                    selectinload(Player.clan),
                )
            )
            result = await self.session.execute(query)
            return result.scalars().first()

        except SQLAlchemyError as exc:
            log.error("Error fetching stock prices: %s", exc)

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database query failed",
            ) from exc

    async def update_active_campaigns(
        self, profile: Player, campaigns: list[str]
    ) -> Player:
        """Update active campaigns for a player profile"""

        profile.active_campaigns = campaigns
        profile.modified = datetime.now(UTC)

        try:
            self.session.add(profile)
            await self.session.commit()
            await self.session.refresh(profile)
            return profile
        except SQLAlchemyError as exc:
            log.error("Error creating stock price: %s", exc)

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database creation failed",
            ) from exc

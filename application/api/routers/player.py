from __future__ import annotations

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from application.api.dependencies.db import async_get_db
from application.api.schemas.player import Player
from infrastructure.database.repositories.player_repository import (
    PlayerRepository,
)


router = APIRouter(
    prefix="/api",
    tags=["Player"],
)

log = logging.getLogger("routers.player")


@router.get(
    "/player/{player_id}",
    response_model=Player,
    status_code=status.HTTP_200_OK,
)
async def get_player_by_id(
    player_id: UUID, session: AsyncSession = Depends(async_get_db)
):
    repository = PlayerRepository(session)
    player = await repository.get_player_profile(player_id)

    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Player not found"
        )

    player_schema = Player.model_validate(player)
    return player_schema

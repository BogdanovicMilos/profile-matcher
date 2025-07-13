from __future__ import annotations

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from application.api.dependencies.db import async_get_db
from application.api.schemas.player import Player
from domain.matching.campaign_matcher import CampaignMatcher
from infrastructure.database.repositories.player_repository import (
    PlayerRepository,
)
from infrastructure.external.campaign.service.campaign import CampaignService


router = APIRouter(
    prefix="/api",
    tags=["Client"],
)

log = logging.getLogger("routers.client")


@router.get(
    "/get_client_config/{player_id}",
    response_model=Player,
    status_code=status.HTTP_200_OK,
)
async def get_client_config(
    player_id: UUID, session: AsyncSession = Depends(async_get_db)
):
    repository = PlayerRepository(session)
    player = await repository.get_player_profile(player_id)

    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Player not found"
        )

    campaign_service = CampaignService()
    campaigns = await campaign_service.fetch_current_campaigns()

    if not campaigns:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active campaigns found",
        )

    player_schema = Player.model_validate(player)
    matcher = CampaignMatcher()
    matched_campaigns = matcher.match_profile(player_schema, campaigns)

    if matched_campaigns != player_schema.active_campaigns:
        updated_campaigns = await repository.update_active_campaigns(
            player, matched_campaigns
        )
        return Player.model_validate(updated_campaigns)
    return player_schema

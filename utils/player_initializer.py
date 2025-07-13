import logging
import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from application.api.dependencies.db import async_get_db
from infrastructure.database.models.clan import Clan
from infrastructure.database.models.device import Device
from infrastructure.database.models.inventory import Inventory
from infrastructure.database.models.player import Player
from utils.player_schema import player_payload


log = logging.getLogger("utils.player_initializer")


def parse_datetime(timestamp: str) -> datetime:
    """Parse RFC 3339/ISO-8601 strings like '2021-01-10T13:37:17Z'."""
    return datetime.fromisoformat(timestamp.replace("Z", "+00:00"))


async def init_player():
    async for session in async_get_db():
        await _init_player(session)


async def _init_player(session: AsyncSession):
    log.info("Initializing player")
    player = await session.get(Player, uuid.UUID(player_payload["player_id"]))
    if player:
        return

    # Insert Clan data
    clan = None
    if (clan_data := player_payload.get("clan")) is not None:
        clan = await session.get(Clan, clan_data["id"])
        if clan is None:
            clan = Clan(id=clan_data["id"], name=clan_data["name"])
            session.add(clan)

    # Insert Player data
    player = Player(
        player_id=uuid.UUID(str(player_payload["player_id"])),
        credential=player_payload["credential"],
        last_session=parse_datetime(str(player_payload["last_session"])),
        last_purchase=parse_datetime(str(player_payload["last_purchase"])),
        total_spent=player_payload["total_spent"],
        total_refund=player_payload["total_refund"],
        total_transactions=player_payload["total_transactions"],
        total_playtime=player_payload["total_playtime"],
        level=player_payload["level"],
        xp=player_payload["xp"],
        country=player_payload["country"],
        language=player_payload["language"],
        gender=player_payload["gender"],
        birthdate=parse_datetime(str(player_payload["birthdate"])),
        active_campaigns=player_payload.get("active_campaigns", []),
        clan=clan,
    )

    # Insert Devices data
    for device in player_payload.get("devices", []):
        player.devices.append(
            Device(
                id=int(device["id"]),
                model=device["model"],
                carrier=device.get("carrier"),
                firmware=device.get("firmware"),
            )
        )

    # Insert Inventory data
    for key, count in player_payload.get("inventory", {}).items():
        player.inventory.append(Inventory(item_key=key, item_count=count))

    session.add(player)
    await session.commit()
    await session.refresh(player)
    log.info("Player initialized")

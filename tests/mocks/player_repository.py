from datetime import datetime
from uuid import UUID

from infrastructure.database.repositories.player_repository import (
    PlayerRepository,
)


class MockPlayerRepository(PlayerRepository):
    def __init__(self, _=None):
        super().__init__(session=None)
        now = datetime(2025, 1, 1)
        self._players = [
            {
                "id": UUID(int=1),
                "player_id": UUID(int=1),
                "credential": "test_credential",
                "created": now,
                "modified": now,
                "last_session": now,
                "total_spent": 0.0,
                "total_refund": 0.0,
                "total_transactions": 0,
                "last_purchase": now,
                "devices": [
                    {
                        "id": 1,
                        "model": "apple iphone 11",
                        "carrier": "vodafone",
                        "firmware": "123",
                    }
                ],
                "level": 6,
                "xp": 1000,
                "experience": 1000,
                "total_playtime": 3600,
                "country": "US",
                "language": "en",
                "birthdate": datetime(2000, 1, 1),
                "gender": "unknown",
                "active_campaigns": ["campaign1", "campaign2"],
                "inventory": [
                    {"id": 1, "item_key": "cash", "item_count": 123},
                    {"id": 2, "item_key": "coins", "item_count": 123},
                    {"id": 3, "item_key": "item_1", "item_count": 1},
                ],
                "clan": {"id": "123456", "name": "Hello world clan"},
            }
        ]

    async def get_player_profile(self, player_id: UUID):
        for player in self._players:
            if player["id"] == player_id:
                return player
        return None

    async def update_active_campaigns(self, profile, campaigns):
        for player in self._players:
            if player["id"] == player["id"]:
                player["active_campaigns"] = campaigns
                return player
        return None

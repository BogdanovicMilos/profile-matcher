import pytest
import uuid
from datetime import datetime

from application.api.schemas.player import Clan, Inventory, Player
from domain.matching.campaign_matcher import CampaignMatcher
from infrastructure.external.campaign.schema.campaign import (
    Campaign,
    CampaignMatchers,
    MatcherRange,
)


clan = Clan(id=str(uuid.uuid4()), name="MockClan")

campaigns = [
    Campaign(
        game="Race Game",
        name="Summer Event",
        priority=10.5,
        matchers=CampaignMatchers(
            level=MatcherRange(min=5, max=10),
            has={"country": ["US"], "items": ["item1"]},
            does_not_have={"items": ["item4"]},
        ),
        start_date=datetime(2025, 1, 1),
        end_date=datetime(2025, 12, 31),
        enabled=True,
        last_updated=datetime(2025, 1, 1),
    ),
    Campaign(
        game="Random Game",
        name="Winter Event",
        priority=8.0,
        matchers=CampaignMatchers(
            level=MatcherRange(min=1, max=10),
            has={"country": ["US"], "items": ["item1"]},
            does_not_have={"items": ["item3"]},
        ),
        start_date=datetime(2025, 1, 1),
        end_date=datetime(2025, 12, 31),
        enabled=True,
        last_updated=datetime(2025, 1, 1),
    ),
    Campaign(
        game="Fighting Game",
        name="Christmas Campaign",
        priority=7.5,
        matchers=CampaignMatchers(
            level=MatcherRange(min=5, max=15),
            has={"country": ["US"], "items": ["item3"]},
            does_not_have={"items": ["item1"]},
        ),
        start_date=datetime(2025, 1, 1),
        end_date=datetime(2025, 12, 31),
        enabled=True,
        last_updated=datetime(2025, 1, 1),
    ),
]


@pytest.mark.parametrize(
    "player_level, player_country, inventory_items, expected_campaigns",
    [
        (
            10,
            "US",
            [(1, "item1", 2), (2, "item2", 0)],
            ["Summer Event", "Winter Event"],
        ),
        (20, "US", [(1, "item1", 2), (2, "item2", 0)], []),
        (10, "UK", [(1, "item1", 2), (2, "item2", 0)], []),
        (10, "US", [(3, "item3", 1)], ["Christmas Campaign"]),
    ],
)
def test_match_profile(
    player_level, player_country, inventory_items, expected_campaigns
):
    """
    Case 1: Matches both campaigns
    Case 2: Level too high, no matches
    Case 3: Wrong country, no matches
    Case 4: Matches only one campaign
    """

    player = Player(
        level=player_level,
        country=player_country,
        inventory=[
            Inventory(id=item[0], item_key=item[1], item_count=item[2])
            for item in inventory_items
        ],
        player_id=uuid.UUID("00000000-0000-0000-0000-000000000001"),
        credential="test_credential",
        last_session=datetime(2025, 1, 1),
        last_purchase=datetime(2025, 1, 1),
        total_spent=100.0,
        total_refund=10.0,
        total_transactions=5,
        total_playtime=10,
        xp=10,
        language="en",
        gender="male",
        birthdate=datetime(2000, 1, 1),
        active_campaigns=[],
        created=datetime.now(),
        modified=datetime.now(),
        devices=[],
        clan=clan,
    )

    result = CampaignMatcher.match_profile(player, campaigns)
    assert sorted(result) == sorted(expected_campaigns)

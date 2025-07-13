from datetime import datetime

from infrastructure.external.campaign.schema.campaign import (
    Campaign,
    CampaignMatchers,
    MatcherRange,
)
from infrastructure.external.campaign.service.campaign import CampaignService


class MockCampaignService(CampaignService):
    def __init__(self):
        super().__init__()
        self.running_campaigns = [
            Campaign(
                game="mygame",
                name="Summer Event",
                priority=10.5,
                matchers=CampaignMatchers(
                    level=MatcherRange(min=5, max=10),
                    has={"country": ["US", "RO", "CA"], "items": ["item_1"]},
                    does_not_have={"items": ["item_4"]},
                ),
                start_date=datetime(2025, 1, 1),
                end_date=datetime(2025, 12, 31),
                enabled=True,
                last_updated=datetime(2025, 1, 1),
            ),
            Campaign(
                game="mygame",
                name="Winter Challenge",
                priority=8.5,
                matchers=CampaignMatchers(
                    level=MatcherRange(min=8, max=15),
                    has={"country": ["US", "RO", "CA"], "items": ["item_1"]},
                    does_not_have={"items": ["item_4"]},
                ),
                start_date=datetime(2025, 1, 1),
                end_date=datetime(2025, 12, 31),
                enabled=True,
                last_updated=datetime(2025, 1, 1),
            ),
        ]

    async def fetch_current_campaigns(self):
        return self.running_campaigns

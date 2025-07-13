from datetime import datetime, timezone

from application.config.settings import settings
from infrastructure.external.campaign.schema.campaign import Campaign


class CampaignService:
    def __init__(self):
        self.base_url = settings.api_url

    async def fetch_current_campaigns(self) -> list[Campaign]:
        """
        Mock function to fetch current campaigns from external API
        """

        running_campaigns = [
            {
                "game": "mygame",
                "name": "mycampaign",
                "priority": 10.5,
                "matchers": {
                    "level": {"min": 1, "max": 3},
                    "has": {
                        "country": ["US", "RO", "CA"],
                        "items": ["item_1"],
                    },
                    "does_not_have": {"items": ["item_4"]},
                },
                "start_date": "2022-01-25T00:00:00Z",
                "end_date": "2022-02-25T00:00:00Z",
                "enabled": True,
                "last_updated": "2021-07-13T11:46:58Z",
            },
            {
                "game": "Minion Rush",
                "name": "Run",
                "priority": 10.5,
                "matchers": {
                    "level": {"min": 1, "max": 3},
                    "has": {
                        "country": ["US", "RO", "CA"],
                        "items": ["item_1"],
                    },
                    "does_not_have": {"items": ["item_4"]},
                },
                "start_date": "2025-07-10T00:00:00Z",
                "end_date": "2025-07-15T00:00:00Z",
                "enabled": True,
                "last_updated": "2025-07-12T11:46:58Z",
            },
        ]

        campaigns = [Campaign(**campaign) for campaign in running_campaigns]
        now = datetime.now(timezone.utc)
        return [
            campaign
            for campaign in campaigns
            if campaign.enabled
            and campaign.start_date <= now <= campaign.end_date
        ]

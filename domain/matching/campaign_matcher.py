from application.api.schemas.player import Player
from infrastructure.external.campaign.schema.campaign import Campaign


class CampaignMatcher:
    @staticmethod
    def match_profile(profile: Player, campaigns: list[Campaign]) -> list[str]:
        """
        Match a player profile against a list of campaigns based on various criteria.
        :param profile: Profile of the player to match
        :param campaigns: List of Campaign objects to match against
        :return: Campaign names that match the player's profile
        """

        # convert an inventory list to a dict for fast lookups
        inventory = {
            item.item_key: item.item_count for item in profile.inventory
        }
        matched = []
        for campaign in campaigns:
            matchers = campaign.matchers
            if not matchers.level.min <= profile.level <= matchers.level.max:
                continue
            if profile.country not in matchers.has.get("country", []):
                continue
            if any(
                inventory.get(item, 0) < 1
                for item in matchers.has.get("items", [])
            ):
                continue
            if any(
                inventory.get(item, 0) > 0
                for item in matchers.does_not_have.get("items", [])
            ):
                continue
            matched.append(campaign.name)
        return matched

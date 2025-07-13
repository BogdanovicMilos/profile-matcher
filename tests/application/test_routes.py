import pytest
from httpx import AsyncClient
from pytest_mock import MockerFixture
from uuid import UUID

from infrastructure.external.campaign.service.campaign import CampaignService
from tests.mocks.campaign_service import MockCampaignService
from tests.mocks.player_repository import MockPlayerRepository


@pytest.mark.asyncio
async def test_get_client_config_success(
    mocker: MockerFixture, client: AsyncClient
):
    """Test successful client config retrieval"""

    mocker.patch(
        "application.api.routers.client.PlayerRepository", MockPlayerRepository
    )
    mocker.patch(
        "application.api.routers.client.CampaignService", MockCampaignService
    )

    player_id = UUID("00000000-0000-0000-0000-000000000001")
    response = await client.get(f"/api/get_client_config/{player_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["player_id"] == "00000000-0000-0000-0000-000000000001"


@pytest.mark.asyncio
async def test_get_client_config_player_not_found(
    mocker: MockerFixture, client: AsyncClient
):
    """Test when a player is not found"""
    mocker.patch(
        "application.api.routers.client.PlayerRepository", MockPlayerRepository
    )

    player_id = UUID("00000000-0000-0000-0000-000000000009")
    response = await client.get(f"/api/get_client_config/{player_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Player not found"


@pytest.mark.asyncio
async def test_get_client_config_with_running_campaign(
    mocker: MockerFixture, client: AsyncClient
):
    """Test client config retrieval with active campaigns"""

    mocker.patch(
        "application.api.routers.client.PlayerRepository", MockPlayerRepository
    )
    mocker.patch(
        "application.api.routers.client.CampaignService", MockCampaignService
    )

    player_id = UUID("00000000-0000-0000-0000-000000000001")
    response = await client.get(f"/api/get_client_config/{player_id}")
    assert response.status_code == 200
    data = response.json()
    assert "Summer Event" in data["active_campaigns"]


@pytest.mark.asyncio
async def test_get_client_config_no_running_campaigns(
    mocker: MockerFixture, client: AsyncClient
):
    """Test client config retrieval when no campaigns are running"""

    mocker.patch(
        "application.api.routers.client.PlayerRepository", MockPlayerRepository
    )

    # Create a campaign service with no active campaigns
    class EmptyCampaignService(CampaignService):
        async def fetch_current_campaigns(self):
            return []

    mocker.patch(
        "application.api.routers.client.CampaignService", EmptyCampaignService
    )

    player_id = UUID("00000000-0000-0000-0000-000000000001")
    response = await client.get(f"/api/get_client_config/{player_id}")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "No active campaigns found"

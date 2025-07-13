import pytest
import uuid
from datetime import UTC, datetime
from httpx import ASGITransport, AsyncClient
from unittest.mock import AsyncMock, Mock

from application.api.main import app
from infrastructure.database.models.player import Player
from infrastructure.database.repositories.player_repository import (
    PlayerRepository,
)


@pytest.fixture(scope="function")
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://testserver"
    ) as client:
        yield client


@pytest.fixture
def mock_session():
    session = AsyncMock()
    session.add = Mock()
    return session


@pytest.fixture
def repository(mock_session):
    return PlayerRepository(session=mock_session)


@pytest.fixture
def player():
    return Player(
        player_id=uuid.uuid4(),
        active_campaigns=["Winter Campaign"],
        modified=datetime.now(UTC),
        devices=[],
        inventory=[],
        clan=None,
    )

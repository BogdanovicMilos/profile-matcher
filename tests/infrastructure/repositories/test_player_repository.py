import pytest
import uuid
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from unittest.mock import Mock


class TestPlayerRepository:
    @pytest.mark.asyncio
    async def test_get_player_profile_success(
        self, repository, mock_session, player
    ):
        mock = Mock()
        mock.scalars.return_value.first.return_value = player
        mock_session.execute.return_value = mock

        result = await repository.get_player_profile(player.player_id)

        assert result == player
        mock_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_player_profile_database_error(
        self, repository, mock_session
    ):
        mock_session.execute.side_effect = SQLAlchemyError("Database error")

        with pytest.raises(HTTPException) as exc_info:
            await repository.get_player_profile(uuid.uuid4())

        assert exc_info.value.status_code == 500
        assert exc_info.value.detail == "Database query failed"

    @pytest.mark.asyncio
    async def test_update_active_campaigns_success(
        self, repository, mock_session, player
    ):
        new_campaigns = ["Summer Campaign", "Winter Campaign"]
        mock_session.refresh.return_value = None

        result = await repository.update_active_campaigns(
            player, new_campaigns
        )

        assert result.active_campaigns == new_campaigns
        mock_session.add.assert_called_once_with(player)
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once_with(player)

    @pytest.mark.asyncio
    async def test_update_active_campaigns_database_error(
        self, repository, mock_session, player
    ):
        mock_session.commit.side_effect = SQLAlchemyError("Database error")

        with pytest.raises(HTTPException) as exc_info:
            await repository.update_active_campaigns(
                player, ["Christmas Campaign"]
            )

        assert exc_info.value.status_code == 500
        assert exc_info.value.detail == "Database creation failed"

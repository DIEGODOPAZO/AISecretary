import json
import pytest
from unittest.mock import patch, MagicMock

from src.utils.email.microsoft_flag_requests import MicrosoftFlagRequests


@pytest.fixture
def mock_token_manager():
    mock = MagicMock()
    mock.get_token.return_value = "mocked_token"
    return mock


@patch("src.utils.email.microsoft_flag_requests.microsoft_patch")
def test_manage_flags_valid_flag(mock_patch, mock_token_manager):
    # Setup
    email_id = "12345"
    flag = "flagged"
    expected_response = {"status": "ok"}
    mock_patch.return_value = (200, expected_response)

    client = MicrosoftFlagRequests(mock_token_manager)

    # Act
    response = client.manage_flags_microsoft_api(email_id, flag)

    # Assert
    assert json.loads(response) == expected_response
    mock_patch.assert_called_once_with(
        f"https://graph.microsoft.com/v1.0/me/messages/{email_id}",
        "mocked_token",
        data={"flag": {"flagStatus": flag}},
    )


def test_manage_flags_invalid_flag(mock_token_manager):
    client = MicrosoftFlagRequests(mock_token_manager)

    response = client.manage_flags_microsoft_api("12345", "invalid_flag")

    assert json.loads(response) == {"error": "Not valid flag submited"}

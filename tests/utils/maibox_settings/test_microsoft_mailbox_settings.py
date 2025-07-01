import json
from types import SimpleNamespace
import pytest
from unittest.mock import patch, MagicMock
from src.utils.mailbox_settings.microsoft_mailbox_settings import MicrosoftMailboxSettings
from src.utils.param_types import MailboxSettingsParams, LanguageSettings, WorkingHours, AutomaticRepliesSetting, DateTimeTimeZone


@pytest.fixture
def mock_token_manager():
    mock = MagicMock()
    mock.get_token.return_value = "mocked_token"
    return mock


@patch("src.utils.mailbox_settings.microsoft_mailbox_settings.microsoft_get")
def test_get_mailbox_settings_success(mock_get, mock_token_manager):
    expected_response = {
        "timeZone": "Pacific Standard Time",
        "dateFormat": "dd/MM/yyyy"
    }
    mock_get.return_value = (200, expected_response)

    client = MicrosoftMailboxSettings(mock_token_manager)
    result = client.get_mailbox_settings()

    result = json.loads(client.get_mailbox_settings())
    assert result == expected_response

@patch("src.utils.mailbox_settings.microsoft_mailbox_settings.microsoft_patch")
@patch("src.utils.mailbox_settings.microsoft_mailbox_settings.microsoft_get")
def test_update_mailbox_settings_success(mock_patch, mock_token_manager):
    expected_response = {"status": "ok"}
    mock_patch.return_value = (200, expected_response)

    params = MailboxSettingsParams(
        timeZone="Pacific Standard Time",
        language=LanguageSettings(locale="en-US", displayName="English (United States)"),
        dateFormat="dd/MM/yyyy",
        timeFormat="HH:mm",
        workingHours=WorkingHours(
            daysOfWeek=["Monday", "Tuesday"],
            startTime="08:00:00",
            endTime="17:00:00",
            timeZone=SimpleNamespace(name="Pacific Standard Time")
        ),
        automaticRepliesSetting=AutomaticRepliesSetting(
            status="scheduled",
            externalAudience="all",
            internalReplyMessage="I am currently out of the office.",
            externalReplyMessage="I am currently unavailable.",
            scheduledStartDateTime=DateTimeTimeZone(
                dateTime="2025-07-01T00:00:00", timeZone="UTC"
            ),
            scheduledEndDateTime=DateTimeTimeZone(
                dateTime="2025-07-10T23:59:59", timeZone="UTC"
            )
        ),
        delegateMeetingMessageDeliveryOptions="sendToDelegatesAndMe"
    )

    client = MicrosoftMailboxSettings(mock_token_manager)
    result = client.update_mailbox_settings(params)
    result = json.loads(client.get_mailbox_settings())
    assert result == expected_response
  

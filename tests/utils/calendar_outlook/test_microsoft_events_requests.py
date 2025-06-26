import json
import pytest
from unittest.mock import patch, MagicMock
from src.utils.calendar_outlook.microsoft_events_requests import MicrosoftEventsRequests
from src.utils.param_types import EventParams, EventQuery


@pytest.fixture
def mock_token_manager():
    mock = MagicMock()
    mock.get_token.return_value = "mocked_token"
    return mock


@patch("src.utils.calendar_outlook.microsoft_events_requests.microsoft_get")
@patch("src.utils.calendar_outlook.microsoft_events_requests.event_query_to_graph_params")
@patch("src.utils.calendar_outlook.microsoft_events_requests.simplify_event")
def test_get_events_dates(mock_simplify, mock_query_params, mock_get, mock_token_manager):
    mock_query_params.return_value = {
        "startDateTime": "2025-01-01T00:00:00Z",
        "endDateTime": "2025-01-02T00:00:00Z"
    }
    mock_get.return_value = (200, {"value": [{"id": "1"}]})
    mock_simplify.return_value = {"id": "1"}

    client = MicrosoftEventsRequests(mock_token_manager)
    query = EventQuery()
    result = json.loads(client.get_events(query))
    assert result == [{"id": "1"}]


@patch("src.utils.calendar_outlook.microsoft_events_requests.microsoft_post")
@patch("src.utils.calendar_outlook.microsoft_events_requests.event_params_to_dict")
@patch("src.utils.calendar_outlook.microsoft_events_requests.simplify_event")
def test_create_event_success(mock_simplify, mock_params_to_dict, mock_post, mock_token_manager):
    mock_params_to_dict.return_value = {"subject": "Test"}
    mock_post.return_value = (201, {"id": "123"})
    mock_simplify.return_value = {"id": "123"}

    client = MicrosoftEventsRequests(mock_token_manager)
    event_params = EventParams(
        subject="Test",
        start={"dateTime": "2024-01-01T10:00:00", "timeZone": "UTC"},
        end={"dateTime": "2024-01-01T11:00:00", "timeZone": "UTC"}
    )
    result = json.loads(client.create_event(event_params))

    assert result == {"id": "123"}


@patch("src.utils.calendar_outlook.microsoft_events_requests.microsoft_patch")
@patch("src.utils.calendar_outlook.microsoft_events_requests.event_params_to_dict")
@patch("src.utils.calendar_outlook.microsoft_events_requests.simplify_event")
def test_update_event_success(mock_simplify, mock_params_to_dict, mock_patch, mock_token_manager):
    mock_params_to_dict.return_value = {"subject": "Updated"}
    mock_patch.return_value = (200, {"id": "123"})
    mock_simplify.return_value = {"id": "123"}

    client = MicrosoftEventsRequests(mock_token_manager)
    event_params = event_params = EventParams(
        subject="Updated",
        start={"dateTime": "2024-01-01T10:00:00", "timeZone": "UTC"},
        end={"dateTime": "2024-01-01T11:00:00", "timeZone": "UTC"}
    )
    result = json.loads(client.update_event("123", event_params))

    assert result == {"id": "123"}


@patch("src.utils.calendar_outlook.microsoft_events_requests.microsoft_delete")
def test_delete_event_success(mock_delete, mock_token_manager):
    mock_delete.return_value = (204, {})
    client = MicrosoftEventsRequests(mock_token_manager)
    result = json.loads(client.delete_event("123"))
    assert result == {"message": "Event deleted successfully"}


@patch("src.utils.calendar_outlook.microsoft_events_requests.microsoft_delete")
def test_delete_event_attachment_failure(mock_delete, mock_token_manager):
    mock_delete.return_value = (500, {})
    client = MicrosoftEventsRequests(mock_token_manager)
    result = json.loads(client.delete_event_attachment("event-id", "attachment-id"))
    assert result == {"error": "Failed to delete attachment"}

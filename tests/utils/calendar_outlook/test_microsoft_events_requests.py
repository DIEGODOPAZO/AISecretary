import json
import pytest
from unittest.mock import patch, MagicMock
from src.utils.calendar_outlook.microsoft_events_requests import MicrosoftEventsRequests
from src.utils.param_types import EventChangesParams, EventParams, EventQuery, EventResponseParams


@pytest.fixture
def mock_token_manager():
    mock = MagicMock()
    mock.get_token.return_value = "mocked_token"
    return mock

@patch.object(MicrosoftEventsRequests, "microsoft_get")
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


@patch.object(MicrosoftEventsRequests, "microsoft_post")
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


@patch.object(MicrosoftEventsRequests, "microsoft_patch")
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


@patch.object(MicrosoftEventsRequests, "microsoft_delete")
def test_delete_event_success(mock_delete, mock_token_manager):
    mock_delete.return_value = (204, {})
    client = MicrosoftEventsRequests(mock_token_manager)
    result = json.loads(client.delete_event("123"))
    assert result == {"message": "Event deleted successfully"}


@patch.object(MicrosoftEventsRequests, "microsoft_delete")
def test_delete_event_attachment_failure(mock_delete, mock_token_manager):
    mock_delete.return_value = (500, {})
    client = MicrosoftEventsRequests(mock_token_manager)
    result = json.loads(client.delete_event_attachment("event-id", "attachment-id"))
    assert result == {"error": "Failed to delete attachment"}

@patch.object(MicrosoftEventsRequests, "download_attachments")
@patch("src.utils.calendar_outlook.microsoft_events_requests.simplify_event_with_attachment_names")
@patch.object(MicrosoftEventsRequests, "microsoft_get")
def test_get_event_success(mock_get, mock_simplify, mock_download, mock_token_manager):
    # Primer GET (event)
    mock_get.side_effect = [
        (200, {"id": "event123"}),  # event data
        (200, {"value": [{"name": "file1.pdf"}]})  # attachments
    ]
    mock_simplify.return_value = {"id": "event123", "subject": "Meeting"}
    mock_download.return_value = ["file1.pdf"]

    client = MicrosoftEventsRequests(mock_token_manager)
    result = json.loads(client.get_event("event123"))

    assert result["id"] == "event123"
    assert result["attachments"] == ["file1.pdf"]


@patch.object(MicrosoftEventsRequests, "microsoft_post")
def test_accept_event_invitation_success(mock_post, mock_token_manager):
    mock_post.return_value = (202, {})
    client = MicrosoftEventsRequests(mock_token_manager)
    response = json.loads(client.accept_event_invitation("event123", EventResponseParams(send_response=True, comment="See you")))
    assert response == {"message": "Event invitation accepted"}


@patch.object(MicrosoftEventsRequests, "microsoft_post")
def test_decline_event_invitation_success(mock_post, mock_token_manager):
    mock_post.return_value = (202, {})
    client = MicrosoftEventsRequests(mock_token_manager)
    response = json.loads(client.decline_event_invitation("event123", EventChangesParams(event_response_params=EventResponseParams(send_response=True, comment="See you"))))
    assert response == {"message": "Event invitation declined"}


@patch.object(MicrosoftEventsRequests, "microsoft_post")
def test_tentative_accept_event_invitation_success(mock_post, mock_token_manager):
    mock_post.return_value = (202, {})
    client = MicrosoftEventsRequests(mock_token_manager)
    response = json.loads(client.tentatively_accept_event_invitation("event123", EventChangesParams(event_response_params=EventResponseParams(send_response=True, comment="Maybe"))))
    assert response == {"message": "Event invitation tentatively accepted"}  

@patch.object(MicrosoftEventsRequests, "microsoft_post")
def test_cancel_event_success(mock_post, mock_token_manager):
    mock_post.return_value = (202, {})
    client = MicrosoftEventsRequests(mock_token_manager)
    response = json.loads(client.cancel_event("event123", comment="Cancelled"))
    assert response == {"message": "Event canceled"}


@patch.object(MicrosoftEventsRequests, "microsoft_post")
@patch("src.utils.calendar_outlook.microsoft_events_requests.event_params_to_dict")
@patch("src.utils.calendar_outlook.microsoft_events_requests.simplify_event")
@patch.object(MicrosoftEventsRequests, "read_file_and_encode_base64")
def test_create_event_attachment_failure(mock_encode, mock_simplify, mock_params_to_dict, mock_post, mock_token_manager):
    mock_params_to_dict.return_value = {"subject": "Test"}
    mock_post.side_effect = [
        (201, {"id": "event456"}),  # event creation
        (500, {})  # attachment failure
    ]
    mock_simplify.return_value = {"id": "event456"}
    mock_encode.return_value = ("test.pdf", "encoded-content")

    client = MicrosoftEventsRequests(mock_token_manager)
    event_params = EventParams(
        subject="Test",
        start={"dateTime": "2024-01-01T10:00:00", "timeZone": "UTC"},
        end={"dateTime": "2024-01-01T11:00:00", "timeZone": "UTC"},
        attachments=["fakepath/test.pdf"]
    )
    result = json.loads(client.create_event(event_params))

    assert result == {"error": "Failed to add attachments"}
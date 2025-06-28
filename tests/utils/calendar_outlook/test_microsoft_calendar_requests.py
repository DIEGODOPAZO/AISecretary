import json
import pytest
from unittest.mock import patch, MagicMock

from src.utils.calendar_outlook.microsoft_calendar_requests import MicrosoftCalendarRequests
from src.utils.param_types import CalendarUpdateParams, ScheduleParams, DateTimeTimeZone


@pytest.fixture
def mock_token_manager():
    mock = MagicMock()
    mock.get_token.return_value = "fake_token"
    return mock


@patch("src.utils.calendar_outlook.microsoft_calendar_requests.microsoft_get")
def test_get_calendars(mock_get, mock_token_manager):
    mock_get.return_value = (
        200,
        {
            "value": [
                {"id": "1", "name": "Calendario A"},
                {"id": "2", "name": "Calendario B"}
            ]
        }
    )

    client = MicrosoftCalendarRequests(mock_token_manager)
    result = json.loads(client.get_calendars())

    assert isinstance(result["calendars: "], list)
    assert result["calendars: "][0]["id"] == "1"


@patch("src.utils.calendar_outlook.microsoft_calendar_requests.microsoft_get")
def test_get_calendars_with_name_filter(mock_get, mock_token_manager):
    mock_get.return_value = (
        200,
        {
            "value": [
                {"id": "1", "name": "Calendario A"},
                {"id": "2", "name": "Filtrado"}
            ]
        }
    )

    client = MicrosoftCalendarRequests(mock_token_manager)
    result = json.loads(client.get_calendars(name="Filtrado"))

    assert len(result["calendars: "]) == 1
    assert result["calendars: "][0]["name"] == "Filtrado"


@patch("src.utils.calendar_outlook.microsoft_calendar_requests.microsoft_get")
def test_get_calendar(mock_get, mock_token_manager):
    mock_get.return_value = (
        200,
        {"id": "123", "name": "Personal"}
    )

    client = MicrosoftCalendarRequests(mock_token_manager)
    result = json.loads(client.get_calendar("123"))

    assert result["id"] == "123"
    assert result["name"] == "Personal"


@patch("src.utils.calendar_outlook.microsoft_calendar_requests.microsoft_post")
def test_create_calendar(mock_post, mock_token_manager):
    mock_post.return_value = (
        201,
        {"id": "new123", "name": "Nuevo Calendario"}
    )

    client = MicrosoftCalendarRequests(mock_token_manager)
    result = json.loads(client.create_calendar("Nuevo Calendario"))

    assert result["id"] == "new123"
    assert result["name"] == "Nuevo Calendario"


@patch("src.utils.calendar_outlook.microsoft_calendar_requests.microsoft_patch")
def test_update_calendar(mock_patch, mock_token_manager):
    mock_patch.return_value = (
        200,
        {"id": "cal123", "name": "Actualizado"}
    )

    update_params = CalendarUpdateParams(name="Actualizado")
    client = MicrosoftCalendarRequests(mock_token_manager)
    result = json.loads(client.update_calendar("cal123", update_params))

    assert result["id"] == "cal123"
    assert result["name"] == "Actualizado"


@patch("src.utils.calendar_outlook.microsoft_calendar_requests.microsoft_delete")
def test_delete_calendar_success(mock_delete, mock_token_manager):
    mock_delete.return_value = (204, None)

    client = MicrosoftCalendarRequests(mock_token_manager)
    result = json.loads(client.delete_calendar("cal123"))

    assert result["message"] == "Calendar deleted successfully"
    assert result["status_code"] == 204


@patch("src.utils.calendar_outlook.microsoft_calendar_requests.microsoft_post")
def test_get_schedule(mock_post, mock_token_manager):
    mock_post.return_value = (
        200,
        {
            "value": [
                {
                    "scheduleId": "user@example.com",
                    "availabilityView": "000222000",
                }
            ]
        }
    )

    schedule_params = ScheduleParams(
        schedules=["user@example.com"],
        start_time=DateTimeTimeZone(dateTime="2025-06-28T08:00:00", timeZone="UTC"),
        end_time=DateTimeTimeZone(dateTime="2025-06-28T17:00:00", timeZone="UTC"),
        availability_view_interval=60
    )

    client = MicrosoftCalendarRequests(mock_token_manager)
    result = json.loads(client.get_schedule(schedule_params))

    assert "value" in result
    assert result["value"][0]["scheduleId"] == "user@example.com"

import json
import pytest
from unittest.mock import patch, MagicMock

from src.utils.calendar_outlook.microsoft_calendar_groups_requests import MicrosoftCalendarGroupsRequests
from src.utils.param_types import CalendarGroupParams


@pytest.fixture
def mock_token_manager():
    mock = MagicMock()
    mock.get_token.return_value = "fake_token"
    return mock


@patch("src.utils.calendar_outlook.microsoft_calendar_groups_requests.microsoft_get")
def test_get_calendar_groups(mock_get, mock_token_manager):
    mock_get.return_value = (
        200,
        {
            "value": [
                {"id": "group1", "name": "Calendario Principal"},
                {"id": "group2", "name": "Eventos"},
            ]
        },
    )

    params = CalendarGroupParams(top=2, filter_name=None)
    client = MicrosoftCalendarGroupsRequests(mock_token_manager)
    response = json.loads(client.get_calendar_groups(params))

    assert isinstance(response, list)
    assert len(response) == 2
    assert response[0]["id"] == "group1"


@patch("src.utils.calendar_outlook.microsoft_calendar_groups_requests.microsoft_get")
def test_get_calendar_groups_with_filter(mock_get, mock_token_manager):
    mock_get.return_value = (
        200,
        {
            "value": [
                {"id": "group2", "name": "Eventos"},
            ]
        },
    )

    params = CalendarGroupParams(top=1, filter_name="Eventos")
    client = MicrosoftCalendarGroupsRequests(mock_token_manager)
    response = json.loads(client.get_calendar_groups(params))

    assert isinstance(response, list)
    assert len(response) == 1
    assert response[0]["name"] == "Eventos"


@patch("src.utils.calendar_outlook.microsoft_calendar_groups_requests.microsoft_post")
def test_create_calendar_group(mock_post, mock_token_manager):
    mock_post.return_value = (
        201,
        {"id": "new123", "name": "Nuevo Grupo"}
    )

    client = MicrosoftCalendarGroupsRequests(mock_token_manager)
    response = json.loads(client.create_calendar_group("Nuevo Grupo"))

    assert response["id"] == "new123"
    assert response["name"] == "Nuevo Grupo"


@patch("src.utils.calendar_outlook.microsoft_calendar_groups_requests.microsoft_patch")
def test_update_calendar_group(mock_patch, mock_token_manager):
    mock_patch.return_value = (
        200,
        {"id": "grp123", "name": "Nombre Actualizado"}
    )

    client = MicrosoftCalendarGroupsRequests(mock_token_manager)
    response = json.loads(client.update_calendar_group("grp123", "Nombre Actualizado"))

    assert response["id"] == "grp123"
    assert response["name"] == "Nombre Actualizado"


@patch("src.utils.calendar_outlook.microsoft_calendar_groups_requests.microsoft_delete")
def test_delete_calendar_group_success(mock_delete, mock_token_manager):
    mock_delete.return_value = (204, None)

    client = MicrosoftCalendarGroupsRequests(mock_token_manager)
    response = json.loads(client.delete_calendar_group("grp123"))

    assert response["status"] == "deleted"

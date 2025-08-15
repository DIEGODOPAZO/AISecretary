import json
import pytest
from unittest.mock import patch, MagicMock

from src.utils.to_do.microsoft_to_do_lists_requests import MicrosoftToDoListsRequests

@pytest.fixture
def mock_token_manager():
    mock = MagicMock()
    mock.get_token.return_value = "fake_token"
    return mock



@patch.object(MicrosoftToDoListsRequests, "microsoft_get")
def test_get_todo_lists(mock_get, mock_token_manager):
    mock_get.return_value = (
        200,
        [
            {"id": "1", "displayName": "List1"},
            {"id": "2", "displayName": "List2"},
        ],
    )

    client = MicrosoftToDoListsRequests(mock_token_manager)
    response = json.loads(client.get_todo_lists())

    assert isinstance(response, list)
    assert response[0]["id"] == "1"
    assert response[1]["displayName"] == "List2"


@patch.object(MicrosoftToDoListsRequests, "microsoft_post")
def test_create_todo_list(mock_post, mock_token_manager):
    mock_post.return_value = (201, {"id": "new123", "displayName": "NewList"})

    client = MicrosoftToDoListsRequests(mock_token_manager)
    response = json.loads(client.create_todo_list("NewList"))

    assert response["id"] == "new123"
    assert response["displayName"] == "NewList"


@patch.object(MicrosoftToDoListsRequests, "microsoft_delete")
def test_delete_todo_list_success(mock_delete, mock_token_manager):
    mock_delete.return_value = (204, {})

    client = MicrosoftToDoListsRequests(mock_token_manager)
    response = json.loads(client.delete_todo_list("list123"))

    assert "message" in response
    assert "deleted successfully" in response["message"]


@patch.object(MicrosoftToDoListsRequests, "microsoft_delete")
def test_delete_todo_list_failure(mock_delete, mock_token_manager):
    mock_delete.return_value = (400, {"error": "Failed to delete"})

    client = MicrosoftToDoListsRequests(mock_token_manager)
    response = json.loads(client.delete_todo_list("list123"))

    assert "error" in response
    assert response["error"]["error"] == "Failed to delete"

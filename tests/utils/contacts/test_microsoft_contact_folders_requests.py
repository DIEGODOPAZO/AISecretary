import json
import pytest
from unittest.mock import patch, MagicMock

from src.utils.contacts.microsoft_contact_folders_requests import MicrosoftContactFoldersRequests

@pytest.fixture
def mock_token_manager():
    mock = MagicMock()
    mock.get_token.return_value = "fake_token"
    return mock

@patch.object(MicrosoftContactFoldersRequests, "microsoft_post")
def test_create_contact_folder(mock_post, mock_token_manager):
    mock_post.return_value = (
        201,
        {"id": "folder123", "displayName": "Clientes"}
    )

    client = MicrosoftContactFoldersRequests(mock_token_manager)
    response = json.loads(client.create_contact_folder("Clientes"))

    assert response["id"] == "folder123"
    assert response["displayName"] == "Clientes"


@patch.object(MicrosoftContactFoldersRequests, "microsoft_get")
def test_get_contact_folders(mock_get, mock_token_manager):
    mock_get.return_value = (
        200,
        {
            "value": [
                {"id": "folder1", "displayName": "Clientes"},
                {"id": "folder2", "displayName": "Proveedores"}
            ]
        }
    )

    client = MicrosoftContactFoldersRequests(mock_token_manager)
    response = json.loads(client.get_contact_folders())

    assert isinstance(response, dict)
    assert "value" in response
    assert len(response["value"]) == 2
    assert response["value"][0]["id"] == "folder1"


@patch.object(MicrosoftContactFoldersRequests, "microsoft_delete")
def test_delete_contact_folder_success(mock_delete, mock_token_manager):
    mock_delete.return_value = (204, None)

    client = MicrosoftContactFoldersRequests(mock_token_manager)
    response = json.loads(client.delete_contact_folder("folder1"))

    assert response["message"] == "Contact folder deleted successfully."


@patch.object(MicrosoftContactFoldersRequests, "microsoft_delete")
def test_delete_contact_folder_not_found(mock_delete, mock_token_manager):
    mock_delete.return_value = (404, None)

    client = MicrosoftContactFoldersRequests(mock_token_manager)
    response = json.loads(client.delete_contact_folder("folder999"))

    assert response["error"] == "Contact folder not found."

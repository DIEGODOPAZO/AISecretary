import json
import pytest
from unittest.mock import patch, MagicMock

from src.utils.email.microsoft_folders_requests import MicrosoftFoldersRequests
from src.utils.param_types import FolderParams


@pytest.fixture
def mock_token_manager():
    mock = MagicMock()
    mock.get_token.return_value = "fake_token"
    return mock


@patch("src.utils.email.microsoft_folders_requests.microsoft_get")
def test_get_folder_names(mock_get, mock_token_manager):
    mock_get.return_value = (
        200,
        {
            "value": [
                {"id": "1", "displayName": "Inbox", "totalItemCount": 10},
                {"id": "2", "displayName": "Sent", "totalItemCount": 5},
            ],
            "@odata.nextLink": "https://next.link",
        },
    )

    client = MicrosoftFoldersRequests(mock_token_manager)
    response = json.loads(client.get_folder_names())

    assert "folders" in response
    assert len(response["folders"]) == 2
    assert response["nextLink"] == "https://next.link"


@patch("src.utils.email.microsoft_folders_requests.microsoft_get")
def test_get_subfolders(mock_get, mock_token_manager):
    mock_get.return_value = (
        200,
        {"value": [{"id": "sub1", "displayName": "SubFolder", "totalItemCount": 3}]},
    )

    client = MicrosoftFoldersRequests(mock_token_manager)
    response = json.loads(client.get_subfolders_microsoft_api("folder123"))

    assert "folders" in response
    assert response["folders"][0]["folder_id"] == "sub1"


@patch("src.utils.email.microsoft_folders_requests.microsoft_post")
def test_create_folder(mock_post, mock_token_manager):
    mock_post.return_value = (201, {"id": "new123", "displayName": "NewFolder"})

    params = FolderParams(folder_name="NewFolder")
    client = MicrosoftFoldersRequests(mock_token_manager)
    response = json.loads(client.create_edit_folder_microsoft_api(params))

    assert response["id"] == "new123"


@patch("src.utils.email.microsoft_folders_requests.microsoft_patch")
def test_edit_folder(mock_patch, mock_token_manager):
    mock_patch.return_value = (200, {"id": "edit123", "displayName": "EditedFolder"})

    params = FolderParams(folder_name="EditedFolder", folder_id="edit123")
    client = MicrosoftFoldersRequests(mock_token_manager)
    response = json.loads(client.create_edit_folder_microsoft_api(params))

    assert response["id"] == "edit123"


@patch("src.utils.email.microsoft_folders_requests.microsoft_post")
def test_create_subfolder(mock_post, mock_token_manager):
    mock_post.return_value = (201, {"id": "sub123", "displayName": "SubFolder"})

    params = FolderParams(folder_name="SubFolder", parent_folder_id="parent456")
    client = MicrosoftFoldersRequests(mock_token_manager)
    response = json.loads(client.create_edit_folder_microsoft_api(params))

    assert response["id"] == "sub123"


@patch("src.utils.email.microsoft_folders_requests.microsoft_delete")
def test_delete_folder_success(mock_delete, mock_token_manager):
    mock_delete.return_value = (204, {})

    client = MicrosoftFoldersRequests(mock_token_manager)
    response = json.loads(client.delete_folder_microsoft_api("folder123"))

    assert "message" in response
    assert "deleted successfully" in response["message"]


@patch("src.utils.email.microsoft_folders_requests.microsoft_delete")
def test_delete_folder_failure(mock_delete, mock_token_manager):
    mock_delete.return_value = (400, {"error": "Failed"})

    client = MicrosoftFoldersRequests(mock_token_manager)
    response = json.loads(client.delete_folder_microsoft_api("folder123"))

    assert "error" in response

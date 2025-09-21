import json
import pytest
from unittest.mock import patch, MagicMock

from src.utils.to_do.microsoft_to_do_tasks_requests import MicrosoftToDoTasksRequests
from src.utils.param_types import TaskCreateRequest, TodoTaskFilter


@pytest.fixture
def mock_token_manager():
    mock = MagicMock()
    mock.get_token.return_value = "fake_token"
    return mock


@patch.object(MicrosoftToDoTasksRequests, "microsoft_get")
def test_get_tasks_in_list(mock_get, mock_token_manager):
    mock_get.return_value = (
        200,
        {
            "value": [
                {"id": "1", "title": "Task 1", "status": "notStarted"},
                {"id": "2", "title": "Task 2", "status": "completed"},
            ]
        },
    )

    client = MicrosoftToDoTasksRequests(mock_token_manager)
    response = json.loads(client.get_tasks_in_list("list123"))

    assert isinstance(response, list)
    assert response[0]["title"] == "Task 1"
    assert response[1]["status"] == "completed"


@patch.object(MicrosoftToDoTasksRequests, "microsoft_get")
def test_get_task_in_list(mock_get, mock_token_manager):
    mock_get.return_value = (
        200,
        {"id": "1", "title": "My Task", "status": "inProgress"},
    )

    client = MicrosoftToDoTasksRequests(mock_token_manager)
    response = json.loads(client.get_task_in_list("list123", "1"))

    assert response["id"] == "1"
    assert response["title"] == "My Task"
    assert response["status"] == "inProgress"


@patch.object(MicrosoftToDoTasksRequests, "microsoft_post")
def test_create_task_in_list(mock_post, mock_token_manager):
    mock_post.return_value = (
        201,
        {"id": "new-task", "title": "New Task", "status": "notStarted"},
    )

    mock_task = MagicMock(spec=TaskCreateRequest)
    mock_task.to_json_object.return_value = {
        "title": "New Task",
        "status": "notStarted"
    }

    client = MicrosoftToDoTasksRequests(mock_token_manager)
    response = json.loads(client.create_update_task_in_list("list123", mock_task))

    assert response["id"] == "new-task"
    assert response["title"] == "New Task"


@patch.object(MicrosoftToDoTasksRequests, "microsoft_patch")
def test_update_task_in_list(mock_patch, mock_token_manager):
    mock_patch.return_value = (
        200,
        {"id": "task-id", "title": "Updated Task", "status": "inProgress"},
    )

    mock_task = MagicMock(spec=TaskCreateRequest)
    mock_task.to_json_object.return_value = {
        "title": "Updated Task",
        "status": "inProgress"
    }

    client = MicrosoftToDoTasksRequests(mock_token_manager)
    response = json.loads(client.create_update_task_in_list("list123", mock_task, task_id="task-id"))

    assert response["id"] == "task-id"
    assert response["title"] == "Updated Task"


@patch.object(MicrosoftToDoTasksRequests, "microsoft_delete")
def test_delete_task_in_list(mock_delete, mock_token_manager):
    mock_delete.return_value = (204, {})

    client = MicrosoftToDoTasksRequests(mock_token_manager)
    response = client.delete_task_in_list("list123", "task-id")

    assert response == "Task deleted successfully."

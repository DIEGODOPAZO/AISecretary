import json
from typing import Optional

from ..param_types import TaskCreateRequest, TodoTaskFilter
from ..helper_functions.helpers_email import *
from ..helper_functions.general_helpers import (
    handle_microsoft_errors,
    microsoft_get,
    microsoft_post,
    microsoft_delete,
    microsoft_patch
)
from ..constants import TODO_TASK, TODO_TASK_BY_ID
from ..microsoft_base_request import MicrosoftBaseRequest


class MicrosoftToDoTasksRequests(MicrosoftBaseRequest):
    """
    Handles requests related to Microsoft To-Do tasks using Microsoft Graph API.
    Inherits from MicrosoftBaseRequest to manage authentication and token retrieval.
    """
    @handle_microsoft_errors
    def get_tasks_in_list(self, todo_list_id: str, task_filter: TodoTaskFilter = None, top: int = 100) -> str:
        """
        Retrieve tasks from a specified to-do list with optional filtering.

        Args:
            todo_list_id (str): ID of the to-do list.
            task_filter (TodoTaskFilter, optional): Filter criteria for tasks.

        Returns:
            str: JSON response containing the list of tasks.
        """
        url = TODO_TASK(todo_list_id)
        params = task_filter.to_odata_filter() if task_filter else None

        if params:
            params["$top"] = top
        else:
            params = {"$top": top}
        status_code, response = microsoft_get(
            url, self.token_manager.get_token(), params=params
        )

        simplified_tasks = [
            {
                "id": task["id"],
                "title": task["title"],
                "status": task["status"]
            }
            for task in response.get("value", [])
        ]

        return json.dumps(simplified_tasks, indent=2)

    @handle_microsoft_errors
    def get_task_in_list(self, todo_list_id: str, task_id: str) -> str:
        """
        Retrieve details of a specific task in a specified to-do list.

        Args:
            todo_list_id (str): ID of the to-do list.
            task_id (str): ID of the task to retrieve.

        Returns:
            str: JSON response containing the task details.
        """
        url = TODO_TASK_BY_ID(todo_list_id, task_id)

        status_code, response = microsoft_get(
            url, self.token_manager.get_token()
        )

        return json.dumps(response, indent=2)
    
    @handle_microsoft_errors
    def create_update_task_in_list(
        self, todo_list_id: str, task_create_requests: TaskCreateRequest, task_id: str = None
    ) -> str:
        """
        Create a new task in a specified to-do list.

        Args:
            todo_list_id (str): ID of the to-do list where the task will be created.
            task_create_requests (TaskCreateRequest): The request object containing task details.
            task_id (str, optional): ID of the task to update. If provided, it will update the existing task.

        Returns:
            str: JSON response with the created task details.
        """
        if task_id:
            return self._update_task_in_list(todo_list_id, task_id, task_create_requests)

        url = TODO_TASK(todo_list_id)
        data = task_create_requests.to_json_object()

        status_code, response = microsoft_post(
            url, self.token_manager.get_token(), data=data
        )

        return json.dumps(response, indent=2)

    def _update_task_in_list(
        self, todo_list_id: str, task_id: str, task_update_request: TaskCreateRequest
    ) -> str:
        """
        Update an existing task in a specified to-do list.

        Args:
            todo_list_id (str): ID of the to-do list.
            task_id (str): ID of the task to update.
            task_update_request (TaskCreateRequest): The request object containing updated task details.

        Returns:
            str: JSON response with the updated task details.
        """
        url = TODO_TASK_BY_ID(todo_list_id, task_id)
        data = task_update_request.to_json_object()

        status_code, response = microsoft_patch(
            url, self.token_manager.get_token(), data=data
        )

        return json.dumps(response, indent=2)

    @handle_microsoft_errors
    def delete_task_in_list(self, todo_list_id: str, task_id: str) -> str:
        """
        Delete a task from a specified to-do list.

        Args:
            todo_list_id (str): ID of the to-do list.
            task_id (str): ID of the task to delete.

        Returns:
            str: Confirmation message or error details.
        """
        url = TODO_TASK_BY_ID(todo_list_id, task_id)

        status_code, response = microsoft_delete(
            url, self.token_manager.get_token()
        )

        return json.dumps(response, indent=2) if response else "Task deleted successfully."
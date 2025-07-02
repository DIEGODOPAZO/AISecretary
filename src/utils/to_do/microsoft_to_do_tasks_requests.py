import json

from ..param_types import TaskCreateRequest
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
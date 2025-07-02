import json

from ..param_types import TaskCreateRequest
from ..helper_functions.helpers_email import *
from ..helper_functions.general_helpers import (
    handle_microsoft_errors,
    microsoft_get,
    microsoft_post,
    microsoft_delete,
)
from ..constants import TODO_TASK
from ..microsoft_base_request import MicrosoftBaseRequest


class MicrosoftToDoTasksRequests(MicrosoftBaseRequest):

    @handle_microsoft_errors
    def create_task_in_list(self, todo_list_id: str, task_create_requests: TaskCreateRequest) -> str:
        """
        Create a new task in a specified to-do list.

        Args:
            task_create_requests (TaskCreateRequest): The request object containing task details.

        Returns:
            str: JSON response with the created task details.
        """
        url = TODO_TASK(todo_list_id)
        data = task_create_requests.to_json_object()
        
        status_code, response = microsoft_post(url, self.token_manager.get_token(), data=data)

        return json.dumps(response, indent=2)
import json

from ..param_types import *
from ..helper_functions.helpers_email import *
from ..token_manager import TokenManager
from ..helper_functions.general_helpers import (
    handle_microsoft_errors,
    microsoft_get,
    microsoft_post,
    microsoft_delete,
)
from ..constants import TODO_LISTS_URL
from ..microsoft_base_request import MicrosoftBaseRequest


class MicrosoftToDoListsRequests(MicrosoftBaseRequest):
    @handle_microsoft_errors
    def get_todo_lists(self) -> str:
        """
        Get the list of to-do lists.

        Returns:
            list: List of to-do lists.
        """
        status_code, response = microsoft_get(TODO_LISTS_URL, self.token_manager.get_token())

        return json.dumps(response, indent=2)

    @handle_microsoft_errors
    def create_todo_list(self, list_name: str) -> str:
        """
        Create a new to-do list.

        Args:
            list_name (str): Name of the new to-do list.

        Returns:
            str: JSON response with the created to-do list details.
        """
        data = {"displayName": list_name}
        status_code, response = microsoft_post(TODO_LISTS_URL, self.token_manager.get_token(), data=data)

        return json.dumps(response, indent=2)
    
    @handle_microsoft_errors
    def delete_todo_list(self, list_id: str) -> str:
        """
        Delete a to-do list by its ID.

        Args:
            list_id (str): ID of the to-do list to delete.

        Returns:
            str: Confirmation message or error details.
        """
        url = f"{TODO_LISTS_URL}/{list_id}"
        status_code, response = microsoft_delete(url, self.token_manager.get_token())

        if status_code == 204:
            return json.dumps({"message": "To-do list deleted successfully."}, indent=2)
        else:
            return json.dumps({"error": response}, indent=2)
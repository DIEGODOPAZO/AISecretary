from typing import Optional
from utils.token_manager import TokenManager
from mcp.server.fastmcp import FastMCP
from utils.param_types import TaskCreateRequest
from utils.to_do.microsoft_to_do_lists_requests import MicrosoftToDoListsRequests
from utils.to_do.microsoft_to_do_tasks_requests import MicrosoftToDoTasksRequests

# Create an MCP server
mcp = FastMCP("ToDo-AISecretary-Outlook", dependencies=["mcp[cli]", "msal"])

token_manager = TokenManager()

to_do_lists_requests = MicrosoftToDoListsRequests(token_manager)
to_do_tasks_requests = MicrosoftToDoTasksRequests(token_manager)

@mcp.tool()
def get_todo_lists() -> str:
    """
    Retrieves the list of to-do lists from Microsoft To-Do.

    Returns:
        str: JSON string containing the list of to-do lists.
    """
    return to_do_lists_requests.get_todo_lists()

@mcp.tool()
def create_todo_list(list_name: str) -> str:
    """
    Creates a new to-do list in Microsoft To-Do.

    Args:
        list_name (str): Name of the new to-do list.

    Returns:
        str: JSON string containing the details of the created to-do list.
    """
    return to_do_lists_requests.create_todo_list(list_name)

@mcp.tool()
def delete_todo_list(list_id: str) -> str:
    """
    Deletes a to-do list by its ID in Microsoft To-Do.

    Args:
        list_id (str): ID of the to-do list to delete.

    Returns:
        str: Confirmation message or error details.
    """
    return to_do_lists_requests.delete_todo_list(list_id)

@mcp.tool()
def get_tasks_in_list(todo_list_id: str, task_filter: Optional[TaskCreateRequest] = None, top: int = 100) -> str:
    """
    Retrieves tasks from a specified to-do list with optional filtering.

    Args:
        todo_list_id (str): ID of the to-do list.
        task_filter (Optional[TaskCreateRequest]): Filter parameters for the tasks.
        top (int): Maximum number of tasks to retrieve.

    Returns:
        str: JSON string containing the list of tasks in the specified to-do list.
    """
    return to_do_tasks_requests.get_tasks_in_list(todo_list_id, task_filter=task_filter, top=top)
@mcp.tool()
def get_task_in_list(todo_list_id: str, task_id: str) -> str:
    """
    Retrieves details of a specific task in a specified to-do list.

    Args:
        todo_list_id (str): ID of the to-do list.
        task_id (str): ID of the task to retrieve.

    Returns:
        str: JSON string containing the details of the specified task.
    """
    return to_do_tasks_requests.get_task_in_list(todo_list_id, task_id)

@mcp.tool()
def create_update_task_in_list(todo_list_id: str, task_create_request: TaskCreateRequest, task_id: Optional[str]) -> str:
    """
    Creates or updates a new task in a specified to-do list.

    Args:
        todo_list_id (str): ID of the to-do list where the task will be created.
        task_create_request (TaskCreateReques): the dataclass containing the details of the task to create.
        task_id (Optional[str]): ID of the task to update. If provided, it will update the existing task.
    Returns:
        str: JSON string containing the details of the created task.
    """
    return to_do_tasks_requests.create_update_task_in_list(todo_list_id, task_create_request, task_id=task_id)

@mcp.tool()
def delete_task_in_list(todo_list_id: str, task_id: str) -> str:
    """
    Deletes a task from a specified to-do list.

    Args:
        todo_list_id (str): ID of the to-do list.
        task_id (str): ID of the task to delete.

    Returns:
        str: Confirmation message or error details.
    """
    return to_do_tasks_requests.delete_task_in_list(todo_list_id, task_id)

if __name__ == "__main__":
    mcp.run()
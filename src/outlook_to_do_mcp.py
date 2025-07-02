from utils.token_manager import TokenManager
from utils.auth_microsoft import get_access_token, load_expiration_time_from_file
from mcp.server.fastmcp import FastMCP

from utils.to_do.microsoft_to_do_lists_requests import MicrosoftToDoListsRequests

# Create an MCP server
mcp = FastMCP("ToDo-AISecretary-Outlook", dependencies=["mcp[cli]", "msal"])

token_manager = TokenManager(
    get_access_token_func=get_access_token, get_expiration_time=load_expiration_time_from_file
)

to_do_lists_requests = MicrosoftToDoListsRequests(token_manager)

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

if __name__ == "__main__":
    mcp.run()
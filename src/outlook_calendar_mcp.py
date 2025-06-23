from typing import Optional
from utils.token_manager import TokenManager
from utils.auth_microsoft import get_access_token, get_token_cache_path
from utils.calendar.microsoft_events_requests import MicrosoftEventsRequests
from utils.param_types import EventParams
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("AISecretary-Outlook-Calendar", dependencies=["mcp[cli]", "msal"])

token_manager = TokenManager(
    get_token_cache_path(), get_access_token_func=get_access_token
)
events_requests = MicrosoftEventsRequests(token_manager)

@mcp.tool()
def create_event_outlook_calendar(
    event_params: EventParams,
    folder_id: Optional[str] = None,
) -> str:
    """
    Create an event in the Outlook calendar.

    Args:
        folder_id (str): The ID of the calendar folder where the event will be created.
        event_params (EventParams): The parameters for the event to be created.

    Returns:
        str: A JSON string containing the response from the Microsoft Graph API.
    """
    return events_requests.create_event(event_params, folder_id)
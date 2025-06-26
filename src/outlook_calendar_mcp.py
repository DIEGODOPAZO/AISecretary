from typing import Optional
from utils.calendar_outlook.microsoft_calendar_groups_requests import MicrosoftCalendarGroupsRequests
from utils.token_manager import TokenManager
from utils.auth_microsoft import get_access_token, get_token_cache_path
from utils.calendar_outlook.microsoft_events_requests import MicrosoftEventsRequests
from utils.param_types import EventParams, EventQuery, CalendarGroupParams, EventResponseParams
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("AISecretary-Outlook-Calendar", dependencies=["mcp[cli]", "msal"])

token_manager = TokenManager(
    get_token_cache_path(), get_access_token_func=get_access_token
)
events_requests = MicrosoftEventsRequests(token_manager)
calendar_groups = MicrosoftCalendarGroupsRequests(token_manager)

@mcp.tool()
def get_events_outlook_calendar(
    event_search_params: EventQuery,
    calendar_id: Optional[str] = None,
) -> str:
    """
    Get events from the Outlook calendar.

    Args:
        event_search_params (EventSearchParams): The parameters to search for events.
        calendar_id (str): The ID of the calendar to retrieve events from.

    Returns:
        str: A JSON string containing the list of events.
    """
    
    return events_requests.get_events(event_search_params, calendar_id)

@mcp.tool()
def get_event_full_information(event_id: str) -> str:
    """
    Get full information about a specific event in the Outlook calendar.

    Args:
        event_id (str): The ID of the event to retrieve information for.

    Returns:
        str: A JSON string containing the full information of the event.
    """
    return events_requests.get_event(event_id)

@mcp.tool()
def create_event_outlook_calendar(
    event_params: EventParams,
    calendar_id: Optional[str] = None,
) -> str:
    """
    Create an event in the Outlook calendar, it also can put file attachments on the event.

    Args:
        event_params (EventParams): The parameters for the event to be created. 
        calendar_id (str): The ID of the calendar where the event will be created.

    Returns:
        str: A JSON string containing the response from the Microsoft Graph API.
    """
    return events_requests.create_event(event_params, calendar_id)

@mcp.tool()
def update_event_outlook_calendar(
    event_id: str,
    event_params: EventParams
) -> str:
    """
    Update an event in the Outlook calendar, can also uptade its attachents.

    Args:
        event_params (EventParams): The parameters for the event to be updated.
        calendar_id (str): The ID of the calendar where the event is located.

    Returns:
        str: A JSON string containing the response from the Microsoft Graph API.
    """
    return events_requests.update_event(event_id, event_params)

@mcp.tool()
def delete_attachment_from_event(
    event_id: str,
    attachment_id: str
) -> str:
    """
    Delete an attachment from an event in the Outlook calendar.

    Args:
        event_id (str): The ID of the event from which the attachment will be deleted.
        attachment_id (str): The ID of the attachment to be deleted.

    Returns:
        str: A JSON string containing the response from the Microsoft Graph API.
    """
    return events_requests.delete_event_attachment(event_id, attachment_id)

@mcp.tool()
def delete_event_outlook_calendar(event_id: str) -> str:
    """
    Delete an event from the Outlook calendar.

    Args:
        event_id (str): The ID of the event to be deleted.

    Returns:
        str: A JSON string containing the response from the Microsoft Graph API.
    """
    return events_requests.delete_event(event_id)

@mcp.tool()
def accept_event(event_id: str, event_response_params: EventResponseParams) -> str:
    """
    Confirm your assistance to an event.

    Args:
        event_id (str): The ID of the event to attend
        event_response_params (EventResponseParams): The parameters for the response to the invitation
    """

    return events_requests.accept_event_invitation(event_id, event_response_params)


@mcp.tool()
def get_calendar_groups(calendar_group_params: CalendarGroupParams) -> str:
    """
    Get calendar groups from the Outlook calendar.

    Returns:
        str: A JSON string containing the list of calendar groups.
    """
    return calendar_groups.get_calendar_groups(calendar_group_params)


@mcp.tool()
def create_calendar_group(calendar_group_name: str) -> str:
    """
    Create a new calendar group in the Outlook calendar.

    Args:
        calendar_group_name (str): The name of the calendar group to be created.

    Returns:
        str: A JSON string containing the response from the Microsoft Graph API.
    """
    return calendar_groups.create_calendar_group(calendar_group_name)

@mcp.tool()
def update_calendar_group(
    calendar_group_id: str,
    calendar_group_name: str
) -> str:
    """
    Update an existing calendar group in the Outlook calendar.

    Args:
        calendar_group_id (str): The ID of the calendar group to be updated.
        calendar_group_name (str): The new name for the calendar group.

    Returns:
        str: A JSON string containing the response from the Microsoft Graph API.
    """
    return calendar_groups.update_calendar_group(calendar_group_id, calendar_group_name)

@mcp.tool()
def delete_calendar_group(calendar_group_id: str) -> str:
    """
    Delete a calendar group in the Outlook calendar.

    Args:
        calendar_group_id (str): The ID of the calendar group to be deleted.

    Returns:
        str: A JSON string containing the response from the Microsoft Graph API.
    """
    return calendar_groups.delete_calendar_group(calendar_group_id)
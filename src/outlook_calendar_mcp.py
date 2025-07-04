from typing import Optional
from utils.calendar_outlook.microsoft_calendar_requests import MicrosoftCalendarRequests
from utils.calendar_outlook.microsoft_calendar_groups_requests import (
    MicrosoftCalendarGroupsRequests,
)
from utils.token_manager import TokenManager
from utils.auth_microsoft import get_access_token, load_expiration_time_from_file
from utils.calendar_outlook.microsoft_events_requests import MicrosoftEventsRequests
from utils.param_types import (
    CalendarUpdateParams,
    EventChangesParams,
    EventParams,
    EventQuery,
    CalendarGroupParams,
    EventResponseParams,
    ScheduleParams,
)
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Calendar-AISecretary-Outlook", dependencies=["mcp[cli]", "msal"])

token_manager = TokenManager(
    get_access_token_func=get_access_token, get_expiration_time=load_expiration_time_from_file
)
events_requests = MicrosoftEventsRequests(token_manager)
calendar_groups = MicrosoftCalendarGroupsRequests(token_manager)
calendars = MicrosoftCalendarRequests(token_manager)


@mcp.tool()
def get_events_outlook_calendar(
    event_search_params: EventQuery,
    calendar_id: Optional[str] = None,
) -> str:
    """
    Gets events from the Outlook calendar.

    Args:
        event_search_params (EventQuery): Parameters to search for events.
        calendar_id (Optional[str], optional): The ID of the calendar to retrieve events from. Defaults to None.

    Returns:
        str: JSON string containing the list of events.
    """
    return events_requests.get_events(event_search_params, calendar_id)


@mcp.tool()
def get_event_full_information(event_id: str) -> str:
    """
    Gets full information about a specific event in the Outlook calendar.

    Args:
        event_id (str): The ID of the event to retrieve information for.

    Returns:
        str: JSON string containing the full information of the event.
    """
    return events_requests.get_event(event_id)


@mcp.tool()
def create_event_outlook_calendar(
    event_params: EventParams,
    calendar_id: Optional[str] = None,
) -> str:
    """
    Creates an event in the Outlook calendar. Can also add file attachments to the event.

    Args:
        event_params (EventParams): Parameters for the event to be created.
        calendar_id (Optional[str], optional): The ID of the calendar where the event will be created. Defaults to None.

    Returns:
        str: JSON string containing the response from the Microsoft Graph API.
    """
    return events_requests.create_event(event_params, calendar_id)


@mcp.tool()
def update_event_outlook_calendar(event_id: str, event_params: EventParams) -> str:
    """
    Updates an event in the Outlook calendar. Can also update its attachments.

    Args:
        event_id (str): The ID of the event to update.
        event_params (EventParams): Parameters for the event to be updated.

    Returns:
        str: JSON string containing the response from the Microsoft Graph API.
    """
    return events_requests.update_event(event_id, event_params)


@mcp.tool()
def delete_attachment_from_event(event_id: str, attachment_id: str) -> str:
    """
    Deletes an attachment from an event in the Outlook calendar.

    Args:
        event_id (str): The ID of the event from which the attachment will be deleted.
        attachment_id (str): The ID of the attachment to be deleted.

    Returns:
        str: JSON string containing the response from the Microsoft Graph API.
    """
    return events_requests.delete_event_attachment(event_id, attachment_id)


@mcp.tool()
def delete_event_outlook_calendar(event_id: str) -> str:
    """
    Deletes an event from the Outlook calendar.

    Args:
        event_id (str): The ID of the event to be deleted.

    Returns:
        str: JSON string containing the response from the Microsoft Graph API.
    """
    return events_requests.delete_event(event_id)


@mcp.tool()
def accept_invitation_to_event(
    event_id: str, event_response_params: EventResponseParams
) -> str:
    """
    Confirms attendance to an event.

    Args:
        event_id (str): The ID of the event to attend.
        event_response_params (EventResponseParams): Parameters for the response to the invitation.

    Returns:
        str: JSON string containing the response from the Microsoft Graph API.
    """
    return events_requests.accept_event_invitation(event_id, event_response_params)


@mcp.tool()
def decline_invitation_to_event(
    event_id: str, event_changes_params: EventChangesParams
) -> str:
    """
    Declines an invitation to an event.

    Args:
        event_id (str): The ID of the event to decline.
        event_changes_params (EventChangesParams): Parameters for the response to the invitation.

    Returns:
        str: JSON string containing the response from the Microsoft Graph API.
    """
    return events_requests.decline_event_invitation(event_id, event_changes_params)


@mcp.tool()
def tentatively_accept_event_invitation(
    event_id: str, event_changes_params: EventChangesParams
) -> str:
    """
    Tentatively accepts an invitation to an event and can suggest changes.

    Args:
        event_id (str): The ID of the event to tentatively accept.
        event_changes_params (EventChangesParams): Parameters for the response to the invitation.

    Returns:
        str: JSON string containing the response from the Microsoft Graph API.
    """
    return events_requests.tentatively_accept_event_invitation(
        event_id, event_changes_params
    )


@mcp.tool()
def cancel_event(event_id: str, comment: Optional[str]) -> str:
    """
    Cancels an event.

    Args:
        event_id (str): The ID of the event to cancel.
        comment (Optional[str]): Comment to send to all attendees of the event.

    Returns:
        str: JSON string containing the response from the Microsoft Graph API.
    """
    return events_requests.cancel_event(event_id, comment)


@mcp.tool()
def get_calendar_groups(calendar_group_params: CalendarGroupParams) -> str:
    """
    Gets calendar groups from the Outlook calendar.

    Args:
        calendar_group_params (CalendarGroupParams): Parameters to filter or search calendar groups.

    Returns:
        str: JSON string containing the list of calendar groups.
    """
    return calendar_groups.get_calendar_groups(calendar_group_params)


@mcp.tool()
def create_calendar_group(calendar_group_name: str) -> str:
    """
    Creates a new calendar group in the Outlook calendar.

    Args:
        calendar_group_name (str): The name of the calendar group to be created.

    Returns:
        str: JSON string containing the response from the Microsoft Graph API.
    """
    return calendar_groups.create_calendar_group(calendar_group_name)


@mcp.tool()
def update_calendar_group(calendar_group_id: str, calendar_group_name: str) -> str:
    """
    Updates an existing calendar group in the Outlook calendar.

    Args:
        calendar_group_id (str): The ID of the calendar group to be updated.
        calendar_group_name (str): The new name for the calendar group.

    Returns:
        str: JSON string containing the response from the Microsoft Graph API.
    """
    return calendar_groups.update_calendar_group(calendar_group_id, calendar_group_name)


@mcp.tool()
def delete_calendar_group(calendar_group_id: str) -> str:
    """
    Deletes a calendar group in the Outlook calendar.

    Args:
        calendar_group_id (str): The ID of the calendar group to be deleted.

    Returns:
        str: JSON string containing the response from the Microsoft Graph API.
    """
    return calendar_groups.delete_calendar_group(calendar_group_id)


@mcp.tool()
def get_calendars(
    calendar_group_id: Optional[str] = None, name: Optional[str] = None
) -> str:
    """
    Retrieves calendars from the Outlook calendar.

    Args:
        calendar_group_id (Optional[str]): The ID of the calendar group to filter calendars. If None, all calendars are retrieved.
        name (Optional[str]): The name of the calendar to filter (it filters an exact match).

    Returns:
        str: JSON string containing the list of calendars.
    """
    return calendars.get_calendars(calendar_group_id, name)


@mcp.tool()
def get_calendar(calendar_id: str) -> str:
    """
    Retrieves a specific calendar from the Outlook calendar.

    Args:
        calendar_id (str): The ID of the calendar to be retrieved.

    Returns:
        str: JSON string containing the details of the calendar.
    """
    return calendars.get_calendar(calendar_id)


@mcp.tool()
def create_calendar(calendar_name: str, calendar_group_id: Optional[str] = None) -> str:
    """
    Creates a new calendar in the Outlook calendar.

    Args:
        calendar_name (str): The name of the calendar to be created.
        calendar_group_id (Optional[str]): The ID of the calendar group where the calendar will be created. If None, the calendar is created in the default group.

    Returns:
        str: JSON string containing the response from the Microsoft Graph API.
    """
    return calendars.create_calendar(calendar_name, calendar_group_id)


@mcp.tool()
def update_calendar(
    calendar_id: str, calendar_update_params: CalendarUpdateParams
) -> str:
    """
    Updates an existing calendar in the Outlook calendar.

    Args:
        calendar_id (str): The ID of the calendar to be updated.
        calendar_update_params (CalendarUpdateParams): Parameters for the calendar to be updated.

    Returns:
        str: JSON string containing the response from the Microsoft Graph API.
    """
    return calendars.update_calendar(calendar_id, calendar_update_params)


@mcp.tool()
def delete_calendar(calendar_id: str) -> str:
    """
    Deletes a calendar in the Outlook calendar.

    Args:
        calendar_id (str): The ID of the calendar to be deleted.

    Returns:
        str: JSON string containing the response from the Microsoft Graph API.
    """
    return calendars.delete_calendar(calendar_id)


@mcp.tool()
def get_schedule(schedule_params: ScheduleParams) -> str:
    """
    Gets the availability (free/busy) of one or more users.

    Args:
        schedule_params (ScheduleParams): Parameters for the schedule request, including the users and time range.

    Returns:
        str: JSON string containing the availability information.
    """
    return calendars.get_schedule(schedule_params)


@mcp.resource("outlook://calendars")
def get_calendars_resource() -> str:
    """
    Gets the calendars of the Outlook mailbox.

    Returns:
        str: A JSON string containing the calendars.
    """
    return calendars.get_calendars()


@mcp.prompt()
def create_event_at_calendar_prompt(
    event_name: str,
    start_time: str,
    end_time: str,
    calendar_name: str,
    day: str,
    month: str,
    year: str,
    location: Optional[str] = None,
    description: Optional[str] = None,
) -> str:
    """
    Creates a prompt for creating an event in the Outlook calendar.

    Args:
        event_name (str): The name of the event.
        start_time (str): The start time of the event in ISO 8601 format.
        end_time (str): The end time of the event in ISO 8601 format.
        location (Optional[str]): The location of the event. Defaults to None.
        description (Optional[str]): A description of the event. Defaults to None.

    Returns:
        str: A prompt string for creating an event.
    """
    return f"Fisrtly I want you to look for a calendar with a similar name to {calendar_name} and obtain its id, you can do this by geting the information about the calendars with the tool get_calendars. Then: Create an event named '{event_name}' starting at {start_time} and ending at {end_time}. Location: {location if location else 'No location provided'}. Description: {description if description else 'No description provided'}. The event will be created in the calendar with the id obtained from the previous step. The day of the event is {day}, the month is {month}, and the year is {year}. If you cannot find a calendar with a similar name, create a new calendar with that name and then create the event in it."

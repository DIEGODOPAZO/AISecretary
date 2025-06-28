import json
from ..token_manager import TokenManager
from ..helper_functions.general_helpers import (
    microsoft_get,
    handle_microsoft_errors,
    microsoft_post,
    microsoft_patch,
    microsoft_delete
    )


class MicrosoftCalendarRequests:
    """
    This class is a placeholder for Microsoft Calendar API requests.
    """

    def __init__(self, token_manager: TokenManager):
        """
        """
        self.token_manager = token_manager
        self.url = "https://graph.microsoft.com/v1.0/me"

    def _get_url(self, calendar_group_id: str = None) -> str:
        """
        Constructs the URL for Microsoft Graph API requests.

        Args:
            calendar_id (str): The ID of the calendar. If None, the base URL is returned.

        Returns:
            str: The complete URL for the request.
        """
        if calendar_group_id:
            return f"{self.url}/calendarGroups/{calendar_group_id}/calendars"
        return f"{self.url}/calendars"
    
    @handle_microsoft_errors
    def get_calendars(self, calendar_group_id: str = None, name: str = None) -> str:
        """
        Retrieves calendars from Microsoft Graph API.

        Args:
            calendar_group_id (str): The ID of the calendar group to filter calendars. If None, all calendars are retrieved.
            name (str): The name of the calendar to filter.

        Returns:
            str: A JSON string containing the calendars.
        """

        final_url = self._get_url(calendar_group_id)
        

        status_code, response = microsoft_get(
            final_url, self.token_manager.get_token()
        )
        
        if name:
            response["value"] = [
                calendar for calendar in response.get("value", [])
                if calendar.get("name") == name
            ]

        return json.dumps(response.get("value", []), indent=2)
    
    @handle_microsoft_errors
    def create_calendar(self, calendar_name: str, calendar_group_id: str = None) -> str:
        """
        Creates a new calendar in Microsoft Graph API.

        Args:
            calendar_name (str): The name of the calendar to be created.
            calendar_group_id (str): The ID of the calendar group where the calendar will be created. If None, the calendar is created in the default group.

        Returns:
            str: A JSON string containing the response from the API.
        """
        final_url = self._get_url(calendar_group_id)
        
        data = {
            "name": calendar_name
        }
        
        status_code, response = microsoft_post(
            final_url, 
            self.token_manager.get_token(), 
            data=data
        )
        
        return json.dumps(response, indent=2)
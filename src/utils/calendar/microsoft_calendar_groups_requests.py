import json

from ..param_types import CalendarGroupParams
from ..token_manager import TokenManager
from ..helper_functions.general_helpers import (
    microsoft_get,
    handle_microsoft_errors,
    microsoft_post
    )

class MicrosoftCalendarGroupsRequests:

    def __init__(self, token_manage: TokenManager):
        """
        Initializes the MicrosoftCalendarGroupsRequests with a token manager.
        
        :param token_manage: An instance of TokenManager to handle authentication tokens.
        """
        self.token_manage = token_manage
        self.url = "https://graph.microsoft.com/v1.0/me/calendarGroups"

    @handle_microsoft_errors
    def get_calendar_groups(self, calendar_group_params: CalendarGroupParams) -> str:
        """
        Retrieves calendar groups from Microsoft Graph API.
        
        :return: A JSON string containing the calendar groups.
        """
        params = {
            "top": calendar_group_params.top,
            "filter": f"name eq '{calendar_group_params.filter_name}'" if calendar_group_params.filter_name else None
        }
        status_code, response = microsoft_get(
            self.url, self.token_manage.get_token(), params=params
        )
        
        return json.dumps(response.get("value", []), indent=2)
    
    @handle_microsoft_errors
    def create_calendar_group(self, calendar_group_name: str) -> str:
        """
        Creates a new calendar group in Microsoft Graph API.
        
        :param calendar_group_name: The name of the calendar group to be created.
        :return: A JSON string containing the response from the API.
        """
        data = {
            "name": calendar_group_name
        }
        
        status_code, response = microsoft_post(
            self.url, 
            self.token_manage.get_token(), 
            data=data
        )
        
        return json.dumps(response, indent=2)
    
    
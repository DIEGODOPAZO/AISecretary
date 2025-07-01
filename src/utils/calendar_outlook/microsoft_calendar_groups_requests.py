import json

from ..param_types import CalendarGroupParams
from ..token_manager import TokenManager
from ..helper_functions.general_helpers import (
    microsoft_get,
    handle_microsoft_errors,
    microsoft_post,
    microsoft_patch,
    microsoft_delete,
)
from ..microsoft_base_request import MicrosoftBaseRequest
from ..constants import CALENDAR_GROUPS_URL


class MicrosoftCalendarGroupsRequests(MicrosoftBaseRequest):
    @handle_microsoft_errors
    def get_calendar_groups(self, calendar_group_params: CalendarGroupParams) -> str:
        """
        Retrieves calendar groups from Microsoft Graph API.

        Args:
            calendar_group_params (CalendarGroupParams): Parameters for filtering and limiting the calendar groups.

        Returns:
            str: A JSON string containing the calendar groups.
        """
        params = {
            "top": calendar_group_params.top,
            "filter": (
                f"name eq '{calendar_group_params.filter_name}'"
                if calendar_group_params.filter_name
                else None
            ),
        }
        status_code, response = microsoft_get(
            CALENDAR_GROUPS_URL, self.token_manager.get_token(), params=params
        )

        return json.dumps(response.get("value", []), indent=2)

    @handle_microsoft_errors
    def create_calendar_group(self, calendar_group_name: str) -> str:
        """
        Creates a new calendar group in Microsoft Graph API.

        Args:
            calendar_group_name (str): The name of the calendar group to be created.

        Returns:
            str: A JSON string containing the response from the API.
        """
        data = {"name": calendar_group_name}

        status_code, response = microsoft_post(
            CALENDAR_GROUPS_URL, self.token_manager.get_token(), data=data
        )

        return json.dumps(response, indent=2)

    @handle_microsoft_errors
    def update_calendar_group(
        self, calendar_group_id: str, calendar_group_name: str
    ) -> str:
        """
        Updates an existing calendar group in Microsoft Graph API.

        Args:
            calendar_group_id (str): The ID of the calendar group to be updated.
            calendar_group_name (str): The new name for the calendar group.

        Returns:
            str: A JSON string containing the response from the API.
        """
        url = f"{CALENDAR_GROUPS_URL}/{calendar_group_id}"
        data = {"name": calendar_group_name}

        status_code, response = microsoft_patch(
            url, self.token_manager.get_token(), data=data
        )

        return json.dumps(response, indent=2)

    def delete_calendar_group(self, calendar_group_id: str) -> str:
        """
        Deletes a calendar group in Microsoft Graph API.

        Args:
            calendar_group_id (str): The ID of the calendar group to be deleted.

        Returns:
            str: A JSON string containing the response from the API or a status message if deleted.
        """
        url = f"{CALENDAR_GROUPS_URL}/{calendar_group_id}"

        status_code, response = microsoft_delete(url, self.token_manager.get_token())

        return (
            json.dumps(response, indent=2)
            if response
            else json.dumps({"status": "deleted"}, indent=2)
        )

from dataclasses import asdict
import json

from ..helper_functions.helpers_calendar import simplify_calendar
from ..param_types import CalendarUpdateParams, ScheduleParams
from ..token_manager import TokenManager
from ..helper_functions.general_helpers import (
    microsoft_get,
    handle_microsoft_errors,
    microsoft_post,
    microsoft_patch,
    microsoft_delete,
)
from ..constants import GRAPH_BASE_URL

class MicrosoftCalendarRequests:

    def __init__(self, token_manager: TokenManager):
        """
        Initializes the MicrosoftCalendarGroupsRequests with a token manager.

        Args:
            token_manage (TokenManager): An instance of TokenManager to handle authentication tokens.
        """
        self.token_manager = token_manager
        

    def _get_url(self, calendar_group_id: str = None) -> str:
        """
        Constructs the URL for Microsoft Graph API requests.

        Args:
            calendar_id (str): The ID of the calendar. If None, the base URL is returned.

        Returns:
            str: The complete URL for the request.
        """
        if calendar_group_id:
            return f"{GRAPH_BASE_URL}/calendarGroups/{calendar_group_id}/calendars"
        return f"{GRAPH_BASE_URL}/calendars"

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

        status_code, response = microsoft_get(final_url, self.token_manager.get_token())

        if name:
            response["value"] = [
                calendar
                for calendar in response.get("value", [])
                if calendar.get("name") == name
            ]
        simplify_calendars = []
        calendars = response.get("value", [])
        for calendar in calendars:
            simplify_calendars.append(simplify_calendar(calendar))
        return json.dumps({"calendars: ": simplify_calendars}, indent=2)

    @handle_microsoft_errors
    def get_calendar(self, calendar_id: str) -> str:
        """
        Retrieves a specific calendar from Microsoft Graph API.

        Args:
            calendar_id (str): The ID of the calendar to be retrieved.

        Returns:
            str: A JSON string containing the details of the calendar.
        """
        url = f"{self._get_url()}/{calendar_id}"

        status_code, response = microsoft_get(url, self.token_manager.get_token())

        return json.dumps(response, indent=2)

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

        data = {"name": calendar_name}

        status_code, response = microsoft_post(
            final_url, self.token_manager.get_token(), data=data
        )

        return json.dumps(response, indent=2)

    @handle_microsoft_errors
    def update_calendar(
        self, calendar_id: str, calendar_update_params: CalendarUpdateParams
    ) -> str:
        """
        Updates an existing calendar in Microsoft Graph API.

        Args:
            calendar_id (str): The ID of the calendar to be updated.
            calendar_name (str): The new name for the calendar.

        Returns:
            str: A JSON string containing the response from the API.
        """
        url = f"{self._get_url()}/{calendar_id}"
        data = {"name": calendar_update_params.name}

        if calendar_update_params.color:
            data["color"] = calendar_update_params.color
        if calendar_update_params.isDefaultCalendar:
            data["isDefaultCalendar"] = calendar_update_params.isDefaultCalendar

        status_code, response = microsoft_patch(
            url, self.token_manager.get_token(), data=data
        )

        return json.dumps(response, indent=2)

    @handle_microsoft_errors
    def delete_calendar(self, calendar_id: str) -> str:
        """
        Deletes a calendar from Microsoft Graph API.

        Args:
            calendar_id (str): The ID of the calendar to be deleted.

        Returns:
            str: A JSON string containing the response from the API.
        """
        url = f"{self._get_url()}/{calendar_id}"

        status_code, response = microsoft_delete(url, self.token_manager.get_token())
        if status_code != 204:
            return json.dumps({"error": "Failed to delete calendar"}, indent=2)
        response = {
            "message": "Calendar deleted successfully",
            "status_code": status_code,
        }
        return json.dumps(response, indent=2)

    @handle_microsoft_errors
    def get_schedule(self, schedule_params: ScheduleParams) -> str:
        """
        Retrieves the schedule of a user or a list of users.

        Args:
            schedule_params (ScheduleParams): Parameters for the schedule request.

        Returns:
            str: A JSON string containing the schedule information.
        """
        url = f"{self.url}/calendar/getSchedule"
        data = {
            "schedules": schedule_params.schedules,
            "startTime": asdict(schedule_params.start_time),
            "endTime": asdict(schedule_params.end_time),
            "availabilityViewInterval": schedule_params.availability_view_interval,
        }

        status_code, response = microsoft_post(
            url, self.token_manager.get_token(), data=data
        )

        return json.dumps(response, indent=2)

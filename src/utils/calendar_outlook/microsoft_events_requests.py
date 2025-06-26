from typing import List
import json
from ..token_manager import TokenManager
from ..param_types import EventChangesParams, EventParams, EventQuery, EventResponseParams
from ..helper_functions.general_helpers import (
    download_attachments,
    handle_microsoft_errors,
    microsoft_get,
    microsoft_post,
    microsoft_patch,
    microsoft_delete,
    read_file_and_encode_base64,
)
from ..helper_functions.helpers_calendar import (
    event_query_to_graph_params,
    simplify_event,
    event_params_to_dict,
    simplify_event_with_attachment_names,
)


class MicrosoftEventsRequests:
    def __init__(self, token_manager: TokenManager):
        self.token_manager = token_manager
        self.url = "https://graph.microsoft.com/v1.0/me/calendar"
        self.event_response_url = "https://graph.microsoft.com/v1.0/me/events"

    def _get_url(self, calendar_id: str = None) -> str:
        if calendar_id is None:
            return f"{self.url}/events"
        else:
            return f"{self.url}/{calendar_id}/events"

    def _add_attachment(
        self, url: str, response_id: str, attachments: List[str]
    ) -> int:
        for file in attachments:
            file_name, encoded_content = read_file_and_encode_base64(file)
            attachment = {
                "@odata.type": "#microsoft.graph.fileAttachment",
                "name": file_name,
                "contentBytes": encoded_content,
                "contentType": "application/pdf",
            }

            url_attachment = f"{url}/{response_id}/attachments"

            status_code, response_attachment = microsoft_post(
                url_attachment, self.token_manager.get_token(), data=attachment
            )
            return status_code

    @handle_microsoft_errors
    def get_events(self, event_query: EventQuery, calendar_id: str = None) -> str:
        params = event_query_to_graph_params(event_query)
        url = self._get_url(calendar_id)

        has_filter = "filter" in params
        has_dates = "startDateTime" in params and "endDateTime" in params

        response_filter = None
        response_dates = None

        if has_filter:
            filter_params = {
                k: v
                for k, v in params.items()
                if k not in ("search", "startDateTime", "endDateTime")
            }
            status_code, response_filter = microsoft_get(
                url, self.token_manager.get_token(), params=filter_params
            )
            response_filter = [
                simplify_event(e) for e in response_filter.get("value", [])
            ]
        if has_dates:
            date_params = {
                k: v for k, v in params.items() if k not in ("search", "filter")
            }
            if calendar_id is not None:
                calendar_url = (
                    f"https://graph.microsoft.com/v1.0/me/{calendar_id}/calendarView"
                )
            else:
                calendar_url = f"https://graph.microsoft.com/v1.0/me/calendarView"
            status_code, response_dates = microsoft_get(
                calendar_url, self.token_manager.get_token(), params=date_params
            )
            response_dates = [
                simplify_event(e) for e in response_dates.get("value", [])
            ]

        if has_filter:
            response_final = response_filter
            if has_dates:
                date_ids = {msg["id"] for msg in response_dates}
                response_final = [
                    msg for msg in response_final if msg["id"] in date_ids
                ]
        elif has_dates:
            response_final = response_dates
        else:
            status_code, response = microsoft_get(
                url, self.token_manager.get_token(), params=params
            )
            response_final = [simplify_event(e) for e in response.get("value", [])]

        return json.dumps(response_final, indent=2)

    @handle_microsoft_errors
    def get_event(self, event_id:str):
        url = self._get_url()
        url = f"{url}/{event_id}"
        status_code, response = microsoft_get(
            url, self.token_manager.get_token()
        )
        response = simplify_event_with_attachment_names(response, self.token_manager.get_token())
        
        attachments_url = f"{url}/attachments"
        status_code, attachments_response = microsoft_get(
            attachments_url, self.token_manager.get_token()
        )
        attachments = attachments_response.get("value", [])
        
        response["attachments"] = download_attachments(attachments)
        return json.dumps(response, indent=2)

    @handle_microsoft_errors
    def create_event(self, event_params: EventParams, calendar_id: str = None) -> str:
        url = self._get_url(calendar_id)

        data = event_params_to_dict(event_params)
        status_code, response = microsoft_post(
            url, self.token_manager.get_token(), data=data
        )
        response = simplify_event(response)

        response_id = response.get("id", "")

        if event_params.attachments:
            status_code = self._add_attachment(
                url, response_id, event_params.attachments
            )
            if status_code != 201:
                return json.dumps({"error": "Failed to add attachments"}, indent=2)
        return json.dumps(response, indent=2)

    @handle_microsoft_errors
    def update_event(self, event_id: str, event_params: EventParams) -> str:
        url = self._get_url()

        data = event_params_to_dict(event_params)
        status_code, response = microsoft_patch(
            f"{url}/{event_id}", self.token_manager.get_token(), data=data
        )

        response = simplify_event(response)
        response_id = response.get("id", "")

        if event_params.attachments:
            status_code = self._add_attachment(
                url, response_id, event_params.attachments
            )
            if status_code != 201:
                return json.dumps({"error": "Failed to add attachments"}, indent=2)
        return json.dumps(response, indent=2)

    @handle_microsoft_errors
    def delete_event_attachment(self, event_id: str, attachment_id: str) -> str:
        url = self._get_url()

        status_code, response = microsoft_delete(
            f"{url}/{event_id}/attachments/{attachment_id}",
            self.token_manager.get_token(),
        )

        if status_code == 204:
            return json.dumps({"message": "Attachment deleted successfully"}, indent=2)
        else:
            return json.dumps({"error": "Failed to delete attachment"}, indent=2)

    @handle_microsoft_errors
    def delete_event(self, event_id: str) -> str:
        url = self._get_url()

        status_code, response = microsoft_delete(
            f"{url}/{event_id}", self.token_manager.get_token()
        )

        if status_code == 204:
            return json.dumps({"message": "Event deleted successfully"}, indent=2)
        else:
            return json.dumps({"error": "Failed to delete event"}, indent=2)

    @handle_microsoft_errors
    def accept_event_invitation(self, event_id: str, event_response_params: EventResponseParams) -> str:
        data = {
            "sendResponse": event_response_params.send_response
        }
        if event_response_params.comment is not None:
            data["comment"] = event_response_params.comment
        status_code, response = microsoft_post(f"{self.event_response_url}/{event_id}/accept", self.token_manager.get_token(), data=data)
        if status_code == 202:
            return json.dumps({"message": "Event invitation accepted"}, indent=2)
        else:
            return json.dumps({"error": "Failed to accept event invitation"}, indent=2)
        
    @handle_microsoft_errors
    def decline_event_invitation(self, event_id: str, event_changes_params: EventChangesParams) -> str:
        data = {
        "sendResponse": event_changes_params.event_response_params.send_response
        }

        if event_changes_params.event_response_params.comment is not None:
            data["comment"] = event_changes_params.event_response_params.comment

        
        if event_changes_params.proposed_new_time is not None:
            data["proposedNewTime"] = {
                "start": {
                    "dateTime": event_changes_params.proposed_new_time.start.dateTime,
                    "timeZone": event_changes_params.proposed_new_time.start.timeZone,
                },
                "end": {
                    "dateTime": event_changes_params.proposed_new_time.end.dateTime,
                    "timeZone": event_changes_params.proposed_new_time.end.timeZone,
                },
            }
        
        status_code, response = microsoft_post(f"{self.event_response_url}/{event_id}/decline", self.token_manager.get_token(), data=data)

        if status_code == 202:
            return json.dumps({"message": "Event invitation declined"}, indent=2)
        else:
            return json.dumps({"error": "Failed to accept event invitation"}, indent=2)
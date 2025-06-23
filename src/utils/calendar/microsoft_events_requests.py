import json
from ..token_manager import TokenManager
from ..helpers import handle_microsoft_errors
from ..param_types import EventParams
from ..helpers import (
    microsoft_get,
    microsoft_post,
    microsoft_patch,
    microsoft_delete,
    simplify_event,
    event_params_to_dict,
)


class MicrosoftEventsRequests:
    def __init__(self, token_manager: TokenManager):
        self.token_manager = token_manager
        self.url = "https://graph.microsoft.com/v1.0/me/calendar"

    @handle_microsoft_errors
    def get_events(self):
        pass

    @handle_microsoft_errors
    def get_event(self):
        pass

    @handle_microsoft_errors
    def create_event(self, event_params: EventParams, folder_id: str = None):
        if folder_id is None:
            url = f"{self.url}/events"
        else:
            url = f"{self.url}/{folder_id}/events"

        # Convert the EventParams dataclass to a dictionary
        data = event_params_to_dict(event_params)
        status_code, response = microsoft_post(url, self.token_manager.get_token(), data=data)
        response = simplify_event(response)

        return json.dumps(response, indent=2)

    @handle_microsoft_errors
    def update_event(self):
        pass

    @handle_microsoft_errors
    def delete_event(self):
        pass

import json

from ..param_types import *
from ..helpers import *
from ..token_manager import TokenManager


class MicrosoftFlagRequests:
    BASE_URL = "https://graph.microsoft.com/v1.0/me/messages/{email_id}"

    def __init__(self, token_manager: TokenManager):
        self.token_manager = token_manager

    @handle_microsoft_errors
    def manage_flags_microsoft_api(self, email_id: str, flag: str):
        url = MicrosoftFlagRequests.BASE_URL.format(email_id=email_id)
        if flag not in ["complete", "notFlagged", "flagged"]:
            return json.dumps({"error": "Not valid flag submited"}, indent=2)

        data = {"flag": {"flagStatus": f"{flag}"}}

        status_code, response = microsoft_patch(
            url, self.token_manager.get_token(), data=data
        )
        response = microsoft_simplify_message(response)
        return json.dumps(response, indent=2)

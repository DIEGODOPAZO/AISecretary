import json

from ..param_types import *
from ..auth_microsoft import get_access_token_microsoft
from ..helpers import *


class MicrosoftFlagRequests:
    BASE_URL = "https://graph.microsoft.com/v1.0/me/messages/{email_id}"

    @staticmethod
    @handle_microsoft_errors
    def manage_flags_microsoft_api(email_id: str, flag: str):
        token = get_access_token_microsoft()
        url = MicrosoftFlagRequests.BASE_URL.format(email_id=email_id)
        if flag not in ["complete", "notFlagged", "flagged"]:
            return json.dumps({"error": "Not valid flag submited"}, indent=2)

        data = {"flag": {"flagStatus": f"{flag}"}}

        status_code, response = microsoft_patch(url, token, data=data)

        return json.dumps(response, indent=2)

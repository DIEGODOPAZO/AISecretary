import json

from ..param_types import *
from ..helper_functions.helpers_email import *
from ..token_manager import TokenManager
from ..helper_functions.general_helpers import handle_microsoft_errors, microsoft_patch


class MicrosoftFlagRequests:
    """Handles flag management for Microsoft Outlook emails via Microsoft Graph API.

    This class provides methods to set or update the flag status of an email message using the Microsoft Graph API.
    """
    BASE_URL = "https://graph.microsoft.com/v1.0/me/messages/{email_id}"

    def __init__(self, token_manager: TokenManager):
        """Initializes MicrosoftFlagRequests with a TokenManager.

        Args:
            token_manager (TokenManager): An instance of TokenManager to handle authentication tokens.
        """
        self.token_manager = token_manager

    @handle_microsoft_errors
    def manage_flags_microsoft_api(self, email_id: str, flag: str):
        """Sets or updates the flag status of an email message.

        Args:
            email_id (str): The unique identifier of the email message to flag.
            flag (str): The flag status to set. Must be one of 'complete', 'notFlagged', or 'flagged'.

        Returns:
            str: A JSON-formatted string containing the API response or an error message if the flag is invalid.
        """
        url = MicrosoftFlagRequests.BASE_URL.format(email_id=email_id)
        if flag not in ["complete", "notFlagged", "flagged"]:
            return json.dumps({"error": "Not valid flag submited"}, indent=2)

        data = {"flag": {"flagStatus": f"{flag}"}}

        status_code, response = microsoft_patch(
            url, self.token_manager.get_token(), data=data
        )
        response = microsoft_simplify_message(response)
        return json.dumps(response, indent=2)

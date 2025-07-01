import json

from ..param_types import *
from ..helper_functions.helpers_email import *
from ..token_manager import TokenManager
from ..helper_functions.general_helpers import (
    handle_microsoft_errors,
    microsoft_get,
    microsoft_post,
    microsoft_patch,
    microsoft_delete,
)
from ..constants import MESSAGE_RULES_URL, MESSAGE_RULES_URL_BY_ID_URL
from ..microsoft_base_request import MicrosoftBaseRequest


class MicrosoftRulesRequests(MicrosoftBaseRequest):
    """Handles Microsoft Graph API requests for Outlook message rules.

    This class provides methods to interact with the Microsoft Graph API for managing
    message rules in the user's inbox, including retrieving, creating, updating, and
    deleting rules.
    """

    @handle_microsoft_errors
    def get_message_rules_microsoft_api(self) -> str:
        """Retrieves all message rules from the user's inbox.

        Returns:
            str: A JSON-formatted string containing the list of message rules.
        """

        (status_code, response) = microsoft_get(
            MESSAGE_RULES_URL, self.token_manager.get_token()
        )
        return json.dumps(response, indent=2)

    @handle_microsoft_errors
    def create_message_rule_microsoft_api(
        self, mail_rule: MailRule, rule_id: Optional[str] = None
    ) -> str:
        """Creates or updates a message rule in the user's inbox.

        Args:
            mail_rule (MailRule): The mail rule to create or update.
            rule_id (Optional[str], optional): The ID of the rule to update. If None, a new rule is created.

        Returns:
            str: A JSON-formatted string containing the created or updated rule's details.
        """

        if rule_id:
            url = MESSAGE_RULES_URL_BY_ID_URL(rule_id)
            (status_code, response) = microsoft_patch(
                url,
                self.token_manager.get_token(),
                data=dataclass_to_clean_dict(mail_rule),
            )
        else:
            (status_code, response) = microsoft_post(
                MESSAGE_RULES_URL,
                self.token_manager.get_token(),
                data=dataclass_to_clean_dict(mail_rule),
            )
        return json.dumps(response, indent=2)

    @handle_microsoft_errors
    def delete_message_rule_microsoft_api(self, rule_id: str) -> str:
        """Deletes a message rule from the user's inbox.

        Args:
            rule_id (str): The ID of the rule to delete.

        Returns:
            str: A JSON-formatted string indicating success or containing an error message.
        """
        url = MESSAGE_RULES_URL_BY_ID_URL(rule_id)
        (status_code, response) = microsoft_delete(url, self.token_manager.get_token())
        if status_code != 204:
            return json.dumps({"error": response}, indent=2)
        return json.dumps(
            {"message": f"Rule with ID {rule_id} deleted successfully."}, indent=2
        )

    @handle_microsoft_errors
    def get_next_link_microsoft_api(self, next_link: str) -> str:
        """Retrieves the next page of results from a paginated Microsoft Graph API response.

        Args:
            next_link (str): The URL for the next page of results.

        Returns:
            str: A JSON-formatted string containing the next page of results.
        """
        (status_code, response) = microsoft_get(
            next_link, self.token_manager.get_token()
        )
        return json.dumps(response, indent=2)

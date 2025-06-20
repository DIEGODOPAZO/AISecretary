import json

from ..param_types import *
from ..auth_microsoft import get_access_token_microsoft
from ..helpers import *


class MicrosoftRulesRequests:
    BASE_URL = "https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messageRules"

    def __init__(self):
        self.token = get_access_token_microsoft()

    @handle_microsoft_errors
    def get_message_rules_microsoft_api(self) -> str:
        url = self.BASE_URL
        (status_code, response) = microsoft_get(url, self.token)
        return json.dumps(response, indent=2)

    @handle_microsoft_errors
    def create_message_rule_microsoft_api(
        self, mail_rule: MailRule, rule_id: Optional[str] = None
    ) -> str:
        url = self.BASE_URL
        if rule_id:
            url = f"{url}/{rule_id}"
            (status_code, response) = microsoft_patch(
                url, self.token, data=dataclass_to_clean_dict(mail_rule)
            )
        else:
            (status_code, response) = microsoft_post(
                url, self.token, data=dataclass_to_clean_dict(mail_rule)
            )
        return json.dumps(response, indent=2)

    @handle_microsoft_errors
    def delete_message_rule_microsoft_api(self, rule_id: str) -> str:
        url = f"{self.BASE_URL}/{rule_id}"
        (status_code, response) = microsoft_delete(url, self.token)
        if status_code != 204:
            return json.dumps({"error": response}, indent=2)
        return json.dumps(
            {"message": f"Rule with ID {rule_id} deleted successfully."}, indent=2
        )

    @handle_microsoft_errors
    def get_next_link_microsoft_api(self, next_link: str) -> str:
        (status_code, response) = microsoft_get(next_link, self.token)
        return json.dumps(response, indent=2)

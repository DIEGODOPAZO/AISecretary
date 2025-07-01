from dataclasses import asdict
import json
from typing import Optional
from ..token_manager import TokenManager
from ..helper_functions.general_helpers import (
    handle_microsoft_errors,
    microsoft_post,
    microsoft_get,
)

from ..microsoft_base_request import MicrosoftBaseRequest
from ..constants import CONTACTS_BY_FOLDER_URL, CONTACTS_URL
from ..param_types import Contact


class MicrosoftContactsRequests(MicrosoftBaseRequest):

    def get_contacts(
        self, folder_id: Optional[str] = None, name: Optional[str] = None
    ) -> str:
        """
        Retrieves all contacts from Microsoft Outlook.

        Args:
            name (Optional[str]): Optional name filter for contacts.

        Returns:
            str: A JSON string containing the API response with the list of contacts.
        """
        params = {}
        if name:
            params["$filter"] = f"startswith(displayName, '{name}')"

        url = CONTACTS_BY_FOLDER_URL(folder_id) if folder_id else CONTACTS_URL
        status_code, response = microsoft_get(
            url, self.token_manager.get_token(), params=params
        )
        return json.dumps(response, indent=2)

    def create_contact(self, contact: Contact, folder_id: Optional[str] = None) -> str:
        """
        Creates a new contact in Microsoft Outlook.

        Args:
            contact (Contact): The contact information to create.
            folder_id (Optional[str]): The ID of the contact folder where the contact will be created.

        Returns:
            str: A JSON string containing the API response with the created contact details.
        """
        data = asdict(contact)
        url = CONTACTS_BY_FOLDER_URL(folder_id) if folder_id else CONTACTS_URL
        status_code, response = microsoft_post(
            url, self.token_manager.get_token(), data=data
        )
        return json.dumps(response, indent=2)

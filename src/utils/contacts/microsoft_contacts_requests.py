from dataclasses import asdict
import json
from typing import Optional
from ..microsoft_base_request import MicrosoftBaseRequest
from ..constants import CONTACTS_BY_FOLDER_URL, CONTACTS_BY_ID_URL, CONTACTS_URL
from ..param_types import Contact


class MicrosoftContactsRequests(MicrosoftBaseRequest):
    """    
    Handles Microsoft Graph API requests related to contacts for a user's mailbox.
    Inherits from MicrosoftBaseRequest to manage authentication and token retrieval.
    """
    @MicrosoftBaseRequest.handle_microsoft_errors
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
        status_code, response = self.microsoft_get(
            url, self.token_manager.get_token(), params=params
        )
        simplified_contacts = [
            {
                "id": contact.get("id"),
                "givenName": contact.get("givenName"),
                "surname": contact.get("surname"),
            }
            for contact in response.get("value", [])
        ]

        return json.dumps(simplified_contacts, indent=2)

    @MicrosoftBaseRequest.handle_microsoft_errors
    def get_contact_info(self, contact_id: str) -> str:
        """
        Retrieves detailed information about a specific contact by its ID.

        Args:
            contact_id (str): The ID of the contact to retrieve.

        Returns:
            str: A JSON string containing the API response with the contact details.
        """
        url = f"{CONTACTS_URL}/{contact_id}"
        status_code, response = self.microsoft_get(url, self.token_manager.get_token())
        return json.dumps(response, indent=2)

    @MicrosoftBaseRequest.handle_microsoft_errors
    def create_edit_contact(
        self,
        contact: Contact,
        folder_id: Optional[str] = None,
        contact_id: Optional[str] = None,
    ) -> str:
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

        if contact_id:
            url = f"{url}/{contact_id}"
            status_code, response = self.microsoft_patch(
                url, self.token_manager.get_token(), data=data
            )

            return json.dumps(response, indent=2)

        status_code, response = self.microsoft_post(
            url, self.token_manager.get_token(), data=data
        )
        return json.dumps(response, indent=2)

    @MicrosoftBaseRequest.handle_microsoft_errors
    def delete_contact(self, contact_id: str) -> str:
        """
        Deletes a contact by its ID.

        Args:
            contact_id (str): The ID of the contact to delete.

        Returns:
            str: A message indicating the result of the operation.
        """
        url = CONTACTS_BY_ID_URL(contact_id)
        status_code, response = self.microsoft_delete(url, self.token_manager.get_token())
        if status_code == 204:
            return json.dumps({"message": "Contact deleted successfully."}, indent=2)
        else:
            return json.dumps({"error": "Failed to delete contact."}, indent=2)

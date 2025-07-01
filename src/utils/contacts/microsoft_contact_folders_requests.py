import json
from ..token_manager import TokenManager
from ..helper_functions.general_helpers import (
    handle_microsoft_errors,
    microsoft_post,
    microsoft_get,
    microsoft_delete,
)
from ..constants import CONTACT_FOLDERS_URL
from ..microsoft_base_request import MicrosoftBaseRequest


class MicrosoftContactFoldersRequests(MicrosoftBaseRequest):
    """
    Handles Microsoft Graph API requests related to contact folders for a user's mailbox.

    """

    @handle_microsoft_errors
    def create_contact_folder(self, folder_name: str) -> str:
        """
        Creates a new contact folder in Microsoft Outlook.

        Args:
            folder_name (str): The name of the contact folder to create.

        Returns:
            str: A JSON string containing the API response with the created folder details.
        """
        data = {"displayName": folder_name}

        status_code, response = microsoft_post(
            CONTACT_FOLDERS_URL, self.token_manager.get_token(), data=data
        )
        return json.dumps(response, indent=2)

    @handle_microsoft_errors
    def get_contact_folders(self) -> str:
        """
        Retrieves all contact folders from Microsoft Outlook.

        Returns:
            str: A JSON string containing the API response with the list of contact folders.
        """
        status_code, response = microsoft_get(
            CONTACT_FOLDERS_URL, self.token_manager.get_token()
        )
        return json.dumps(response, indent=2)

    @handle_microsoft_errors
    def delete_contact_folder(self, folder_id: str) -> str:
        """
        Deletes a contact folder by its ID.

        Args:
            folder_id (str): The ID of the contact folder to delete.

        Returns:
            str: A JSON string containing the API response confirming the deletion.
        """
        url = f"{CONTACT_FOLDERS_URL}/{folder_id}"
        status_code, response = microsoft_delete(url, self.token_manager.get_token())

        if status_code == 204:
            response = {"message": "Contact folder deleted successfully."}
        elif status_code == 404:
            response = {"error": "Contact folder not found."}

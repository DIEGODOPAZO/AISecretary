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
from ..constants import MAIL_FOLDER_CHILDREN_URL, MAIL_FOLDERS_URL
from ..microsoft_base_request import MicrosoftBaseRequest


class MicrosoftFoldersRequests(MicrosoftBaseRequest):
    """
    Handles Microsoft Graph API requests related to mail folders for a user's mailbox.

    This class provides methods to retrieve, create, edit, and delete mail folders using the Microsoft Graph API.
    """

    @handle_microsoft_errors
    def get_folder_names(self) -> str:
        """
        Retrieves the names and details of all mail folders in the user's mailbox.

        Returns:
            str: A JSON-formatted string containing a list of folders with their IDs, display names, and item counts. Includes '@odata.nextLink' if pagination is required.
        """
        (status_code, response) = microsoft_get(
            MAIL_FOLDERS_URL, self.token_manager.get_token()
        )
        folders = response.get("value", [])
        simplified_folders = []

        for folder in folders:
            simplified = {
                "folder_id": folder.get("id"),
                "displayName": folder.get("displayName"),
                "totalItemCount": folder.get("totalItemCount"),
            }
            simplified_folders.append(simplified)

        result = {"folders": simplified_folders}

        # Agregar @odata.nextLink si existe
        if "@odata.nextLink" in response:
            result["nextLink"] = response["@odata.nextLink"]

        return json.dumps(result, indent=2)

    @handle_microsoft_errors
    def get_subfolders_microsoft_api(self, folder_id: str) -> str:
        """
        Retrieves the subfolders of a specified mail folder.

        Args:
            folder_id (str): The ID of the parent folder whose subfolders are to be retrieved.

        Returns:
            str: A JSON-formatted string containing a list of subfolders with their IDs, display names, and item counts. Includes '@odata.nextLink' if pagination is required.
        """
        url = MAIL_FOLDER_CHILDREN_URL(folder_id)
        (status_code, response) = microsoft_get(url, self.token_manager.get_token())
        folders = response.get("value", [])
        simplified_folders = []

        for folder in folders:
            simplified = {
                "folder_id": folder.get("id"),
                "displayName": folder.get("displayName"),
                "totalItemCount": folder.get("totalItemCount"),
            }
            simplified_folders.append(simplified)

        result = {"folders": simplified_folders}

        if "@odata.nextLink" in response:
            result["nextLink"] = response["@odata.nextLink"]

        return json.dumps(result, indent=2)

    @handle_microsoft_errors
    def create_edit_folder_microsoft_api(self, folder_params: FolderParams) -> str:
        """
        Creates a new mail folder or edits an existing one in the user's mailbox.

        If 'parent_folder_id' is provided, creates a new child folder under the specified parent. If 'folder_id' is provided, edits the folder with that ID. Otherwise, creates a new folder at the root level.

        Args:
            folder_params (FolderParams): Parameters for the folder, including name, parent folder ID, and folder ID.

        Returns:
            str: A JSON-formatted string indicating the result of the operation or an error message if the folder name is missing.
        """
        url = MAIL_FOLDERS_URL
        data = {
            "displayName": folder_params.folder_name,
        }
        if not folder_params.folder_name:
            return json.dumps({"error": "Folder name is required."}, indent=2)

        if folder_params.parent_folder_id:
            url = MAIL_FOLDER_CHILDREN_URL(folder_params.parent_folder_id)
            (status_code, response) = microsoft_post(
                url, self.token_manager.get_token(), data
            )
        elif folder_params.folder_id:
            url = f"{url}/{folder_params.folder_id}"
            (status_code, response) = microsoft_patch(
                url, self.token_manager.get_token(), data
            )
        else:
            (status_code, response) = microsoft_post(
                url, self.token_manager.get_token(), data
            )

        return json.dumps(response, indent=2)

    @handle_microsoft_errors
    def delete_folder_microsoft_api(self, folder_id: str) -> str:
        """
        Deletes a mail folder from the user's mailbox.

        Args:
            folder_id (str): The ID of the folder to delete.

        Returns:
            str: A JSON-formatted string indicating success or an error message if the deletion fails.
        """
        url = f"{MAIL_FOLDERS_URL}/{folder_id}"
        (status_code, response) = microsoft_delete(url, self.token_manager.get_token())
        if status_code != 204:
            return json.dumps({"error": response}, indent=2)
        return json.dumps(
            {"message": f"Folder with ID {folder_id} deleted successfully."}, indent=2
        )

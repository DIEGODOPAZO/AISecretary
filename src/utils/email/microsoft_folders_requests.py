import json

from ..param_types import *
from ..helpers import *
from ..token_manager import TokenManager


class MicrosoftFoldersRequests:
    def __init__(self, token_manager: TokenManager):
        self.base_url = "https://graph.microsoft.com/v1.0/me/mailFolders"
        self.token_manager = token_manager

    @handle_microsoft_errors
    def get_folder_names(self) -> str:
        (status_code, response) = microsoft_get(
            self.base_url, self.token_manager.get_token()
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
        url = f"{self.base_url}/{folder_id}/childFolders"
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
        Creates or edits a folder in the user's mailbox.

        :param folder_name: The name of the folder to create or edit.
        :param folder_id: The ID of the folder to edit (if it exists).
        :return: JSON response indicating success or failure.
        """
        url = self.base_url
        data = {
            "displayName": folder_params.folder_name,
        }
        if not folder_params.folder_name:
            return json.dumps({"error": "Folder name is required."}, indent=2)

        if folder_params.parent_folder_id:
            url = f"{url}/{folder_params.parent_folder_id}/childFolders"
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
        Deletes a folder from the user's mailbox.

        :param folder_id: The ID of the folder to delete.
        :return: JSON response indicating success or failure.
        """
        url = f"{self.base_url}/{folder_id}"
        (status_code, response) = microsoft_delete(url, self.token_manager.get_token())
        if status_code != 204:
            return json.dumps({"error": response}, indent=2)
        return json.dumps(
            {"message": f"Folder with ID {folder_id} deleted successfully."}, indent=2
        )

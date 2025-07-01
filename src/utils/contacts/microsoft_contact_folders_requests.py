import json
from ..token_manager import TokenManager
from ..helper_functions.general_helpers import handle_microsoft_errors, microsoft_post, microsoft_get
from ..constants import CONTACT_FOLDERS_URL
class MicrosoftContactFoldersRequests:
    """
    Handles Microsoft Graph API requests related to contact folders for a user's mailbox.

    Attributes:
        token_manager (TokenManager): The token manager for authentication.
      
    """

    def __init__(self, token_manager: TokenManager):
        """
        Initializes MicrosoftContactFoldersRequests with a TokenManager.

        Args:
            token_manager (TokenManager): An instance of TokenManager to handle authentication tokens.
        """
        self.token_manager = token_manager
        

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


import json
from ..token_manager import TokenManager
from ..helper_functions.general_helpers import handle_microsoft_errors, microsoft_post

class MicrosoftContactFoldersRequests:
    def __init__(self, token_manager: TokenManager):
        """Initializes MicrosoftContactFoldersRequests with a TokenManager.

        Args:
            token_manager (TokenManager): An instance of TokenManager to handle authentication tokens.
        """
        self.token_manager = token_manager
        self.base_url = "https://graph.microsoft.com/v1.0/me/contactFolders"

    @handle_microsoft_errors
    def create_contact_folder(self, folder_name: str) -> str:
        """Creates a new contact folder in Microsoft Outlook.

        Args:
            folder_name (str): The name of the contact folder to create.

        Returns:
            dict: A dictionary containing the API response with the created folder details.
        """
        
        data = {"displayName": folder_name}

        status_code, response = microsoft_post(
            self.base_url, self.token_manager.get_token(), data=data
        )
        return json.dumps(response, indent=2)
    
    
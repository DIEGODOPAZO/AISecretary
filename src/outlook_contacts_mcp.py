from typing import Optional
from utils.token_manager import TokenManager
from utils.auth_microsoft import get_access_token, get_token_cache_path
from utils.contacts.microsoft_contact_folders_requests import MicrosoftContactFoldersRequests
from utils.contacts.microsoft_contacts_requests import MicrosoftContactsRequests
from utils.param_types import Contact
# server.py
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Contacts-AISecretary-Outlook", dependencies=["mcp[cli]", "msal"])

token_manager = TokenManager(
    get_token_cache_path(), get_access_token_func=get_access_token
)

contact_folders_requests = MicrosoftContactFoldersRequests(token_manager)
contacts = MicrosoftContactsRequests(token_manager)

@mcp.tool()
def create_contact_folder(folder_name: str) -> str:
    """Creates a new contact folder in Microsoft Outlook.

    Args:
        folder_name (str): The name of the contact folder to create.

    Returns:
        str: A message indicating the result of the operation.
    """
    response = contact_folders_requests.create_contact_folder(folder_name)
    
    return response

@mcp.tool()
def get_contact_folders() -> str:
    """Retrieves all contact folders from Microsoft Outlook.

    Returns:
        str: A JSON string containing the list of contact folders.
    """
    response = contact_folders_requests.get_contact_folders()
    
    return response

@mcp.tool()
def get_contacts(folder_id: Optional[str], name: str = None) -> str:
    """Retrieves contacts from a specific folder in Microsoft Outlook.

    Args:
        folder_id (Optional[str]): The ID of the contact folder.
        name (str, optional): Optional name filter for contacts.

    Returns:
        str: A JSON string containing the list of contacts.
    """
    response = contacts.get_contacts(folder_id, name)
    
    return response

@mcp.tool()
def create_contact(contact: Contact, folder_id: Optional[str]) -> str:
    """Creates a new contact in a specific folder in Microsoft Outlook.

    Args:
        contact (Contact): The contact information to create.
        folder_id (Optional[str]): The ID of the contact folder.

    Returns:
        str: A JSON string containing the details of the created contact.
    """
    response = contacts.create_contact(contact, folder_id)
    
    return response

if __name__ == "__main__":
    # Start the MCP server
    mcp.run()
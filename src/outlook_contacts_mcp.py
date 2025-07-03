from typing import Optional
from utils.token_manager import TokenManager
from utils.auth_microsoft import get_access_token, load_expiration_time_from_file
from utils.contacts.microsoft_contact_folders_requests import (
    MicrosoftContactFoldersRequests,
)
from utils.contacts.microsoft_contacts_requests import MicrosoftContactsRequests
from utils.param_types import Contact

# server.py
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Contacts-AISecretary-Outlook", dependencies=["mcp[cli]", "msal"])

token_manager = TokenManager(
    get_access_token_func=get_access_token, get_expiration_time=load_expiration_time_from_file
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
def delete_contact_folder(folder_id: str) -> str:
    """Deletes a contact folder by its ID.

    Args:
        folder_id (str): The ID of the contact folder to delete.

    Returns:
        str: A message indicating the result of the operation.
    """
    response = contact_folders_requests.delete_contact_folder(folder_id)

    return response


@mcp.tool()
def get_contacts(folder_id: Optional[str], name: str = None) -> str:
    """Retrieves contacts from a specific folder in Microsoft Outlook. If no folder ID is provided, it retrieves contacts from the default folder (this defaulf folder has no ID).

    Args:
        folder_id (Optional[str]): The ID of the contact folder.
        name (str, optional): Optional name filter for contacts.

    Returns:
        str: A JSON string containing the list of contacts.
    """
    response = contacts.get_contacts(folder_id, name)

    return response


@mcp.tool()
def get_contact_info(contact_id: str) -> str:
    """Retrieves detailed information about a specific contact by its ID.

    Args:
        contact_id (str): The ID of the contact to retrieve.

    Returns:
        str: A JSON string containing the details of the contact.
    """
    response = contacts.get_contact_info(contact_id)

    return response


@mcp.tool()
def create_update_contact(contact: Contact, folder_id: Optional[str], contact_id: Optional[str]) -> str:
    """Creates a new contact in a specific folder in Microsoft Outlook, if folder_id is None, it will be created in the default folder. If contact_id is provided, it updates the existing contact with that ID.

    Args:
        contact (Contact): The contact information to create.
        folder_id (Optional[str]): The ID of the contact folder.

    Returns:
        str: A JSON string containing the details of the created contact.
    """
    response = contacts.create_edit_contact(contact, folder_id, contact_id)

    return response

@mcp.tool()
def delete_contact(contact_id: str) -> str:
    """Deletes a contact by its ID.

    Args:
        contact_id (str): The ID of the contact to delete.

    Returns:
        str: A message indicating the result of the operation.
    """
    response = contacts.delete_contact(contact_id)

    return response

if __name__ == "__main__":
    # Start the MCP server
    mcp.run()

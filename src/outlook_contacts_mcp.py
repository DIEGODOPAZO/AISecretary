from utils.token_manager import TokenManager
from utils.auth_microsoft import get_access_token, get_token_cache_path
from utils.contacts.microsoft_contact_folders_requests import MicrosoftContactFoldersRequests
# server.py
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Contacts-AISecretary-Outlook", dependencies=["mcp[cli]", "msal"])

token_manager = TokenManager(
    get_token_cache_path(), get_access_token_func=get_access_token
)

contact_folders_requests = MicrosoftContactFoldersRequests(token_manager)

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

if __name__ == "__main__":
    # Start the MCP server
    mcp.run()
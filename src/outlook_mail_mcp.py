from utils.auth_microsoft import get_access_token_microsoft
from utils.microsoft_api_requests import get_request_microsoft_api, get_folder_names

# server.py
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("AISecretary", dependencies=["mcp[cli]", "msal"])

filter_dateTime = "receivedDateTime ge 2016-01-01T00:00:00Z" # Needed to have the params of orderBy in the filter

@mcp.tool()
def get_last_emails_outlook(number_emails: int, folder_id: str = "ALL", unread_only: bool = False) -> str:
    """
    Gets the last {number_emails} emails from the Outlook mailbox that were sent to the user.
    params:
        number_emails (int): The number of emails to retrieve.
        folder_id (str): The id of the folder from which to retrieve the emails. You can get the folder ids using the get_user_folders resource. If the string ALL is provided, it will search in all the folders.
        unread_only (bool): If True, only retrieves unread emails. Defaults to False.
    returns:
        str: A JSON string containing the emails.
    """
    params = {
        "$top": number_emails,
        "$orderBy": "receivedDateTime DESC"
    }

    return get_request_microsoft_api(params, folder_id=folder_id, unread_only=unread_only)

@mcp.tool()
def get_important_emails_outlook(number_emails: int = 10, folder_id: str = "ALL", unread_only: bool = False) -> str:
    """
    Gets the important emails from the Outlook mailbox that were sent to the user.
    params:
        number_emails (int): The number of important emails to retrieve, by default 10.
        folder_id (str): The id of the folder from which to retrieve the emails. You can get the folder ids using the get_user_folders resource. If the string ALL is provided, it will search in all the folders.
        unread_only (bool): If True, only retrieves unread emails. Defaults to False.
    returns:
        str: A JSON string containing the important emails.
    """
    
    params = {
        "$filter": f"{filter_dateTime} and importance eq 'high'",
        "$top": number_emails,
        "$orderBy": "receivedDateTime DESC"
    }
    return get_request_microsoft_api(params, folder_id=folder_id, unread_only=unread_only)

@mcp.tool()
def get_emails_from_mail_sender(sender_email: str, number_emails: int = 10, unread_only: bool = False) -> str:
    """
    Gets the emails from a specific sender's email address.
    params:
        sender_email (str): The email address of the sender.
        number_emails (int): The number of emails to retrieve, by default 10.
        unread_only (bool): If True, only retrieves unread emails. Defaults to False.
    returns:
        str: A JSON string containing the emails from the specified sender.
    """
   
    params = {
        "$filter": f"{filter_dateTime} and from/emailAddress/address eq '{sender_email}'",
        "$top": number_emails,
        "$orderBy": "receivedDateTime DESC"
    }

    return get_request_microsoft_api(params, unread_only=unread_only)

@mcp.tool()
def get_emails_with_keyword(keyword: str, number_emails: int = 10, folder_id: str = "ALL", unread_only: bool = False) -> str:
    """
    Gets the emails that contain a specific keyword in the subject or body.
    params:
        keyword (str): The keyword to search for in the emails.
        number_emails (int): The number of emails to retrieve, by default 10.
        folder_id (str): The id of the folder from which to retrieve the emails. You can get the folder ids using the get_user_folders resource. If the string ALL is provided, it will search in all the folders.
        unread_only (bool): If True, only retrieves unread emails. Defaults to False.
    returns:
        str: A JSON string containing the emails that match the keyword.
    """
    
    params = {
        "$seach": f"{keyword}",
        "$top": number_emails,
        "$orderBy": "receivedDateTime DESC"
    }
    
    return get_request_microsoft_api(params, folder_id=folder_id, unread_only=unread_only)

@mcp.resource("usersfolders://userFoldersInformation}")
def get_user_folders() -> str:
    """
    Gets the folders of the Outlook mailbox.
    returns:
        str: A JSON string containing the folders.
    """

    return get_folder_names()


if __name__ == "__main__":
    # Start the MCP server
    token = get_access_token_microsoft()
    mcp.run()
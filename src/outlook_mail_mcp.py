from utils.auth_microsoft import get_access_token_microsoft
from utils.microsoft_api_requests import get_request_microsoft_api
import urllib.parse
# server.py
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("AISecretary")
token = get_access_token_microsoft()

@mcp.tool()
def get_last_emails_outlook(number_emails: int) -> str:
    """
    Gets the last {number_emails} emails from the Outlook mailbox that were sent to the user.
    params:
        number_emails (int): The number of emails to retrieve.
    returns:
        str: A JSON string containing the emails.
    """
    params = {
        "$top": number_emails,
        "$orderBy": "receivedDateTime DESC"
    }
    return get_request_microsoft_api(params, token)

@mcp.tool()
def get_important_emails_outlook(number_emails: int = 10) -> str:
    """
    Gets the important emails from the Outlook mailbox that were sent to the user.
    params:
        number_emails (int): The number of important emails to retrieve, by default 10.
    returns:
        str: A JSON string containing the important emails.
    """
    
    params = {
        "$filter": "receivedDateTime ge 2016-01-01T00:00:00Z and importance eq 'high'",
        "$top": number_emails,
        "$orderBy": "receivedDateTime DESC"
    }
    
    return get_request_microsoft_api(params, token)

@mcp.tool()
def get_emails_from_mail_sender(sender_email: str, number_emails: int = 10) -> str:
    """
    Gets the emails from a specific sender's email address.
    params:
        sender_email (str): The email address of the sender.
        number_emails (int): The number of emails to retrieve, by default 10.
    returns:
        str: A JSON string containing the emails from the specified sender.
    """
   
    params = {
        "$filter": f"receivedDateTime ge 2016-01-01T00:00:00Z and from/emailAddress/address eq '{sender_email}'",
        "$top": number_emails,
        "$orderBy": "receivedDateTime DESC"
    }
    
    return get_request_microsoft_api(params, token)

if __name__ == "__main__":
    # Start the MCP server
    mcp.run()
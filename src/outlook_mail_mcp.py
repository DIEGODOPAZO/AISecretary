import json
from utils.auth_microsoft import get_access_token_microsoft
import requests
# server.py
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("AISecretary")


@mcp.tool()
def get_emails_outlook(number_emails: int) -> str:
    """
    Gets emails from the Outlook mailbox.
    params:
        number_emails (int): The number of emails to retrieve.
    returns:
        str: A JSON string containing the emails.
    """
    token = get_access_token_microsoft()
    url = f"https://graph.microsoft.com/v1.0/me/messages?$top={number_emails}&$orderby=receivedDateTime desc"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Lanza excepción si algo va mal

    messages = response.json().get("value", [])
    simplified_messages = []

    for msg in messages:
        simplified = {
            "id": msg.get("id"),
            "subject": msg.get("subject"),
            "from": {
                "name": msg.get("from", {}).get("emailAddress", {}).get("name"),
                "address": msg.get("from", {}).get("emailAddress", {}).get("address")
            },
            "toRecipients": [
                {
                    "name": r.get("emailAddress", {}).get("name"),
                    "address": r.get("emailAddress", {}).get("address")
                } for r in msg.get("toRecipients", [])
            ],
            "ccRecipients": [
                {
                    "name": r.get("emailAddress", {}).get("name"),
                    "address": r.get("emailAddress", {}).get("address")
                } for r in msg.get("ccRecipients", [])
            ],
            "receivedDateTime": msg.get("receivedDateTime"),
            "sentDateTime": msg.get("sentDateTime"),
            "isRead": msg.get("isRead"),
            "hasAttachments": msg.get("hasAttachments"),
            "bodyPreview": msg.get("bodyPreview"),
            "importance": msg.get("importance"),
            "conversationId": msg.get("conversationId"),
            "internetMessageId": msg.get("internetMessageId")
        }
        simplified_messages.append(simplified)

    return json.dumps(simplified_messages, indent=2)

if __name__ == "__main__":
    # Start the MCP server
    mcp.run()
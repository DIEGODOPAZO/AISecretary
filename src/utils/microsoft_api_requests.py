import requests
import json

from utils.auth_microsoft import get_access_token_microsoft

def get_folder_names() -> str:
    token = get_access_token_microsoft()
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    base_url = "https://graph.microsoft.com/v1.0/me/mailFolders"
    response = requests.get(base_url, headers=headers)
    response.raise_for_status()  # Lanza excepción si algo va mal
    
    folders = response.json().get("value", [])
    simplified_folders = []

    for folder in folders:
        simplified = {
            "id": folder.get("id"),
            "displayName": folder.get("displayName"),
            "totalItemCount": folder.get("totalItemCount")
        }
        simplified_folders.append(simplified)

    return json.dumps(simplified_folders, indent=2) 


def get_request_microsoft_api(params: dict, folder_id: str = "ALL") -> str:
    token = get_access_token_microsoft()
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    if folder_id == "ALL":
        base_url = "https://graph.microsoft.com/v1.0/me/messages"
    else:
        base_url = f"https://graph.microsoft.com/v1.0/me/mailFolders/{folder_id}/messages"

    response = requests.get(base_url, headers=headers, params=params)
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
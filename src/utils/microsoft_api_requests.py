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
            "folder_id": folder.get("id"),
            "displayName": folder.get("displayName"),
            "totalItemCount": folder.get("totalItemCount")
        }
        simplified_folders.append(simplified)

    return json.dumps(simplified_folders, indent=2) 


def get_request_microsoft_api(params: dict, folder_id: str = "ALL", unread_only: bool = False) -> str:
    token = get_access_token_microsoft()
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    if folder_id == "ALL":
        base_url = "https://graph.microsoft.com/v1.0/me/messages"
    else:
        base_url = f"https://graph.microsoft.com/v1.0/me/mailFolders/{folder_id}/messages"

    if unread_only:
        # add the filer"isRead eq false" to the existing filters
        existing_filter = params.get("$filter", "")
        unread_filter = "isRead eq false"
        if existing_filter:
            params["$filter"] = f"{existing_filter} and {unread_filter}"
        else:
            params["$filter"] = unread_filter

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

def mark_as_read_microsoft_api(message_id: str) -> str:
    token = get_access_token_microsoft()
    url = f'https://graph.microsoft.com/v1.0/me/messages/{message_id}'

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    data = {
        "isRead": True
    }
    response = requests.patch(url, headers=headers, json=data)
    response.raise_for_status()  # Lanza excepción si la petición falla

    # Recuperar el mensaje actualizado para devolverlo en el formato deseado
    get_response = requests.get(url, headers=headers)
    get_response.raise_for_status()
    msg = get_response.json()

    # Formatear el mensaje como en tu ejemplo
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

    return json.dumps(simplified, indent=2)
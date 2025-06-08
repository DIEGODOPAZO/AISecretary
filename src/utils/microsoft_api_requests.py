import base64
import os
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

def get_full_message_and_attachments(message_id: str) -> str:
    token = get_access_token_microsoft()
    
    base_url = f"https://graph.microsoft.com/v1.0/me/messages/{message_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    msg_response = requests.get(base_url, headers=headers)
    msg_response.raise_for_status()
    msg_data = msg_response.json()

    # Obtener adjuntos
    attachments_url = f"{base_url}/attachments"
    att_response = requests.get(attachments_url, headers=headers)
    att_response.raise_for_status()
    attachments = att_response.json().get("value", [])

    # Crear directorio para guardar archivos
    download_dir = download_dir = os.path.join(os.path.expanduser("~"), "Downloads", "attachments")

    os.makedirs(download_dir, exist_ok=True)

    downloaded_attachments = []

    for att in attachments:
        if att.get("@odata.type") == "#microsoft.graph.fileAttachment":
            name = att.get("name")
            content_type = att.get("contentType")
            content_bytes = att.get("contentBytes")

            if name and content_bytes:
                file_path = os.path.join(download_dir, name)
                with open(file_path, "wb") as f:
                    f.write(base64.b64decode(content_bytes))

                downloaded_attachments.append({
                    "name": name,
                    "contentType": content_type,
                    "path": file_path
                })

    # Simplificar respuesta
    simplified = {
        "id": msg_data.get("id"),
        "subject": msg_data.get("subject"),
        "from": {
            "name": msg_data.get("from", {}).get("emailAddress", {}).get("name"),
            "address": msg_data.get("from", {}).get("emailAddress", {}).get("address")
        },
        "toRecipients": [
            {
                "name": r.get("emailAddress", {}).get("name"),
                "address": r.get("emailAddress", {}).get("address")
            } for r in msg_data.get("toRecipients", [])
        ],
        "ccRecipients": [
            {
                "name": r.get("emailAddress", {}).get("name"),
                "address": r.get("emailAddress", {}).get("address")
            } for r in msg_data.get("ccRecipients", [])
        ],
        "receivedDateTime": msg_data.get("receivedDateTime"),
        "sentDateTime": msg_data.get("sentDateTime"),
        "isRead": msg_data.get("isRead"),
        "hasAttachments": msg_data.get("hasAttachments"),
        "body": {
            "contentType": msg_data.get("body", {}).get("contentType"),
            "content": msg_data.get("body", {}).get("content")
        },
        "importance": msg_data.get("importance"),
        "conversationId": msg_data.get("conversationId"),
        "internetMessageId": msg_data.get("internetMessageId"),
        "attachments": downloaded_attachments
    }

    return json.dumps(simplified, indent=2)

    return json.dumps(simplified, indent=2)
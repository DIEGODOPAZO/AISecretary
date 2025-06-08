import base64
import os
import requests
import json

from utils.auth_microsoft import get_access_token_microsoft
from utils.helpers import microsoft_get, microsoft_simplify_message  

def get_folder_names() -> str:
    token = get_access_token_microsoft()
    base_url = "https://graph.microsoft.com/v1.0/me/mailFolders"
    response = microsoft_get(base_url, token)    
    folders = response.get("value", [])
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

    response = microsoft_get(base_url, token, params=params)

    messages = response.get("value", [])
    simplified_messages = []

    for msg in messages:
        simplified_messages.append(microsoft_simplify_message(msg))

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

    return json.dumps(microsoft_simplify_message(msg), indent=2)


def get_full_message_and_attachments(message_id: str) -> str:
    token = get_access_token_microsoft()
    
    base_url = f"https://graph.microsoft.com/v1.0/me/messages/{message_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    msg_data = microsoft_get(base_url, token)

    # Obtain the attachments
    attachments_url = f"{base_url}/attachments"
    att_response = requests.get(attachments_url, headers=headers)
    att_response.raise_for_status()
    attachments = att_response.json().get("value", [])

    # Create the directory to save attachments
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


    return json.dumps(microsoft_simplify_message(msg_data, full=True, attachments=attachments, attachments_download_path=downloaded_attachments), indent=2)

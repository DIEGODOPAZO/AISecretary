import base64
import requests
import os


def microsoft_get(url: str, token: str, params: dict = None) -> dict:
    """Sends a GET request to the Microsoft Graph API."""
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def microsoft_delete(url: str, token: str) -> str:
    """Sends a DELETE request to the Microsoft Graph API."""
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    response = requests.delete(url, headers=headers)

    if response.status_code == 204:
        return "Message correctly deleted"
    else:
        return "Error deleting message: " + response.text


def microsoft_post(url: str, token: str, data: dict) -> dict:
    """Sends a POST request to the Microsoft Graph API."""
    response = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json=data,
    )

    if response.status_code == 204:
        return {"message": "Request completed successfully, no content returned."}
    elif response.status_code == 202:
        return {"message": "Draft email sent successfully."}
    elif response.status_code == 200 or response.status_code == 201:
        return response.json()
    else:
        return {"error": response.text}



def microsoft_patch(url: str, token: str, data: dict) -> dict:
    """Sends a PATCH request to the Microsoft Graph API."""
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    response = requests.patch(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()


def read_file_and_encode_base64(file_path: str) -> tuple[str, str]:
    """Reads a file and encodes its content to base64."""
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")

    filename = os.path.basename(file_path)

    with open(file_path, "rb") as file:
        file_content = file.read()
        encoded_content = base64.b64encode(file_content).decode("utf-8")

    return filename, encoded_content


def microsoft_simplify_message(
    msg: dict,
    full: bool = False,
    attachments: list = None,
    attachments_download_path: list = None,
) -> dict:
    """
    Simplifies a Microsoft Graph API message object to a more manageable format.
    """
    data = {
        "id": msg.get("id"),
        "subject": msg.get("subject"),
        "from": {
            "name": msg.get("from", {}).get("emailAddress", {}).get("name"),
            "address": msg.get("from", {}).get("emailAddress", {}).get("address"),
        },
        "toRecipients": [
            {
                "name": r.get("emailAddress", {}).get("name"),
                "address": r.get("emailAddress", {}).get("address"),
            }
            for r in msg.get("toRecipients", [])
        ],
        "ccRecipients": [
            {
                "name": r.get("emailAddress", {}).get("name"),
                "address": r.get("emailAddress", {}).get("address"),
            }
            for r in msg.get("ccRecipients", [])
        ],
        "receivedDateTime": msg.get("receivedDateTime"),
        "sentDateTime": msg.get("sentDateTime"),
        "isRead": msg.get("isRead"),
        "hasAttachments": msg.get("hasAttachments"),
        "importance": msg.get("importance"),
        "conversationId": msg.get("conversationId"),
        "internetMessageId": msg.get("internetMessageId"),
    }

    if full:
        data["body"] = {
            "contentType": msg.get("body", {}).get("contentType"),
            "content": msg.get("body", {}).get("content"),
        }
        # Of the attachments, we only keep the name and contentType because the content might be too large for the LLM context
        if attachments:
            data["attachments"] = [
                {
                    "name": a.get("name"),
                    "contentType": a.get("contentType"),
                    "attachment_id": a.get("id"),
                }
                for a in attachments
            ]
        else:
            data["attachments"] = []

        if attachments_download_path:
            data["attachments_download_path"] = attachments_download_path

    else:
        data["bodyPreview"] = msg.get("bodyPreview")

    return data

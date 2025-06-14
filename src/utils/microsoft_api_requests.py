import base64
import os
import json

from utils.auth_microsoft import get_access_token_microsoft
from utils.helpers import *


@handle_microsoft_errors
def get_folder_names() -> str:
    token = get_access_token_microsoft()
    base_url = "https://graph.microsoft.com/v1.0/me/mailFolders"
    (status_code, response) = microsoft_get(base_url, token)
    folders = response.get("value", [])
    simplified_folders = []

    for folder in folders:
        simplified = {
            "folder_id": folder.get("id"),
            "displayName": folder.get("displayName"),
            "totalItemCount": folder.get("totalItemCount"),
        }
        simplified_folders.append(simplified)

    return json.dumps(simplified_folders, indent=2)


@handle_microsoft_errors
def get_messages_from_folder_microsoft_api(
    params: dict, folder_id: str = "ALL", unread_only: bool = False
) -> str:
    token = get_access_token_microsoft()
    if folder_id == "ALL":
        base_url = "https://graph.microsoft.com/v1.0/me/messages"
    else:
        base_url = (
            f"https://graph.microsoft.com/v1.0/me/mailFolders/{folder_id}/messages"
        )

    if unread_only:
        # add the filer"isRead eq false" to the existing filters
        existing_filter = params.get("$filter", "")
        unread_filter = "isRead eq false"
        if existing_filter:
            params["$filter"] = f"{existing_filter} and {unread_filter}"
        else:
            params["$filter"] = unread_filter

    (status_code, response) = microsoft_get(base_url, token, params=params)

    messages = response.get("value", [])
    simplified_messages = []

    for msg in messages:
        simplified_messages.append(microsoft_simplify_message(msg))

    return json.dumps(simplified_messages, indent=2)


@handle_microsoft_errors
def mark_as_read_microsoft_api(message_id: str) -> str:
    token = get_access_token_microsoft()
    url = f"https://graph.microsoft.com/v1.0/me/messages/{message_id}"
    data = {"isRead": True}

    microsoft_patch(url, token, data)

    (status_code, response) = microsoft_get(url, token)

    return json.dumps(microsoft_simplify_message(response), indent=2)


@handle_microsoft_errors
def get_full_message_and_attachments(message_id: str) -> str:
    token = get_access_token_microsoft()

    base_url = f"https://graph.microsoft.com/v1.0/me/messages/{message_id}"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

    (status_code, msg_data) = microsoft_get(base_url, token)

    # Obtain the attachments
    attachments_url = f"{base_url}/attachments"
    (att_status, att_data) = microsoft_get(attachments_url, token)
    attachments = att_data.get("value", [])

    # Create the directory to save attachments
    download_dir = os.path.join(os.path.expanduser("~"), "Downloads", "attachments")

    os.makedirs(download_dir, exist_ok=True)

    downloaded_attachments = []

    for att in attachments:
        if att.get("@odata.type") == "#microsoft.graph.fileAttachment":
            name = att.get("name")
            content_type = att.get("contentType")
            content_bytes = att.get("contentBytes")
            id = att.get("id")

            if name and content_bytes:
                file_path = os.path.join(download_dir, name)
                with open(file_path, "wb") as f:
                    f.write(base64.b64decode(content_bytes))

                downloaded_attachments.append(
                    {
                        "name": name,
                        "contentType": content_type,
                        "path": file_path,
                        "attachment_id": id,
                    }
                )

    return json.dumps(
        microsoft_simplify_message(
            msg_data,
            full=True,
            attachments=attachments,
            attachments_download_path=downloaded_attachments,
        ),
        indent=2,
    )


@handle_microsoft_errors
def delete_message_microsoft_api(message_id: str) -> str:
    token = get_access_token_microsoft()
    url = f"https://graph.microsoft.com/v1.0/me/messages/{message_id}"
    (status_code, response) = microsoft_delete(url, token)

    if status_code != 204:
        return json.dumps({"error": response}, indent=2)
    return json.dumps(
        {"message": f"Message with ID {message_id} deleted successfully."}, indent=2
    )


@handle_microsoft_errors
def create_edit_draft_microsoft_api(
    subject: str,
    body: str,
    to_recipients: list[str] = None,
    cc_recipients: list[str] = None,
    draft_id: str = None,
    importance: str = "normal",
) -> str:
    if not subject or not body:
        return json.dumps({"error": "Subject and body are required."}, indent=2)
    token = get_access_token_microsoft()
    url = "https://graph.microsoft.com/v1.0/me/messages"

    data = {
        "subject": subject,
        "body": {"contentType": "HTML", "content": body},
        "toRecipients": (
            [{"emailAddress": {"address": email}} for email in to_recipients]
            if to_recipients
            else []
        ),
        "ccRecipients": (
            [{"emailAddress": {"address": email}} for email in cc_recipients]
            if cc_recipients
            else []
        ),
        "importance": importance.lower(),
    }

    if draft_id:
        url = f"{url}/{draft_id}"
        (status_code, response) = microsoft_patch(url, token, data)
    else:
        (status_code, response) = microsoft_post(url, token, data)

    return json.dumps(response, indent=2)


@handle_microsoft_errors
def add_attachment_to_draft_microsoft_api(
    draft_id: str, attachment_path: str, content_type: str
) -> str:
    token = get_access_token_microsoft()
    url = f"https://graph.microsoft.com/v1.0/me/messages/{draft_id}/attachments"
    try:
        attachment_name, attachment_content = read_file_and_encode_base64(
            attachment_path
        )
    except FileNotFoundError as e:
        return json.dumps({"error": str(e)}, indent=2)

    data = {
        "@odata.type": "#microsoft.graph.fileAttachment",
        "name": attachment_name,
        "contentBytes": attachment_content,
        "contentType": content_type,
    }

    status_code, response = microsoft_post(url, token, data)
    response_data = {
        "attachment_id": response.get("id"),
        "name": response.get("name"),
        "contentType": response.get("contentType"),
        "size": response.get("size"),
    }
    return json.dumps(response_data, indent=2)


@handle_microsoft_errors
def send_draft_email_microsoft_api(draft_id: str) -> str:
    token = get_access_token_microsoft()
    url = f"https://graph.microsoft.com/v1.0/me/messages/{draft_id}/send"
    (status_code, response) = microsoft_post(url, token, data={})
    return json.dumps(response, indent=2)


@handle_microsoft_errors
def delete_attachment_from_draft_microsoft_api(
    draft_id: str, attachment_id: str
) -> str:
    token = get_access_token_microsoft()
    url = f"https://graph.microsoft.com/v1.0/me/messages/{draft_id}/attachments/{attachment_id}"
    (status_code, response) = microsoft_delete(url, token)
    if status_code != 204:
        return json.dumps({"error": response}, indent=2)
    return json.dumps(
        {"message": f"Attachment with ID {attachment_id} deleted successfully."},
        indent=2,
    )


@handle_microsoft_errors
def move_or_copy_email_microsoft_api(
    email_id: str, destination_folder_id: str, move: bool = True
) -> str:
    """
    Moves or copies an email to a specified folder.

    :param email_id: The ID of the email to move or copy.
    :param destination_folder_id: The ID of the destination folder.
    :param action: "move" to move the email, "copy" to copy it.
    :return: JSON response indicating success or failure.
    """
    token = get_access_token_microsoft()
    url = (
        f"https://graph.microsoft.com/v1.0/me/messages/{email_id}/move"
        if move
        else f"https://graph.microsoft.com/v1.0/me/messages/{email_id}/copy"
    )

    data = {"destinationId": destination_folder_id}

    (status_code, response) = microsoft_post(url, token, data)
    return json.dumps(response, indent=2)


@handle_microsoft_errors
def reply_to_email_microsoft_api(
    email_id: str,
    reply_all: bool = False,
    to_recipients: list[str] = None,
    cc_recipients: list[str] = None,
) -> str:
    token = get_access_token_microsoft()
    url = (
        f"https://graph.microsoft.com/v1.0/me/messages/{email_id}/createReplyAll"
        if reply_all
        else f"https://graph.microsoft.com/v1.0/me/messages/{email_id}/createReply"
    )

    data = {
        "message": {
            "body": {"contentType": "Text", "content": "..."},
            "toRecipients": (
                [{"emailAddress": {"address": email}} for email in to_recipients]
                if to_recipients
                else []
            ),
            "ccRecipients": (
                [{"emailAddress": {"address": email}} for email in cc_recipients]
                if cc_recipients
                else []
            ),
        }
    }
    (status_code, response) = microsoft_post(url, token, data)
    return json.dumps(response, indent=2)


@handle_microsoft_errors
def forward_email_microsoft_api(
    email_id: str,
    comment: str = "...",
    to_recipients: list[str] = None,
    cc_recipients: list[str] = None,
) -> str:
    token = get_access_token_microsoft()
    url = f"https://graph.microsoft.com/v1.0/me/messages/{email_id}/forward"

    data = {
        "toRecipients": (
            [{"emailAddress": {"address": email}} for email in to_recipients]
            if to_recipients
            else []
        ),
        "ccRecipients": (
            [{"emailAddress": {"address": email}} for email in cc_recipients]
            if cc_recipients
            else []
        ),
        "comment": comment,
    }

    (status_code, response) = microsoft_post(url, token, data)
    return json.dumps(response, indent=2)


@handle_microsoft_errors
def create_edit_folder_microsoft_api(
    folder_name: str, folder_id: str = None, parent_folder_id: str = None
) -> str:
    """
    Creates or edits a folder in the user's mailbox.

    :param folder_name: The name of the folder to create or edit.
    :param folder_id: The ID of the folder to edit (if it exists).
    :return: JSON response indicating success or failure.
    """
    token = get_access_token_microsoft()
    url = "https://graph.microsoft.com/v1.0/me/mailFolders"

    data = {
        "displayName": folder_name,
    }
    if not folder_name:
        return json.dumps({"error": "Folder name is required."}, indent=2)

    if parent_folder_id:
        url = f"{url}/{parent_folder_id}/childFolders"
        (status_code, response) = microsoft_post(url, token, data)
    elif folder_id:
        url = f"{url}/{folder_id}"
        (status_code, response) = microsoft_patch(url, token, data)
    else:
        (status_code, response) = microsoft_post(url, token, data)

    return json.dumps(response, indent=2)


@handle_microsoft_errors
def delete_folder_microsoft_api(folder_id: str) -> str:
    """
    Deletes a folder from the user's mailbox.

    :param folder_id: The ID of the folder to delete.
    :return: JSON response indicating success or failure.
    """
    token = get_access_token_microsoft()
    url = f"https://graph.microsoft.com/v1.0/me/mailFolders/{folder_id}"
    (status_code, response) = microsoft_delete(url, token)
    if status_code != 204:
        return json.dumps({"error": response}, indent=2)
    return json.dumps(
        {"message": f"Folder with ID {folder_id} deleted successfully."}, indent=2
    )

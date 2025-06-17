import base64
import os
import json

from utils.param_types import *
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
def get_subfolders_microsoft_api(folder_id: str) -> str:
    token = get_access_token_microsoft()
    base_url = (
        f"https://graph.microsoft.com/v1.0/me/mailFolders/{folder_id}/childFolders"
    )
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
    params: dict, email_search_params: EmailSearchParams
) -> str:
    token = get_access_token_microsoft()
    if email_search_params.folder_id is None:
        base_url = "https://graph.microsoft.com/v1.0/me/messages"
    else:
        base_url = f"https://graph.microsoft.com/v1.0/me/mailFolders/{email_search_params.folder_id}/messages"

    if email_search_params.unread_only:
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
def mark_as_read_unread_microsoft_api(message_id: str, is_read: bool = True) -> str:
    token = get_access_token_microsoft()
    url = f"https://graph.microsoft.com/v1.0/me/messages/{message_id}"
    data = {"isRead": is_read}

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
def create_edit_draft_microsoft_api(draft_email_data: DraftEmailData) -> str:
    if not draft_email_data.subject or not draft_email_data.body:
        return json.dumps({"error": "Subject and body are required."}, indent=2)
    token = get_access_token_microsoft()
    url = "https://graph.microsoft.com/v1.0/me/messages"

    if draft_email_data.importance.lower() not in ["low", "normal", "high"]:
        return json.dumps(
            {"error": "Importance must be one of: low, normal, high."}, indent=2
        )

    data = {
        "subject": draft_email_data.subject,
        "body": {"contentType": "HTML", "content": draft_email_data.body},
        "toRecipients": (
            [
                {"emailAddress": {"address": email}}
                for email in draft_email_data.email_recipients.to_recipients
            ]
            if draft_email_data.email_recipients.to_recipients
            else []
        ),
        "ccRecipients": (
            [
                {"emailAddress": {"address": email}}
                for email in draft_email_data.email_recipients.cc_recipients
            ]
            if draft_email_data.email_recipients.cc_recipients
            else []
        ),
        "importance": draft_email_data.importance.lower(),
    }

    if draft_email_data.draft_id:
        url = f"{url}/{draft_email_data.draft_id}"
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
    return json.dumps({"message": "Email sent successfully."}, indent=2)


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
    email_operation_params: EmailOperationParams,
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
        f"https://graph.microsoft.com/v1.0/me/messages/{email_operation_params.email_id}/move"
        if email_operation_params.move
        else f"https://graph.microsoft.com/v1.0/me/messages/{email_operation_params.email_id}/copy"
    )

    data = {"destinationId": email_operation_params.destination_folder_id}

    (status_code, response) = microsoft_post(url, token, data)
    return json.dumps(response, indent=2)


@handle_microsoft_errors
def reply_to_email_microsoft_api(email_reply_params: EmailReplyParams) -> str:
    token = get_access_token_microsoft()
    url = (
        f"https://graph.microsoft.com/v1.0/me/messages/{email_reply_params.email_id}/createReplyAll"
        if email_reply_params.reply_all
        else f"https://graph.microsoft.com/v1.0/me/messages/{email_reply_params.email_id}/createReply"
    )

    data = {"comment": email_reply_params.body}
    (status_code, response) = microsoft_post(url, token, data)
    return json.dumps(response, indent=2)


@handle_microsoft_errors
def forward_email_microsoft_api(email_forward_params: EmailForwardParams) -> str:
    token = get_access_token_microsoft()
    url = f"https://graph.microsoft.com/v1.0/me/messages/{email_forward_params.email_id}/forward"

    data = {
        "toRecipients": (
            [
                {"emailAddress": {"address": email}}
                for email in email_forward_params.email_recipients.to_recipients
            ]
            if email_forward_params.email_recipients.to_recipients
            else []
        ),
        "ccRecipients": (
            [
                {"emailAddress": {"address": email}}
                for email in email_forward_params.email_recipients.cc_recipients
            ]
            if email_forward_params.email_recipients.cc_recipients
            else []
        ),
        "comment": email_forward_params.comment,
    }

    (status_code, response) = microsoft_post(url, token, data)
    return json.dumps(response, indent=2)


@handle_microsoft_errors
def create_edit_folder_microsoft_api(folder_params: FolderParams) -> str:
    """
    Creates or edits a folder in the user's mailbox.

    :param folder_name: The name of the folder to create or edit.
    :param folder_id: The ID of the folder to edit (if it exists).
    :return: JSON response indicating success or failure.
    """
    token = get_access_token_microsoft()
    url = "https://graph.microsoft.com/v1.0/me/mailFolders"

    data = {
        "displayName": folder_params.folder_name,
    }
    if not folder_params.folder_name:
        return json.dumps({"error": "Folder name is required."}, indent=2)

    if folder_params.parent_folder_id:
        url = f"{url}/{folder_params.parent_folder_id}/childFolders"
        (status_code, response) = microsoft_post(url, token, data)
    elif folder_params.folder_id:
        url = f"{url}/{folder_params.folder_id}"
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

import base64
import json
import os

from ..helpers import handle_microsoft_errors, microsoft_delete, microsoft_get, microsoft_patch, microsoft_post, microsoft_simplify_message, read_file_and_encode_base64
from ..param_types import *
from ..auth_microsoft import get_access_token_microsoft


class MicrosoftMessagesRequests:
    def __init__(self):
        self.token = get_access_token_microsoft()
        self.base_url = "https://graph.microsoft.com/v1.0/me/messages"

    @handle_microsoft_errors
    def get_messages_from_folder_microsoft_api(
        self, params: dict, email_search_params: EmailSearchParams
    ) -> str:
        if email_search_params.folder_id is None:
            base_url = self.base_url
        else:
            base_url = f"https://graph.microsoft.com/v1.0/me/mailFolders/{email_search_params.folder_id}/messages"

        if email_search_params.unread_only:
            existing_filter = params.get("$filter", "")
            unread_filter = "isRead eq false"
            if existing_filter:
                params["$filter"] = f"{existing_filter} and {unread_filter}"
            else:
                params["$filter"] = unread_filter

        (status_code, response) = microsoft_get(base_url, self.token, params=params)

        messages = response.get("value", [])
        simplified_messages = [microsoft_simplify_message(msg) for msg in messages]

        result = {"messages": simplified_messages}
        if "@odata.nextLink" in response:
            result["nextLink"] = response["@odata.nextLink"]
        return json.dumps(result, indent=2)

    @handle_microsoft_errors
    def get_conversation_messages_microsoft_api(self, params: dict) -> str:
        (status_code, response) = microsoft_get(
            self.base_url, self.token, params=params
        )
        messages = response.get("value", [])
        simplified_messages = [microsoft_simplify_message(msg) for msg in messages]
        result = {"messages": simplified_messages}
        if "@odata.nextLink" in response:
            result["nextLink"] = response["@odata.nextLink"]
        return json.dumps(result, indent=2)

    @handle_microsoft_errors
    def mark_as_read_unread_microsoft_api(
        self, message_id: str, is_read: bool = True
    ) -> str:
        url = f"{self.base_url}/{message_id}"
        data = {"isRead": is_read}
        microsoft_patch(url, self.token, data)
        (status_code, response) = microsoft_get(url, self.token)
        return json.dumps(microsoft_simplify_message(response), indent=2)

    @handle_microsoft_errors
    def get_full_message_and_attachments(self, message_id: str) -> str:
        base_url = f"{self.base_url}/{message_id}"
        (status_code, msg_data) = microsoft_get(base_url, self.token)
        attachments_url = f"{base_url}/attachments"
        (att_status, att_data) = microsoft_get(attachments_url, self.token)
        attachments = att_data.get("value", [])
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
    def delete_message_microsoft_api(self, message_id: str) -> str:
        url = f"{self.base_url}/{message_id}"
        (status_code, response) = microsoft_delete(url, self.token)
        if status_code != 204:
            return json.dumps({"error": response}, indent=2)
        return json.dumps(
            {"message": f"Message with ID {message_id} deleted successfully."}, indent=2
        )

    @handle_microsoft_errors
    def create_edit_draft_microsoft_api(self, draft_email_data: DraftEmailData) -> str:
        if not draft_email_data.subject or not draft_email_data.body:
            return json.dumps({"error": "Subject and body are required."}, indent=2)
        url = self.base_url
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
            (status_code, response) = microsoft_patch(url, self.token, data)
        else:
            (status_code, response) = microsoft_post(url, self.token, data)
        return json.dumps(response, indent=2)

    @handle_microsoft_errors
    def add_attachment_to_draft_microsoft_api(
        self, draft_id: str, attachment_path: str, content_type: str
    ) -> str:
        url = f"{self.base_url}/{draft_id}/attachments"
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
        status_code, response = microsoft_post(url, self.token, data)
        response_data = {
            "attachment_id": response.get("id"),
            "name": response.get("name"),
            "contentType": response.get("contentType"),
            "size": response.get("size"),
        }
        return json.dumps(response_data, indent=2)

    @handle_microsoft_errors
    def send_draft_email_microsoft_api(self, draft_id: str) -> str:
        url = f"{self.base_url}/{draft_id}/send"
        (status_code, response) = microsoft_post(url, self.token, data={})
        return json.dumps({"message": "Email sent successfully."}, indent=2)

    @handle_microsoft_errors
    def delete_attachment_from_draft_microsoft_api(
        self, draft_id: str, attachment_id: str
    ) -> str:
        url = f"{self.base_url}/{draft_id}/attachments/{attachment_id}"
        (status_code, response) = microsoft_delete(url, self.token)
        if status_code != 204:
            return json.dumps({"error": response}, indent=2)
        return json.dumps(
            {"message": f"Attachment with ID {attachment_id} deleted successfully."},
            indent=2,
        )

    @handle_microsoft_errors
    def move_or_copy_email_microsoft_api(
        self, email_operation_params: EmailOperationParams
    ) -> str:
        url = (
            f"{self.base_url}/{email_operation_params.email_id}/move"
            if email_operation_params.move
            else f"{self.base_url}/{email_operation_params.email_id}/copy"
        )
        data = {"destinationId": email_operation_params.destination_folder_id}
        (status_code, response) = microsoft_post(url, self.token, data)
        return json.dumps(response, indent=2)

    @handle_microsoft_errors
    def reply_to_email_microsoft_api(self, email_reply_params: EmailReplyParams) -> str:
        url = (
            f"{self.base_url}/{email_reply_params.email_id}/createReplyAll"
            if email_reply_params.reply_all
            else f"{self.base_url}/{email_reply_params.email_id}/createReply"
        )
        data = {"comment": email_reply_params.body}
        (status_code, response) = microsoft_post(url, self.token, data)
        return json.dumps(response, indent=2)

    @handle_microsoft_errors
    def forward_email_microsoft_api(
        self, email_forward_params: EmailForwardParams
    ) -> str:
        url = f"{self.base_url}/{email_forward_params.email_id}/forward"
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
        (status_code, response) = microsoft_post(url, self.token, data)
        return json.dumps(response, indent=2)

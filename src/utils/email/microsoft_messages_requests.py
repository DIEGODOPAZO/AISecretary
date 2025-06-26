import base64
import json
import os

from ..helper_functions.helpers_email import (
    build_filter_params,
    build_search_params,
    microsoft_simplify_message,
    remove_duplicate_messages,
)
from ..helper_functions.general_helpers import (
    download_attachments,
    handle_microsoft_errors,
    microsoft_get,
    microsoft_post,
    microsoft_patch,
    microsoft_delete,
    read_file_and_encode_base64,
)

from ..param_types import *
from ..token_manager import TokenManager


class MicrosoftMessagesRequests:
    def __init__(self, token_manager: TokenManager):
        self.base_url = "https://graph.microsoft.com/v1.0/me/messages"
        self.token_manager = token_manager

    @handle_microsoft_errors
    def get_messages_from_folder_microsoft_api(
        self,
        email_query: Optional[EmailQuery] = None,
        params: Optional[dict] = None,
        folder_id: Optional[str] = None
    ) -> str:
        
        if params is not None:
            return self._get_and_format_messages(params, folder_id)

        if email_query is None:
            raise json.dumps({"error": "You must provided search params"}, indent=2)

        has_search = bool(
            email_query.search and (email_query.search.keyword or email_query.search.subject)
        )
        has_filters = bool(
            email_query.filters and (
                email_query.filters.date_filter
                or email_query.filters.importance
                or email_query.filters.sender
                or email_query.filters.unread_only
                or email_query.filters.has_attachments
                or email_query.filters.categories
            )
        )

        search_params = build_search_params(email_query.search)
        filter_params = build_filter_params(email_query.filters)

        if "$top" not in search_params:
            search_params["$top"] = email_query.number_emails
        if "$top" not in filter_params:
            filter_params["$top"] = email_query.number_emails

        # If both search and filter are provided, we need to intersect the results
        if has_search and has_filters:
            search_result = self._get_and_format_messages(search_params, email_query.folder_id)
            filter_result = self._get_and_format_messages(filter_params, email_query.folder_id)

            search_messages = json.loads(search_result).get("messages", [])
            filter_messages = json.loads(filter_result).get("messages", [])

            # Intersect the results based on message IDs
            search_ids = {msg["id"] for msg in search_messages}
            filtered_ids = {msg["id"]: msg for msg in filter_messages}

            intersected = [filtered_ids[msg_id] for msg_id in search_ids if msg_id in filtered_ids]
            unique_messages = remove_duplicate_messages(intersected)
            return json.dumps({"messages": unique_messages}, indent=2)

        # Just search or filter
        final_params = search_params if has_search else filter_params
        if not final_params:
            final_params = {"$top": email_query.number_emails}

        return self._get_and_format_messages(final_params, email_query.folder_id)

    @handle_microsoft_errors
    def get_conversation_messages_microsoft_api(self, params: dict) -> str:
        (status_code, response) = microsoft_get(
            self.base_url, self.token_manager.get_token(), params=params
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
        microsoft_patch(url, self.token_manager.get_token(), data)
        (status_code, response) = microsoft_get(url, self.token_manager.token)
        return json.dumps(microsoft_simplify_message(response), indent=2)

    @handle_microsoft_errors
    def get_full_message_and_attachments(self, message_id: str) -> str:
        base_url = f"{self.base_url}/{message_id}"

        (status_code, msg_data) = microsoft_get(
            base_url, self.token_manager.get_token()
        )
        attachments_url = f"{base_url}/attachments"
        (att_status, att_data) = microsoft_get(
            attachments_url, self.token_manager.get_token()
        )
        attachments = att_data.get("value", [])
        downloaded_attachments = download_attachments(attachments)
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

        (status_code, response) = microsoft_delete(url, self.token_manager.get_token())
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
            (status_code, response) = microsoft_patch(
                url, self.token_manager.get_token(), data
            )
        else:
            (status_code, response) = microsoft_post(
                url, self.token_manager.get_token(), data
            )
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
        status_code, response = microsoft_post(
            url, self.token_manager.get_token(), data
        )
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
        (status_code, response) = microsoft_post(
            url, self.token_manager.get_token(), data={}
        )
        return json.dumps({"message": "Email sent successfully."}, indent=2)

    @handle_microsoft_errors
    def delete_attachment_from_draft_microsoft_api(
        self, draft_id: str, attachment_id: str
    ) -> str:
        url = f"{self.base_url}/{draft_id}/attachments/{attachment_id}"
        (status_code, response) = microsoft_delete(url, self.token_manager.get_token())
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
        (status_code, response) = microsoft_post(
            url, self.token_manager.get_token(), data
        )
        return json.dumps(response, indent=2)

    @handle_microsoft_errors
    def reply_to_email_microsoft_api(self, email_reply_params: EmailReplyParams) -> str:
        url = (
            f"{self.base_url}/{email_reply_params.email_id}/createReplyAll"
            if email_reply_params.reply_all
            else f"{self.base_url}/{email_reply_params.email_id}/createReply"
        )
        data = {"comment": email_reply_params.body}
        (status_code, response) = microsoft_post(
            url, self.token_manager.get_token(), data
        )
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
        (status_code, response) = microsoft_post(
            url, self.token_manager.get_token(), data
        )
        return json.dumps(response, indent=2)

    def _get_and_format_messages(self, params: dict, folder_id: Optional[str] = None) -> str:
    
        base_url = (
            f"https://graph.microsoft.com/v1.0/me/mailFolders/{folder_id}/messages"
            if folder_id else self.base_url
        )

        status_code, response = microsoft_get(base_url, self.token_manager.get_token(), params=params)
        messages = response.get("value", [])
        simplified_messages = [microsoft_simplify_message(msg) for msg in messages]
        unique_messages = remove_duplicate_messages(simplified_messages)

        result = {"messages": unique_messages}
        if "@odata.nextLink" in response:
            result["nextLink"] = response["@odata.nextLink"]
        
        return json.dumps(result, indent=2)
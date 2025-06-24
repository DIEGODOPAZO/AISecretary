import json
from src.utils.helper_functions.helpers_email import build_search_params, build_filter_params
from utils.param_types import *
from utils.email.microsoft_folders_requests import MicrosoftFoldersRequests
from utils.email.microsoft_messages_requests import MicrosoftMessagesRequests
from utils.email.microsoft_rules_requests import MicrosoftRulesRequests
from utils.email.microsoft_flag_requests import MicrosoftFlagRequests
from utils.categories.microsoft_categories_requests import MicrosoftCategoriesRequests
from utils.token_manager import TokenManager
from utils.auth_microsoft import get_access_token, get_token_cache_path

# server.py
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("AISecretary-Outlook-Mail", dependencies=["mcp[cli]", "msal"])

token_manager = TokenManager(
    get_token_cache_path(), get_access_token_func=get_access_token
)

filter_dateTime = "receivedDateTime ge 2016-01-01T00:00:00Z"  # Needed to have the params of orderBy in the filter

folders_requests = MicrosoftFoldersRequests(token_manager)
messages_requests = MicrosoftMessagesRequests(token_manager)
rules_requests = MicrosoftRulesRequests(token_manager)
flag_requests = MicrosoftFlagRequests(token_manager)
categories_requests = MicrosoftCategoriesRequests(token_manager)


@mcp.tool()
def search_emails_outlook(email_query: EmailQuery) -> str:
    """
    Searches emails in Outlook mailbox using Microsoft Graph API with advanced filtering capabilities.
    Supports filtering by date, importance, sender, keywords, subject, unread status, and more.
    You can't use both search and filter parameters at the same time, if you do, it will return an error message.
    If you want to use this tool with filter and with search, you can use the tool twice, once with the search parameters and once with the filter parameters an then combine the results.

    Args:
        email_query (EmailQuery): The query parameters for searching emails, including filters and pagination options.

    Returns:
        str: A JSON string containing the emails and pagination information if available.
    """
    has_search = bool(
        email_query.search
        and (email_query.search.keyword or email_query.search.subject)
    )
    has_filters = bool(
        email_query.filters
        and (
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

    # If both search and filter are provided, we need to handle them separately
    if has_search and has_filters:
        search_result = messages_requests.get_messages_from_folder_microsoft_api(
            search_params, folder_id=email_query.folder_id
        )
        filter_result = messages_requests.get_messages_from_folder_microsoft_api(
            filter_params, folder_id=email_query.folder_id
        )

        search_messages = json.loads(search_result).get("messages", [])
        filter_messages = json.loads(filter_result).get("messages", [])

        # Intersección por ID
        search_ids = {msg["id"] for msg in search_messages}
        filtered_ids = {msg["id"]: msg for msg in filter_messages}

        intersected = [
            filtered_ids[msg_id] for msg_id in search_ids if msg_id in filtered_ids
        ]

        return json.dumps({"messages": intersected}, indent=2)

    # Solo search o solo filter
    final_params = search_params if has_search else filter_params
    if not final_params:
        final_params = {"$top": email_query.number_emails}

    return messages_requests.get_messages_from_folder_microsoft_api(
        final_params, folder_id=email_query.folder_id
    )


@mcp.tool()
def get_conversation_emails(conversation_id: str, number_email: int) -> str:
    """
    Gets the emails from the conversation with conversation_id in the Outlook mailbox.
    params:
        conversation_id (str): The id of the conversation to retrieve emails from.
        number_email (int): The number of emails to retrieve from the conversation.
    returns:
        str: A JSON string containing the emails from the conversation view. And if there are more emails, it will return the nextLink to get the next page of emails.
    """
    params = {
        "$top": number_email,
        "$filter": "conversationId eq '" + conversation_id + "'",
    }
    return messages_requests.get_conversation_messages_microsoft_api(params)


@mcp.tool()
def mark_email_as_read(email_id: str) -> str:
    """
    Marks an email as read.
    params:
        email_id (str): The id of the email to mark as read.
    returns:
        str: Information about the changed email.
    """
    return messages_requests.mark_as_read_unread_microsoft_api(email_id)


@mcp.tool()
def mark_email_as_unread(email_id: str) -> str:
    """
    Marks an email as unread.
    params:
        email_id (str): The id of the email to mark as unread.
    returns:
        str: Information about the changed email.
    """
    return messages_requests.mark_as_read_unread_microsoft_api(email_id, is_read=False)


@mcp.tool()
def get_full_email_and_attachments(email_id: str) -> str:
    """
    Gets the full email and its attachments.
    params:
        email_id (str): The id of the email to retrieve.
    returns:
        str: A JSON string containing the full email and its attachments names, the files will be downloaded.
    """

    return messages_requests.get_full_message_and_attachments(email_id)


@mcp.tool()
def delete_email(email_id: str) -> str:
    """
    Deletes an email from the Outlook mailbox.
    params:
        email_id (str): The id of the email to delete.
    returns:
        str: A confirmation message.
    """
    return messages_requests.delete_message_microsoft_api(email_id)


@mcp.tool()
def create_edit_draft_email(draft_email_data: DraftEmailData) -> str:
    """
    Creates a draft email in the Outlook mailbox.
    params:
        draft_email_data (DraftEmailData): The data for creating or editing a draft email, including subject, body, recipients, draft_id (if editing), and importance.
    returns:
        str: The id of the created draft email or a error message.
    """

    return messages_requests.create_edit_draft_microsoft_api(
        draft_email_data=draft_email_data
    )


@mcp.tool()
def add_attachment_to_draft_email(
    draft_id: str, attachment_path: str, content_type: str = "application/octet-stream"
) -> str:
    """
    Adds an attachment to a draft email.
    params:
        draft_id (str): The id of the draft email to which the attachment will be added.
        attachment_path (str): The path to the attachment file.
    returns:
        str: The information about the attachment or an error message.
    """

    return messages_requests.add_attachment_to_draft_microsoft_api(
        draft_id=draft_id, attachment_path=attachment_path, content_type=content_type
    )


@mcp.tool()
def delete_attachment_from_draft_email(draft_id: str, attachment_id: str) -> str:
    """
    Deletes an attachment from a draft email.
    params:
        draft_id (str): The id of the draft email from which the attachment will be deleted.
        attachment_id (str): The id of the attachment to delete.
    returns:
        str: A confirmation message or an error message.
    """
    return messages_requests.delete_attachment_from_draft_microsoft_api(
        draft_id, attachment_id
    )


@mcp.tool()
def send_draft_email(draft_id: str) -> str:
    """
    Sends a draft email.
    params:
        draft_id (str): The id of the draft email to send.
    returns:
        str: A confirmation message or an error message.
    """
    return messages_requests.send_draft_email_microsoft_api(draft_id)


@mcp.tool()
def move_or_copy_email(email_operation_params: EmailOperationParams) -> str:
    """
    Moves or copies an email to a different folder.

    returns:
        str: The data of the copied/moved email or an error message.
    """
    return messages_requests.move_or_copy_email_microsoft_api(email_operation_params)


@mcp.tool()
def create_reply_to_email(email_reply_params: EmailReplyParams) -> str:
    """
    Creates the draft for the reply of an email, it does not add content, for editing it you can use tools such as create_edit_draft_email.

    returns:
        str: Information about the created reply or an error message.
    """
    return messages_requests.reply_to_email_microsoft_api(email_reply_params)


@mcp.tool()
def forward_email(email_forward_params: EmailForwardParams) -> str:
    """
    Creates the draft for the forward of an email, it does not add content, for editing it you can use tools such as create_edit_draft_email.

    returns:
        str: A confirmation message or an error message.
    """
    return messages_requests.forward_email_microsoft_api(email_forward_params)


@mcp.tool()
def create_edit_folder(folder_params: FolderParams) -> str:
    """
    Creates or edits a folder in the Outlook mailbox.

    returns:
        str: The id of the created or edited folder with more information, or an error message.
    """
    return folders_requests.create_edit_folder_microsoft_api(folder_params)


@mcp.tool()
def delete_folder(folder_id: str) -> str:
    """
    Deletes a folder from the Outlook mailbox.
    params:
        folder_id (str): The id of the folder to delete.
    returns:
        str: A confirmation message or an error message.
    """
    return folders_requests.delete_folder_microsoft_api(folder_id)


@mcp.tool()
def get_folders_info_at_outlook() -> str:
    """
    Gets the names and the folder_id of the folders in Outlook.
    This is useful to know the id of a folder to use it in other tools, such as get_last_emails_outlook.
    You can also use the get_subfolders tool to get the subfolders of a specific folder.
    params:
        None
    returns:
        str: A JSON string containing the folders. And if there are more folders, it will return the nextLink to get the next page of folders.
    """
    return folders_requests.get_folder_names()


@mcp.tool()
def get_subfolders(folder_id: str) -> str:
    """
    Gets the subfolders of a specific folder in the Outlook mailbox.
    params:
        folder_id (str): The id of the folder for which to retrieve the subfolders.
    returns:
        str: A JSON string containing the subfolders information. And if there are more subfolders, it will return the nextLink to get the next page of subfolders.
    """
    return folders_requests.get_subfolders_microsoft_api(folder_id)


@mcp.tool()
def add_delete_flag_or_mark_as_complete(email_id: str, flag: str):
    """
    Marks an email with email_id with a flag or removes its flags or marks it as completed.
    params:
        email_id (str): The id of the email to mark with a flag
        flag (str): The type of the flag that is put to the email, it can have the following values:
            - "flagged": it is marked
            - "notFlagged": it is not marked
            - "complete":  it is marked as completed
    returns:
        The info about the email that was actualized
    """
    return flag_requests.manage_flags_microsoft_api(email_id, flag)


@mcp.tool()
def get_message_rules():
    """
    Gets the message rules of the Outlook mailbox.
    returns:
        str: A JSON string containing the message rules.
    """
    return rules_requests.get_message_rules_microsoft_api()


@mcp.tool()
def create_edit_message_rule(mail_rule: MailRule, rule_id: Optional[str] = None):
    """
    Creates a message rule in the Outlook mailbox.
    params:
        mail_rule (MailRule): The message rule to create.
        rule_id (str): The id of the rule to edit, if not provided, a new rule will be created.
    returns:
        str: A confirmation message or an error message.
    """

    return rules_requests.create_message_rule_microsoft_api(mail_rule, rule_id)


@mcp.tool()
def delete_message_rule(rule_id: str):
    """
    Deletes a message rule in the Outlook mailbox.
    params:
        rule_id (str): The id of the rule to delete.
    """
    return rules_requests.delete_message_rule_microsoft_api(rule_id)


@mcp.tool()
def get_next_link(next_link: str):
    """
    Gets the next page of the given link.
    params:
        next_link (str): The nextLink to get the next page of.
    returns:
        str: A JSON string containing the next page of the given link.
    """
    return rules_requests.get_next_link_microsoft_api(next_link)


@mcp.resource("outlook://root/folders")
def get_user_folders() -> str:
    """
    Gets the folders of the Outlook mailbox.
    returns:
        str: A JSON string containing the folders. And if there are more folders, it will return the nextLink to get the next page of folders.
    """
    return folders_requests.get_folder_names()


@mcp.prompt()
def get_emails_sender(
    sender_email: str,
    number_emails: Optional[str] = "10",
    folder_name: Optional[str] = None,
    unread_only: Optional[str] = "false",
) -> str:
    """
    Prompt to get the latest unread number_emails emails from the Outlook inbox with the specified caracteristics.
    params:
        number_emails (int): The number of latest unread emails to retrieve.
    returns:
        str: A JSON string containing the latest unread emails.
    """
    ret_str = ""
    if folder_name:
        ret_str += f"Search in the folder '{folder_name}', to get the id of the folder and use the get_folders_info_at_outlook tool. If you don't see the folder, or one with a similar name, you can use the tool get_subfolders to get the subfolders of a specific folder and look there."
    ret_str += f"Search for the latest {number_emails} emails from the sender '{sender_email}'. The emails have to be unread = {unread_only}"

    return ret_str


@mcp.prompt()
def get_emails_keyword(
    keyword: str,
    number_emails: Optional[str] = "10",
    folder_name: Optional[str] = None,
    unread_only: Optional[str] = "false",
) -> str:
    """
    Prompt to get the latest unread number_emails emails from the Outlook inbox with the specified caracteristics.
    params:
        number_emails (int): The number of latest unread emails to retrieve.
    returns:
        str: A JSON string containing the latest unread emails.
    """
    ret_str = ""
    if folder_name:
        ret_str += f"Search in the folder '{folder_name}', to get the id of the folder use the get_folders_info_at_outlook tool. If you don't see the folder, or one with a similar name, you can use the tool get_subfolders to get the subfolders of a specific folder and look there."
    ret_str += f"Search for the latest {number_emails} emails with the keyword '{keyword}' in the subject or body. The emails have to be unread = {unread_only}."

    return ret_str


@mcp.prompt()
def create_edit_rules(rule_name: str, rule_description: str) -> str:
    """
    Prompt to create or edit a message rule in the Outlook mailbox.
    returns:
        str: A JSON string containing the message rule to create or edit.
    """
    return f"Use the tools get_message_rules to get the current message rules, if there is a rules with the a very similar name, you edit it, otherwise you create a new rule. The rule name is: {rule_name}. The rule consiste on the following: {rule_description}"


@mcp.prompt()
def create_draft_email(
    subject: str,
    body: str,
    to_recipients: str,
    cc_recipients: Optional[str] = None,
    importance: Optional[str] = "normal",
) -> str:
    """
    Prompt to create a draft email with the specified subject, body, recipients and importance.
    params:
        subject (str): The subject of the email.
        body (str): The body of the email.
        to_recipients (List[str]): The list of email addresses for the "To" field.
        cc_recipients (Optional[List[str]]): The list of email addresses for the "CC" field.
        importance (Optional[str]): The importance level of the email. Default is "normal".
    returns:
        str: A JSON string containing the created draft email.
    """
    return f"Create a draft email with subject '{subject}' and body '{body}' to {to_recipients} with CC {cc_recipients} and importance {importance}"


if __name__ == "__main__":
    # Start the MCP server
    mcp.run()

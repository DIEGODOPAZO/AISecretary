from utils.param_types import *
from utils.email.microsoft_folders_requests import MicrosoftFoldersRequests
from utils.email.microsoft_messages_requests import MicrosoftMessagesRequests
from utils.email.microsoft_rules_requests import MicrosoftRulesRequests
from utils.email.microsoft_flag_requests import MicrosoftFlagRequests
from utils.categories.microsoft_categories_requests import MicrosoftCategoriesRequests

# server.py
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("AISecretary-Outlook-Mail", dependencies=["mcp[cli]", "msal"])

filter_dateTime = "receivedDateTime ge 2016-01-01T00:00:00Z"  # Needed to have the params of orderBy in the filter

folders_requests = MicrosoftFoldersRequests()
messages_requests = MicrosoftMessagesRequests()
rules_requests = MicrosoftRulesRequests()
flag_requests = MicrosoftFlagRequests()
categories_requests = MicrosoftCategoriesRequests()


@mcp.tool()
def get_last_emails_outlook(email_search_params: EmailSearchParams) -> str:
    """
    Gets the last {number_emails} emails from the Outlook mailbox that were sent to the user.

    returns:
        str: A JSON string containing the emails. And if there are more emails, it will return the nextLink to get the next page of emails.
    """
    params = {
        "$top": email_search_params.number_emails,
        "$orderBy": "receivedDateTime DESC",
    }

    return messages_requests.get_messages_from_folder_microsoft_api(
        params, email_search_params=email_search_params
    )


@mcp.tool()
def get_important_emails_outlook(email_search_params: EmailSearchParams) -> str:
    """
    Gets the important emails from the Outlook mailbox that were sent to the user.
    returns:
        str: A JSON string containing the important emails. And if there are more emails, it will return the nextLink to get the next page of emails.
    """

    params = {
        "$filter": f"{filter_dateTime} and importance eq 'high'",
        "$top": email_search_params.number_emails,
        "$orderBy": "receivedDateTime DESC",
    }
    return messages_requests.get_messages_from_folder_microsoft_api(
        params, email_search_params=email_search_params
    )


@mcp.tool()
def get_emails_from_mail_sender(
    sender_email: str, email_search_params: EmailSearchParams
) -> str:
    """
    Gets the emails from a specific sender's email address.

    returns:
        str: A JSON string containing the emails from the specified sender. And if there are more emails, it will return the nextLink to get the next page of emails.
    """

    params = {
        "$filter": f"{filter_dateTime} and from/emailAddress/address eq '{sender_email}'",
        "$top": email_search_params.number_emails,
        "$orderBy": "receivedDateTime DESC",
    }

    return messages_requests.get_messages_from_folder_microsoft_api(
        params, email_search_params=email_search_params
    )


@mcp.tool()
def get_emails_with_keyword(
    keyword: str, email_search_params: EmailSearchParams
) -> str:
    """
    Gets the emails that contain a specific keyword in the subject or body.

    returns:
        str: A JSON string containing the emails that match the keyword. And if there are more emails, it will return the nextLink to get the next page of emails.
    """

    params = {"$search": f"{keyword}", "$top": email_search_params.number_emails}

    return messages_requests.get_messages_from_folder_microsoft_api(
        params, email_search_params=email_search_params
    )


@mcp.tool()
def get_emails_with_subject(
    subject: str, email_search_params: EmailSearchParams
) -> str:
    """
    Gets the emails with a specific subject

    returns:
        str: A JSON string containing the emails that have the specified subject. And if there are more emails, it will return the nextLink to get the next page of emails.
    """
    params = {
        "$search": f'"subject:{subject}"',
        "$top": email_search_params.number_emails,
    }

    return messages_requests.get_messages_from_folder_microsoft_api(
        params, email_search_params=email_search_params
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
def outlook_inbox_new(number_emails: int) -> str:
    """
    Prompt to get the latest unread number_emails emails from the Outlook inbox.
    params:
        number_emails (int): The number of latest unread emails to retrieve.
    returns:
        str: A JSON string containing the latest unread emails.
    """
    return f"Give me the latest {number_emails} unread emails from my Outlook inbox"


@mcp.prompt()
def outlook_inbox_important(number_emails: int) -> str:
    """
    Prompt to get the latest important emails from the Outlook inbox.
    params:
        number_emails (int): The number of latest important emails to retrieve.
    returns:
        str: A JSON string containing the latest important emails.
    """
    return f"Give me the latest {number_emails} important emails from my Outlook inbox"


@mcp.prompt()
def outlook_inbox_from_sender(sender_email: str, number_emails: int) -> str:
    """
    Prompt to get the latest emails from a specific sender's email address.
    params:
        sender_email (str): The email address of the sender.
        number_emails (int): The number of latest emails to retrieve.
    returns:
        str: A JSON string containing the latest emails from the specified sender.
    """
    return f"Give me the latest {number_emails} emails from {sender_email} in my Outlook inbox"


@mcp.prompt()
def outlook_inbox_with_keyword(keyword: str, number_emails: Optional[int] = 10) -> str:
    """
    Prompt to get the latest emails that contain a specific keyword in the subject or body.
    params:
        keyword (str): The keyword to search for in the emails.
        number_emails (int): The number of latest emails to retrieve.
    returns:
        str: A JSON string containing the latest emails that match the keyword.
    """
    return f"Give me the latest {number_emails} emails that contain '{keyword}' in my Outlook inbox"


@mcp.prompt()
def outlook_inbox_from_folder(folder_name: str, number_emails: int) -> str:
    """
    Prompt to get the latest emails from a specific folder in the Outlook inbox.
    params:
        folder_name (str): The name of the folder to search in.
        number_emails (int): The number of latest emails to retrieve.
    returns:
        str: A JSON string containing the latest emails from the specified folder.
    """
    return f"Give me the latest {number_emails} emails from the '{folder_name}' folder in my Outlook inbox"


if __name__ == "__main__":
    # Start the MCP server
    mcp.run()

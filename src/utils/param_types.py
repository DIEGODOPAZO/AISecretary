from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class EmailSearchParams:
    """
    Parameter for searching emails
        number_emails: Number of emails to retrieve
        folder_id: ID of the folder to search in, if None, searches in all folders. To obtain the folder ID, use the `get_folder_names_at_mailbox` tool and then if you don't find the folder, use the `get_subfolders` tool to get all subfolders of the folder
        unread_only: If True, only retrieves unread emails
    """

    number_emails: int = 10
    folder_id: Optional[str] = None
    unread_only: bool = False


@dataclass
class EmailRecipients:
    """
    Describes the recipients of an email
        to_recipients: List of email addresses for the "To" field
        cc_recipients: List of email addresses for the "CC" field
    """

    to_recipients: List[str] = field(default_factory=list)
    cc_recipients: List[str] = field(default_factory=list)


@dataclass
class DraftEmailData:
    """
    Data for creating or updating a draft email
        subject: Subject of the email
        body: Body of the email
        to_recipients: List of email addresses for the "To" field
        cc_recipients: List of email addresses for the "CC" field
        draft_id: ID of the draft email, if updating an existing draft, if none, creates a new draft
        importance: Importance level of the email, default is "normal", other options are "low" and "high"
    """

    subject: str
    body: str
    email_recipients: EmailRecipients
    draft_id: Optional[str] = None
    importance: str = "normal"


@dataclass
class EmailForwardParams:
    """
    Parameters for forwarding an email
        email_id: ID of the email to forward
        to_recipients: List of email addresses to forward the email to
        cc_recipients: List of email addresses to CC in the forwarded email
        comment: Optional comment to add when forwarding
    """

    email_id: str
    email_recipients: EmailRecipients
    comment: Optional[str] = None


@dataclass
class EmailReplyParams:
    """
    Parameters for replying to an email
        email_id: ID of the email to reply to
        body: Body of the reply
        reply_all: If True, replies to all recipients
    """

    email_id: str
    body: str = "Thank you for your email. I will get back to you soon."
    reply_all: bool = False


@dataclass
class EmailOperationParams:
    """
    Parameters for moving or copying an email
        email_id: ID of the email to move or copy
        destination_folder_id: ID of the folder to move or copy the email to, if None, moves or copies to the inbox
        move: If True, moves the email, if False, copies it
    """

    email_id: str
    destination_folder_id: Optional[str] = None
    move: bool = True


@dataclass
class FolderParams:
    """
    Parameters for editing or creating
        folder_name: Name of the folder to create or edit
        folder_id: folder ID of the folder to edit, if None, it creates a new folder
        parent_folder_id: ID of the parent folder where to create the new folder, if None, it creates it to the root folder
    """

    folder_name: str
    folder_id: Optional[str] = None
    parent_folder_id: Optional[str] = None

@dataclass
class CategoryParams:
    """
    Parameters for creating or editing a category
        category_name: Name of the category to create or edit
        category_id: ID of the category to edit, if None, it creates a new category
        preset_color: Color of the category, it ranges from preset0 to preset25
    """
    category_name: str
    category_id: Optional[str] = None
    preset_color: str = "preset0"
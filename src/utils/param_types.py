from dataclasses import dataclass, field
from typing import List, Optional, Literal


@dataclass
class EmailSearchParams:
    """
    Parameter for searching emails.

    Args:
        number_emails (int): Number of emails to retrieve.
        folder_id (Optional[str]): ID of the folder to search in. If None, searches in all folders.
        unread_only (bool): If True, only retrieves unread emails.
    """

    number_emails: int = 10
    folder_id: Optional[str] = None
    unread_only: bool = False


@dataclass
class EmailRecipients:
    """
    Describes the recipients of an email.

    Args:
        to_recipients (List[str]): List of email addresses for the "To" field.
        cc_recipients (List[str]): List of email addresses for the "CC" field.
    """

    to_recipients: List[str] = field(default_factory=list)
    cc_recipients: List[str] = field(default_factory=list)


@dataclass
class DraftEmailData:
    """
    Data for creating or updating a draft email.

    Args:
        subject (str): Subject of the email.
        body (str): Body of the email.
        email_recipients (EmailRecipients): Recipients of the email (to and cc).
        draft_id (Optional[str]): ID of the draft email, if updating an existing draft. If None, creates a new draft.
        importance (str): Importance level of the email. Default is "normal". Other options are "low" and "high".
    """

    subject: str
    body: str
    email_recipients: EmailRecipients
    draft_id: Optional[str] = None
    importance: str = "normal"


@dataclass
class EmailForwardParams:
    """
    Parameters for forwarding an email.

    Args:
        email_id (str): ID of the email to forward.
        email_recipients (EmailRecipients): Recipients to forward the email to (to and cc).
        comment (Optional[str]): Optional comment to add when forwarding.
    """

    email_id: str
    email_recipients: EmailRecipients
    comment: Optional[str] = None


@dataclass
class EmailReplyParams:
    """
    Parameters for replying to an email.

    Args:
        email_id (str): ID of the email to reply to.
        body (str): Body of the reply.
        reply_all (bool): If True, replies to all recipients.
    """

    email_id: str
    body: str = "Thank you for your email. I will get back to you soon."
    reply_all: bool = False


@dataclass
class EmailOperationParams:
    """
    Parameters for moving or copying an email.

    Args:
        email_id (str): ID of the email to move or copy.
        destination_folder_id (Optional[str]): ID of the folder to move or copy the email to. If None, moves or copies to the inbox.
        move (bool): If True, moves the email. If False, copies it.
    """

    email_id: str
    destination_folder_id: Optional[str] = None
    move: bool = True


@dataclass
class FolderParams:
    """
    Parameters for editing or creating a folder.

    Args:
        folder_name (str): Name of the folder to create or edit.
        folder_id (Optional[str]): ID of the folder to edit. If None, creates a new folder.
        parent_folder_id (Optional[str]): ID of the parent folder where to create the new folder. If None, creates it in the root folder.
    """

    folder_name: str
    folder_id: Optional[str] = None
    parent_folder_id: Optional[str] = None


@dataclass
class CategoryParams:
    """
    Parameters for creating or editing a category.

    Args:
        category_name (str): Name of the category to create or edit.
        category_id (Optional[str]): ID of the category to edit. If None, creates a new category.
        preset_color (str): Color of the category. Ranges from preset0 to preset25.
    """

    category_name: str
    category_id: Optional[str] = None
    preset_color: str = "preset0"


@dataclass
class HandleCategoryToResourceParams:
    """
    Parameters for adding or removing a category to/from a resource.

    Args:
        resource_id (str): ID of the resource to add or remove the category to/from. Can be an email or a calendar event.
        category_names (List[str]): Names of the categories to add or remove.
        remove (bool): If True, removes the category from the resource. If False, adds the category to the resource.
    """

    resource_id: str
    category_names: List[str] = field(default_factory=list)
    remove: bool = False


@dataclass
class EmailAddressValue:
    address: str


@dataclass
class EmailAddress:
    emailAddress: EmailAddressValue


@dataclass
class RuleConditions:
    """
    Conditions for a mail rule.
    All conditions are optional, so you can create a rule with no conditions.
    Args:
        subjectContains (Optional[List[str]]): List of strings that the subject must contain.
        bodyContains (Optional[List[str]]): List of strings that the body must contain.
        senderContains (Optional[List[str]]): List of strings that the sender must contain.
        recipientContains (Optional[List[str]]): List of strings that the recipient must contain.
        fromAddresses (Optional[List[EmailAddress]]): List of sender email addresses.
        sentToAddresses (Optional[List[EmailAddress]]): List of recipient email addresses.
        importance (Optional[Literal["Low", "Normal", "High"]]): Importance level.
        hasAttachments (Optional[bool]): Whether the email has attachments.
        isApprovalRequest (Optional[bool]): Whether the email is an approval request.
        isAutomaticForward (Optional[bool]): Whether the email is an automatic forward.
        isReadReceipt (Optional[bool]): Whether the email is a read receipt.
        isMeetingRequest (Optional[bool]): Whether the email is a meeting request.
    """

    subjectContains: Optional[List[str]] = None
    bodyContains: Optional[List[str]] = None
    senderContains: Optional[List[str]] = None
    recipientContains: Optional[List[str]] = None
    fromAddresses: Optional[List[EmailAddress]] = None
    sentToAddresses: Optional[List[EmailAddress]] = None
    importance: Optional[Literal["Low", "Normal", "High"]] = None
    hasAttachments: Optional[bool] = None
    isApprovalRequest: Optional[bool] = None
    isAutomaticForward: Optional[bool] = None
    isReadReceipt: Optional[bool] = None
    isMeetingRequest: Optional[bool] = None


@dataclass
class RuleActions:
    """
    Actions for a mail rule.
    All actions are optional, so you can create a rule with no actions.
    Args:
        moveToFolder (Optional[str]): Folder ID to move the email to.
        copyToFolder (Optional[str]): Folder ID to copy the email to.
        delete (Optional[bool]): Whether to delete the email.
        forwardTo (Optional[List[EmailAddress]]): List of email addresses to forward to.
        redirectTo (Optional[List[EmailAddress]]): List of email addresses to redirect to.
        markAsRead (Optional[bool]): Whether to mark the email as read.
        markImportance (Optional[Literal["Low", "Normal", "High"]]): Importance level to mark.
        permanentDelete (Optional[bool]): Whether to permanently delete the email.
        stopProcessingRules (Optional[bool]): Whether to stop processing further rules.
    """

    moveToFolder: Optional[str] = None
    copyToFolder: Optional[str] = None
    delete: Optional[bool] = None
    forwardTo: Optional[List[EmailAddress]] = None
    redirectTo: Optional[List[EmailAddress]] = None
    markAsRead: Optional[bool] = None
    markImportance: Optional[Literal["Low", "Normal", "High"]] = None
    permanentDelete: Optional[bool] = None
    stopProcessingRules: Optional[bool] = None


@dataclass
class MailRule:
    """
    Represents a mail rule.

    Args:
        displayName (str): Name of the rule.
        sequence (int): Sequence/order of the rule.
        conditions (Optional[RuleConditions]): Conditions for the rule.
        actions (Optional[RuleActions]): Actions to perform if conditions are met.
        isEnabled (bool): Whether the rule is enabled.
        isReadOnly (bool): Whether the rule is read-only.
    """

    displayName: str
    sequence: int
    conditions: Optional[RuleConditions] = None
    actions: Optional[RuleActions] = None
    isEnabled: bool = True
    isReadOnly: bool = False

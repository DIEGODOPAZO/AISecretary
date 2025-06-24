from dataclasses import dataclass, field
from datetime import datetime as DateTime
from typing import List, Optional, Literal


@dataclass
class DateFilter:
    """Filter for date ranges
    Args:
        start_date (Optional[DateTime]): Start date for the filter. Example: 2025-06-19T23:59:59.000Z
        end_date (Optional[DateTime]): End date for the filter. Example: 2025-06-19T23:59:59.000Z
    """

    start_date: Optional[DateTime] = None
    end_date: Optional[DateTime] = None


@dataclass
class SearchParams:
    """Parameters for search operations ($search in Graph API)
    Args:
        keyword (Optional[str]): Keyword to search for in the emails.
        subject (Optional[str]): Subject to search for in the emails.
    """

    keyword: Optional[str] = None
    subject: Optional[str] = None


@dataclass
class EmailFilters:
    """All available email filters
    Args:
        date_filter (Optional[DateFilter]): Filter for date ranges.
        importance (Optional[str]): Importance level of the email ('high', 'normal', 'low').
        sender (Optional[str]): Email address of the sender to filter by.
        unread_only (bool): If True, filters only unread emails.
        has_attachments (bool): If True, filters emails that have attachments.
        categories (Optional[List[str]]): List of category names to filter by.
    """

    date_filter: Optional[DateFilter] = None
    importance: Optional[str] = None  # 'high', 'normal', 'low'
    sender: Optional[str] = None
    unread_only: bool = False
    has_attachments: bool = False
    categories: Optional[List[str]] = None


@dataclass
class EmailQuery:
    """Complete email query parameters
    Args:
        filters (EmailFilters): Filters to apply to the email query.
        search (Optional[SearchParams]): Search parameters for the email query.
        number_emails (int): Number of emails to retrieve. Default is 10.
        folder_id (Optional[str]): ID of the folder to query emails from. If None, queries all folders.
    """

    filters: EmailFilters = field(default_factory=EmailFilters)
    search: Optional[SearchParams] = None
    number_emails: int = 10
    folder_id: Optional[str] = None


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


@dataclass
class EmailAddressCalendar:
    """Represents an email address with an optional name.
    Args:
        address (str): The email address.
        name (Optional[str]): The name associated with the email address.
    """
    address: str
    name: Optional[str] = None

@dataclass
class Attendee:
    """Represents an attendee for a calendar event.
    Args:   
    emailAddress (EmailAddress): The email address of the attendee.
        type (Optional[str]): The type of attendee, e.g., "required", "optional" or "resource".
    """
    emailAddress: EmailAddressCalendar
    type: Optional[str] = "required"  # Puede ser "required", "optional", etc.

@dataclass
class EventBody:
    """Represents the body of an event.
    Args:
        contentType (str): Type of the content, e.g., "HTML" or "Text".
        content (str): The content of the body.
    """
    contentType: str
    content: str

@dataclass
class DateTimeTimeZone:
    """Represents a date and time with a time zone.
    Args:
        dateTime (str): The date and time in ISO 8601 format, e.g., "2025-06-24T14:00:00".
        timeZone (str): The time zone, e.g., "America/Bogota".
    """
    dateTime: str  
    timeZone: str  

@dataclass
class Location:
    """Represents a location for an event.
    Args:   
        displayName (str): The name of the location.
    """
    displayName: str

@dataclass
class RecurrencePattern:
    """Represents the recurrence pattern for an event.
    Args:   
    type (str): The type of recurrence, e.g., "daily", "weekly", "absoluteMonthly", etc.
        interval (Optional[int]): The interval of recurrence, e.g., every 2 weeks.
        month (Optional[int]): The month of recurrence, if applicable (1-12).
        dayOfMonth (Optional[int]): The day of the month for monthly recurrences (1-31).
        daysOfWeek (Optional[List[str]]): List of days of the week for weekly recurrences, e.g., ["monday", "wednesday"].
        firstDayOfWeek (Optional[str]): The first day of the week, e.g., "sunday".
        index (Optional[str]): The index of the occurrence in the month, e.g., "first", "second", "third", etc.
    """
    type: str
    interval: int
    month: int
    dayOfMonth: int
    firstDayOfWeek: str  
    index: str 
    daysOfWeek: List[str] = field(default_factory=list) 

@dataclass
class RecurrenceRange:
    """Represents the range of recurrence for an event.
    Args:
        type (str): The type of recurrence range, e.g., "endDate", "noEnd", "numbered".
        startDate (str): The start date of the recurrence in "YYYY-MM-DD" format.
        endDate (Optional[str]): The end date of the recurrence, if type is "endDate".
        numberOfOccurrences (Optional[int]): The number of occurrences, if type is "numbered".
        recurrenceTimeZone (Optional[str]): The time zone for the recurrence.       
    """
    type: str 
    startDate: str  
    endDate: str 
    numberOfOccurrences: int
    recurrenceTimeZone: str

@dataclass
class PatternedRecurrence:
    """
    Represents a recurrence pattern for an event.
    Args:
        pattern (RecurrencePattern): The recurrence pattern.    
        range (RecurrenceRange): The range of the recurrence.
    """
    pattern: RecurrencePattern
    range: RecurrenceRange

@dataclass
class EventParams:
    """Represents a calendar event. 
    Args:
        subject (str): The subject of the event.
        start (DateTimeTimeZone): Start date and time of the event.
        end (DateTimeTimeZone): End date and time of the event.
        body (Optional[EventBody]): Body of the event.
        location (Optional[Location]): Location of the event.
        attendees (Optional[List[Attendee]]): List of attendees for the event.
        isOnlineMeeting (Optional[bool]): Whether the event is an online meeting.
        onlineMeetingProvider (Optional[str]): Provider for the online meeting, e.g., "teamsForBusiness".
        recurrence (Optional[PatternedRecurrence]): Recurrence pattern for the event, if applicable.
        sensitivity (Optional[str]): Sensitivity of the event, e.g., "normal", "personal", "private", "confidential".
        importance (Optional[str]): Importance of the event, e.g., "low", "normal", "high".
        showAs (Optional[str]): How the event should be shown, e.g., "free", "tentative", "busy".
        isAllDay (Optional[bool]): Whether the event is an all-day event.
        categories (Optional[List[str]]): List of categories for the event.
        transactionId (Optional[str]): Transaction ID for the event, if applicable.
        reminderMinutesBeforeStart (Optional[int]): Reminder time in minutes before the event starts.
        responseRequested (Optional[bool]): Whether a response is requested from attendees.
        allowNewTimeProposals (Optional[bool]): Whether to allow new time proposals from attendees.
        hideAttendees (Optional[bool]): Whether to hide attendees from the event details.
    """
    subject: str
    start: DateTimeTimeZone
    end: DateTimeTimeZone
    body: Optional[EventBody] = None
    location: Optional[Location] = None
    locations: Optional[List[Location]] = field(default_factory=list)
    attendees: Optional[List[Attendee]] = field(default_factory=list)
    isOnlineMeeting: Optional[bool] = None
    onlineMeetingProvider: Optional[str] = None  
    recurrence: Optional[PatternedRecurrence] = None  
    sensitivity: Optional[str] = None  
    importance: Optional[str] = None 
    showAs: Optional[str] = None 
    isAllDay: Optional[bool] = None
    categories: Optional[List[str]] = field(default_factory=list)
    transactionId: Optional[str] = None
    reminderMinutesBeforeStart: Optional[int] = None
    responseRequested: Optional[bool] = None
    allowNewTimeProposals: Optional[bool] = None
    hideAttendees: Optional[bool] = None


@dataclass
class EventSearchParams:
    """Parameters for searching calendar events using filters.
    Args:
        search_params (Optional[SearchParams]): Search parameters for the event search.
        location (Optional[str]): Location to filter events by.
        body (Optional[str]): Body content to filter events by.
    """
    subject: Optional[str] = None
    body: Optional[str] = None

@dataclass
class EventFilters:
    """
    All available filters for calendar events

    Args:
        date_filter (Optional[DateFilter]): Start/end datetime range.
        importance (Optional[str]): 'low', 'normal', 'high'.
        is_all_day (Optional[bool]): If True, only all-day events.
        has_attachments (Optional[bool]): Filter by presence of attachments.
        categories (Optional[List[str]]): Filter by category tags.
        is_cancelled (Optional[bool]): Include only cancelled events.
    """
    date_filter: Optional[DateFilter] = None
    importance: Optional[str] = None  # 'low' | 'normal' | 'high'
    is_all_day: Optional[bool] = None
    has_attachments: Optional[bool] = None
    categories: Optional[List[str]] = None
    is_cancelled: Optional[bool] = None

@dataclass
class EventQuery:
    """
    Complete event query parameters

    Args:
        filters (EventFilters): Filtering options for the event query.
        search (Optional[EventSearchParams]): Search terms for events.
        number_events (int): Number of events to retrieve. Default is 10.
        calendar_id (Optional[str]): ID of the calendar to query. Default uses primary calendar.
    """
    filters: EventFilters = field(default_factory=EventFilters)
    search: Optional[EventSearchParams] = None
    number_events: int = 10
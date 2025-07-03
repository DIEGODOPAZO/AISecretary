from dataclasses import asdict, dataclass, field
from datetime import datetime as DateTime

from typing import Any, Dict, List, Optional, Literal


@dataclass
class DateFilter:
    """
    Filter for date ranges.

    Args:
        start_date (Optional[DateTime]): Start date for the filter. Example: 2025-06-19T23:59:59.000Z
        end_date (Optional[DateTime]): End date for the filter. Example: 2025-06-19T23:59:59.000Z
    """

    start_date: Optional[DateTime] = None
    end_date: Optional[DateTime] = None


@dataclass
class SearchParams:
    """
    Parameters for search operations ($search in Graph API).

    Args:
        keyword (Optional[str]): Keyword to search for in the emails.
        subject (Optional[str]): Subject to search for in the emails.
    """

    keyword: Optional[str] = None
    subject: Optional[str] = None


@dataclass
class EmailFilters:
    """
    All available email filters.

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
    """
    Complete email query parameters.

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

PresetColor = Literal[
    "preset0", "preset1", "preset2", "preset3", "preset4", "preset5",
    "preset6", "preset7", "preset8", "preset9", "preset10", "preset11",
    "preset12", "preset13", "preset14", "preset15", "preset16", "preset17",
    "preset18", "preset19", "preset20", "preset21", "preset22", "preset23",
    "preset24", "preset25"
]
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
    preset_color: PresetColor = "preset0"



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
    """
    Represents an email address value.

    Args:
        address (str): The email address.
    """
    address: str


@dataclass
class EmailAddress:
    """
    Represents an email address object.

    Args:
        emailAddress (EmailAddressValue): The email address value object.
    """
    emailAddress: EmailAddressValue


@dataclass
class RuleConditions:
    """
    Conditions for a mail rule. All conditions are optional, so you can create a rule with no conditions.

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
    Actions for a mail rule. All actions are optional, so you can create a rule with no actions.

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
    """
    Represents an email address with an optional name.

    Args:
        address (str): The email address.
        name (Optional[str]): The name associated with the email address.
    """
    address: str
    name: Optional[str] = None


@dataclass
class Attendee:
    """
    Represents an attendee for a calendar event.

    Args:
        emailAddress (EmailAddress): The email address of the attendee.
        type (Optional[str]): The type of attendee, e.g., "required", "optional" or "resource".
    """
    emailAddress: EmailAddressCalendar
    type: Optional[str] = "required"  # Puede ser "required", "optional", etc.


@dataclass
class EventBody:
    """
    Represents the body of an event.

    Args:
        contentType (str): Type of the content, e.g., "HTML" or "Text".
        content (str): The content of the body.
    """
    contentType: str
    content: str


@dataclass
class DateTimeTimeZone:
    """
    Represents a date and time with a time zone.

    Args:
        dateTime (str): The date and time in ISO 8601 format, e.g., "2025-06-24T14:00:00".
        timeZone (str): The time zone, e.g., "America/Bogota".
    """
    dateTime: str  
    timeZone: str  


@dataclass
class Location:
    """
    Represents a location for an event.

    Args:
        displayName (str): The name of the location.
    """
    displayName: str


@dataclass
class RecurrencePattern:
    """
    Represents the recurrence pattern for an event.

    Args:
        type (str): The type of recurrence, e.g., "daily", "weekly", "absoluteMonthly", etc.
        interval (int): The interval of recurrence, e.g., every 2 weeks.
        month (int): The month of recurrence, if applicable (1-12).
        dayOfMonth (int): The day of the month for monthly recurrences (1-31).
        firstDayOfWeek (str): The first day of the week, e.g., "sunday".
        index (str): The index of the occurrence in the month, e.g., "first", "second", "third", etc.
        daysOfWeek (List[str]): List of days of the week for weekly recurrences, e.g., ["monday", "wednesday"].
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
    """
    Represents the range of recurrence for an event.

    Args:
        type (str): The type of recurrence range, e.g., "endDate", "noEnd", "numbered".
        startDate (str): The start date of the recurrence in "YYYY-MM-DD" format.
        endDate (str): The end date of the recurrence, if type is "endDate".
        numberOfOccurrences (int): The number of occurrences, if type is "numbered".
        recurrenceTimeZone (str): The time zone for the recurrence.
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
    """
    Represents a calendar event.

    Args:
        subject (str): The subject of the event.
        start (DateTimeTimeZone): Start date and time of the event.
        end (DateTimeTimeZone): End date and time of the event.
        body (Optional[EventBody]): Body of the event.
        location (Optional[Location]): Location of the event.
        locations (Optional[List[Location]]): List of locations for the event.
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
        attachments (Optional[List[str]]): List of attachments files paths for the event.
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
    attachments: Optional[List[str]] = field(default_factory=list)


@dataclass
class EventSearchParams:
    """
    Parameters for searching calendar events using filters.

    Args:
        subject (Optional[str]): Subject to filter events by.
        body (Optional[str]): Body content to filter events by.
    """
    subject: Optional[str] = None
    body: Optional[str] = None


@dataclass
class EventFilters:
    """
    All available filters for calendar events.

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
    Complete event query parameters.

    Args:
        filters (EventFilters): Filtering options for the event query.
        search (Optional[EventSearchParams]): Search terms for events.
        number_events (int): Number of events to retrieve. Default is 10.
    """
    filters: EventFilters = field(default_factory=EventFilters)
    search: Optional[EventSearchParams] = None
    number_events: int = 10


@dataclass
class CalendarGroupParams:
    """
    Parameters for retrieving calendar groups.

    Args:
        top (Optional[int]): Number of calendar groups to retrieve. Default is 10.
        filter_name (Optional[str]): Name to filter by calendar group name.
    """
    top: Optional[int] = 10
    filter_name: Optional[str] = None


@dataclass
class TimeZoneSettings:
    """
    Represents time zone settings for mailbox configuration.

    Args:
        name (str): Name of the time zone (e.g. "America/Bogota").
    """
    name: str

@dataclass
class WorkingHours:
    """
    Represents working hours configuration for mailbox settings.

    Args:
        daysOfWeek (List[str]): List of days of the week when the user is available (e.g. ["monday", "tuesday", ...]).
        startTime (str): Start time of the working hours in "HH:mm:ss.fffffff" format.
        endTime (str): End time of the working hours in "HH:mm:ss.fffffff" format.
        timeZone (TimeZoneSettings): Time zone settings for the working hours.
    """
    daysOfWeek: List[str] 
    startTime: str  
    endTime: str    
    timeZone: TimeZoneSettings

Status = Literal[
    "disabled",
    "alwaysEnabled",
    "scheduled"
]
@dataclass
class AutomaticRepliesSetting:
    """
    Represents automatic replies settings for mailbox configuration.

    Args:
        status (Status): Status of automatic replies ("disabled", "alwaysEnabled", "scheduled").
        externalAudience (str): Audience for external replies ("none", "contactsOnly", "all").
        internalReplyMessage (str): Message for internal automatic replies.
        externalReplyMessage (str): Message for external automatic replies.
        scheduledStartDateTime (DateTimeTimeZone): Start date and time for scheduled automatic replies.
        scheduledEndDateTime (DateTimeTimeZone): End date and time for scheduled automatic replies.
    """
    status: Status 
    externalAudience: str  
    internalReplyMessage: str
    externalReplyMessage: str
    scheduledStartDateTime: DateTimeTimeZone
    scheduledEndDateTime: DateTimeTimeZone


@dataclass
class MailboxSettingsParams:
    """
    Parameters for updating mailbox settings in Microsoft Graph API.

    Args:
        timeZone (Optional[str]): Time zone identifier (e.g. "America/Bogota").
        dateFormat (Optional[str]): Date format (e.g. "dd/MM/yyyy").
        timeFormat (Optional[str]): Time format (e.g. "2024-07-01T10:00:00Z").
        workingHours (Optional[WorkingHours]): Working hours configuration.
        automaticRepliesSetting (Optional[AutomaticRepliesSetting]): Automatic replies configuration.
        delegateMeetingMessageDeliveryOptions (Optional[str]): Delegate meeting message delivery options.
    """
    timeZone: Optional[str] = None
    workingHours: Optional[WorkingHours] = None
    automaticRepliesSetting: Optional[AutomaticRepliesSetting] = None


@dataclass
class EventResponseParams:
    """
    Parameters for accepting a calendar event.

    Args:
        send_response (bool): If True, sends a response to the organizer.
        comment (Optional[str]): Optional comment to include in the response.
    """
    send_response: bool = True
    comment: Optional[str] = None


@dataclass
class ProposedNewTime:
    """
    Represents a proposed new time for an event.

    Args:
        start (DateTimeTimeZone): Proposed start date and time.
        end (DateTimeTimeZone): Proposed end date and time.
    """
    start: DateTimeTimeZone
    end: DateTimeTimeZone


@dataclass
class EventChangesParams: 
    """
    Parameters for declining a calendar event.

    Args:
        event_response_params (Optional[EventResponseParams]): Parameters for the event response.
        proposed_new_time (Optional[ProposedNewTime]): Proposed new time for the event.
    """
    event_response_params: Optional[EventResponseParams]
    proposed_new_time: Optional[ProposedNewTime] = None


@dataclass
class EventCancelParams:
    """
    Parameters for cancelling a calendar event.

    Args:
        comment (Optional[str]): Optional comment for the cancellation.
        meeting_cancelation_message (Optional[DraftEmailData]): Optional draft email data for the cancellation message.
    """
    comment: Optional[str] = None
    meeting_cancelation_message: Optional[DraftEmailData] = None

CalendarColor = Literal[
    "LightBlue",    
    "LightGreen",   
    "LightOrange",  
    "LightGray",    
    "LightYellow",  
    "LightTeal",    
    "LightPink",    
    "LightBrown",   
    "LightRed",     
    "MaxColor",     
    "Auto"          
]

@dataclass
class CalendarUpdateParams:
    """
    Representa un calendario en Microsoft Graph API con propiedades esenciales.

    Args:
        name (str): El nombre del calendario.
        isDefaultCalendar (bool): True si es el calendario predeterminado del usuario, False en caso contrario.
        color (CalendarColor): Tema de color para distinguir el calendario. Valores posibles:
            - "LightBlue" (0)
            - "LightGreen" (1)
            - "LightOrange" (2)
            - "LightGray" (3)
            - "LightYellow" (4)
            - "LightTeal" (5)
            - "LightPink" (6)
            - "LightBrown" (7)
            - "LightRed" (8)
            - "MaxColor" (9)
            - "Auto" (-1) [valor por defecto]
    """
    name: str
    isDefaultCalendar: Optional[bool] = None
    color: Optional[CalendarColor] = None


@dataclass
class ScheduleParams:
    """
    Parameters for retrieving a schedule.

    Args:
        schedules (List[str]): List of email addresses to retrieve the schedule for.
        start_time (DateTimeTimeZone): Start time for the schedule.
        end_time (DateTimeTimeZone): End time for the schedule.
        availability_view_interval (int): Interval in minutes for the availability view. Default is 30 minutes.
    """
    schedules: List[str]
    start_time: DateTimeTimeZone
    end_time: DateTimeTimeZone
    availability_view_interval: int = 30

@dataclass
class EmailAddressContact:
    """
    Represents an email address with an optional name for a contact.

    Args:
        address (str): The email address.
        name (Optional[str]): The name associated with the email address.
    """
    address: str
    name: Optional[str] = None

@dataclass
class Contact:
    """
    Represents a contact with personal and business information.
    Attributes:
        givenName (str): The given name (first name) of the contact.
        surname (str): The surname (last name) of the contact.
        emailAddresses (List[EmailAddressContact]): A list of email addresses associated with the contact.
        businessPhones (List[str]): A list of business phone numbers for the contact.
        mobilePhone (str): The mobile phone number of the contact.
    """
    givenName: str
    surname: str
    emailAddresses: List[EmailAddressContact] = field(default_factory=list)
    businessPhones: List[str] = field(default_factory=list)
    mobilePhone: str = ""

@dataclass
class ItemBody:
    """
    Represents the body of a task or message.

    Args:
        content (str): The actual content of the body.
        contentType (Literal["text", "html"]): The type of content, either "text" or "html". Default is "text".
    """
    content: str
    contentType: Literal["text", "html"] = "text"

@dataclass
class PatternedRecurrence:
    """
    Represents a recurrence pattern for a task or event.

    Args:
        pattern (Dict[str, Any]): The recurrence pattern (e.g., daily, weekly, etc.).
        range (Dict[str, Any]): The range of the recurrence (e.g., start/end dates, number of occurrences).
    """
    pattern: Dict[str, Any]
    range: Dict[str, Any]


@dataclass
class TaskCreateRequest:
    """
    Represents the data required to create a Microsoft To Do task.

    Args:
        title (str): The title of the task.
        body (Optional[ItemBody]): The body/content of the task.
        dueDateTime (Optional[DateTimeTimeZone]): Due date and time for the task.
        startDateTime (Optional[DateTimeTimeZone]): Start date and time for the task.
        completedDateTime (Optional[DateTimeTimeZone]): Completion date and time for the task.
        importance (Optional[Literal["low", "normal", "high"]]): Importance of the task. Default is "normal".
        isReminderOn (Optional[bool]): Whether a reminder is set for the task.
        reminderDateTime (Optional[DateTimeTimeZone]): Date and time for the reminder.
        recurrence (Optional[PatternedRecurrence]): Recurrence pattern for the task.
        status (Optional[Literal["notStarted", "inProgress", "completed", "waitingOnOthers", "deferred"]]): Status of the task. Default is "notStarted".
    """
    title: str
    body: Optional[ItemBody] = None
    dueDateTime: Optional[DateTimeTimeZone] = None
    startDateTime: Optional[DateTimeTimeZone] = None
    completedDateTime: Optional[DateTimeTimeZone] = None
    importance: Optional[Literal["low", "normal", "high"]] = "normal"
    isReminderOn: Optional[bool] = None
    reminderDateTime: Optional[DateTimeTimeZone] = None
    recurrence: Optional[PatternedRecurrence] = None
    status: Optional[Literal["notStarted", "inProgress", "completed", "waitingOnOthers", "deferred"]] = "notStarted"

    def to_json_object(self):
        def serialize(obj):
            if isinstance(obj, list):
                return [serialize(i) for i in obj]
            elif hasattr(obj, "__dataclass_fields__"):
                return {k: serialize(v) for k, v in asdict(obj).items() if v is not None}
            else:
                return obj

        return serialize(self)
    

@dataclass
class TodoTaskFilter:
    """
    Filter parameters for querying Microsoft To Do tasks.

    Args:
        status (Optional[str]): Status of the task (e.g., 'notStarted', 'inProgress', 'completed', etc.).
        importance (Optional[str]): Importance of the task (e.g., 'low', 'normal', 'high').
        is_reminder_on (Optional[bool]): Whether the task has a reminder set.
        due_before (Optional[datetiem]): Only include tasks due before this date/time.
        due_after (Optional[datetime]): Only include tasks due after this date/time.
        created_after (Optional[datetime]): Only include tasks created after this date/time.
        created_before (Optional[datetime]): Only include tasks created before this date/time.
    """
    status: Optional[str] = None               
    importance: Optional[str] = None           
    is_reminder_on: Optional[bool] = None     
    due_before: Optional[DateTime] = None      
    due_after: Optional[DateTime] = None       
    created_after: Optional[DateTime] = None   
    created_before: Optional[DateTime] = None  

    def to_odata_filter(self) -> Optional[str]:
        """Builds the $filter string for Microsoft Graph from the provided fields."""
        filters = []

        if self.status:
            filters.append(f"status eq '{self.status}'")
        if self.importance:
            filters.append(f"importance eq '{self.importance}'")
        if self.is_reminder_on is not None:
            filters.append(f"isReminderOn eq {str(self.is_reminder_on).lower()}")
        if self.due_before:
            filters.append(f"dueDateTime/dateTime lt {self.due_before.isoformat()}Z")
        if self.due_after:
            filters.append(f"dueDateTime/dateTime gt {self.due_after.isoformat()}Z")
        if self.created_before:
            filters.append(f"createdDateTime lt {self.created_before.isoformat()}Z")
        if self.created_after:
            filters.append(f"createdDateTime gt {self.created_after.isoformat()}Z")

        return " and ".join(filters) if filters else None
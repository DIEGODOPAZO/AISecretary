GRAPH_BASE_URL = "https://graph.microsoft.com/v1.0/me"

# Settings
MAILBOX_SETTINGS_URL = f"{GRAPH_BASE_URL}/mailboxSettings"

# To-Do
TODO_LISTS_URL = f"{GRAPH_BASE_URL}/todo/lists"

# Calendars
CALENDAR_GROUPS_URL = f"{GRAPH_BASE_URL}/calendarGroups"
CALENDAR_URL = f"{GRAPH_BASE_URL}/calendar"
CALENDAR_EVENTS_URL = f"{CALENDAR_URL}/events"
CALENDAR_VIEW_URL = f"{GRAPH_BASE_URL}/calendarView"
CALENDAR_SCHEDULES_URL =  f"{GRAPH_BASE_URL}/calendar/getSchedule"
EVENTS_URL = f"{GRAPH_BASE_URL}/events"

# Categories
MASTER_CATEGORIES_URL = f"{GRAPH_BASE_URL}/outlook/masterCategories"

# Contacts
CONTACT_FOLDERS_URL = f"{GRAPH_BASE_URL}/contactFolders"
CONTACTS_URL = f"{GRAPH_BASE_URL}/contacts"
CONTACTS_BY_ID_URL = lambda contact_id: f"{CONTACTS_URL}/{contact_id}"
CONTACTS_BY_FOLDER_URL = lambda folder_id: f"{CONTACT_FOLDERS_URL}/{folder_id}/contacts"
# Mail folders
MAIL_FOLDERS_URL = f"{GRAPH_BASE_URL}/mailFolders"
MAIL_FOLDER_CHILDREN_URL = lambda folder_id: f"{MAIL_FOLDERS_URL}/{folder_id}/childFolders"
MESSAGES_IN_FOLDER_URL = lambda folder_id: f"{MAIL_FOLDERS_URL}/{folder_id}/messages"

# Messages (Emails)
MESSAGES_URL = f"{GRAPH_BASE_URL}/messages"
MESSAGE_BY_ID_URL = lambda message_id: f"{MESSAGES_URL}/{message_id}"
MESSAGE_ATTACHMENTS_URL = lambda message_id: f"{MESSAGES_URL}/{message_id}/attachments"
ATTACHMENT_BY_ID_URL = lambda message_id, attachment_id: f"{MESSAGES_URL}/{message_id}/attachments/{attachment_id}"
MESSAGE_RULES_URL = f"{GRAPH_BASE_URL}/mailFolders/inbox/messageRules"
MESSAGE_RULES_URL_BY_ID_URL = lambda rule_id: f"{MESSAGE_RULES_URL}/{rule_id}"

# Draft emails
DRAFT_BY_ID_URL = lambda draft_id: f"{MESSAGES_URL}/{draft_id}"
ADD_ATTACHMENT_TO_DRAFT_URL = lambda draft_id: f"{MESSAGES_URL}/{draft_id}/attachments"
SEND_DRAFT_URL = lambda draft_id: f"{MESSAGES_URL}/{draft_id}/send"

# Email operations
MOVE_EMAIL_URL = lambda email_id: f"{MESSAGES_URL}/{email_id}/move"
COPY_EMAIL_URL = lambda email_id: f"{MESSAGES_URL}/{email_id}/copy"

# Replies and forwards
CREATE_REPLY_URL = lambda email_id: f"{MESSAGES_URL}/{email_id}/createReply"
CREATE_REPLY_ALL_URL = lambda email_id: f"{MESSAGES_URL}/{email_id}/createReplyAll"
FORWARD_EMAIL_URL = lambda email_id: f"{MESSAGES_URL}/{email_id}/forward"
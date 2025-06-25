from  .general_helpers import microsoft_get
from ..param_types import EventParams, EventQuery


def event_params_to_dict(event_params: EventParams) -> dict:
    data = {
        "subject": event_params.subject,
        "start": {
            "dateTime": event_params.start.dateTime,
            "timeZone": event_params.start.timeZone,
        },
        "end": {
            "dateTime": event_params.end.dateTime,
            "timeZone": event_params.end.timeZone,
        },
    }

    if event_params.body:
        data["body"] = {
            "contentType": event_params.body.contentType,
            "content": event_params.body.content,
        }

    if event_params.location:
        data["location"] = {"displayName": event_params.location.displayName}

    if event_params.locations:
        data["locations"] = [{"displayName": loc.displayName} for loc in event_params.locations]

    if event_params.attendees:
        data["attendees"] = [
            {
                "emailAddress": {
                    "address": attendee.emailAddress.address,
                    "name": attendee.emailAddress.name,
                },
                "type": attendee.type,
            }
            for attendee in event_params.attendees
        ]

    if event_params.isOnlineMeeting is not None:
        data["isOnlineMeeting"] = event_params.isOnlineMeeting

    if event_params.onlineMeetingProvider:
        data["onlineMeetingProvider"] = event_params.onlineMeetingProvider

    if event_params.recurrence:
        recurrence = event_params.recurrence
        data["recurrence"] = {
            "pattern": {
                "type": recurrence.pattern.type,
                "interval": recurrence.pattern.interval,
                "month": recurrence.pattern.month,
                "dayOfMonth": recurrence.pattern.dayOfMonth,
                "daysOfWeek": recurrence.pattern.daysOfWeek or [],
                "firstDayOfWeek": recurrence.pattern.firstDayOfWeek,
                "index": recurrence.pattern.index,
            },
            "range": {
                "type": recurrence.range.type,
                "startDate": recurrence.range.startDate,
                "endDate": recurrence.range.endDate,
                "numberOfOccurrences": recurrence.range.numberOfOccurrences,
                "recurrenceTimeZone": recurrence.range.recurrenceTimeZone,
            },
        }

    if event_params.sensitivity:
        data["sensitivity"] = event_params.sensitivity

    if event_params.importance:
        data["importance"] = event_params.importance

    if event_params.showAs:
        data["showAs"] = event_params.showAs

    if event_params.isAllDay is not None:
        data["isAllDay"] = event_params.isAllDay

    if event_params.categories:
        data["categories"] = event_params.categories

    if event_params.transactionId:
        data["transactionId"] = event_params.transactionId

    if event_params.reminderMinutesBeforeStart is not None:
        data["reminderMinutesBeforeStart"] = event_params.reminderMinutesBeforeStart

    if event_params.responseRequested is not None:
        data["responseRequested"] = event_params.responseRequested

    if event_params.allowNewTimeProposals is not None:
        data["allowNewTimeProposals"] = event_params.allowNewTimeProposals

    if event_params.hideAttendees is not None:
        data["hideAttendees"] = event_params.hideAttendees

    return data

def event_query_to_graph_params(event_query: EventQuery) -> dict:
    params = {}

    # Número de eventos → $top
    if event_query.number_events:
        params["$top"] = str(event_query.number_events)

    filters = event_query.filters
    filter_clauses = []

    # Fechas para calendarView (no se incluyen en $filter)
    if filters.date_filter:
        if filters.date_filter.start_date:
            params["startDateTime"] = filters.date_filter.start_date.isoformat()
        if filters.date_filter.end_date:
            params["endDateTime"] = filters.date_filter.end_date.isoformat()

    # Filtros para $filter
    if filters.importance:
        filter_clauses.append(f"importance eq '{filters.importance}'")
    if filters.is_all_day is not None:
        filter_clauses.append(f"isAllDay eq {str(filters.is_all_day).lower()}")
    if filters.has_attachments is not None:
        filter_clauses.append(f"hasAttachments eq {str(filters.has_attachments).lower()}")
    if filters.categories:
        for cat in filters.categories:
            filter_clauses.append(f"categories/any(c:c eq '{cat}')")
    if filters.is_cancelled is not None:
        filter_clauses.append(f"isCancelled eq {str(filters.is_cancelled).lower()}")

    # Convertir búsquedas a filtros con contains()
    search = event_query.search
    if search:
        if search.body:
            filter_clauses.append(f"contains(body/content, '{search.body}')")
        if search.subject:
                filter_clauses.append(f"contains(subject, '{search.subject}')")

    if filter_clauses:
        params["$filter"] = " and ".join(filter_clauses)

    return params


def simplify_event(event: dict) -> dict:
    """Simplifies an event object to a more manageable format."""
    return {
        "id": event.get("id"),
        "subject": event.get("subject"),
        "start": event.get("start", {}).get("dateTime"),
        "end": event.get("end", {}).get("dateTime")
    }


def simplify_event_with_attachment_names(event: dict, token: str) -> dict:
    simplified_event = {
        "id": event.get("id"),
        "subject": event.get("subject"),
        "start": event.get("start", {}).get("dateTime"),
        "end": event.get("end", {}).get("dateTime"),
        "organizer": event.get("organizer", {}).get("emailAddress", {}).get("address"),
        "attendees": [
            a["emailAddress"]["address"] for a in event.get("attendees", [])
        ],
        "web_link": event.get("webLink"),
        "location": event.get("location", {}).get("displayName"),
        "html_description": event.get("body", {}).get("content"),
        "attachment_names": []
    }

    if event.get("hasAttachments"):
        event_id = event["id"]
        url = f"https://graph.microsoft.com/v1.0/me/events/{event_id}/attachments"
       
        status_code, response = microsoft_get(url, token)
        if status_code == 200:
            for attachment in response.get("value", []):
                simplified_event["attachment_names"].append(attachment.get("name"))

    return simplified_event
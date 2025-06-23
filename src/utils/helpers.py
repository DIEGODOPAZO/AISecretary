import base64
import requests
import os
from functools import wraps
import json
from dataclasses import asdict, is_dataclass
from typing import Any, List

from .param_types import DateFilter, EventParams


def handle_microsoft_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.HTTPError as e:
            return json.dumps(
                {"error": f"HTTP error: {e.response.status_code} - {e.response.text}"},
                indent=2,
            )
        except requests.RequestException as e:
            return json.dumps({"error": f"Request failed: {str(e)}"}, indent=2)
        except Exception as e:
            return json.dumps({"error": f"Internal error: {str(e)}"}, indent=2)

    return wrapper


def microsoft_get(url: str, token: str, params: dict = {}) -> tuple[int, dict]:
    """Sends a GET request to the Microsoft Graph API."""
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.status_code, response.json()


def microsoft_delete(url: str, token: str) -> tuple[int, str]:
    """Sends a DELETE request to the Microsoft Graph API and returns status code and response text."""
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    response = requests.delete(url, headers=headers)
    response.raise_for_status()
    return response.status_code, response.text


def microsoft_post(url: str, token: str, data: dict = {}) -> tuple[int, dict]:
    response = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json=data,
    )
    response.raise_for_status()
    try:
        return response.status_code, response.json()
    except ValueError:
        return response.status_code, {}


def microsoft_patch(url: str, token: str, data: dict = {}) -> tuple[int, dict]:
    """Sends a PATCH request to the Microsoft Graph API and returns status code and response json/text."""
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    response = requests.patch(url, headers=headers, json=data)
    response.raise_for_status()

    return response.status_code, response.json()


def read_file_and_encode_base64(file_path: str) -> tuple[str, str]:
    """Reads a file and encodes its content to base64."""
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")

    filename = os.path.basename(file_path)

    with open(file_path, "rb") as file:
        file_content = file.read()
        encoded_content = base64.b64encode(file_content).decode("utf-8")

    return filename, encoded_content


def microsoft_simplify_message(
    msg: dict,
    full: bool = False,
    attachments: list = None,
    attachments_download_path: list = None,
) -> dict:
    """
    Simplifies a Microsoft Graph API message object to a more manageable format.
    """
    data = {
        "id": msg.get("id"),
        "subject": msg.get("subject"),
        "from": {
            "name": msg.get("from", {}).get("emailAddress", {}).get("name"),
            "address": msg.get("from", {}).get("emailAddress", {}).get("address"),
        },
        "toRecipients": [
            {
                "name": r.get("emailAddress", {}).get("name"),
                "address": r.get("emailAddress", {}).get("address"),
            }
            for r in msg.get("toRecipients", [])
        ],
        "ccRecipients": [
            {
                "name": r.get("emailAddress", {}).get("name"),
                "address": r.get("emailAddress", {}).get("address"),
            }
            for r in msg.get("ccRecipients", [])
        ],
        "flag": msg.get("flag"),
        "receivedDateTime": msg.get("receivedDateTime"),
        "categories": msg.get("categories"),
        "sentDateTime": msg.get("sentDateTime"),
        "isRead": msg.get("isRead"),
        "hasAttachments": msg.get("hasAttachments"),
        "importance": msg.get("importance"),
        "conversationId": msg.get("conversationId"),
        "internetMessageId": msg.get("internetMessageId"),
    }

    if full:
        data["body"] = {
            "contentType": msg.get("body", {}).get("contentType"),
            "content": msg.get("body", {}).get("content"),
        }
        # Of the attachments, we only keep the name and contentType because the content might be too large for the LLM context
        if attachments:
            data["attachments"] = [
                {
                    "name": a.get("name"),
                    "contentType": a.get("contentType"),
                    "attachment_id": a.get("id"),
                }
                for a in attachments
            ]
        else:
            data["attachments"] = []

        if attachments_download_path:
            data["attachments_download_path"] = attachments_download_path

    else:
        data["bodyPreview"] = msg.get("bodyPreview")

    return data


def get_preset_color_scheme() -> str:
    """Returns a preset color scheme for the Microsoft Graph API."""

    preset_colors = {
        "preset0": ("Rojo", "#E81123"),
        "preset1": ("Naranja oscuro", "#F7630C"),
        "preset2": ("Naranja", "#FF8C00"),
        "preset3": ("Amarillo", "#FFF100"),
        "preset4": ("Verde lima", "#BAD80A"),
        "preset5": ("Verde claro", "#107C10"),
        "preset6": ("Verde bosque", "#008272"),
        "preset7": ("Verde azulado", "#00B294"),
        "preset8": ("Azul cielo", "#00B7C3"),
        "preset9": ("Azul claro", "#0078D4"),
        "preset10": ("Azul oscuro", "#004E8C"),
        "preset11": ("Índigo", "#5C2D91"),
        "preset12": ("Violeta", "#B146C2"),
        "preset13": ("Fucsia", "#E3008C"),
        "preset14": ("Rosa", "#FF69B4"),
        "preset15": ("Marrón claro", "#A0522D"),
        "preset16": ("Marrón oscuro", "#8B4513"),
        "preset17": ("Gris claro", "#D3D3D3"),
        "preset18": ("Gris", "#A9A9A9"),
        "preset19": ("Gris oscuro", "#696969"),
        "preset20": ("Negro", "#000000"),
        "preset21": ("Azul pastel", "#8FD8F4"),
        "preset22": ("Verde pastel", "#ACE1AF"),
        "preset23": ("Amarillo pastel", "#FFFACD"),
        "preset24": ("Rosa pastel", "#FFD1DC"),
        "preset25": ("Lavanda", "#E6E6FA"),
    }
    return json.dumps(preset_colors, indent=2)


def dataclass_to_clean_dict(obj: Any) -> Any:
    if is_dataclass(obj):
        result = {}
        for k, v in asdict(obj).items():
            cleaned = dataclass_to_clean_dict(v)
            if cleaned is not None:
                result[k] = cleaned
        return result or None
    elif isinstance(obj, list):
        cleaned_list = [
            dataclass_to_clean_dict(item)
            for item in obj
            if dataclass_to_clean_dict(item) is not None
        ]
        return cleaned_list or None
    elif isinstance(obj, dict):
        return {
            k: dataclass_to_clean_dict(v)
            for k, v in obj.items()
            if dataclass_to_clean_dict(v) is not None
        }
    else:
        return obj


def build_date_filter(date_filter: DateFilter) -> str:
    """Helper to build date filter clause"""
    clauses = []
    if date_filter.start_date:
        clauses.append(f"receivedDateTime ge {date_filter.start_date.isoformat()}")
    if date_filter.end_date:
        clauses.append(f"receivedDateTime le {date_filter.end_date.isoformat()}")
    return " and ".join(clauses) if clauses else ""


def build_categories_filter(categories: List[str]) -> str:
    """Helper to build categories filter"""
    if not categories:
        return ""

    # Escape single quotes in category names by doubling them (OData standard)
    escaped_categories = [c.replace("'", "''") for c in categories if c]

    if not escaped_categories:
        return ""

    # Build individual category conditions
    category_conditions = [f"categories/any(c:c eq '{c}')" for c in escaped_categories]

    # Combine with OR and wrap in parentheses
    return f"({' or '.join(category_conditions)})"


def remove_duplicate_messages(messages: List[dict]) -> List[dict]:
    """Remove duplicate messages based on their ID while preserving order."""
    seen_ids = set()
    unique_messages = []

    for msg in messages:
        msg_id = msg.get("id")
        if msg_id and msg_id not in seen_ids:
            seen_ids.add(msg_id)
            unique_messages.append(msg)

    return unique_messages


def build_search_params(search) -> dict:
    if not search:
        return {}
    if search.keyword:
        return {"$search": f'"{search.keyword}"'}
    if search.subject:
        return {"$search": f'"subject:{search.subject}"'}
    return {}


def build_filter_params(filters) -> dict:
    parts = []
    if filters.date_filter:
        date_filter = build_date_filter(filters.date_filter)
        if date_filter:
            parts.append(date_filter)
    if filters.importance:
        parts.append(f"importance eq '{filters.importance}'")
    if filters.sender:
        parts.append(f"from/emailAddress/address eq '{filters.sender}'")
    if filters.unread_only:
        parts.append("isRead eq false")
    if filters.has_attachments:
        parts.append("hasAttachments eq true")
    if filters.categories:
        parts.append(build_categories_filter(filters.categories))
    return {"$filter": " and ".join(parts)} if parts else {}


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

def simplify_event(event: dict) -> dict:
    """Simplifies an event object to a more manageable format."""
    return {
        "id": event.get("id"),
        "subject": event.get("subject"),
        "start": event.get("start", {}).get("dateTime"),
        "end": event.get("end", {}).get("dateTime")
    }
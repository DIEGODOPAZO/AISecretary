import requests
import json

def get_request_microsoft_api(params: dict, token: str) -> str:
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    base_url = "https://graph.microsoft.com/v1.0/me/messages"

    response = requests.get(base_url, headers=headers, params=params)
    response.raise_for_status()  # Lanza excepción si algo va mal

    messages = response.json().get("value", [])
    simplified_messages = []

    for msg in messages:
        simplified = {
            "id": msg.get("id"),
            "subject": msg.get("subject"),
            "from": {
                "name": msg.get("from", {}).get("emailAddress", {}).get("name"),
                "address": msg.get("from", {}).get("emailAddress", {}).get("address")
            },
            "toRecipients": [
                {
                    "name": r.get("emailAddress", {}).get("name"),
                    "address": r.get("emailAddress", {}).get("address")
                } for r in msg.get("toRecipients", [])
            ],
            "ccRecipients": [
                {
                    "name": r.get("emailAddress", {}).get("name"),
                    "address": r.get("emailAddress", {}).get("address")
                } for r in msg.get("ccRecipients", [])
            ],
            "receivedDateTime": msg.get("receivedDateTime"),
            "sentDateTime": msg.get("sentDateTime"),
            "isRead": msg.get("isRead"),
            "hasAttachments": msg.get("hasAttachments"),
            "bodyPreview": msg.get("bodyPreview"),
            "importance": msg.get("importance"),
            "conversationId": msg.get("conversationId"),
            "internetMessageId": msg.get("internetMessageId")
        }
        simplified_messages.append(simplified)

    return json.dumps(simplified_messages, indent=2)
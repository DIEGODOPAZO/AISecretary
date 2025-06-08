import requests

def microsoft_get(url: str, token: str, params: dict = None) -> dict:
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def microsoft_simplify_message(msg: dict, full: bool = False, attachments: list = None, attachments_download_path: list = None) -> dict:
    data = {
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
        "importance": msg.get("importance"),
        "conversationId": msg.get("conversationId"),
        "internetMessageId": msg.get("internetMessageId")
    }

    if full:
        data["body"] = {
            "contentType": msg.get("body", {}).get("contentType"),
            "content": msg.get("body", {}).get("content")
        }
        # Of the attachments, we only keep the name and contentType because the content might be too large for the LLM context
        if attachments:
            data["attachments"] = [
                {
                    "name": a.get("name"),
                    "contentType": a.get("contentType")
                } for a in attachments
            ]
        else:
            data["attachments"] = []
            
        if attachments_download_path:
            data["attachments_download_path"] = attachments_download_path

    else:
        data["bodyPreview"] = msg.get("bodyPreview")

    return data

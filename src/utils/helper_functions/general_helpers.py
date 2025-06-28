"""
General helper functions for Microsoft Graph API integration and file operations.

This module provides utility functions for handling HTTP requests to the Microsoft Graph API, error handling decorators, file encoding to base64, and downloading attachments from API responses.
"""

import base64
import json
import requests
import os
from functools import wraps


def handle_microsoft_errors(func):
    """Decorator to handle errors from Microsoft Graph API requests.

    Args:
        func (Callable): The function to wrap.

    Returns:
        Callable: The wrapped function that returns a JSON error message on exception.
    """
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
    """Sends a GET request to the Microsoft Graph API.

    Args:
        url (str): The endpoint URL.
        token (str): The OAuth2 access token.
        params (dict, optional): Query parameters for the request. Defaults to {}.

    Returns:
        tuple[int, dict]: The HTTP status code and the response JSON.
    """
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.status_code, response.json()


def microsoft_delete(url: str, token: str) -> tuple[int, str]:
    """Sends a DELETE request to the Microsoft Graph API.

    Args:
        url (str): The endpoint URL.
        token (str): The OAuth2 access token.

    Returns:
        tuple[int, str]: The HTTP status code and the response text.
    """
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    response = requests.delete(url, headers=headers)
    response.raise_for_status()
    return response.status_code, response.text


def microsoft_post(url: str, token: str, data: dict = {}) -> tuple[int, dict]:
    """Sends a POST request to the Microsoft Graph API.

    Args:
        url (str): The endpoint URL.
        token (str): The OAuth2 access token.
        data (dict, optional): The JSON payload for the request. Defaults to {}.

    Returns:
        tuple[int, dict]: The HTTP status code and the response JSON (or empty dict if no JSON).
    """
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
    """Sends a PATCH request to the Microsoft Graph API.

    Args:
        url (str): The endpoint URL.
        token (str): The OAuth2 access token.
        data (dict, optional): The JSON payload for the request. Defaults to {}.

    Returns:
        tuple[int, dict]: The HTTP status code and the response JSON.
    """
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    response = requests.patch(url, headers=headers, json=data)
    response.raise_for_status()

    return response.status_code, response.json()


def read_file_and_encode_base64(file_path: str) -> tuple[str, str]:
    """Reads a file and encodes its content to base64.

    Args:
        file_path (str): The path to the file to encode.

    Returns:
        tuple[str, str]: The filename and the base64-encoded content.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")

    filename = os.path.basename(file_path)

    with open(file_path, "rb") as file:
        file_content = file.read()
        encoded_content = base64.b64encode(file_content).decode("utf-8")

    return filename, encoded_content

def download_attachments(attachments: list) -> list:
    """Downloads attachments from a list of attachments.

    Args:
        attachments (list): List of attachment dictionaries from Microsoft Graph API.

    Returns:
        list: List of dictionaries with details about the downloaded attachments (name, contentType, path, attachment_id).
    """
    download_dir = os.path.join(os.path.expanduser("~"), "Downloads", "attachments")
    os.makedirs(download_dir, exist_ok=True)
    downloaded_attachments = []
    for att in attachments:
        if att.get("@odata.type") == "#microsoft.graph.fileAttachment":
            name = att.get("name")
            content_type = att.get("contentType")
            content_bytes = att.get("contentBytes")
            id = att.get("id")
            if name and content_bytes:
                file_path = os.path.join(download_dir, name)
                with open(file_path, "wb") as f:
                    f.write(base64.b64decode(content_bytes))
                downloaded_attachments.append(
                    {
                        "name": name,
                        "contentType": content_type,
                        "path": file_path,
                        "attachment_id": id,
                    }
                )
    return downloaded_attachments
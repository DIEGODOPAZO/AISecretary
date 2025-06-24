import base64
import json
import requests
import os
from functools import wraps


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
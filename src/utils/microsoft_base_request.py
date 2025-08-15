import os
import json
import base64
import requests
from functools import wraps
from .token_manager import TokenManager

class MicrosoftBaseRequest:
    """
    Base class for making requests to the Microsoft Graph API.

    Provides helper methods for GET, POST, PATCH, DELETE requests, error handling,
    file encoding, and attachment downloading.

    Attributes:
        token_manager (TokenManager): Instance to manage authentication tokens.
    """

    def __init__(self, token_manager: TokenManager):
        """
        Initializes the MicrosoftBaseRequest with a token manager.

        Args:
            token_manager (TokenManager): An instance of TokenManager to handle authentication tokens.
        """
        self.token_manager = token_manager

    @staticmethod
    def handle_microsoft_errors(func):
        """
        Decorator to handle Microsoft Graph API request errors.

        Args:
            func (Callable): The function to wrap.

        Returns:
            Callable: The wrapped function with error handling.
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
    
    @staticmethod
    def microsoft_get(url: str, token: str, params: dict | None = None):
        """
        Sends a GET request to the Microsoft Graph API.

        Args:
            url (str): The endpoint URL.
            token (str): Bearer token for authentication.
            params (Optional[dict]): Query parameters for the request.

        Returns:
            Tuple[int, dict]: The HTTP status code and the JSON response.
        """
        params = params or {}
        headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.status_code, response.json()
    @staticmethod
    def microsoft_post(url: str, token: str, data: dict | None = None):
        """
        Sends a POST request to the Microsoft Graph API.

        Args:
            url (str): The endpoint URL.
            token (str): Bearer token for authentication.
            data (Optional[dict]): Data to send in the request body.

        Returns:
            Tuple[int, dict]: The HTTP status code and the JSON response (empty dict if no JSON).
        """
        data = data or {}
        response = requests.post(
            url,
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            json=data,
        )
        response.raise_for_status()
        try:
            return response.status_code, response.json()
        except ValueError:
            return response.status_code, {}

    @staticmethod
    def microsoft_patch(url: str, token: str, data: dict | None = None):
        """
        Sends a PATCH request to the Microsoft Graph API.

        Args:
            url (str): The endpoint URL.
            token (str): Bearer token for authentication.
            data (Optional[dict]): Data to send in the request body.

        Returns:
            Tuple[int, dict]: The HTTP status code and the JSON response.
        """
        data = data or {}
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        response = requests.patch(url, headers=headers, json=data)
        response.raise_for_status()
        return response.status_code, response.json()
    @staticmethod
    def microsoft_delete(url: str, token: str):
        """
        Sends a DELETE request to the Microsoft Graph API.

        Args:
            url (str): The endpoint URL.
            token (str): Bearer token for authentication.

        Returns:
            Tuple[int, str]: The HTTP status code and the response text.
        """
        headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        return response.status_code, response.text

    @staticmethod
    def read_file_and_encode_base64(file_path: str) -> tuple[str, str]:
        """
        Reads a file and encodes its contents in base64.

        Args:
            file_path (str): The path to the file to encode.

        Returns:
            Tuple[str, str]: The filename and the base64-encoded content.

        Raises:
            FileNotFoundError: If the file does not exist.
        """
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"The file '{file_path}' does not exist.")
        filename = os.path.basename(file_path)
        with open(file_path, "rb") as file:
            encoded_content = base64.b64encode(file.read()).decode("utf-8")
        return filename, encoded_content

    @staticmethod
    def download_attachments(attachments: list) -> list:
        """
        Downloads file attachments from a list of Microsoft Graph attachment objects.

        Args:
            attachments (list): List of attachment objects from Microsoft Graph API.

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
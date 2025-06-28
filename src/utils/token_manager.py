import json
import time

class TokenManager:
    """
    Manages access tokens, handling expiration and automatic refresh.

    Args:
        token_json_path (str): Path to the token JSON file.
        get_access_token_func (Callable): Function to call to refresh the token.
        margin_seconds (int, optional): Time in seconds before actual expiration to consider token as 'expired'. Defaults to 500.
    """
    def __init__(self, token_json_path: str, get_access_token_func, margin_seconds: int = 500):
        """
        Initializes the TokenManager and loads the initial token and expiration time.

        Args:
            token_json_path (str): Path to the token JSON file.
            get_access_token_func (Callable): Function to call to refresh the token.
            margin_seconds (int, optional): Time in seconds before actual expiration to consider token as 'expired'. Defaults to 500.
        """
        self.token_json_path = token_json_path
        self.get_access_token_func = get_access_token_func
        self.margin_seconds = margin_seconds
        self.expires_on = 0
        # Load on init
        self.token = self.get_access_token_func()
        self._load_expiration_time_from_file()

    def _load_expiration_time_from_file(self):
        """
        Loads the token expiration time from the token JSON file and updates self.expires_on.
        """
        with open(self.token_json_path, "r") as f:
            data = json.load(f)
        
        access_token_data = list(data["AccessToken"].values())[0]  
        self.expires_on = int(access_token_data["expires_on"])

    def get_token(self) -> str:
        """
        Returns the current access token, refreshing it if it is close to expiration.

        Returns:
            str: The current (possibly refreshed) access token.
        """
        now = int(time.time())
        if now + self.margin_seconds >= self.expires_on:
            self.token = self.get_access_token_func()
            self._load_expiration_time_from_file()
        return self.token
import json
import time

class TokenManager:
    def __init__(self, token_json_path: str, get_access_token_func, margin_seconds: int = 500):
        """
        :param token_json_path: Path to the token JSON file.
        :param get_access_token_func: Function to call to refresh the token.
        :param margin_seconds: Time before actual expiration to consider token as 'expired'.
        """
        self.token_json_path = token_json_path
        self.get_access_token_func = get_access_token_func
        self.margin_seconds = margin_seconds
        self.expires_on = 0
        # Load on init
        self.token = self.get_access_token_func()
        self._load_expiration_time_from_file()

    def _load_expiration_time_from_file(self):
        with open(self.token_json_path, "r") as f:
            data = json.load(f)
        
        access_token_data = list(data["AccessToken"].values())[0]  
        self.expires_on = int(access_token_data["expires_on"])

    def get_token(self) -> str:
        now = int(time.time())
        if now + self.margin_seconds >= self.expires_on:
            self.token = self.get_access_token_func()
            self._load_expiration_time_from_file()
        return self.token
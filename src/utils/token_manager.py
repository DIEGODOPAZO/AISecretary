import time

class TokenManager:
    """
    Manages access tokens, handling expiration and automatic refresh.

    Args:
        token_json_path (str): Path to the token JSON file.
        get_access_token_func (Callable): Function to call to refresh the token.
        margin_seconds (int, optional): Time in seconds before actual expiration to consider token as 'expired'. Defaults to 500.
    """
    def __init__(self, get_access_token_func, get_expiration_time, margin_seconds: int = 500):
        """
        Initializes the TokenManager and loads the initial token and expiration time.

        Args:
            get_access_token_func (Callable): Function to call to refresh the token.
            get_expiration_time (Callable): Function to call to get the expiration time of the token.
            margin_seconds (int, optional): Time in seconds before actual expiration to consider token as 'expired'. Defaults to 500.
        """
        self.get_access_token_func = get_access_token_func
        self.get_expiration_time = get_expiration_time
        self.margin_seconds = margin_seconds
        # Load on init
        self.token = self.get_access_token_func()
        self.expires_on = self.get_expiration_time()

    def get_token(self) -> str:
        """
        Returns the current access token, refreshing it if it is close to expiration.

        Returns:
            str: The current (possibly refreshed) access token.
        """
        now = int(time.time())
        if now + self.margin_seconds >= self.expires_on:
            self.token = self.get_access_token_func()
            self.expires_on = self.get_expiration_time()
        return self.token
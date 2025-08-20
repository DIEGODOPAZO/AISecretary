import os
import json
import time
from pathlib import Path
import msal
from dotenv import load_dotenv
from filelock import FileLock, Timeout

class TokenManager:
    """
    Manages Microsoft authentication, token caching, and automatic refresh.

    Loads configuration from .env automatically.
    """

    def __init__(self, margin_seconds: int = 500):
        """
        Initializes the TokenManager, loads environment variables and token cache.
        
        Args:
            margin_seconds (int, optional): Time in seconds before actual expiration to refresh the token. Defaults to 500.
        """
        # Load .env
        dotenv_path = Path(__file__).resolve().parents[2] / ".env"
        load_dotenv(dotenv_path=dotenv_path)
        self.ENV_BASE_DIR = dotenv_path.parent

        # Config
        self.CLIENT_ID = os.getenv("CLIENT_ID")
        self.TENANT_ID = os.getenv("TENANT_ID", "common")
        self.AUTHORITY = f"https://login.microsoftonline.com/{self.TENANT_ID}"
        self.SCOPES = os.getenv("SCOPES", "User.Read,Mail.ReadWrite").split(",")
        raw_token_cache_path = os.getenv("TOKEN_CACHE_FILE", "token_cache.json")
        self.TOKEN_CACHE_FILE = (self.ENV_BASE_DIR / raw_token_cache_path).resolve()

        self.margin_seconds = margin_seconds

        # Load cache
        self.cache = self._load_cache()

        # Load initial token
        self.token = self._get_access_token()
        self.expires_on = self._load_expiration_time_from_file()

    def _save_cache(self):
        if self.cache.has_state_changed:
            lock_path = str(self.TOKEN_CACHE_FILE) + ".lock"
            with FileLock(lock_path):
                with open(self.TOKEN_CACHE_FILE, "w") as f:
                    f.write(self.cache.serialize())

    def _load_cache(self):
        cache = msal.SerializableTokenCache()
        if os.path.exists(self.TOKEN_CACHE_FILE):
            lock_path = str(self.TOKEN_CACHE_FILE) + ".lock"
            with FileLock(lock_path):
                with open(self.TOKEN_CACHE_FILE, "r") as f:
                    cache.deserialize(f.read())
        return cache

    def _get_access_token(self):
        """Obtains an access token, using the cache if possible."""
        self.cache = self._load_cache()
        app = msal.PublicClientApplication(
            self.CLIENT_ID, authority=self.AUTHORITY, token_cache=self.cache
        )

        accounts = app.get_accounts()
        if accounts:
            result = app.acquire_token_silent(self.SCOPES, account=accounts[0])
        else:
            result = app.acquire_token_interactive(self.SCOPES)

        self._save_cache()

        if result and "access_token" in result:
            return result["access_token"]
        else:
            raise Exception(
                f"Error in authentication: {result.get('error_description') if result else 'No token found'}"
            )

    def _load_expiration_time_from_file(self):
        if not os.path.exists(self.TOKEN_CACHE_FILE):
            return 0

        lock_path = str(self.TOKEN_CACHE_FILE) + ".lock"
        try:
            with FileLock(lock_path, timeout=5):
                with open(self.TOKEN_CACHE_FILE, "r") as f:
                    data = json.load(f)
        except Timeout:
            # Si no puede obtener lock en 5 seg, leer sin lock como fallback
            with open(self.TOKEN_CACHE_FILE, "r") as f:
                data = json.load(f)

        access_token_data = list(data.get("AccessToken", {}).values())
        if access_token_data:
            return int(access_token_data[0]["expires_on"])
        return 0

    def get_token(self) -> str:
        now = int(time.time())
        if now + self.margin_seconds >= self.expires_on:
            lock_path = str(self.TOKEN_CACHE_FILE) + ".lock"
            with FileLock(lock_path):
                # recarga la expiración después de obtener lock
                self.expires_on = self._load_expiration_time_from_file()
                now = int(time.time())
                if now + self.margin_seconds >= self.expires_on:
                    self.token = self._get_access_token()
                    self.expires_on = self._load_expiration_time_from_file()
        return self.token

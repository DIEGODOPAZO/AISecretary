"""auth_microsoft.py

Handles Microsoft authentication using MSAL and environment variables.

This module loads environment variables from a .env file, manages token cache, and provides functions to obtain access tokens for Microsoft APIs.
"""

import os
from pathlib import Path
import msal
from dotenv import load_dotenv


# Load .env from the root of the proyect (2 levels up)
dotenv_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=dotenv_path)

# Dir of the .env file, used for relative paths
ENV_BASE_DIR = dotenv_path.parent

# Leer variables del entorno
CLIENT_ID = os.getenv("CLIENT_ID")
TENANT_ID = os.getenv("TENANT_ID", "common")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"

SCOPES = os.getenv("SCOPES", "User.Read,Mail.ReadWrite").split(",")

# Use the relative path from the .env file to the token cache file
raw_token_cache_path = os.getenv("TOKEN_CACHE_FILE")
TOKEN_CACHE_FILE = (ENV_BASE_DIR / raw_token_cache_path).resolve()


def load_cache():
    """Loads the token cache from a file if it exists.

    Returns:
        msal.SerializableTokenCache: The loaded token cache object.
    """
    cache = msal.SerializableTokenCache()
    if os.path.exists(TOKEN_CACHE_FILE):
        with open(TOKEN_CACHE_FILE, "r") as f:
            cache.deserialize(f.read())
    return cache


def save_cache(cache):
    """Saves the token cache to a file if its state has changed.

    Args:
        cache (msal.SerializableTokenCache): The token cache to save.
    """
    if cache.has_state_changed:
        with open(TOKEN_CACHE_FILE, "w") as f:
            f.write(cache.serialize())


def get_token_cache_path():
    """Returns the path to the token cache file.

    Returns:
        pathlib.Path: The resolved path to the token cache file.
    """
    return TOKEN_CACHE_FILE


def get_access_token(scopes=SCOPES):
    """Obtains an access token, using the cache if possible.

    Args:
        scopes (list, optional): List of scopes for which to request the token. Defaults to SCOPES.

    Returns:
        str: The access token string.

    Raises:
        Exception: If authentication fails or no token is found.
    """
    cache = load_cache()
    app = msal.PublicClientApplication(
        CLIENT_ID, authority=AUTHORITY, token_cache=cache
    )

    accounts = app.get_accounts()

    if accounts:
        result = app.acquire_token_silent(scopes, account=accounts[0])
    else:
        result = app.acquire_token_interactive(scopes)

    save_cache(cache)

    if result and "access_token" in result:
        return result["access_token"]
    else:
        raise Exception(
            f"Error in the authentication: {result.get('error_description') if result else 'No token found'}"
        )


if __name__ == "__main__":
    get_access_token()

import os
from pathlib import Path
import msal
from dotenv import load_dotenv

# Cargar variables desde .env
load_dotenv()

# Leer variables del entorno
CLIENT_ID = os.getenv("CLIENT_ID")
TENANT_ID = os.getenv("TENANT_ID", "common")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"

SCOPES = os.getenv("SCOPES", "User.Read,Mail.ReadWrite").split(",")
TOKEN_CACHE_FILE = Path(os.getenv("TOKEN_CACHE_FILE")).resolve()

def load_cache():
    """Carga la caché del token desde un archivo (si existe)."""
    cache = msal.SerializableTokenCache()
    if os.path.exists(TOKEN_CACHE_FILE):
        with open(TOKEN_CACHE_FILE, "r") as f:
            cache.deserialize(f.read())
    return cache

def save_cache(cache):
    """Guarda el estado del token en el archivo si hubo cambios."""
    if cache.has_state_changed:
        with open(TOKEN_CACHE_FILE, "w") as f:
            f.write(cache.serialize())

def get_access_token_microsoft(scopes=SCOPES):
    """Obtiene un token de acceso, usando la caché si es posible."""
    cache = load_cache()
    app = msal.PublicClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        token_cache=cache
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
        raise Exception(f"Error in the authentication: {result.get('error_description') if result else 'No token found'}")

if __name__ == "__main__":
    get_access_token_microsoft()

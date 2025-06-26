from utils.token_manager import TokenManager
from utils.auth_microsoft import get_access_token, get_token_cache_path
from mcp.server.fastmcp import FastMCP
from utils.mailboxSettings.microsoft_mailbox_settings import MicrosoftMailboxSettings
from utils.param_types import MailboxSettingsParams
# Create an MCP server
mcp = FastMCP("AISecretary-Outlook-MailboxSettings", dependencies=["mcp[cli]", "msal"])

token_manager = TokenManager(
    get_token_cache_path(), get_access_token_func=get_access_token
)

mailbox_settings = MicrosoftMailboxSettings(token_manager)

@mcp.tool()
def get_mailbox_settings() -> str:
    """
    Get the mailbox settings from Outlook.

    Returns:
        str: A JSON string containing the mailbox settings.
    """
    return mailbox_settings.get_mailbox_settings()

@mcp.tool()
def update_mailbox_settings(mailbox_settings_params: MailboxSettingsParams) -> str:
    """
    Update the mailbox settings in Outlook.

    Args:
        mailbox_settings_params (MailboxSettingsParams): The parameters for updating mailbox settings.

    Returns:
        str: A JSON string containing the updated mailbox settings.
    """
    return mailbox_settings.update_mailbox_settings(mailbox_settings_params)
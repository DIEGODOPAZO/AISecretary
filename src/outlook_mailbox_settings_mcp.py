from utils.token_manager import TokenManager
from mcp.server.fastmcp import FastMCP
from utils.mailbox_settings.microsoft_mailbox_settings import MicrosoftMailboxSettings
from utils.param_types import MailboxSettingsParams
# Create an MCP server
mcp = FastMCP("MailboxSettings-AISecretary-Outlook", dependencies=["mcp[cli]", "msal"])

token_manager = TokenManager()
mailbox_settings = MicrosoftMailboxSettings(token_manager)

@mcp.tool()
def get_mailbox_settings() -> str:
    """
    Retrieves the mailbox settings from Outlook.

    Returns:
        str: JSON string containing the mailbox settings.
    """
    return mailbox_settings.get_mailbox_settings()

@mcp.tool()
def update_mailbox_settings(mailbox_settings_params: MailboxSettingsParams) -> str:
    """
    Updates the mailbox settings in Outlook.

    Args:
        mailbox_settings_params (MailboxSettingsParams): Parameters for updating mailbox settings.

    Returns:
        str: JSON string containing the updated mailbox settings.
    """
    return mailbox_settings.update_mailbox_settings(mailbox_settings_params)
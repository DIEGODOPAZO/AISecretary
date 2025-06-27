from ..param_types import MailboxSettingsParams
from ..token_manager import TokenManager
from ..helper_functions.general_helpers import (
    microsoft_get,
    microsoft_patch,
    handle_microsoft_errors
)

class MicrosoftMailboxSettings:
    """
    Handles operations related to Microsoft mailbox settings using Microsoft Graph API.

    Attributes:
        token_manager (TokenManager): The token manager for authentication.
        url (str): The Microsoft Graph API endpoint for mailbox settings.
    """
    def __init__(self, token_manager: TokenManager):
        """
        Initializes MicrosoftMailboxSettings with a token manager.

        Args:
            token_manager (TokenManager): The token manager instance for authentication.
        """
        self.token_manager = token_manager
        self.url = "https://graph.microsoft.com/v1.0/me/mailboxSettings"

    @handle_microsoft_errors
    def get_mailbox_settings(self) -> str:
        """
        Retrieves the mailbox settings from Microsoft Graph API.

        Returns:
            str: A JSON string containing the mailbox settings.
        """
        status_code, response = microsoft_get(
            self.url, self.token_manager.get_token()
        )

        return response
    
    @handle_microsoft_errors
    def update_mailbox_settings(self, mailbox_settings_params: MailboxSettingsParams) -> str:
        """
        Updates the mailbox settings in Microsoft Graph API.

        Args:
            mailbox_settings_params (MailboxSettingsParams): The parameters for updating mailbox settings.

        Returns:
            str: A JSON string containing the response from the API.
        """
        data = {}

        if mailbox_settings_params.timeZone:
            data["timeZone"] = mailbox_settings_params.timeZone

        if mailbox_settings_params.language:
            data["language"] = {
                "locale": mailbox_settings_params.language.locale,
                "displayName": mailbox_settings_params.language.displayName,
            }

        if mailbox_settings_params.dateFormat:
            data["dateFormat"] = mailbox_settings_params.dateFormat

        if mailbox_settings_params.timeFormat:
            data["timeFormat"] = mailbox_settings_params.timeFormat

        if mailbox_settings_params.workingHours:
            data["workingHours"] = {
                "daysOfWeek": mailbox_settings_params.workingHours.daysOfWeek,
                "startTime": mailbox_settings_params.workingHours.startTime,
                "endTime": mailbox_settings_params.workingHours.endTime,
                "timeZone": {
                    "name": mailbox_settings_params.workingHours.timeZone.name
                }
            }

        if mailbox_settings_params.automaticRepliesSetting:
            ar = mailbox_settings_params.automaticRepliesSetting
            data["automaticRepliesSetting"] = {
                "status": ar.status,
                "externalAudience": ar.externalAudience,
                "internalReplyMessage": ar.internalReplyMessage,
                "externalReplyMessage": ar.externalReplyMessage,
                "scheduledStartDateTime": {
                    "dateTime": ar.scheduledStartDateTime.dateTime,
                    "timeZone": ar.scheduledStartDateTime.timeZone,
                },
                "scheduledEndDateTime": {
                    "dateTime": ar.scheduledEndDateTime.dateTime,
                    "timeZone": ar.scheduledEndDateTime.timeZone,
                },
            }

        if mailbox_settings_params.delegateMeetingMessageDeliveryOptions:
            data["delegateMeetingMessageDeliveryOptions"] = mailbox_settings_params.delegateMeetingMessageDeliveryOptions
            
        status_code, response = microsoft_patch(
            self.url, 
            self.token_manager.get_token(), 
            data=data
        )

        return response
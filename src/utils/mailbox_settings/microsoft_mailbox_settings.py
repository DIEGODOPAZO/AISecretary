import json
from ..param_types import MailboxSettingsParams
from ..constants import MAILBOX_SETTINGS_URL
from ..microsoft_base_request import MicrosoftBaseRequest


class MicrosoftMailboxSettings(MicrosoftBaseRequest):
    """
    Handles operations related to Microsoft mailbox settings using Microsoft Graph API.
    Inherits from MicrosoftBaseRequest to manage authentication and token retrieval.
    """

    @MicrosoftBaseRequest.handle_microsoft_errors
    def get_mailbox_settings(self) -> str:
        """
        Retrieves the mailbox settings from Microsoft Graph API.

        Returns:
            str: A JSON string containing the mailbox settings.
        """
        status_code, response = self.microsoft_get(
            MAILBOX_SETTINGS_URL, self.token_manager.get_token()
        )

        return json.dumps(response, indent=2)

    @MicrosoftBaseRequest.handle_microsoft_errors
    def update_mailbox_settings(
        self, mailbox_settings_params: MailboxSettingsParams
    ) -> str:
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


        if mailbox_settings_params.workingHours:
            data["workingHours"] = {
                "daysOfWeek": mailbox_settings_params.workingHours.daysOfWeek,
                "startTime": mailbox_settings_params.workingHours.startTime,
                "endTime": mailbox_settings_params.workingHours.endTime,
                "timeZone": {
                    "name": mailbox_settings_params.workingHours.timeZone.name
                },
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

        status_code, response = self.microsoft_patch(
            MAILBOX_SETTINGS_URL, self.token_manager.get_token(), data=data
        )

        return json.dumps(response, indent=2)

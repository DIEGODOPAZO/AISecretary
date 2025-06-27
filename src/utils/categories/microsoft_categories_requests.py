import json

from ..helper_functions.helpers_calendar import simplify_event
from ..param_types import *
from ..helper_functions.helpers_email import *
from ..token_manager import TokenManager
from ..helper_functions.general_helpers import (
    handle_microsoft_errors,
    microsoft_get,
    microsoft_post,
    microsoft_patch,
    microsoft_delete,
)


class MicrosoftCategoriesRequests:
    """
    Handles Microsoft Outlook category operations via Microsoft Graph API.

    This class provides methods to get, create, edit, and delete categories, as well as add or remove categories from emails and calendar events.

    Attributes:
        url (str): Base URL for the master categories endpoint.
        token_manager (TokenManager): Manages access tokens for Microsoft API requests.
    """
    def __init__(self, token_manager: TokenManager):
        """
        Initializes MicrosoftCategoriesRequests with a token manager.

        Args:
            token_manager (TokenManager): An instance to manage Microsoft API tokens.
        """
        self.url = "https://graph.microsoft.com/v1.0/me/outlook/masterCategories"
        self.token_manager = token_manager

    @handle_microsoft_errors
    def get_categories_microsoft_api(self) -> str:
        """
        Retrieves the categories from the user's mailbox.

        Returns:
            str: JSON-formatted list of categories with their IDs and display names.
        """
        (status_code, response) = microsoft_get(
            self.url, self.token_manager.get_token()
        )
        categories = response.get("value", [])
        simplified_categories = [
            {"id": cat.get("id"), "displayName": cat.get("displayName")}
            for cat in categories
        ]
        return json.dumps(simplified_categories, indent=2)

    @handle_microsoft_errors
    def create_edit_category_microsoft_api(
        self, category_params: CategoryParams
    ) -> str:
        """
        Creates a new category or edits an existing one.

        Args:
            category_params (CategoryParams): Parameters for the category (name, color, id).

        Returns:
            str: JSON-formatted response from the Microsoft API.
        """
        url = self.url
        params = {
            "displayName": category_params.category_name,
            "color": category_params.preset_color,
        }
        if not category_params.category_id:
            # Create a new category
            (status_code, response) = microsoft_post(
                url, self.token_manager.get_token(), params
            )
        else:
            # Edit an existing category
            url = f"{url}/{category_params.category_id}"
            (status_code, response) = microsoft_patch(
                url, self.token_manager.get_token(), params
            )
        return json.dumps(response, indent=2)

    @handle_microsoft_errors
    def delete_category_microsoft_api(self, category_id: str) -> str:
        """
        Deletes a category by its ID.

        Args:
            category_id (str): The ID of the category to delete.

        Returns:
            str: JSON-formatted message indicating success or error.
        """
        url = f"{self.url}/{category_id}"
        (status_code, response) = microsoft_delete(url, self.token_manager.get_token())
        if status_code != 204:
            return json.dumps({"error": response}, indent=2)
        return json.dumps(
            {"message": f"Category with ID {category_id} deleted successfully."},
            indent=2,
        )

    @handle_microsoft_errors
    def add_delete_category_to_email(
        self, handle_category_to_resource_params: HandleCategoryToResourceParams
    ) -> str:
        """
        Adds or removes categories from an email message.

        Args:
            handle_category_to_resource_params (HandleCategoryToResourceParams):
                Parameters including resource_id, category_names, and remove flag.

        Returns:
            str: JSON-formatted response with the updated message.
        """
        url = f"https://graph.microsoft.com/v1.0/me/messages/{handle_category_to_resource_params.resource_id}"
        # get current categories
        status_code, message_data = microsoft_get(url, self.token_manager.get_token())
        existing_categories = message_data.get("categories", [])

        existing_categories = set(message_data.get("categories", []))
        new_categories = set(handle_category_to_resource_params.category_names)

        if handle_category_to_resource_params.remove:
            updated_categories = list(existing_categories.difference(new_categories))
        else:
            updated_categories = list(existing_categories.union(new_categories))

        data = {"categories": updated_categories}
        status_code, response = microsoft_patch(
            url, self.token_manager.get_token(), data
        )
        response = microsoft_simplify_message(response)
        return json.dumps(response, indent=2)

    @handle_microsoft_errors
    def add_delete_category_to_event(
        self, handle_category_to_resource_params: HandleCategoryToResourceParams
    ) -> str:
        """
        Adds or removes categories from a Microsoft calendar event.

        Args:
            handle_category_to_resource_params (HandleCategoryToResourceParams):
                Parameters including resource_id, category_names, and remove flag.

        Returns:
            str: JSON-formatted response with the updated event.
        """
        url = f"https://graph.microsoft.com/v1.0/me/events/{handle_category_to_resource_params.resource_id}"
        status_code, event_data = microsoft_get(url, self.token_manager.get_token())
        existing_categories = set(event_data.get("categories", []))
        new_categories = set(handle_category_to_resource_params.category_names)
        updated_categories = (
            list(existing_categories.difference(new_categories))
            if handle_category_to_resource_params.remove
            else list(existing_categories.union(new_categories))
        )
        data = {"categories": updated_categories}
        status_code, response = microsoft_patch(
            url, self.token_manager.get_token(), data
        )
        response = simplify_event(response)
        return json.dumps(response, indent=2)

    def get_preset_color_equivalence_microsoft(self) -> str:
        """
        Returns the preset color scheme equivalence for Microsoft categories.

        Returns:
            str: JSON-formatted color scheme equivalence.
        """
        return get_preset_color_scheme()

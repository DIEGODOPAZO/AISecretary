import json

from ..param_types import *
from ..helpers import *
from ..token_manager import TokenManager


class MicrosoftCategoriesRequests:
    def __init__(self, token_manager: TokenManager):
        self.url = "https://graph.microsoft.com/v1.0/me/outlook/masterCategories"
        self.token_manager = token_manager

    @handle_microsoft_errors
    def get_categories_microsoft_api(self) -> str:
        """
        Retrieves the categories from the user's mailbox.

        :return: JSON response containing the categories.
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
        url = f"{self.url}/{category_id}"
        (status_code, response) = microsoft_delete(url, self.token_manager.get_token())
        if status_code != 204:
            return json.dumps({"error": response}, indent=2)
        return json.dumps(
            {"message": f"Category with ID {category_id} deleted successfully."},
            indent=2,
        )

    @handle_microsoft_errors
    def add_delete_category_to_resource_microsoft_api(
        self, handle_category_to_resource_params: HandleCategoryToResourceParams
    ) -> str:

        url = f"https://graph.microsoft.com/v1.0/me/messages/{handle_category_to_resource_params.resource_id}"
        # get current categories
        status_code, message_data = microsoft_get(url, self.token_manager.get_token())
        existing_categories = message_data.get("categories", [])

        existing_categories = set(message_data.get("categories", []))
        new_categories = set(handle_category_to_resource_params.category_names)

        # Agregar o quitar categorías
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

    def get_preset_color_equivalence_microsoft(self) -> str:
        return get_preset_color_scheme()

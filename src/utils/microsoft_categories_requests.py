import json

from utils.param_types import *
from utils.auth_microsoft import get_access_token_microsoft
from utils.helpers import *

@handle_microsoft_errors
def get_categories_microsoft_api() -> str:
    """
    Retrieves the categories from the user's mailbox.

    :return: JSON response containing the categories.
    """
    token = get_access_token_microsoft()
    url = "https://graph.microsoft.com/v1.0/me/outlook/masterCategories"
    (status_code, response) = microsoft_get(url, token)

    categories = response.get("value", [])
    simplified_categories = [
        {"id": cat.get("id"), "displayName": cat.get("displayName")}
        for cat in categories
    ]

    return json.dumps(simplified_categories, indent=2)


@handle_microsoft_errors
def create_edit_category_microsoft_api(category_params: CategoryParams) -> str:
    token = get_access_token_microsoft()
    url = "https://graph.microsoft.com/v1.0/me/outlook/masterCategories"
    
    params = {
        "displayName": category_params.category_name,
        "color": category_params.preset_color,
    }   
    
    if not category_params.category_id:
        # Create a new category
        (status_code, response) = microsoft_post(url, token, params)
    else:
        # Edit an existing category
        url = f"{url}/{category_params.category_id}"
        (status_code, response) = microsoft_patch(url, token, params)
    
    return json.dumps(response, indent=2)

@handle_microsoft_errors
def delete_category_microsoft_api(category_id: str) -> str:
    token = get_access_token_microsoft()
    url = f"https://graph.microsoft.com/v1.0/me/outlook/masterCategories/{category_id}"
    (status_code, response) = microsoft_delete(url, token)
    if status_code != 204:
        return json.dumps({"error": response}, indent=2)
    return json.dumps(
        {"message": f"Category with ID {category_id} deleted successfully."}, indent=2)


def get_preset_color_equivalence_microsoft() -> str:

    return get_preset_color_scheme()
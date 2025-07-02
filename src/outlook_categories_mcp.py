from utils.categories.microsoft_categories_requests import MicrosoftCategoriesRequests
from utils.param_types import *
from utils.token_manager import TokenManager
from utils.auth_microsoft import get_access_token, load_expiration_time_from_file


# server.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Categories-AISecretary-Outlook", dependencies=["mcp[cli]", "msal"])

token_manager = TokenManager(
    get_access_token_func=get_access_token, get_expiration_time=load_expiration_time_from_file
)
categories_requests = MicrosoftCategoriesRequests(token_manager)


@mcp.tool()
def get_categores() -> str:
    """
    Gets the categories of Outlook.

    Returns:
        str: A JSON string containing the categories.
    """
    return categories_requests.get_categories_microsoft_api()


@mcp.tool()
def create_edit_category(category_params: CategoryParams) -> str:
    """
    Creates or edits a category in Outlook.

    Args:
        category_params (CategoryParams): The parameters for creating or editing a category.

    Returns:
        str: The id of the created or edited category with more information, or an error message.
    """
    return categories_requests.create_edit_category_microsoft_api(category_params)


@mcp.tool()
def delete_category(category_id: str) -> str:
    """
    Deletes a category from Outlook.

    Args:
        category_id (str): The id of the category to delete.

    Returns:
        str: A confirmation message or an error message.
    """
    return categories_requests.delete_category_microsoft_api(category_id)


@mcp.tool()
def add_delete_category_to_email(
    handle_category_to_resource_params: HandleCategoryToResourceParams,
) -> str:
    """
    Adds or deletes a category to/from an email in the Outlook mailbox.

    Args:
        handle_category_to_resource_params (HandleCategoryToResourceParams): The parameters for adding or deleting a category to/from an email.

    Returns:
        str: A confirmation message or an error message.
    """
    return categories_requests.add_delete_category_to_email(
        handle_category_to_resource_params
    )

@mcp.tool()
def add_delete_category_to_event(
    handle_category_to_resource_params: HandleCategoryToResourceParams,
) -> str:
    """
    Adds or deletes a category to/from an event in the Outlook mailbox.

    Args:
        handle_category_to_resource_params (HandleCategoryToResourceParams): The parameters for adding or deleting a category to/from an event.

    Returns:
        str: A confirmation message or an error message.
    """
    return categories_requests.add_delete_category_to_event(handle_category_to_resource_params)

@mcp.tool()
def get_preset_colors() -> str:
    """
    Gets the equivalence between colors and preset colors for the categories in Outlook.
    This is useful for understanding the available color options for categories (it gives the presetX to color equivalence).

    Returns:
        str: A JSON string containing the preset colors.
    """
    return categories_requests.get_preset_color_equivalence_microsoft()

@mcp.resource("outlook://categories")
def get_categories() -> str:
    """
    Gets the categories of the Outlook mailbox.

    Returns:
        str: A JSON string containing the categories.
    """
    return categories_requests.get_categories_microsoft_api()


@mcp.resource("outlook://preset/colors")
def get_preset_colors() -> str:
    """
    Gets the equivalence between colors and preset colors for the categories in the Outlook mailbox.

    Returns:
        str: A JSON string containing the preset colors.
    """
    return categories_requests.get_preset_color_equivalence_microsoft()


@mcp.prompt()
def create_edit_category_prompt(
    category_name: str,
    category_color: str = "red",
) -> str:
    """
    Creates or edits a category in the Outlook mailbox.

    Args:
        category_name (str): The name of the category.
        category_color (str, optional): The color of the category. Defaults to "red".

    Returns:
        str: The id of the created or edited category with more information, or an error message.
    """
    return f"Use the tool get_preset_colors to get the equivalence of the preset colors to colors. Then use the tool get_categories to get the categoires, if the category provided is very similar to one category, edit it, otherwise create it. The name of the category is {category_name} and the color is {category_color}."

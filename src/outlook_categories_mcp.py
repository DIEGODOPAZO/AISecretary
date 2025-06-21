import os
from pathlib import Path
from utils.categories.microsoft_categories_requests import MicrosoftCategoriesRequests
from utils.param_types import *
from utils.token_manager import TokenManager
from utils.auth_microsoft import get_access_token, get_token_cache_path
from dotenv import load_dotenv

# server.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("AISecretary-Outlook-Categories", dependencies=["mcp[cli]", "msal"])

token_manager = TokenManager(
    get_token_cache_path(), get_access_token_func=get_access_token
)

categories_requests = MicrosoftCategoriesRequests(token_manager)


@mcp.tool()
def get_categores() -> str:
    """
    Gets the categories of the Outlook mailbox.
    returns:
        str: A JSON string containing the categories.
    """
    return categories_requests.get_categories_microsoft_api()


@mcp.tool()
def create_edit_category(category_params: CategoryParams) -> str:
    """
    Creates or edits a category in the Outlook mailbox.
    params:
        category_params (CategoryParams): The parameters for creating or editing a category.
    returns:
        str: The id of the created or edited category with more information, or an error message.
    """
    return categories_requests.create_edit_category_microsoft_api(category_params)


@mcp.tool()
def delete_category(category_id: str) -> str:
    """
    Deletes a category from the Outlook mailbox.
    params:
        category_id (str): The id of the category to delete.
    returns:
        str: A confirmation message or an error message.
    """
    return categories_requests.delete_category_microsoft_api(category_id)


@mcp.tool()
def add_delete_category_to_email(
    handle_category_to_resource_params: HandleCategoryToResourceParams,
) -> str:
    """
    Adds or deletes a category to/from an email in the Outlook mailbox.
    params:
        handle_category_to_resource_params (HandleCategoryToResourceParams): The parameters for adding or deleting a category to/from an email.
    returns:
        str: A confirmation message or an error message.
    """
    return categories_requests.add_delete_category_to_resource_microsoft_api(
        handle_category_to_resource_params
    )


@mcp.resource("outlook://categories")
def get_categories() -> str:
    """
    Gets the categories of the Outlook mailbox.
    returns:
        str: A JSON string containing the categories.
    """
    return categories_requests.get_categories_microsoft_api()


@mcp.resource("outlook://preset/colors")
def get_preset_colors() -> str:
    """
    Gets the preset colors for the categories in the Outlook mailbox.
    returns:
        str: A JSON string containing the preset colors.
    """
    return categories_requests.get_preset_color_equivalence_microsoft()

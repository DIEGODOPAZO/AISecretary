from utils.microsoft_categories_requests import *
from utils.param_types import *

# server.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("AISecretary-Outlook-Categories", dependencies=["mcp[cli]", "msal"])


@mcp.tool()
def get_categores() -> str:
    """
    Gets the categories of the Outlook mailbox.
    returns:
        str: A JSON string containing the categories.
    """
    return get_categories_microsoft_api()


@mcp.tool()
def create_edit_category(category_params: CategoryParams) -> str:
    """
    Creates or edits a category in the Outlook mailbox.
    params:
        category_params (CategoryParams): The parameters for creating or editing a category.
    returns:
        str: The id of the created or edited category with more information, or an error message.
    """
    return create_edit_category_microsoft_api(category_params)

@mcp.tool()
def delete_category(category_id: str) -> str:
    """
    Deletes a category from the Outlook mailbox.
    params:
        category_id (str): The id of the category to delete.
    returns:        
        str: A confirmation message or an error message.
    """
    return delete_category_microsoft_api(category_id)



@mcp.resource("outlook://preset/colors")
def get_preset_colors() -> str:
    """
    Gets the preset colors for the categories in the Outlook mailbox.
    returns:
        str: A JSON string containing the preset colors.
    """
    return get_preset_color_equivalence_microsoft()
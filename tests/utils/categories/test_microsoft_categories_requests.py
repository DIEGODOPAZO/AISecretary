# tests/test_categories.py

import json
import pytest
from unittest.mock import patch, MagicMock

from src.utils.categories.microsoft_categories_requests import MicrosoftCategoriesRequests
from src.utils.token_manager import TokenManager
from src.utils.param_types import CategoryParams, HandleCategoryToResourceParams

@pytest.fixture
def token_manager():
    return MagicMock(spec=TokenManager, get_token=MagicMock(return_value="fake-token"))

@pytest.fixture
def service(token_manager):
    return MicrosoftCategoriesRequests(token_manager)


@patch.object(MicrosoftCategoriesRequests, "microsoft_get")
def test_get_categories(mock_get, service):
    mock_get.return_value = (
        200,
        {
            "value": [
                {"id": "1", "displayName": "Category 1"},
                {"id": "2", "displayName": "Category 2"},
            ]
        },
    )

    result = service.get_categories_microsoft_api()
    data = json.loads(result)
    assert isinstance(data, list)
    assert data[0]["displayName"] == "Category 1"

@patch.object(MicrosoftCategoriesRequests, "microsoft_post")
def test_create_category(mock_post, service):
    mock_post.return_value = (201, {"id": "123", "displayName": "New Category"})

    params = CategoryParams(category_name="New Category", preset_color="preset1", category_id=None)
    result = service.create_edit_category_microsoft_api(params)

    data = json.loads(result)
    assert data["id"] == "123"

@patch.object(MicrosoftCategoriesRequests, "microsoft_patch")
def test_edit_category(mock_patch, service):
    mock_patch.return_value = (200, {"id": "123", "displayName": "Updated Category"})

    params = CategoryParams(category_name="Updated Category", preset_color="preset2", category_id="123")
    result = service.create_edit_category_microsoft_api(params)

    data = json.loads(result)
    assert data["displayName"] == "Updated Category"

@patch.object(MicrosoftCategoriesRequests, "microsoft_delete")
def test_delete_category(mock_delete, service):
    mock_delete.return_value = (204, {})

    result = service.delete_category_microsoft_api("123")
    data = json.loads(result)
    assert "deleted successfully" in data["message"]

@patch.object(MicrosoftCategoriesRequests, "microsoft_get")
@patch.object(MicrosoftCategoriesRequests, "microsoft_patch")
def test_add_category_to_resource(mock_patch, mock_get, service):
    mock_get.return_value = (200, {"categories": ["Old"]})
    mock_patch.return_value = (200, {"categories": ["Old", "New"]})

    params = HandleCategoryToResourceParams(
        resource_id="abc",
        category_names=["New"],
        remove=False,
    )

    result = service.add_delete_category_to_email(params)
    data = json.loads(result)
    assert "New" in data["categories"]

@patch("src.utils.categories.microsoft_categories_requests.get_preset_color_scheme")
def test_get_color_scheme(mock_get_color, service):
    mock_get_color.return_value = {"Red": "#FF0000"}
    result = service.get_preset_color_equivalence_microsoft()
    assert "Red" in result

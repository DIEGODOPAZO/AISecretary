import json
import pytest
from unittest.mock import patch, MagicMock
from src.utils.email.microsoft_rules_requests import MicrosoftRulesRequests
from src.utils.param_types import MailRule


@pytest.fixture
def token_manager_mock():
    tm = MagicMock()
    tm.get_token.return_value = "fake-token"
    return tm


@pytest.fixture
def client(token_manager_mock):
    return MicrosoftRulesRequests(token_manager_mock)

@patch.object(MicrosoftRulesRequests, "microsoft_get")
def test_get_message_rules_microsoft_api(mock_get, client):
    fake_response = {"value": [{"id": "rule1", "displayName": "Rule 1"}]}
    mock_get.return_value = (200, fake_response)

    result = client.get_message_rules_microsoft_api()
    data = json.loads(result)

    mock_get.assert_called_once()
    assert "value" in data
    assert data["value"][0]["id"] == "rule1"


@patch.object(MicrosoftRulesRequests, "microsoft_post")
def test_create_message_rule_microsoft_api_post(mock_post, client):
    mail_rule = MailRule("Test Rule", 1, conditions={}, actions={})
    fake_response = {"id": "new_rule", "displayName": "Test Rule"}
    mock_post.return_value = (201, fake_response)

    result = client.create_message_rule_microsoft_api(mail_rule)
    data = json.loads(result)

    mock_post.assert_called_once()
    assert data["id"] == "new_rule"


@patch.object(MicrosoftRulesRequests, "microsoft_patch")
def test_create_message_rule_microsoft_api_patch(mock_patch, client):
    mail_rule = MailRule("Test Rule", 1, conditions={}, actions={})
    fake_response = {"id": "rule123", "displayName": "Test Rule"}
    mock_patch.return_value = (200, fake_response)

    result = client.create_message_rule_microsoft_api(mail_rule, rule_id="rule123")
    data = json.loads(result)

    mock_patch.assert_called_once()
    assert data["id"] == "rule123"


@patch.object(MicrosoftRulesRequests, "microsoft_delete")
def test_delete_message_rule_microsoft_api_success(mock_delete, client):
    mock_delete.return_value = (204, None)

    result = client.delete_message_rule_microsoft_api("rule123")
    data = json.loads(result)

    mock_delete.assert_called_once()
    assert "message" in data
    assert "rule123" in data["message"]

@patch.object(MicrosoftRulesRequests, "microsoft_delete")
def test_delete_message_rule_microsoft_api_failure(mock_delete, client):
    mock_delete.return_value = (400, {"error": "Bad Request"})

    result = client.delete_message_rule_microsoft_api("rule123")
    data = json.loads(result)

    mock_delete.assert_called_once()
    assert "error" in data


@patch.object(MicrosoftRulesRequests, "microsoft_get")
def test_get_next_link_microsoft_api(mock_get, client):
    fake_response = {"value": [{"id": "rule2"}]}
    mock_get.return_value = (200, fake_response)

    next_link = (
        "https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messageRules?$skip=10"
    )
    result = client.get_next_link_microsoft_api(next_link)
    data = json.loads(result)

    mock_get.assert_called_once_with(next_link, "fake-token")
    assert "value" in data
    assert data["value"][0]["id"] == "rule2"

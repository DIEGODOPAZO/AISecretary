import json
import pytest
from unittest.mock import patch, MagicMock

from src.utils.contacts.microsoft_contacts_requests import MicrosoftContactsRequests
from src.utils.param_types import Contact, EmailAddressContact


@pytest.fixture
def mock_token_manager():
    mock = MagicMock()
    mock.get_token.return_value = "fake_token"
    return mock


@patch.object(MicrosoftContactsRequests, "microsoft_get")
def test_get_contacts(mock_get, mock_token_manager):
    mock_get.return_value = (
        200,
        {
            "value": [
                {"id": "1", "givenName": "Juan", "surname": "Pérez"},
                {"id": "2", "givenName": "Ana", "surname": "García"},
            ]
        }
    )

    client = MicrosoftContactsRequests(mock_token_manager)
    response = json.loads(client.get_contacts())

    assert isinstance(response, list)
    assert response[0]["givenName"] == "Juan"
    assert response[1]["surname"] == "García"


@patch.object(MicrosoftContactsRequests, "microsoft_get")
def test_get_contacts_with_name_filter(mock_get, mock_token_manager):
    mock_get.return_value = (
        200,
        {
            "value": [
                {"id": "3", "givenName": "Pedro", "surname": "López"},
            ]
        }
    )

    client = MicrosoftContactsRequests(mock_token_manager)
    response = json.loads(client.get_contacts(name="Pedro"))

    assert isinstance(response, list)
    assert len(response) == 1
    assert response[0]["givenName"] == "Pedro"


@patch.object(MicrosoftContactsRequests, "microsoft_get")
def test_get_contact_info(mock_get, mock_token_manager):
    mock_get.return_value = (
        200,
        {"id": "abc123", "givenName": "Laura", "surname": "Martínez"}
    )

    client = MicrosoftContactsRequests(mock_token_manager)
    response = json.loads(client.get_contact_info("abc123"))

    assert response["id"] == "abc123"
    assert response["givenName"] == "Laura"

@patch.object(MicrosoftContactsRequests, "microsoft_post")
def test_create_contact(mock_post, mock_token_manager):
    mock_post.return_value = (
        201,
        {"id": "new456", "givenName": "Carlos", "surname": "Ruiz"}
    )

    contact = Contact(
        givenName="Carlos",
        surname="Ruiz",
        emailAddresses=[EmailAddressContact(address="carlos@correo.com")],
        businessPhones=["12345678"],
        mobilePhone="87654321"
    )

    client = MicrosoftContactsRequests(mock_token_manager)
    response = json.loads(client.create_edit_contact(contact))

    assert response["id"] == "new456"
    assert response["surname"] == "Ruiz"


@patch.object(MicrosoftContactsRequests, "microsoft_patch")
def test_edit_contact(mock_patch, mock_token_manager):
    mock_patch.return_value = (
        200,
        {"id": "c123", "givenName": "María", "surname": "Rodríguez"}
    )

    contact = Contact(
        givenName="María",
        surname="Rodríguez",
        emailAddresses=[EmailAddressContact(address="maria@correo.com")],
        businessPhones=[],
        mobilePhone=""
    )

    client = MicrosoftContactsRequests(mock_token_manager)
    response = json.loads(client.create_edit_contact(contact, contact_id="c123"))

    assert response["givenName"] == "María"
    assert response["id"] == "c123"


@patch.object(MicrosoftContactsRequests, "microsoft_delete")
def test_delete_contact_success(mock_delete, mock_token_manager):
    mock_delete.return_value = (204, None)

    client = MicrosoftContactsRequests(mock_token_manager)
    response = json.loads(client.delete_contact("id567"))

    assert response["message"] == "Contact deleted successfully."


@patch.object(MicrosoftContactsRequests, "microsoft_delete")
def test_delete_contact_failure(mock_delete, mock_token_manager):
    mock_delete.return_value = (404, None)

    client = MicrosoftContactsRequests(mock_token_manager)
    response = json.loads(client.delete_contact("nonexistent_id"))

    assert response["error"] == "Failed to delete contact."

import json
import pytest
from unittest.mock import patch, MagicMock

from src.utils.email.microsoft_messages_requests import MicrosoftMessagesRequests
from src.utils.param_types import (
    EmailQuery,
    DraftEmailData,
    EmailRecipients,
    EmailOperationParams,
    EmailReplyParams,
    EmailForwardParams,
)


@pytest.fixture
def mock_token_manager():
    mock = MagicMock()
    mock.get_token.return_value = "fake_token"
    return mock


@pytest.fixture
def client(mock_token_manager):
    return MicrosoftMessagesRequests(mock_token_manager)



@patch.object(MicrosoftMessagesRequests, "microsoft_get")
@patch("src.utils.email.microsoft_messages_requests.microsoft_simplify_message")
def test_get_messages_from_folder(mock_simplify, mock_get, client):
    # Simula dos mensajes con el mismo ID para probar que se eliminan duplicados
    mock_get.return_value = (
        200,
        {"value": [{"id": "msg1"}, {"id": "msg1"}], "@odata.nextLink": "next"},
    )
    mock_simplify.return_value = {"id": "msg1"}  # Ambos mensajes se simplifican igual

    params = {}
    email_params = EmailQuery(folder_id=None)
    response = json.loads(
        client.get_messages_from_folder_microsoft_api(params, email_params)
    )

    assert "messages" in response
    assert (
        len(response["messages"]) == 1
    )  # Solo debe quedar un mensaje después de eliminar duplicados
    assert response["messages"][0]["id"] == "msg1"


@patch.object(MicrosoftMessagesRequests, "microsoft_patch")
@patch.object(MicrosoftMessagesRequests, "microsoft_get")
def test_mark_as_read(mock_get, mock_patch, client):
    mock_get.return_value = (200, {"id": "msg1", "subject": "Hi"})
    with patch(
        "src.utils.email.microsoft_messages_requests.microsoft_simplify_message",
        return_value={"id": "msg1"},
    ):
        response = json.loads(
            client.mark_as_read_unread_microsoft_api("msg1", is_read=True)
        )
    assert response["id"] == "msg1"


@patch.object(MicrosoftMessagesRequests, "microsoft_get")
def test_get_conversation_messages(mock_get, client):
    mock_get.return_value = (200, {"value": [{"id": "conv1"}]})
    with patch(
        "src.utils.email.microsoft_messages_requests.microsoft_simplify_message",
        return_value={"id": "conv1"},
    ):
        response = json.loads(client.get_conversation_messages_microsoft_api({}))
    assert response["messages"][0]["id"] == "conv1"


@patch.object(MicrosoftMessagesRequests, "microsoft_get")
@patch.object(MicrosoftMessagesRequests, "microsoft_patch")
def test_create_edit_draft(mock_patch, mock_get, client):
    mock_patch.return_value = (200, {"id": "draft123"})
    data = DraftEmailData(
        subject="Test",
        body="Body",
        importance="normal",
        draft_id="draft123",
        email_recipients=EmailRecipients([], []),
    )
    response = json.loads(client.create_edit_draft_microsoft_api(data))
    assert response["id"] == "draft123"


@patch.object(MicrosoftMessagesRequests, "microsoft_post")
def test_send_draft_email(mock_post, client):
    mock_post.return_value = (202, {})
    response = json.loads(client.send_draft_email_microsoft_api("draft123"))
    assert response["message"] == "Email sent successfully."

@patch.object(MicrosoftMessagesRequests, "read_file_and_encode_base64")
@patch.object(MicrosoftMessagesRequests, "microsoft_post")
def test_add_attachment_to_draft(mock_post, mock_read, client):
    mock_read.return_value = ("file.txt", "base64encoded")
    mock_post.return_value = (
        200,
        {"id": "att123", "name": "file.txt", "contentType": "text/plain", "size": 123},
    )
    response = json.loads(
        client.add_attachment_to_draft_microsoft_api(
            "draft123", "path/to/file.txt", "text/plain"
        )
    )
    assert response["attachment_id"] == "att123"


@patch.object(MicrosoftMessagesRequests, "microsoft_post")
def test_forward_email(mock_post, client):
    mock_post.return_value = (200, {"status": "ok"})
    params = EmailForwardParams(
        email_id="email123",
        comment="Forward this",
        email_recipients=EmailRecipients(
            to_recipients=["a@example.com"], cc_recipients=[]
        ),
    )
    response = json.loads(client.forward_email_microsoft_api(params))
    assert response["status"] == "ok"


@patch.object(MicrosoftMessagesRequests, "microsoft_post")
def test_reply_to_email(mock_post, client):
    mock_post.return_value = (200, {"id": "reply1"})
    params = EmailReplyParams(
        email_id="email123", body="Reply content", reply_all=False
    )
    response = json.loads(client.reply_to_email_microsoft_api(params))
    assert response["id"] == "reply1"


@patch.object(MicrosoftMessagesRequests, "microsoft_post")
def test_move_email(mock_post, client):
    mock_post.return_value = (200, {"id": "movedEmail"})
    params = EmailOperationParams(
        email_id="email1", destination_folder_id="dest123", move=True
    )
    response = json.loads(client.move_or_copy_email_microsoft_api(params))
    assert response["id"] == "movedEmail"


@patch.object(MicrosoftMessagesRequests, "microsoft_delete")
def test_delete_message(mock_delete, client):
    mock_delete.return_value = (204, {})
    response = json.loads(client.delete_message_microsoft_api("msg123"))
    assert "deleted successfully" in response["message"]

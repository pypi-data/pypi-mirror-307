import pytest
from unittest.mock import MagicMock, patch
from happtiq_commons_gen_ai.chatgpt_api_service import ChatgptApiService

@pytest.fixture
def chatgpt_api_service():
    return ChatgptApiService(api_key="test-api-key", model="some-model")

def mock_openai_client():
    mock = MagicMock()
    mock.chat.completions.create.return_value = {
        "choices": [
            {
                "message": {
                    "content": "Generated text"
                }
            }
        ]
    }
    return mock

def test_send_prompt_to_api(chatgpt_api_service, monkeypatch):
    monkeypatch.setattr(chatgpt_api_service, "client", mock_openai_client())

    system_message = "You are a helpful assistant."
    text = "Test prompt"
    
    response = chatgpt_api_service.send_prompt_to_api(system_message, text)
    assert response == "Generated text"
    chatgpt_api_service.client.chat.completions.create.assert_called_once_with(
        model="some-model",
        messages=[{"role": "system", "content": system_message}, {"role": "user", "content": text}]
    )

def test_send_prompt_to_api_error(chatgpt_api_service, monkeypatch):
    mock_client = MagicMock()
    mock_client.chat.completions.create.side_effect = Exception("Error generating from chatgpt")
    monkeypatch.setattr(chatgpt_api_service, "client", mock_client)

    system_message = "You are a helpful assistant."
    text = "Test prompt"
    
    with pytest.raises(Exception):
        chatgpt_api_service.send_prompt_to_api(system_message, text)

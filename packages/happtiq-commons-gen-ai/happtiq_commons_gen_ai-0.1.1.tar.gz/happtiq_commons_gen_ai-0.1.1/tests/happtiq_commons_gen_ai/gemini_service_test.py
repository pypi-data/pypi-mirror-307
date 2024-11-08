import pytest
from unittest.mock import MagicMock, patch
from happtiq_commons_gen_ai.gemini_service import GeminiService

@pytest.fixture
def vertex_ai_service(monkeypatch):
    monkeypatch.setattr("google.auth.default", MagicMock(return_value=(MagicMock(),MagicMock())))
    monkeypatch.setattr("vertexai.init", MagicMock())
    return GeminiService(project_id="some-project", location="some-location", model_id="some-model")

def mockGenerativeModel():
    mock = MagicMock()    
    mock.generate_content.return_value = MagicMock(text="Generated text")
    return mock

def test_send_single_data_prompt_to_api(vertex_ai_service, monkeypatch):
    monkeypatch.setattr(vertex_ai_service, "model", mockGenerativeModel())

    prompt = "Test prompt"
    data_file_gcs_uri = "gs://test-bucket/test-file.txt"
    mime_type = "text/plain"
    
    response = vertex_ai_service.send_single_data_prompt_to_api(prompt, data_file_gcs_uri, mime_type)
    assert response == "Generated text"
    vertex_ai_service.model.generate_content.assert_called_once()

def test_send_data_prompt_to_api(vertex_ai_service, monkeypatch):
    monkeypatch.setattr(vertex_ai_service, "model", mockGenerativeModel())
    prompts = ["Test prompt 1", "Test prompt 2"]
    data_file_gcs_uris = ["gs://test-bucket/test-file1.txt", "gs://test-bucket/test-file2.txt"]
    mime_types = ["text/plain", "text/plain"]
    response = vertex_ai_service.send_data_prompt_to_api(prompts, data_file_gcs_uris, mime_types)
    assert response == "Generated text"
    vertex_ai_service.model.generate_content.assert_called_once()

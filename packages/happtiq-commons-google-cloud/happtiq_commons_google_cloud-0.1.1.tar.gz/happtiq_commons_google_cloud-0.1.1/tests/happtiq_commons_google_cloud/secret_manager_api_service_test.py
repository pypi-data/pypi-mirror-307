import pytest
from happtiq_commons_google_cloud.secret_manager_api_service import SecretManagerApiService
from unittest.mock import MagicMock, patch

@pytest.fixture
def secret_manager_api_service(monkeypatch):
    monkeypatch.setattr("google.auth.default", MagicMock(return_value=(MagicMock(),"some-proje")))
    return SecretManagerApiService()

def test_read_secret(secret_manager_api_service, monkeypatch):
    secret_value = "test-secret"
    
    mock_client = MagicMock()
    mock_client.access_secret_version.return_value = MagicMock(payload=MagicMock(data=bytes(secret_value, "utf-8")))
    monkeypatch.setattr(secret_manager_api_service, "client", mock_client)
    
    secret_name = "some-secret"
    secret_key = secret_manager_api_service.read_secret(secret_name)
    assert secret_key == secret_value

def test_build_secret_name():
    project_id = "test-project"
    secret_id = "test-secret"
    secret_name = SecretManagerApiService.build_secret_name(project_id, secret_id)
    assert secret_name == "projects/test-project/secrets/test-secret/versions/latest"

def test_read_secret_error(secret_manager_api_service, monkeypatch):
    mock_client = MagicMock()
    mock_client.access_secret_version.side_effect = Exception("Error accessing secret")
    monkeypatch.setattr(secret_manager_api_service, "client", mock_client)
    
    secret_name = "some-secret"
    with pytest.raises(Exception):
        secret_manager_api_service.read_secret(secret_name)

import pytest
from happtiq_commons_google_cloud.auth_service import GoogleOAuth2Service
from unittest.mock import MagicMock, patch
from google.oauth2.credentials import Credentials

@pytest.fixture
def auth_service():
    return GoogleOAuth2Service()

def test_auth(auth_service, monkeypatch):
    mock_credentials = MagicMock(spec=Credentials)
    mock_credentials.refresh.return_value = None
    monkeypatch.setattr(Credentials, "from_authorized_user_file", MagicMock(return_value=mock_credentials))

    file = "test_credentials.json"
    credentials = auth_service.auth(file)
    assert credentials == mock_credentials
    Credentials.from_authorized_user_file.assert_called_once_with(file)
    mock_credentials.refresh.assert_called_once()

def test_auth_error(auth_service, monkeypatch):
    mock_credentials = MagicMock(spec=Credentials)
    mock_credentials.refresh.side_effect = Exception("Error refreshing credentials")
    monkeypatch.setattr(Credentials, "from_authorized_user_file", MagicMock(return_value=mock_credentials))

    file = "test_credentials.json"
    with pytest.raises(Exception):
        auth_service.auth(file)

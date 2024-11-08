import pytest
from happtiq_commons_google_cloud.logging_utils import is_cloud_function, setup_logging
from unittest.mock import MagicMock, patch
import os

@pytest.fixture
def empty_fixture():
    return

def test_is_cloud_function_with_k_service(monkeypatch):
    monkeypatch.setenv('K_SERVICE', 'test-service')
    assert is_cloud_function()

def test_is_cloud_function_without_k_service(monkeypatch):
    monkeypatch.delenv('K_SERVICE', raising=False)
    assert not is_cloud_function()

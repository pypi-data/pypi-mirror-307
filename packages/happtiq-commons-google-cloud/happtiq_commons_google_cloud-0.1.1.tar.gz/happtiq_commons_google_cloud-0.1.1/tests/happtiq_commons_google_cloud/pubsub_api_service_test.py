import pytest
from happtiq_commons_google_cloud.pubsub_api_service import PubsubApiService
from unittest.mock import MagicMock
import json


@pytest.fixture
def pubsub_api_service(monkeypatch):
    monkeypatch.setattr("google.auth.default", MagicMock(return_value=(MagicMock(),"some-proje")))
    return PubsubApiService()

def test_publish_message(pubsub_api_service, monkeypatch):
    mock_publisher = MagicMock()
    monkeypatch.setattr(pubsub_api_service, "publisher", mock_publisher)

    topic = "projects/test-project/topics/test-topic"
    message = {"key": "value"}
    pubsub_api_service.publish_message(topic, message)
    mock_publisher.publish.assert_called_once_with(topic, json.dumps(message).encode('utf-8'))

def test_build_topic_path(pubsub_api_service):
    project_id = "test-project"
    topic_id = "test-topic"
    topic_path = pubsub_api_service.build_topic_path(project_id, topic_id)
    assert topic_path == "projects/test-project/topics/test-topic"

def test_publish_message_error(pubsub_api_service, monkeypatch):
    mock_publisher = MagicMock()
    mock_publisher.publish.side_effect = Exception("Error publishing message")
    monkeypatch.setattr(pubsub_api_service, "publisher", mock_publisher)
    topic = "projects/test-project/topics/test-topic"
    message = {"key": "value"}
    with pytest.raises(Exception):
        pubsub_api_service.publish_message(topic, message)

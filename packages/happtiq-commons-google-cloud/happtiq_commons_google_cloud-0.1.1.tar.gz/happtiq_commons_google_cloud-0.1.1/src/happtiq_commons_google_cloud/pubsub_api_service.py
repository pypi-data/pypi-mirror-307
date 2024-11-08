import json
import logging
from google.cloud import pubsub_v1


class PubsubApiService:
    def __init__(self):
        self.publisher = pubsub_v1.PublisherClient()
        self.logger = logging.getLogger(__name__)

    def publish_message(self, topic, message: dict):
        try:
            self.logger.info(f"Publishing message {message} to topic {topic}")

            data = json.dumps(message).encode('utf-8')
            future = self.publisher.publish(topic, data)
            future.result()
            
            self.logger.info(f"Published message to pubsub {message}")
        except Exception as e:
            self.logger.error(f"Error publishing {message}: {e}")
            raise

    def build_topic_path(self, project_id: str, topic_id: str):
        return self.publisher.topic_path(project_id, topic_id)

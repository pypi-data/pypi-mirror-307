import logging
import json
import base64

class InputParserService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)


    def parse_input(self, data):
        self.logger.info(f"Decoding data {data}")
        base64message = data["message"]["data"]
        pubsub_message = base64.b64decode(base64message).decode('utf-8')
        self.logger.debug(f"Decoded message {pubsub_message}")
        
        self.logger.debug(f"Parsing message {pubsub_message} as json")
        message_data = json.loads(pubsub_message)
        self.logger.info(f"Parsed message {message_data}")

        return message_data

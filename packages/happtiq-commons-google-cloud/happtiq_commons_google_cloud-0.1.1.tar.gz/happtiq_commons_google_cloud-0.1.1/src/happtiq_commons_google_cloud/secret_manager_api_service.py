from google.cloud import secretmanager
import logging


class SecretManagerApiService:
    def __init__(self):
        self.client = secretmanager.SecretManagerServiceClient()
        self.logger = logging.getLogger(__name__)

    def read_secret(self, secret_name: str):
        self.logger.info(f"Getting secret {secret_name}")
        
        try:
            response = self.client.access_secret_version(request={"name": secret_name})
            self.logger.info(f"Got secret {secret_name} successfully")
        except Exception as e:
            self.logger.error(f"Failed to acess secret {secret_name}: {e}")
            raise

        # Extract 'Plain Text' Key
        try:
            self.logger.debug(f"Decoding secret {secret_name}")
            secret_key = response.payload.data.decode("UTF-8")
            self.logger.info(f"Decoded secret {secret_name} successfully")
        except Exception as e:
            self.logger.error(f"Failed to decode secret: {e}")
            raise

        return secret_key
    
    def build_secret_name(project_id: str, secret_id: str, version_id: str = "latest"):
        return f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

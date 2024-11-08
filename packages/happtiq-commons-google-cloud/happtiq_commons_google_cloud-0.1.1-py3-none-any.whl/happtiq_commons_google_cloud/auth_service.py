import logging
from google.oauth2.credentials import Credentials
import google.auth.transport.requests

class GoogleOAuth2Service:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def auth(self, file):
        self.logger.info("Logging in")
        credentials = Credentials.from_authorized_user_file(file)
        request = google.auth.transport.requests.Request()
        credentials.refresh(request)
        self.logger.info("Logged in")
        return credentials

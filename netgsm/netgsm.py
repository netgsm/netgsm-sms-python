"""
Main class for Netgsm SMS API.
"""

import base64
from .sms.sms_service import SmsService
from .utils.config import Config


class Netgsm:
    """
    Netgsm API client.

    This class is the main entry point for interacting with Netgsm APIs.
    """

    def __init__(self, username, password, api_url=None, appname=None):
        """
        Initialize Netgsm client.

        Args:
            username (str): Netgsm username
            password (str): Netgsm password
            api_url (str, optional): Netgsm API URL. Uses Config.API_URL by default.
            appname (str, optional): Application name.
        """
        self.username = username
        self.password = password
        self.api_url = api_url or Config.API_URL
        self.appname = appname

        # Header for Basic Authentication
        auth_str = f"{username}:{password}"
        auth_bytes = auth_str.encode("ascii")
        auth_b64 = base64.b64encode(auth_bytes).decode("ascii")
        self.auth_header = {"Authorization": f"Basic {auth_b64}"}

        # SMS service
        self._sms = None

    @property
    def sms(self):
        """
        SMS service.

        Returns:
            SmsService: SMS service
        """
        if self._sms is None:
            self._sms = SmsService(self)
        return self._sms

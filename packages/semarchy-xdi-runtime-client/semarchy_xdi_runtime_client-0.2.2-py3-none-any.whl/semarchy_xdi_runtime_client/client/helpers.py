import logging
from typing import Optional

import requests


class LoggingMixin:
    """A simple mixin providing logging capability"""

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        console_handler = logging.StreamHandler()
        self._logger.addHandler(console_handler)
        formatter = logging.Formatter(
            "{asctime} - {levelname} - {message}",
            style="{",
            datefmt="%Y-%m-%d %H:%M",
        )

        console_handler.setFormatter(formatter)

    @property
    def log(self):
        return self._logger


class PreparedRequest:
    """A prepared request wrapper around the request Session class"""

    def __init__(
        self,
        session: requests.Session,
        url: str,
        method: str,
        verify_host: bool,
        payload: Optional[dict] = None,
    ):
        """Initialize a prepared Request.

        Args:
            session (requests.Session): A request session used for the request
            url (str): The URL to connect to
            method (str): The HTTP method used
            verify_host (bool): Verify the SSL certs
            payload (Optional[dict], optional): The payload to send, will be send as json  . Defaults to None.
        """
        self.sync_session = session
        self.url = url
        self.method = method
        self.payload = payload
        self.verify_host = verify_host

    def run(self):
        return self.sync_session.request(
            method=self.method,
            url=self.url,
            json=self.payload,
            verify=self.verify_host,
        )

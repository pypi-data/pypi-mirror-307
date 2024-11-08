"""Authentication class for the Allphins API."""
import os
from typing import Optional

import requests
from requests import HTTPError

from allphins.const import ACCESS_TOKEN_URL
from allphins.const import REFRESH_TOKEN_URL
from allphins.const import USER_AGENT
from allphins.status import HTTP_401_UNAUTHORIZED


class Auth:
    """Authentication class for the Allphins API.

    This class manages the access and refresh tokens.
    The credentials are provided in the constructor or via environment variables.

    Attributes:
        _access_token: The access token.
        _refresh_token: The refresh token.
    """

    REQUEST_TIMEOUT = 3
    USER_AGENT_HEADER = {'User-Agent': USER_AGENT}

    def __init__(self, username: Optional[str] = None, password: Optional[str] = None):
        """Initialize the authentication object.

        Credentials are extracted from method parameters in priority and then from environment variable.

        Args:
            username: (Optional str) The username to use for authentication.
            password: (Optional str) The password to use for authentication.

        Raises:
            ValueError: If the username or password is not provided.
        """
        self._access_token: Optional[str] = None
        self._refresh_token: Optional[str] = None

        username = os.environ.get('ALLPHINS_APIKEY') if username is None else username
        password = os.environ.get('ALLPHINS_PASSKEY') if password is None else password
        error_message = '{credential} must be provided. You can setup the {env_var} environment variable.'

        if not username:
            raise ValueError(error_message.format(credential='Username', env_var='ALLPHINS_APIKEY'))

        if not password:
            raise ValueError(error_message.format(credential='Password', env_var='ALLPHINS_PASSKEY'))

        self.username = username
        self.password = password

        self._get_tokens()

    def _get_tokens(self):
        """Get the access and refresh token.

        This method is called in the constructor to get the tokens.

        Raises:
            ValueError: If the username or password is invalid.
            HTTPError: If the request fails.
        """
        json = {
            'username': self.username,
            'password': self.password,
        }
        response = requests.post(
            ACCESS_TOKEN_URL, json=json, timeout=self.REQUEST_TIMEOUT, headers=self.USER_AGENT_HEADER
        )
        try:
            response.raise_for_status()
        except HTTPError as e:
            if response.status_code == HTTP_401_UNAUTHORIZED:
                raise ValueError('Invalid username or password')
            else:
                raise e
        response_json = response.json()
        self._access_token = response_json['access']
        self._refresh_token = response_json['refresh']

    def refresh_access_token(self):
        """Refresh the access token.

        Raises:
             HTTPError: If the request fails.
        """
        json = {
            'refresh': self._refresh_token,
        }
        response = requests.post(
            REFRESH_TOKEN_URL, json=json, timeout=self.REQUEST_TIMEOUT, headers=self.USER_AGENT_HEADER
        )
        response.raise_for_status()
        self._access_token = response.json()['access']

    def get_authentication_header(self) -> dict:
        """Get the authentication header to be added in any requests.

        Returns:
            The authentication header.
            Example: {'Authorization': 'Bearer xxxx'}.
        """
        return {'Authorization': f'Bearer {self._access_token}', **self.USER_AGENT_HEADER}

"""Base class for client used to interact with Allphins API."""

import logging
from typing import Any
from typing import Optional

import requests
from requests import HTTPError
from requests import Response
from tqdm import tqdm

from allphins.client.auth import Auth
from allphins.const import SSL_IGNORE
from allphins.singleton import Singleton
from allphins.status import HTTP_403_FORBIDDEN

logger = logging.getLogger(__name__)


class Client(metaclass=Singleton):
    """Client to bundle configuration needed for API requests.

    The Client is a singleton. It is instantiated once and then reused, it's to avoid requesting different tokens
    for every type of objects using a :class:`Client`


    Attributes:
        auth: The authentication object to use for authentication.
    """

    REQUEST_TIMEOUT = 180  # seconds

    def __init__(self, auth: Optional[Auth] = None):
        """Initialize the client.

        If no value is passed in for auth, a :class:`Auth` instance will be created with credentials read
        via environment variables.

        Args:
            auth: (Optional) The authentication object to use for authentication.
        """
        if auth is None:
            auth = Auth()
        self.auth = auth

    def call_api(
        self,
        url: str,
        method: str,
        json: Optional[dict] = None,
        headers: Optional[dict] = None,
        page_size: Optional[int] = None,
    ) -> Any:
        """Call the API.

        Access token is automatically manged by the Auth class.
        If the token is expired, it will be refreshed and the call will be retried.

        Args:
            url: (str) The url to call.
            method: (str) The method to use for the request (GET, POST, PUT, DELETE...).
            json: (Optional dict) The json to send with the request.
            headers: (Optional dict) The headers to send with the request.
            page_size: (Optional int) Specify the page size for the pagination. None means no pagination.

        Returns:
            Any: The response from the API.

        Raises:
             HTTPError: If the request fails.
        """
        response = self._perform_call(url, method, json, headers, page_size)
        try:
            response.raise_for_status()
        except HTTPError as e:
            if response.status_code == HTTP_403_FORBIDDEN:
                self.auth.refresh_access_token()
                response = self._perform_call(url, method, json, headers, page_size)
                response.raise_for_status()
            else:
                raise e
        return response.json()

    def call_api_with_pagination(
        self,
        url: str,
        method: str,
        page_size: int,
        json: Optional[dict] = None,
        headers: Optional[dict] = None,
    ) -> list:
        """Call the API with pagination.

        Automatically iterate through the pages to get all the results.
        Display progress bar based on the number of results.
        Access token is automatically manged by the Auth class.
        If the token is expired, it will be refreshed and the call will be retried.

        Args:
            url: (str) The url to call.
            method: (str) The method to use for the request (GET, POST, PUT, DELETE...).
            page_size: (int) Specify the page size for the pagination.
            json: (Optional dict) The json to send with the request.
            headers: (Optional dict) The headers to send with the request.

        Returns:
            Any: The response from the API.

        Raises:
             HTTPError: If the request fails.
        """
        result: list = list()
        page: int = 1

        call = self.call_api(url, method, json, headers, page_size)
        call_count = call['count']
        logger.debug(f"Fetching {call_count} items")
        with tqdm(total=call_count) as pbar:
            while call.get('next') is not None:
                result.extend(call.get('results', []))
                pbar.update(len(call.get('results', [])))
                pbar.refresh()
                page += 1
                url, json = self._set_page_number(url, page, json)
                call = self.call_api(url, method, json, headers, page_size)

            result.extend(call.get('results', []))
            pbar.update(call_count - len(result))

        return result

    def _perform_call(
        self,
        url: str,
        method: str,
        json: Optional[dict],
        headers: Optional[dict],
        page_size: Optional[int],
    ) -> Response:
        """Perform the API call.

        Args:
            url: (str) The url to call.
            method: (str) The method to use for the request (GET, POST, PUT, DELETE...).
            json: (Optional dict) The json to send with the request.
            headers: (Optional dict) The headers to send with the request.
            page_size: (Optional int) Specify the page size for the pagination. None means no pagination.


        Returns:
            Response: The Response object from requests.

        Raises:
             HTTPError: If the request fails.
        """
        if headers is None:
            headers = {}

        auth_header = self.auth.get_authentication_header()
        headers = {**headers, **auth_header}
        url, json = self._set_page_size(url, page_size, json)

        response = requests.request(
            method, url, headers=headers, json=json, timeout=self.REQUEST_TIMEOUT, verify=SSL_IGNORE
        )
        return response

    @staticmethod
    def _set_page_size(url: str, page_size: Optional[int], json: Optional[dict]) -> tuple:
        """Append the pagination to the url and add it to the json payload.

        By default, the API paginates the results. To get all the results, we explicitly set the pageSize to None.

        Args:
            url: The url to append the pagination to.
            json: The json payload to append the pagination to.

        Returns:
            tuple[str, dict]: The url and the json payload with the pagination added.
        """
        if json is not None:
            json['pageSize'] = page_size

        if 'pageSize' in url:
            return url, json

        if '?' in url:
            url += '&'
        else:
            url += '?'
        url += f'pageSize={page_size}'
        return url, json

    @staticmethod
    def _set_page_number(url: str, page_number: int, json: Optional[dict]) -> tuple:
        """Append the page number to the url and add it to the json payload.

        Args:
            url: The url to append the page number to.
            json: The json payload to append the page number to.

        Returns:
            tuple[str, dict]: The url and the json payload with the page number added.
        """
        if json is not None:
            json['page'] = page_number

        if '?' in url:
            url += '&'
        else:
            url += '?'
        url += f'page={page_number}'
        return url, json

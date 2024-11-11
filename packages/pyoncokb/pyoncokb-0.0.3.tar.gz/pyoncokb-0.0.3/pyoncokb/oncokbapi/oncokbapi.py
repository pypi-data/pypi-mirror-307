"""OncoKB API."""

import logging
import time
from typing import Dict, List, Union

import requests

logger = logging.getLogger(__name__)


class OncokbApi:
    """Provide components to make OncoKB API request."""

    base_url = "https://www.oncokb.org/api/v1"

    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(
        self,
        auth: str,
        sleep_seconds: int = 5,
        sleep_queries: int = 100,
        timeout: int = 10,
    ):
        """Initialize.

        :param auth: OncoKB API authorization.
        :type auth: str
        :param sleep_seconds: sleep seconds for every `sleep_queries` queries, defaults to 5
        :type sleep_seconds: int, optional
        :param sleep_queries: sleep for a number of queries, defaults to 100
        :type sleep_queries: int, optional
        :param timeout: time out for HTTP request, defaults to 10
        :type timeout: int, optional
        """
        self.auth = auth
        self.sleep_seconds = sleep_seconds
        self.sleep_queries = sleep_queries
        self.timeout = timeout
        self.count = 0

    def get_data(self, url: str) -> Union[List, Dict, None]:
        """Use HTTP GET method to get data.

        :param url: URL of a query.
        :type url: str
        :return: convert API JSON response to Python data structure.
        :rtype: Union[List, Dict, None]
        """
        response = self.get_response(url=url)
        if response.status_code == 200:
            # Extract the response data in JSON format
            return response.json()
        logger.warning("Request failed with status code %i", response.status_code)
        return None

    def get_response(
        self,
        url: str,
    ) -> requests.Response:
        """Get HTTP response of GET method for a query.

        :param url: URL of a query.
        :type url: str
        :return: a :class:`requests.Response`.
        :rtype: requests.Response
        """
        headers = self.get_headers()
        response = requests.get(url, headers=headers, timeout=self.timeout)
        return response

    def post_data(self, url: str, data: Union[List, Dict]) -> Union[List, Dict, None]:
        """Use HTTP POST method to get data.

        :param url: URL of a query.
        :type url: str
        :param data: data for POST method.
        :type data: Union[List, Dict]
        :return: convert API JSON response to Python data structure.
        :rtype: Union[List, Dict, None]
        """
        response = self.post_response(url=url, data=data)
        if response.status_code == 200:
            # Extract the response data in JSON format
            return response.json()
        logger.warning("Request failed with status code %i", response.status_code)
        return None

    def post_response(self, url: str, data: Union[List, Dict]) -> requests.Response:
        """Get HTTP response of POST method for a query.

        :param url: URL of a query.
        :type url: str
        :param data: data for POST method.
        :type data: Union[List, Dict]
        :return: a :class:`requests.Response`.
        :rtype: requests.Response
        """
        headers = self.get_headers()
        response = requests.post(url, json=data, headers=headers, timeout=self.timeout)
        return response

    def get_headers(self) -> Dict:
        """Get OncoKB API headers for an API request.

        :return: a `dict` of two items: `accept` which is always `"application/json"`,
            `Authorization`: a token string.
        :rtype: Dict
        """
        """Get OncoKB API headers.

        Returns:
            dict: 
        """
        headers = {"accept": "application/json", "Authorization": self.auth}
        return headers

    def count_and_sleep(self) -> bool:
        """Count and sleep.

        Sleep `sleep_seconds` seconds for every `sleep_queries` queries.

        :return: True if sleep.
        :rtype: bool
        """
        self.add_count(by=1)
        if self.count % self.sleep_queries == 0:
            logger.debug(
                "sleep %s seconds for %s queries", self.sleep_seconds, self.count
            )
            time.sleep(self.sleep_seconds)
            return True
        return False

    def add_count(self, by: int = 1) -> int:
        self.count = self.count + by
        return self.count

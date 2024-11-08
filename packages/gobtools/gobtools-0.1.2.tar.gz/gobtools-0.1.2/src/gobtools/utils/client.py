"""
A module providing a Client class for making HTTP requests.

This module defines a Client class that allows checking connectivity
and sending JSON-formatted POST requests to specified endpoints.
"""

import json
from urllib.parse import urljoin

import requests


class Client:
    """
    A client for making HTTP requests to a specified base URL.

    Attributes:
        path_root (str): The base URL for all requests made by this client.

    """

    def __init__(self, path_root: str) -> None:
        """
        Initialize the Client with a base URL.

        Arguments:
        ---------
            path_root (str): The base URL for requests made by this client.

        """
        self.path_root = path_root

    def is_connected(self) -> bool:
        """
        Check if the client can connect to the base URL.

        Sends a GET request to the base URL and checks if the status
        code indicates a successful or client error response.

        Returns:
            bool: True if the connection is successful (status code is between
            200 and 499), False otherwise.

        """
        request = requests.get(self.path_root, timeout=5)
        status_code = request.status_code

        success_min = 200
        client_error_max = 499
        return status_code >= success_min and status_code <= client_error_max

    def post_dict(self, path: str, data: dict) -> dict:
        """
        Send a POST request with JSON data to a specified endpoint.

        Arguments:
        ---------
            path (str): The endpoint path to send the POST request to,
                relative to the base URL.
            data (dict): The dictionary to send as JSON data.

        Returns:
        -------
            dict: The response data parsed as a dictionary.

        """
        request = requests.post(urljoin(self.path_root, path), json=data, timeout=None)  # noqa: S113
        return json.loads(request.text)

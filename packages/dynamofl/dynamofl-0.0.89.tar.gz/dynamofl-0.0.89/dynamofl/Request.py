"""
This module provides a class for making HTTP requests with authentication.
It supports various HTTP methods (GET, POST, PUT, PATCH, DELETE) and
handles error logging and response parsing.
"""
import json
import logging

import requests

logger = logging.getLogger("Request")

API_VERSION = "v1"


def _check_for_error(r):
    if not r.ok:
        logger.error(json.dumps(json.loads(r.text), indent=4))
    r.raise_for_status()


class _Request:
    """
    Handles HTTP requests with Bearer token authentication.

    Attributes:
        token (str): Bearer token for authorization.
        host (str): Base URL for the API.

    Methods:
        _get_route(): Constructs the base API route.
        _get_headers(): Returns the headers required for the request.
        _log_error(response): Logs errors based on response status.
        _make_request(method, url, ...): Makes an HTTP request and handles the response with optional error logging.
    """

    def __init__(self, token, host):
        self.token = token
        self.host = host

    def _get_route(self):
        return f"{self.host}/{API_VERSION}"

    def _get_headers(self):
        return {"Authorization": f"Bearer {self.token}"}

    def _log_error(self, response):
        if not response.ok:
            logger.error(json.dumps(json.loads(response.text), indent=4))

    def _make_request(
        self,
        method,
        url,
        params=None,
        files=None,
        list=False,
        throw_error=True,
        print_error=True,
    ):
        try:
            request_method_mapper = {
                "POST": requests.post,
                "GET": requests.get,
                "DELETE": requests.delete,
                "PATCH": requests.patch,
                "PUT": requests.put,
            }
            if method not in request_method_mapper:
                raise ValueError("Method must be GET, POST, PUT, PATCH or DELETE")

            request_method = request_method_mapper[method]
            response = request_method(
                f"{self._get_route()}{url}",
                headers=self._get_headers(),
                json=params if method in ["POST", "DELETE", "PATCH", "PUT"] else None,
                params=params if method == "GET" else None,
                files=files,
                verify=False,
            )
            if print_error:
                self._log_error(response)
            response.raise_for_status()
            if response.content:
                if list:
                    return response.json()["data"]
                else:
                    return response.json()
        except requests.exceptions.RequestException:
            if throw_error:
                raise

import http
import json

import requests

from transstellar.framework.loggable import Loggable

from .errors import ClientError, ServerError, UnauthorizedError


class APIClient(Loggable):
    token = ""
    headers = {"content-type": "application/json", "accept": "application/json"}

    def __init__(self, base_url: str, options=None):
        super().__init__()

        self.base_url = base_url

        if options is None:
            options = {}

        if options.get("debug") is True:

            def httpclient_log(*args):
                self.logger.debug(" ".join(args))

            # mask the print() built-in in the http.client module to use
            # logging instead
            http.client.print = httpclient_log
            # enable debugging
            http.client.HTTPConnection.debuglevel = 1

    def as_token(self, token):
        self.token = token

        return self

    def get(self, endpoint, params=None, headers=None):

        url = f"{self.base_url}/{endpoint}"

        return self.__get(url, params, headers)

    def post(
        self, endpoint, payload=None, headers=None, expected_successful_status_code=201
    ):
        url = f"{self.base_url}/{endpoint}"
        return self.__post(url, payload, headers, expected_successful_status_code)

    def patch(
        self, endpoint, payload, headers=None, expected_successful_status_code=200
    ):
        url = f"{self.base_url}/{endpoint}"
        return self.__patch(url, payload, headers, expected_successful_status_code)

    def put(self, endpoint, payload, headers=None, expected_successful_status_code=200):
        url = f"{self.base_url}/{endpoint}"
        return self.__put(url, payload, headers, expected_successful_status_code)

    def delete(self, endpoint, headers=None):
        url = f"{self.base_url}/{endpoint}"

        return self.__delete(url, headers)

    def __get(self, url, params, headers):
        headers = self.__get_headers(headers)

        response = requests.get(url, params=params, headers=headers, timeout=10)

        return self.__handle_response(response)

    def __post(self, url, payload, headers=None, expected_successful_status_code=201):
        headers = self.__get_headers(headers)
        response = requests.post(url, json=payload, headers=headers, timeout=10)

        return self.__handle_response(response, expected_successful_status_code)

    def __patch(self, url, payload, headers=None, expected_successful_status_code=200):
        headers = self.__get_headers(headers)
        response = requests.patch(url, json=payload, headers=headers, timeout=10)

        return self.__handle_response(response, expected_successful_status_code)

    def __put(self, url, payload, headers=None, expected_successful_status_code=200):
        headers = self.__get_headers(headers)
        response = requests.put(url, json=payload, headers=headers, timeout=10)

        return self.__handle_response(response, expected_successful_status_code)

    def __delete(self, url, headers=None):
        headers = self.__get_headers(headers)
        response = requests.delete(url, headers=headers, timeout=10)

        return self.__handle_response(response, expected_successful_status_code=204)

    def __get_headers(self, headers):
        if headers is None:
            headers = {}
        return {**self.headers, **headers, "Authorization": f"Bearer {self.token}"}

    def __handle_response(
        self, response: requests.models.Response, expected_successful_status_code=200
    ):
        status_code = response.status_code
        response_json = None

        if response.text:
            response_json = json.loads(response.text)

        if 200 <= status_code < 300:
            if status_code != expected_successful_status_code:
                raise RuntimeError(
                    # pylint: disable-next=C0301
                    "Response status code ({status_code}) is not as expected: {expected_successful_status_code}"
                )
            return response_json

        if 400 <= status_code < 500:
            error_message = response_json.get("message", "Unknown client error")

            if status_code == 400:
                raise ClientError(f"Client error: {error_message}")

            if status_code == 401:
                raise UnauthorizedError("Unauthorized: Check your credentials")

            error_message = response_json.get("message", "Unknown client error")
            raise ClientError(f"Client error: HTTP {status_code}. {error_message}")

        if status_code >= 500:
            error_message = response_json.get("message", "Internal Server Error")
            raise ServerError(f"Server error: HTTP {status_code}. {error_message}")

        raise ServerError(f"Unknown server error: HTTP {status_code}. {error_message}")

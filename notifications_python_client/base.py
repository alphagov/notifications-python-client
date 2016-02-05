from __future__ import absolute_import
from monotonic import monotonic
from notifications_python_client.errors import HTTPError, InvalidResponse
from notifications_python_client.authentication import create_jwt_token
from notifications_python_client.version import __version__
import json

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

import requests


class BaseAPIClient(object):
    def __init__(self, base_url=None, client_id=None, secret=None):
        """
        Initialise the client
        Error if either of base_url or secret missing
        :param base_url - base URL of GOV.UK Notify API:
        :param secret - application secret - used to sign the request:
        :return:
        """
        assert base_url, "Missing base url"
        assert client_id, "Missing client id"
        assert secret, "Missing secret"
        self.base_url = base_url
        self.client_id = client_id
        self.secret = secret

    def put(self, url, data):
        return self.request("PUT", url, data=data)

    def get(self, url, params=None):
        return self.request("GET", url, params=params)

    def post(self, url, data):
        return self.request("POST", url, data=data)

    def delete(self, url, data=None):
        return self.request("DELETE", url, data=data)

    def request(self, method, url, data=None, params=None):

        print("API request {} {}".format(method, url))

        payload = json.dumps(data) if data else None

        api_token = create_jwt_token(
            method,
            url,
            self.secret,
            self.client_id,
            payload
        )

        headers = {
            "Content-type": "application/json",
            "Authorization": "Bearer {}".format(api_token),
            "User-agent": "NOTIFY-API-PYTHON-CLIENT/{}".format(__version__),
        }

        url = urlparse.urljoin(self.base_url, url)

        start_time = monotonic()
        try:
            response = requests.request(
                method,
                url,
                headers=headers,
                data=payload,
                params=params
            )
            response.raise_for_status()
        except requests.RequestException as e:
            api_error = HTTPError.create(e)
            print(
                "API {} request on {} failed with {} '{}'".format(
                    method,
                    url,
                    api_error.status_code,
                    api_error.message
                )
            )
            raise api_error
        finally:
            elapsed_time = monotonic() - start_time
            print("API {} request on {} finished in {}".format(method, url, elapsed_time))

        try:
            if response.status_code == 204:
                return
            return response.json()
        except ValueError:
            raise InvalidResponse(
                response,
                message="No JSON response object could be decoded"
            )

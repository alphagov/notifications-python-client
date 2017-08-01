from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from future import standard_library
standard_library.install_aliases()
import urllib.parse
import logging
import json

from monotonic import monotonic
import requests

from notifications_python_client import __version__
from notifications_python_client.errors import HTTPError, InvalidResponse
from notifications_python_client.authentication import create_jwt_token


logger = logging.getLogger(__name__)


class BaseAPIClient(object):
    def __init__(
            self,
            api_key,
            base_url='https://api.notifications.service.gov.uk'
    ):
        """
        Initialise the client
        Error if either of base_url or secret missing
        :param base_url - base URL of GOV.UK Notify API:
        :param secret - application secret - used to sign the request:
        :return:
        """
        service_id = api_key[-73:-37]
        api_key = api_key[-36:]

        assert base_url, "Missing base url"
        assert service_id, "Missing service ID"
        assert api_key, "Missing API key"
        self.base_url = base_url
        self.service_id = service_id
        self.api_key = api_key

    def put(self, url, data):
        return self.request("PUT", url, data=data)

    def get(self, url, params=None):
        return self.request("GET", url, params=params)

    def post(self, url, data):
        return self.request("POST", url, data=data)

    def delete(self, url, data=None):
        return self.request("DELETE", url, data=data)

    def generate_headers(self, api_token):
        return {
            "Content-type": "application/json",
            "Authorization": "Bearer {}".format(api_token),
            "User-agent": "NOTIFY-API-PYTHON-CLIENT/{}".format(__version__)
        }

    def request(self, method, url, data=None, params=None):

        logger.debug("API request {} {}".format(method, url))

        payload = json.dumps(data)

        api_token = create_jwt_token(
            self.api_key,
            self.service_id
        )

        url = urllib.parse.urljoin(str(self.base_url), str(url))

        start_time = monotonic()
        try:
            response = requests.request(
                method,
                url,
                headers=self.generate_headers(api_token),
                data=payload,
                params=params
            )
            response.raise_for_status()
        except requests.RequestException as e:
            api_error = HTTPError.create(e)
            logger.error(
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
            logger.debug("API {} request on {} finished in {}".format(method, url, elapsed_time))

        try:
            if response.status_code == 204:
                return
            return response.json()
        except ValueError:
            raise InvalidResponse(
                response,
                message="No JSON response object could be decoded"
            )

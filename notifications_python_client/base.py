import json
import logging
import time
import urllib.parse

import requests

from notifications_python_client import __version__
from notifications_python_client.authentication import create_jwt_token
from notifications_python_client.errors import HTTPError, InvalidResponse

logger = logging.getLogger(__name__)


class BaseAPIClient:
    def __init__(
        self,
        api_key,
        base_url="https://api.notifications.service.gov.uk",
        timeout=30,
        request_session=None,
    ):
        """
        Initialise the client
        Error if either of base_url or secret missing
        :param base_url - base URL of GOV.UK Notify API:
        :param secret - application secret - used to sign the request:
        :param timeout - request timeout on the client
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
        self.timeout = timeout
        self.request_session = request_session or requests.Session()

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
            "Authorization": f"Bearer {api_token}",
            "User-agent": f"NOTIFY-API-PYTHON-CLIENT/{__version__}",
        }

    def request(self, method, url, data=None, params=None):
        logger.debug("API request %s %s", method, url)
        url, kwargs = self._create_request_objects(url, data, params)

        response = self._perform_request(method, url, kwargs)

        return self._process_json_response(response)

    def _create_request_objects(self, url, data, params):
        api_token = create_jwt_token(self.api_key, self.service_id)

        kwargs = {"headers": self.generate_headers(api_token), "timeout": self.timeout}

        if data is not None:
            kwargs.update(data=self._serialize_data(data))

        if params is not None:
            kwargs.update(params=params)

        url = urllib.parse.urljoin(str(self.base_url), str(url))

        return url, kwargs

    def _serialize_data(self, data):
        return json.dumps(data, default=self._extended_json_encoder)

    def _extended_json_encoder(self, obj):
        if isinstance(obj, set):
            return list(obj)

        raise TypeError

    def _perform_request(self, method, url, kwargs):
        start_time = time.monotonic()
        try:
            response = self.request_session.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            api_error = HTTPError.create(e)
            logger.warning(
                "API %s request on %s failed with %s '%s'", method, url, api_error.status_code, api_error.message
            )
            raise api_error from e
        finally:
            elapsed_time = time.monotonic() - start_time
            logger.debug("API %s request on %s finished in %s", method, url, elapsed_time)

    def _process_json_response(self, response):
        try:
            if response.status_code == 204:
                return
            return response.json()
        except ValueError as e:
            raise InvalidResponse(response, message="No JSON response object could be decoded") from e

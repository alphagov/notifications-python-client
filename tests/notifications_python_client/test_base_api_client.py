import requests
from unittest import mock

import pytest
from notifications_python_client.errors import HTTPError, InvalidResponse
from notifications_python_client.base import BaseAPIClient
from tests.conftest import API_KEY_ID, SERVICE_ID


COMBINED_API_KEY = '-'.join(['name_of_key', SERVICE_ID, API_KEY_ID])
EMOJI_API_KEY = '😬'.join(['name_of_key', SERVICE_ID, API_KEY_ID])


@pytest.mark.parametrize('client', [
    BaseAPIClient(service_id=SERVICE_ID, api_key=API_KEY_ID),
    BaseAPIClient(api_key=COMBINED_API_KEY),
    BaseAPIClient(api_key=EMOJI_API_KEY),
    BaseAPIClient(service_id=SERVICE_ID, api_key=COMBINED_API_KEY),
    BaseAPIClient(COMBINED_API_KEY),
], ids=[
    'service and api as kwargs',
    'combined api key',
    'key with emoji',
    'service id and combined api key',
    'positional api key'
])
def test_passes_through_service_id_and_key(rmock, client):
    with mock.patch('notifications_python_client.base.create_jwt_token') as mock_create_token:
        rmock.request("GET", "/", status_code=204)
        client.request("GET", '/')
    mock_create_token.assert_called_once_with(API_KEY_ID, SERVICE_ID)
    assert client.base_url == 'https://api.notifications.service.gov.uk'


def test_can_set_base_url():
    client = BaseAPIClient(base_url='foo', service_id=SERVICE_ID, api_key=COMBINED_API_KEY)
    assert client.base_url == 'foo'


def test_fails_if_client_id_missing():
    with pytest.raises(AssertionError) as err:
        BaseAPIClient(api_key=API_KEY_ID)
    assert str(err.value) == "Missing service ID"


def test_connection_error_raises_api_error(base_client, rmock_patch):
    rmock_patch.side_effect = requests.exceptions.ConnectionError(None)

    with pytest.raises(HTTPError) as e:
        base_client.request("GET", '/')

    assert str(e.value) == "503 - Request failed"
    assert e.value.message == "Request failed"
    assert e.value.status_code == 503


def test_http_error_raises_api_error(base_client, rmock):
    rmock.request(
        "GET",
        "http://test-host/",
        text="Internal Error",
        status_code=500)

    with pytest.raises(HTTPError) as e:
        base_client.request("GET", '/')

    assert str(e.value) == "500 - Request failed"
    assert e.value.message == "Request failed"
    assert e.value.status_code == 500


def test_non_2xx_response_raises_api_error(base_client, rmock):
    rmock.request(
        "GET",
        "http://test-host/",
        json={"message": "Not found"},
        status_code=404)

    with pytest.raises(HTTPError) as e:
        base_client.request("GET", '/')

    assert str(e.value) == "404 - Not found"
    assert e.value.message == "Not found"
    assert e.value.status_code == 404


def test_invalid_json_raises_api_error(base_client, rmock):
    rmock.request(
        "GET",
        "http://test-host/",
        text="Internal Error",
        status_code=200)

    with pytest.raises(InvalidResponse) as e:
        base_client.request("GET", '/')

    assert str(e.value) == "200 - No JSON response object could be decoded"
    assert e.value.message == "No JSON response object could be decoded"
    assert e.value.status_code == 200


def test_user_agent_is_set(base_client, rmock):
    rmock.request(
        "GET",
        "http://test-host/",
        json={},
        status_code=200)

    base_client.request('GET', '/')

    assert rmock.last_request.headers.get("User-Agent").startswith("NOTIFY-API-PYTHON-CLIENT/")

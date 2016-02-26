import pytest
from notifications_python_client.errors import HTTPError, InvalidResponse
import requests


def test_connection_error_raises_api_error(base_client, rmock_patch):
    rmock_patch.side_effect = requests.exceptions.ConnectionError(
        None
    )

    with pytest.raises(HTTPError) as e:
        base_client.request("GET", '/')

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

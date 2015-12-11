import requests_mock
import pytest
from client.base import BaseAPIClient
from client.notifications import NotificationsAPIClient
import mock


@pytest.yield_fixture
def rmock():
    with requests_mock.mock() as rmock:
        yield rmock


@pytest.yield_fixture
def rmock_patch():
    with mock.patch('client.base.requests.request') as rmock_patch:
        yield rmock_patch


@pytest.yield_fixture
def base_client():
    yield BaseAPIClient(base_url='http://test-host', client_id="tests", secret='very')


@pytest.yield_fixture
def notifications_client():
    yield NotificationsAPIClient(base_url='http://test-host', client_id="tests", secret='very')

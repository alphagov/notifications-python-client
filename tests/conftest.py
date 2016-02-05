import requests_mock
import pytest
from notifications_python_client.base import BaseAPIClient
from notifications_python_client.notifications import NotificationsAPIClient
import mock


TEST_HOST = 'http://test-host'
TEST_CLIENT_ID = "tests"
TEST_SECRET = 'very'


@pytest.yield_fixture
def rmock():
    with requests_mock.mock() as rmock:
        yield rmock


@pytest.yield_fixture
def rmock_patch():
    with mock.patch('notifications_python_client.base.requests.request') as rmock_patch:
        yield rmock_patch


@pytest.yield_fixture
def base_client():
    yield BaseAPIClient(base_url=TEST_HOST,
                        client_id=TEST_CLIENT_ID,
                        secret=TEST_SECRET)


@pytest.yield_fixture
def notifications_client():
    yield NotificationsAPIClient(base_url=TEST_HOST,
                                 client_id=TEST_CLIENT_ID,
                                 secret=TEST_SECRET)

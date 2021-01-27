import mock

import requests_mock
import pytest

from notifications_python_client.base import BaseAPIClient
from notifications_python_client.notifications import NotificationsAPIClient


TEST_HOST = 'http://test-host'
SERVICE_ID = 'c745a8d8-b48a-4b0d-96e5-dbea0165ebd1'
API_KEY_ID = '8b3aa916-ec82-434e-b0c5-d5d9b371d6a3'
COMBINED_API_KEY = 'key_name-{}-{}'.format(SERVICE_ID, API_KEY_ID)


@pytest.fixture
def rmock():
    with requests_mock.mock() as rmock:
        yield rmock


@pytest.fixture
def rmock_patch():
    with mock.patch('notifications_python_client.base.requests.request') as rmock_patch:
        yield rmock_patch


@pytest.fixture
def base_client():
    yield BaseAPIClient(base_url=TEST_HOST,
                        api_key=COMBINED_API_KEY)


@pytest.fixture
def notifications_client():
    yield NotificationsAPIClient(base_url=TEST_HOST,
                                 api_key=COMBINED_API_KEY)

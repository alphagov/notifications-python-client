from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
import mock

import requests_mock
import pytest

from notifications_python_client.base import BaseAPIClient
from notifications_python_client.notifications import NotificationsAPIClient


TEST_HOST = 'http://test-host'
SERVICE_ID = 'c745a8d8-b48a-4b0d-96e5-dbea0165ebd1'
API_KEY_ID = '8b3aa916-ec82-434e-b0c5-d5d9b371d6a3'
COMBINED_API_KEY = 'key_name-{}-{}'.format(SERVICE_ID, API_KEY_ID)


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
                        api_key=COMBINED_API_KEY)


@pytest.yield_fixture
def notifications_client():
    yield NotificationsAPIClient(base_url=TEST_HOST,
                                 api_key=COMBINED_API_KEY)

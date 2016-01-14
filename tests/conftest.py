import requests_mock
import pytest
from client.base import BaseAPIClient
from client.notifications import NotificationsAPIClient
from client.services import ServicesAPIClient
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
    with mock.patch('client.base.requests.request') as rmock_patch:
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


@pytest.yield_fixture
def services_client():
    yield ServicesAPIClient(base_url=TEST_HOST,
                            client_id=TEST_CLIENT_ID,
                            secret=TEST_SECRET)


def gen_service(id_, name, user=1, limit=1000, active=False, restricted=False):
    return {
        'id': id_,
        'name': name,
        'users': [user],
        'limit': limit,
        'active': active,
        'restricted': restricted}


def gen_service_template(id_,
                         name,
                         template_type="sms",
                         content="Service template",
                         service="1"):
    return {
        'id': id_,
        'name': name,
        'template_type': template_type,
        'content': content,
        'service': service}


@pytest.fixture(scope='function')
def service_json():
    return gen_service(1, "service one")


@pytest.fixture(scope='function')
def services_json():
    return [gen_service(1, "service one"), gen_service(2, "service two")]


@pytest.fixture(scope='function')
def service_template_json():
    return gen_service_template(1, "service one template one")


@pytest.fixture(scope='function')
def service_templates_json():
    return [gen_service_template(1, "service one template one"),
            gen_service_template(2, "service one template two")]

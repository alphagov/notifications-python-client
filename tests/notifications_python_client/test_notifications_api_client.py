from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from tests.conftest import TEST_HOST


def test_get_notification_by_id(notifications_client, rmock):
    endpoint = "{0}/v2/notifications/{1}".format(TEST_HOST, "123")
    rmock.request(
        "GET",
        endpoint,
        json={"status": "success"},
        status_code=200)

    notifications_client.get_notification_by_id(123)

    assert rmock.called


def test_get_all_notifications_by_type_and_status(notifications_client, rmock):
    endpoint = "{0}/v2/notifications?status={1}&template_type={2}".format(TEST_HOST, "status", "type")
    rmock.request(
        "GET",
        endpoint,
        json={"status": "success"},
        status_code=200)

    notifications_client.get_all_notifications("status", "type")

    assert rmock.called


def test_get_all_notifications_by_type(notifications_client, rmock):
    endpoint = "{0}/v2/notifications?template_type={1}".format(TEST_HOST, "type")
    rmock.request(
        "GET",
        endpoint,
        json={"status": "success"},
        status_code=200)

    notifications_client.get_all_notifications(template_type="type")

    assert rmock.called


def test_get_all_notifications_by_reference(notifications_client, rmock):
    endpoint = "{0}/v2/notifications?reference={1}".format(TEST_HOST, "reference")
    rmock.request(
        "GET",
        endpoint,
        json={"status": "success"},
        status_code=200)

    notifications_client.get_all_notifications(reference="reference")

    assert rmock.called


def test_get_all_notifications_by_older_than(notifications_client, rmock):
    endpoint = "{0}/v2/notifications?older_than={1}".format(TEST_HOST, "older_than")
    rmock.request(
        "GET",
        endpoint,
        json={"status": "success"},
        status_code=200)

    notifications_client.get_all_notifications(older_than="older_than")

    assert rmock.called


def test_get_all_notifications_by_status(notifications_client, rmock):
    endpoint = "{0}/v2/notifications?status={1}".format(TEST_HOST, "status")
    rmock.request(
        "GET",
        endpoint,
        json={"status": "success"},
        status_code=200)

    notifications_client.get_all_notifications(status="status")

    assert rmock.called


def test_get_all_notifications(notifications_client, rmock):
    endpoint = "{0}/v2/notifications".format(TEST_HOST)
    rmock.request(
        "GET",
        endpoint,
        json={"status": "success"},
        status_code=200)

    notifications_client.get_all_notifications()

    assert rmock.called


def test_create_sms_notification(notifications_client, rmock):
    endpoint = "{0}/v2/notifications/sms".format(TEST_HOST)
    rmock.request(
        "POST",
        endpoint,
        json={"status": "success"},
        status_code=200)

    notifications_client.send_sms_notification(
        phone_number="07700 900000", template_id="456"
    )

    assert rmock.last_request.json() == {
        'template_id': '456', 'phone_number': '07700 900000'
    }


def test_create_sms_notification_with_personalisation(notifications_client, rmock):
    endpoint = "{0}/v2/notifications/sms".format(TEST_HOST)
    rmock.request(
        "POST",
        endpoint,
        json={"status": "success"},
        status_code=200)

    notifications_client.send_sms_notification(
        phone_number="07700 900000", template_id="456", personalisation={'name': 'chris'}
    )

    assert rmock.last_request.json() == {
        'template_id': '456', 'phone_number': '07700 900000', 'personalisation': {'name': 'chris'}
    }


def test_create_email_notification(notifications_client, rmock):
    endpoint = "{0}/v2/notifications/email".format(TEST_HOST)
    rmock.request(
        "POST",
        endpoint,
        json={"status": "success"},
        status_code=200)

    notifications_client.send_email_notification(
        email_address="to@example.com", template_id="456")

    assert rmock.last_request.json() == {
        'template_id': '456', 'email_address': 'to@example.com'
    }


def test_create_email_notification_with_personalisation(notifications_client, rmock):
    endpoint = "{0}/v2/notifications/email".format(TEST_HOST)
    rmock.request(
        "POST",
        endpoint,
        json={"status": "success"},
        status_code=200)

    notifications_client.send_email_notification(
        email_address="to@example.com", template_id="456", personalisation={'name': 'chris'}
    )

    assert rmock.last_request.json() == {
        'template_id': '456', 'email_address': 'to@example.com', 'personalisation': {'name': 'chris'}
    }

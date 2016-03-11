from ..conftest import TEST_HOST


def test_get_notification_by_id(notifications_client, rmock):
    endpoint = "{0}/notifications/{1}".format(TEST_HOST, "123")
    rmock.request(
        "GET",
        endpoint,
        json={"status": "success"},
        status_code=200)

    notifications_client.get_notification_by_id(123)

    assert rmock.called


def test_create_sms_notification(notifications_client, rmock):
    endpoint = "{0}/notifications/sms".format(TEST_HOST)
    rmock.request(
        "POST",
        endpoint,
        json={"status": "success"},
        status_code=200)

    notifications_client.send_sms_notification(
        "07700 900000", template_id="456"
    )

    assert rmock.last_request.json() == {
        'template': '456', 'to': '07700 900000'
    }


def test_create_sms_notification_with_personalisation(notifications_client, rmock):
    endpoint = "{0}/notifications/sms".format(TEST_HOST)
    rmock.request(
        "POST",
        endpoint,
        json={"status": "success"},
        status_code=200)

    notifications_client.send_sms_notification(
        "1234", template_id="456", personalisation={'name': 'chris'}
    )

    assert rmock.last_request.json() == {
        'template': '456', 'to': '1234', 'personalisation': {'name': 'chris'}
    }


def test_create_email_notification(notifications_client, rmock):
    endpoint = "{0}/notifications/email".format(TEST_HOST)
    rmock.request(
        "POST",
        endpoint,
        json={"status": "success"},
        status_code=200)

    notifications_client.send_email_notification(
        "to@example.com", template_id="456")

    assert rmock.last_request.json() == {
        'template': '456', 'to': 'to@example.com'
    }


def test_create_email_notification_with_personalisation(notifications_client, rmock):
    endpoint = "{0}/notifications/email".format(TEST_HOST)
    rmock.request(
        "POST",
        endpoint,
        json={"status": "success"},
        status_code=200)

    notifications_client.send_email_notification(
        "to@example.com", template_id="456", personalisation={'name': 'chris'}
    )

    assert rmock.last_request.json() == {
        'template': '456', 'to': 'to@example.com', 'personalisation': {'name': 'chris'}
    }

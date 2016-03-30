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


def test_get_all_notifications_by_stype_and_status(notifications_client, rmock):
    endpoint = "{0}/notifications?status={1}&template_type={2}".format(TEST_HOST, "status", "type")
    rmock.request(
        "GET",
        endpoint,
        json={"status": "success"},
        status_code=200)

    notifications_client.get_all_notifications("status", "type")

    assert rmock.called


def test_get_all_notifications_by_type(notifications_client, rmock):
    endpoint = "{0}/notifications?template_type={1}".format(TEST_HOST, "type")
    rmock.request(
        "GET",
        endpoint,
        json={"status": "success"},
        status_code=200)

    notifications_client.get_all_notifications(template_type="type")

    assert rmock.called


def test_get_all_notifications_by_status(notifications_client, rmock):
    endpoint = "{0}/notifications?status={1}".format(TEST_HOST, "status")
    rmock.request(
        "GET",
        endpoint,
        json={"status": "success"},
        status_code=200)

    notifications_client.get_all_notifications(status="status")

    assert rmock.called


def test_get_all_notifications(notifications_client, rmock):
    endpoint = "{0}/notifications".format(TEST_HOST)
    rmock.request(
        "GET",
        endpoint,
        json={"status": "success"},
        status_code=200)

    notifications_client.get_all_notifications()

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

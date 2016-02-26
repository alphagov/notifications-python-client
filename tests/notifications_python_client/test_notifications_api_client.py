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


def test_create_sms_notification_template(notifications_client, rmock):
    endpoint = "{0}/notifications/sms".format(TEST_HOST)
    rmock.request(
        "POST",
        endpoint,
        json={"status": "success"},
        status_code=200)

    notifications_client.send_sms_notification("1234", template_id="456")

    assert rmock.called


def test_create_email_notification(notifications_client, rmock):
    endpoint = "{0}/notifications/email".format(TEST_HOST)
    rmock.request(
        "POST",
        endpoint,
        json={"status": "success"},
        status_code=200)

    notifications_client.send_email_notification(
        "to@notify.com", template_id="456")

    assert rmock.called

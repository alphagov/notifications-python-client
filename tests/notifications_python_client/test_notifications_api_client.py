from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
import base64
import io
from future import standard_library
from mock import Mock
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


def test_get_received_texts(notifications_client, rmock):
    endpoint = "{0}/v2/received-text-messages".format(TEST_HOST)
    rmock.request(
        "GET",
        endpoint,
        json={"status": "success"},
        status_code=200)

    notifications_client.get_received_texts()
    assert rmock.called


def test_get_received_texts_older_than(notifications_client, rmock):
    endpoint = "{0}/v2/received-text-messages?older_than={1}".format(TEST_HOST, "older_id")
    rmock.request(
        "GET",
        endpoint,
        json={"status": "success"},
        status_code=200)

    notifications_client.get_received_texts(older_than="older_id")
    assert rmock.called


def test_get_all_received_texts_iterator_calls_get_received_texts(notifications_client, rmock):
    endpoint = "{0}/v2/received-text-messages".format(TEST_HOST)
    rmock.request(
        "GET",
        endpoint,
        json={"status": "success"},
        status_code=200)

    list(notifications_client.get_received_texts_iterator())
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


def test_create_sms_notification_with_sms_sender_id(notifications_client, rmock):
    endpoint = "{0}/v2/notifications/sms".format(TEST_HOST)
    rmock.request(
        "POST",
        endpoint,
        json={"status": "success"},
        status_code=200)

    notifications_client.send_sms_notification(
        phone_number="07700 900000", template_id="456", sms_sender_id="789"
    )

    assert rmock.last_request.json() == {
        'template_id': '456', 'phone_number': '07700 900000', 'sms_sender_id': '789'
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


def test_create_email_notification_with_email_reply_to_id(notifications_client, rmock):
    endpoint = "{0}/v2/notifications/email".format(TEST_HOST)
    rmock.request(
        "POST",
        endpoint,
        json={"status": "success"},
        status_code=200)

    notifications_client.send_email_notification(
        email_address="to@example.com", template_id="456", email_reply_to_id="789")

    assert rmock.last_request.json() == {
        'template_id': '456', 'email_address': 'to@example.com', 'email_reply_to_id': '789'
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


def test_create_email_notification_with_document_upload(notifications_client, rmock):
    endpoint = "{0}/v2/notifications/email".format(TEST_HOST)
    rmock.request(
        "POST",
        endpoint,
        json={"status": "success"},
        status_code=200)

    if hasattr(io, 'BytesIO'):
        mock_file = io.BytesIO(b'file-contents')
    else:
        mock_file = io.StringIO('file-contents')

    notifications_client.send_email_notification(
        email_address="to@example.com", template_id="456", personalisation={
            'name': 'chris',
            'doc': mock_file
        }
    )

    assert rmock.last_request.json() == {
        'template_id': '456', 'email_address': 'to@example.com',
        'personalisation': {
            'name': 'chris',
            'doc': {'file': 'ZmlsZS1jb250ZW50cw=='}
        }
    }


def test_create_letter_notification(notifications_client, rmock):
    endpoint = "{0}/v2/notifications/letter".format(TEST_HOST)
    rmock.request(
        "POST",
        endpoint,
        json={"status": "success"},
        status_code=200)

    notifications_client.send_letter_notification(
        template_id="456",
        personalisation={'address_line_1': 'Foo', 'address_line_2': 'Bar', 'postcode': 'Baz'}
    )

    assert rmock.last_request.json() == {
        'template_id': '456',
        'personalisation': {
            'address_line_1': 'Foo',
            'address_line_2': 'Bar',
            'postcode': 'Baz'
        }
    }


def test_create_letter_notification_with_reference(notifications_client, rmock):
    endpoint = "{0}/v2/notifications/letter".format(TEST_HOST)
    rmock.request(
        "POST",
        endpoint,
        json={"status": "success"},
        status_code=200)

    notifications_client.send_letter_notification(
        template_id="456",
        personalisation={'address_line_1': 'Foo', 'address_line_2': 'Bar', 'postcode': 'Baz'},
        reference='Baz'
    )

    assert rmock.last_request.json() == {
        'template_id': '456',
        'personalisation': {
            'address_line_1': 'Foo',
            'address_line_2': 'Bar',
            'postcode': 'Baz'
        },
        'reference': 'Baz'
    }


def test_send_precompiled_letter_notification(notifications_client, rmock, mocker):
    endpoint = "{0}/v2/notifications/letter".format(TEST_HOST)
    rmock.request(
        "POST",
        endpoint,
        json={"status": "success"},
        status_code=200)
    mock_file = Mock(
        read=Mock(return_value=b'file_contents'),
    )

    notifications_client.send_precompiled_letter_notification(
        reference='Baz',
        pdf_file=mock_file
    )

    assert rmock.last_request.json() == {
        'reference': 'Baz',
        'content': base64.b64encode(b'file_contents').decode('utf-8')
    }


def test_get_all_notifications_iterator_calls_get_notifications(notifications_client, rmock):
    endpoint = "{0}/v2/notifications".format(TEST_HOST)
    rmock.request(
        "GET",
        endpoint,
        json={"status": "success"},
        status_code=200)

    list(notifications_client.get_all_notifications_iterator())

    assert rmock.called


def test_get_all_notifications_iterator_stops_if_empty_notification_list_returned(
    notifications_client,
    rmock
):
    responses = [
        _generate_response('79f9c6ce-cd6a-4b47-a3e7-41e155f112b0', [1, 2]),
        _generate_response('3e8f2f0a-0f2b-4d1b-8a01-761f14a281bb')
    ]

    endpoint = "{0}/v2/notifications".format(TEST_HOST)
    rmock.request(
        "GET",
        endpoint,
        responses
    )

    list(notifications_client.get_all_notifications_iterator())
    assert rmock.call_count == 2


def test_get_all_notifications_iterator_gets_more_notifications_with_correct_id(
    notifications_client,
    rmock
):
    responses = [
        _generate_response('79f9c6ce-cd6a-4b47-a3e7-41e155f112b0', [1, 2]),
        _generate_response('ea179232-3190-410d-b8ab-23dfecdd3157', [3, 4]),
        _generate_response('3e8f2f0a-0f2b-4d1b-8a01-761f14a281bb')
    ]

    endpoint = "{0}/v2/notifications".format(TEST_HOST)
    rmock.request("GET", endpoint, responses)
    list(notifications_client.get_all_notifications_iterator())
    assert rmock.call_count == 3


def test_get_template(notifications_client, rmock):
    endpoint = "{0}/v2/template/{1}".format(TEST_HOST, "123")
    rmock.request(
        "GET",
        endpoint,
        json={"status": "success"},
        status_code=200)

    notifications_client.get_template(123)

    assert rmock.called


def test_get_template_version(notifications_client, rmock):
    endpoint = "{0}/v2/template/{1}/version/{2}".format(TEST_HOST, "123", 1)
    rmock.request(
        "GET",
        endpoint,
        json={"status": "success"},
        status_code=200)

    notifications_client.get_template_version(123, 1)

    assert rmock.called


def test_post_template_preview(notifications_client, rmock):
    endpoint = "{0}/v2/template/{1}/preview".format(TEST_HOST, "123")
    rmock.request(
        "POST",
        endpoint,
        json={"status": "success"},
        status_code=200)

    notifications_client.post_template_preview(123, personalisation={'name': 'chris'})

    assert rmock.called
    assert rmock.last_request.json() == {
        'personalisation': {'name': 'chris'}
    }


def test_get_all_templates(notifications_client, rmock):
    endpoint = "{0}/v2/templates".format(TEST_HOST)
    rmock.request(
        "GET",
        endpoint,
        json={"status": "success"},
        status_code=200)

    notifications_client.get_all_templates()

    assert rmock.called


def test_get_all_templates_by_type(notifications_client, rmock):
    endpoint = "{0}/v2/templates?type={1}".format(TEST_HOST, 'type')
    rmock.request(
        "GET",
        endpoint,
        json={"status": "success"},
        status_code=200)

    notifications_client.get_all_templates('type')

    assert rmock.called


def _generate_response(next_link_uuid, notifications=[]):
    return {
        'json': {
            'notifications': notifications,
            'links': {
                'next': 'http://localhost:6011/v2/notifications?older_than={}'.format(next_link_uuid)
            }
        },
        'status_code': 200
    }

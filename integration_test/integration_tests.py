import os
import uuid

from jsonschema import Draft4Validator

from integration_test.schemas.v2.inbound_sms_schemas import get_inbound_sms_response
from integration_test.schemas.v2.notification_schemas import (
    post_sms_response,
    post_email_response,
    post_letter_response,
    get_notification_response,
    get_notifications_response,
    post_precompiled_letter_response)
from integration_test.schemas.v2.template_schemas import get_template_by_id_response, post_template_preview_response
from integration_test.schemas.v2.templates_schemas import get_all_template_response
from integration_test.enums import SMS_TYPE, EMAIL_TYPE, LETTER_TYPE

from notifications_python_client.notifications import NotificationsAPIClient


def validate(json_to_validate, schema):
    validator = Draft4Validator(schema)
    validator.validate(json_to_validate, schema)


def send_sms_notification_test_response(python_client, sender_id=None):
    mobile_number = os.environ['FUNCTIONAL_TEST_NUMBER']
    template_id = os.environ['SMS_TEMPLATE_ID']
    unique_name = str(uuid.uuid4())
    personalisation = {'name': unique_name}
    sms_sender_id = sender_id
    response = python_client.send_sms_notification(phone_number=mobile_number,
                                                   template_id=template_id,
                                                   personalisation=personalisation,
                                                   sms_sender_id=sms_sender_id)
    validate(response, post_sms_response)
    assert unique_name in response['content']['body']  # check placeholders are replaced
    return response['id']


def send_email_notification_test_response(python_client, reply_to=None):
    email_address = os.environ['FUNCTIONAL_TEST_EMAIL']
    template_id = os.environ['EMAIL_TEMPLATE_ID']
    email_reply_to_id = reply_to
    unique_name = str(uuid.uuid4())
    personalisation = {'name': unique_name}
    response = python_client.send_email_notification(email_address=email_address,
                                                     template_id=template_id,
                                                     personalisation=personalisation,
                                                     email_reply_to_id=email_reply_to_id)
    validate(response, post_email_response)
    assert unique_name in response['content']['body']  # check placeholders are replaced
    return response['id']


def send_letter_notification_test_response(python_client):
    template_id = os.environ['LETTER_TEMPLATE_ID']
    unique_name = str(uuid.uuid4())
    personalisation = {
        'address_line_1': unique_name,
        'address_line_2': 'foo',
        'postcode': 'bar'
    }
    response = python_client.send_letter_notification(
        template_id=template_id,
        personalisation=personalisation
    )
    validate(response, post_letter_response)
    assert unique_name in response['content']['body']  # check placeholders are replaced
    return response['id']


def send_precompiled_letter_notification_test_response(python_client):
    unique_name = str(uuid.uuid4())
    with open('integration_test/test_files/one_page_pdf.pdf', "rb") as pdf_file:
        response = python_client.send_precompiled_letter_notification(
            reference=unique_name,
            pdf_file=pdf_file
        )
    validate(response, post_precompiled_letter_response)
    assert unique_name in response['reference']
    return response['id']


def get_notification_by_id(python_client, id, notification_type):
    response = python_client.get_notification_by_id(id)
    if notification_type == EMAIL_TYPE:
        validate(response, get_notification_response)
    elif notification_type == SMS_TYPE:
        validate(response, get_notification_response)
    elif notification_type == LETTER_TYPE:
        validate(response, get_notification_response)
    else:
        raise KeyError("notification type should be email|sms")


def get_received_text_messages():
    client = NotificationsAPIClient(
        base_url=os.environ['NOTIFY_API_URL'],
        api_key=os.environ['INBOUND_SMS_QUERY_KEY']
    )

    response = client.get_received_texts()
    validate(response, get_inbound_sms_response)
    assert len(response['received_text_messages']) > 0


def get_all_notifications(client):
    response = client.get_all_notifications()
    validate(response, get_notifications_response)


def get_template_by_id(python_client, template_id, notification_type):
    response = python_client.get_template(template_id)

    if notification_type == EMAIL_TYPE:
        validate(response, get_template_by_id_response)
    elif notification_type == SMS_TYPE:
        validate(response, get_template_by_id_response)
        assert response['subject'] is None
    else:
        raise KeyError("template type should be email|sms")

    assert template_id == response['id']


def get_template_by_id_and_version(python_client, template_id, version, notification_type):
    response = python_client.get_template_version(template_id, version)

    if notification_type == EMAIL_TYPE:
        validate(response, get_template_by_id_response)
    elif notification_type == SMS_TYPE:
        validate(response, get_template_by_id_response)
        assert response['subject'] is None
    else:
        raise KeyError("template type should be email|sms")

    assert template_id == response['id']
    assert version == response['version']


def post_template_preview(python_client, template_id, notification_type):
    unique_name = str(uuid.uuid4())
    personalisation = {'name': unique_name}

    response = python_client.post_template_preview(template_id, personalisation)

    if notification_type == EMAIL_TYPE:
        validate(response, post_template_preview_response)
    elif notification_type == SMS_TYPE:
        validate(response, post_template_preview_response)
        assert response['subject'] is None
    else:
        raise KeyError("template type should be email|sms")

    assert template_id == response['id']
    assert unique_name in response['body']


def get_all_templates(python_client):
    response = python_client.get_all_templates()
    validate(response, get_all_template_response)


def get_all_templates_for_type(python_client, template_type):
    response = python_client.get_all_templates(template_type)
    validate(response, get_all_template_response)


def test_integration():
    client = NotificationsAPIClient(
        base_url=os.environ['NOTIFY_API_URL'],
        api_key=os.environ['API_KEY']
    )
    client_using_whitelist_key = NotificationsAPIClient(
        base_url=os.environ['NOTIFY_API_URL'],
        api_key=os.environ['API_SENDING_KEY']
    )

    sms_template_id = os.environ['SMS_TEMPLATE_ID']
    sms_sender_id = os.environ['SMS_SENDER_ID']
    email_template_id = os.environ['EMAIL_TEMPLATE_ID']
    email_reply_to_id = os.environ['EMAIL_REPLY_TO_ID']

    assert sms_template_id
    assert sms_sender_id
    assert email_template_id
    assert email_reply_to_id

    version_number = 1

    sms_id = send_sms_notification_test_response(client)
    sms_with_sender_id = send_sms_notification_test_response(client_using_whitelist_key, sms_sender_id)
    email_id = send_email_notification_test_response(client)
    email_with_reply_id = send_email_notification_test_response(client, email_reply_to_id)
    letter_id = send_letter_notification_test_response(client)
    precompiled_letter_id = send_precompiled_letter_notification_test_response(client)

    get_notification_by_id(client, sms_id, SMS_TYPE)
    get_notification_by_id(client, sms_with_sender_id, SMS_TYPE)
    get_notification_by_id(client, email_id, EMAIL_TYPE)
    get_notification_by_id(client, email_with_reply_id, EMAIL_TYPE)
    get_notification_by_id(client, letter_id, LETTER_TYPE)
    get_notification_by_id(client, precompiled_letter_id, LETTER_TYPE)

    get_all_notifications(client)

    get_template_by_id(client, sms_template_id, SMS_TYPE)
    get_template_by_id(client, email_template_id, EMAIL_TYPE)
    get_template_by_id_and_version(client, sms_template_id, version_number, SMS_TYPE)
    get_template_by_id_and_version(client, email_template_id, version_number, EMAIL_TYPE)
    post_template_preview(client, sms_template_id, SMS_TYPE)
    post_template_preview(client, email_template_id, EMAIL_TYPE)

    get_all_templates(client)
    get_all_templates_for_type(client, EMAIL_TYPE)
    get_all_templates_for_type(client, SMS_TYPE)

    if (os.environ['INBOUND_SMS_QUERY_KEY']):
        get_received_text_messages()

    print("notifications-python-client integration tests are successful")


if __name__ == "__main__":
    test_integration()

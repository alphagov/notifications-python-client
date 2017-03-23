import os
import uuid

from jsonschema import Draft4Validator

from integration_test.schemas.v2.notification_schemas import (post_sms_response,
                                                              post_email_response,
                                                              get_notification_response,
                                                              get_notifications_response)
from integration_test.schemas.v2.template_schemas import get_template_by_id_response, post_template_preview_response
from integration_test.enums import SMS_TYPE, EMAIL_TYPE

from notifications_python_client.notifications import NotificationsAPIClient


def validate(json_to_validate, schema):
    validator = Draft4Validator(schema)
    validator.validate(json_to_validate, schema)


def send_sms_notification_test_response(python_client):
    mobile_number = os.environ['FUNCTIONAL_TEST_NUMBER']
    template_id = os.environ['SMS_TEMPLATE_ID']
    unique_name = str(uuid.uuid4())
    personalisation = {'name': unique_name}
    response = python_client.send_sms_notification(phone_number=mobile_number,
                                                   template_id=template_id,
                                                   personalisation=personalisation)
    validate(response, post_sms_response)
    assert unique_name in response['content']['body']  # check placeholders are replaced
    return response['id']


def send_email_notification_test_response(python_client):
    email_address = os.environ['FUNCTIONAL_TEST_EMAIL']
    template_id = os.environ['EMAIL_TEMPLATE_ID']
    unique_name = str(uuid.uuid4())
    personalisation = {'name': unique_name}
    response = python_client.send_email_notification(email_address=email_address,
                                                     template_id=template_id,
                                                     personalisation=personalisation)
    validate(response, post_email_response)
    assert unique_name in response['content']['body']  # check placeholders are resplaced
    return response['id']


def get_notification_by_id(python_client, id, notification_type):
    response = python_client.get_notification_by_id(id)
    if notification_type == EMAIL_TYPE:
        validate(response, get_notification_response)
    elif notification_type == SMS_TYPE:
        validate(response, get_notification_response)
    else:
        raise KeyError("notification type should be email|sms")


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


def test_integration():
    client = NotificationsAPIClient(
        base_url=os.environ['NOTIFY_API_URL'],
        api_key=os.environ['API_KEY']
    )

    sms_template_id = os.environ['SMS_TEMPLATE_ID']
    email_template_id = os.environ['EMAIL_TEMPLATE_ID']
    version_number = 1

    sms_id = send_sms_notification_test_response(client)
    email_id = send_email_notification_test_response(client)
    get_notification_by_id(client, sms_id, SMS_TYPE)
    get_notification_by_id(client, email_id, EMAIL_TYPE)

    get_all_notifications(client)

    get_template_by_id(client, sms_template_id, SMS_TYPE)
    get_template_by_id(client, email_template_id, EMAIL_TYPE)
    get_template_by_id_and_version(client, sms_template_id, version_number, SMS_TYPE)
    get_template_by_id_and_version(client, email_template_id, version_number, EMAIL_TYPE)
    post_template_preview(client, sms_template_id, SMS_TYPE)
    post_template_preview(client, email_template_id, EMAIL_TYPE)

    print("notifications-python-client integration tests are successful")

if __name__ == "__main__":
    test_integration()

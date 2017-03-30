import os
import uuid

from jsonschema import Draft4Validator

from integration_test.schemas.v2.notification_schemas import (post_sms_response,
                                                              post_email_response,
                                                              get_notification_response,
                                                              get_notifications_response)
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
    if notification_type == 'email':
        validate(response, get_notification_response)
    elif notification_type == 'sms':
        validate(response, get_notification_response)
    else:
        raise KeyError("notification type should be email|sms")


def get_all_notifications(client):
    response = client.get_all_notifications()
    validate(response, get_notifications_response)


def test_integration():
    client = NotificationsAPIClient(
        base_url=os.environ['NOTIFY_API_URL'],
        api_key=os.environ['API_KEY']
    )

    sms_id = send_sms_notification_test_response(client)
    email_id = send_email_notification_test_response(client)
    get_notification_by_id(client, sms_id, 'sms')
    get_notification_by_id(client, email_id, 'email')

    get_all_notifications(client)

    print("notifications-python-client integration tests are successful")

if __name__ == "__main__":
    test_integration()

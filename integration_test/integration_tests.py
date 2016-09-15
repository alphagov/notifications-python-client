import os
import uuid

from integration_test import validate
from notifications_python_client.errors import HTTPError
from notifications_python_client.notifications import NotificationsAPIClient


def send_sms_notification_test_response(python_client):
    mobile_number = os.environ['FUNCTIONAL_TEST_NUMBER']
    template_id = os.environ['SMS_TEMPLATE_ID']
    unique_name = str(uuid.uuid4())
    personalisation = {'name': unique_name}
    response = python_client.send_sms_notification(to=mobile_number,
                                                   template_id=template_id,
                                                   personalisation=personalisation)
    # do we want to test content of message? guess not
    assert response['data']['body'] == 'Hello {},\nFunctional test help make our world a better place'.format(
        unique_name)
    validate(response, 'POST_notification_return_sms.json')
    return response['data']['notification']['id']


def send_email_notification_test_response(python_client):
    email_address = os.environ['FUNCTIONAL_TEST_EMAIL']
    template_id = os.environ['EMAIL_TEMPLATE_ID']
    unique_name = str(uuid.uuid4())
    personalisation = {'name': unique_name}
    response = python_client.send_email_notification(to=email_address,
                                                     template_id=template_id,
                                                     personalisation=personalisation)
    # do we want to test
    assert response['data']['body'] == 'Hello {},\nFunctional test help make our world a better place'.format(
        unique_name)
    validate(response, 'POST_notification_return_email.json')
    return response['data']['notification']['id']


def get_notification_by_id(python_client, id, notification_type):
    response = python_client.get_notification_by_id(id)

    if notification_type == 'email':
        validate(response, 'GET_notification_return_email.json')
    elif notification_type == 'sms':
        validate(response, 'GET_notification_return_sms.json')
    else:
        raise KeyError("notification type should be email|sms")


def get_all_notifications(client):
    response = client.get_all_notifications()
    validate(response, 'GET_notifications_return.json')


if __name__ == "__main__":
    client = NotificationsAPIClient(
        os.environ['NOTIFY_API_URL'],
        os.environ['SERVICE_ID'],
        os.environ['API_KEY']
    )

    sms_id = send_sms_notification_test_response(client)
    email_id = send_email_notification_test_response(client)
    get_notification_by_id(client, sms_id, 'sms')
    get_notification_by_id(client, email_id, 'email')

    get_all_notifications(client)

    print("notifications-python-client integration tests are successful")

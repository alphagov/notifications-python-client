"""

Usage:
    utils/make_api_call.py <base_url> <service_id> <secret> <call> <type>

Example:
    ./make_api_call.py http://api my_service super_secret fetch|create email|sms
"""

import json
from notifications_python_client.notifications import NotificationsAPIClient
from docopt import docopt


def create_sms_notification(notifications_client):
    mobile_number = input("enter number (+441234123123): ")
    template_id = input("template id: ")
    personalisation = input("personalisation (JSON string):")
    personalisation = personalisation and json.loads(personalisation)
    print(notifications_client.send_sms_notification(
        mobile_number, template_id=template_id, personalisation=personalisation
    ))


def create_email_notification(notifications_client):
    mobile_number = input("enter email: ")
    template_id = input("template id: ")
    personalisation = input("personalisation (as JSON):") or None
    personalisation = personalisation and json.loads(personalisation)
    print(notifications_client.send_email_notification(
        mobile_number, template_id=template_id, personalisation=personalisation
    ))


def get_notification(notifications_client):
    id = input("Notification id: ")
    print(notifications_client.get_notification_by_id(id))

if __name__ == "__main__":
    arguments = docopt(__doc__)

    client = NotificationsAPIClient(
        arguments['<base_url>'],
        arguments['<service_id>'],
        arguments['<secret>']
    )

    if arguments['<call>'] == 'create' and arguments['<type>'] == 'sms':
        create_sms_notification(
            notifications_client=client
        )

    if arguments['<call>'] == 'create' and arguments['<type>'] == 'email':
        create_email_notification(
            notifications_client=client
        )

    if arguments['<call>'] == 'fetch':
        get_notification(
            notifications_client=client
        )

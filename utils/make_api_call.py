"""

Usage:
    utils/make_api_call.py <base_url> <service_id> <secret> <call>

Example:
    ./make_api_call.py http://api my_service super_secret fetch|create
"""

from client.notifications import NotificationsAPIClient
from docopt import docopt


def create_sms_notification(notifications_client):
    mobile_number = input("enter number (+441234123123): ")
    message = input("message: ")
    print(notifications_client.send_sms_notification(mobile_number, message))


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

    if arguments['<call>'] == 'create':
        create_sms_notification(
            notifications_client=client
        )

    if arguments['<call>'] == 'fetch':
        get_notification(
            notifications_client=client
        )

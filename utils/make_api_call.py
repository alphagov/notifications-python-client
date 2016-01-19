"""

Usage:
    utils/make_api_call.py <base_url> <service_id> <secret> <to> <message>

Example:
    ./make_api_call.py http://api my_service super_secret +441234123123 my_message
"""


from client.notifications import NotificationsAPIClient
from docopt import docopt


def make_sms(notifications_client, to, message):
    response = notifications_client.send_sms_notification(to, message)

if __name__ == "__main__":
    arguments = docopt(__doc__)

    client = NotificationsAPIClient(
        arguments['<base_url>'],
        arguments['<service_id>'],
        arguments['<secret>']
    )

    make_sms(
        notifications_client=client,
        to=arguments['<to>'],
        message=arguments['<message>']
    )

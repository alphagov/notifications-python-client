"""

Usage:
    utils/make_api_call.py <base_url> <service_id> <secret> <call>

Example:
    ./make_api_call.py http://api my_service super_secret \
    fetch|fetch-all|create|preview|template|all_templates|template_version|all_template_versions
"""

import json
from notifications_python_client.notifications import NotificationsAPIClient
from docopt import docopt
import sys


def create_notification(notifications_client):
    notification_type = input("enter type email|sms: ")
    if notification_type == 'sms':
        return create_sms_notification(notifications_client)
    if notification_type == 'email':
        return create_email_notification(notifications_client)
    print("Invalid type: {}, exiting".format(notification_type))
    sys.exit(1)


def create_sms_notification(notifications_client):
    mobile_number = input("enter number (+441234123123): ")
    template_id = input("template id: ")
    personalisation = input("personalisation (JSON string):")
    personalisation = personalisation and json.loads(personalisation)
    return notifications_client.send_sms_notification(
        mobile_number, template_id=template_id, personalisation=personalisation
    )


def create_email_notification(notifications_client):
    mobile_number = input("enter email: ")
    template_id = input("template id: ")
    personalisation = input("personalisation (as JSON):") or None
    personalisation = personalisation and json.loads(personalisation)
    return notifications_client.send_email_notification(
        mobile_number, template_id=template_id, personalisation=personalisation
    )


def get_notification(notifications_client):
    id = input("Notification id: ")
    return notifications_client.get_notification_by_id(id)


def get_all_notifications(notifications_client):
    status = input("Notification status: ")
    template_type = input("Notification template type: ")
    include_jobs = input("Include jobs: ")
    return notifications_client.get_all_notifications(status, template_type, include_jobs)


def get_notification_statistics_for_day(notifications_client):
    day = input("Day: ")
    return notifications_client.get_notification_statistics_for_day(day)


def preview_template(notifications_client):
    template_id = input("Template id: ")
    return notifications_client.get_template_preview(template_id)


def get_template(notifications_client):
    template_id = input("Template id: ")
    return notifications_client.get_template(template_id)


def get_all_templates(notifications_client):
    return notifications_client.get_all_templates()


def get_all_template_versions(notifications_client):
    template_id = input("Template id: ")
    return notifications_client.get_all_template_versions(template_id)


def get_template_version(notifications_client):
    template_id = input("Template id: ")
    version = input("Version: ")
    return notifications_client.get_template_version(template_id, version)


if __name__ == "__main__":
    arguments = docopt(__doc__)

    client = NotificationsAPIClient(
        arguments['<base_url>'],
        arguments['<service_id>'],
        arguments['<secret>']
    )

    if arguments['<call>'] == 'create':
        print(create_notification(
            notifications_client=client
        ))

    if arguments['<call>'] == 'fetch':
        print(get_notification(
            notifications_client=client
        ))

    if arguments['<call>'] == 'fetch-all':
        print(get_all_notifications(
            notifications_client=client
        ))

    if arguments['<call>'] == 'statistics':
        print(get_notification_statistics_for_day(
            notifications_client=client
        ))

    if arguments['<call>'] == 'preview':
        print(preview_template(notifications_client=client))

    if arguments['<call>'] == 'template':
        print(get_template(notifications_client=client))

    if arguments['<call>'] == 'all_templates':
        print(get_all_templates(notifications_client=client))

    if arguments['<call>'] == 'template_version':
        print(get_template_version(notifications_client=client))

    if arguments['<call>'] == 'all_template_versions':
        print(get_all_template_versions(notifications_client=client))

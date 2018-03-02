"""

Usage:
    utils/make_api_call.py <base_url> <secret> <call> [options]

Options:
    --type=<sms>
    --to=<07123456789>
    --template=<4051caf5-3c65-4dd3-82d7-31c8c8e82e27>
    --personalisation=<{}>
    --reference=<''>
    --sms_sender_id=<''>
    --filename=<''>

Example:
    ./make_api_call.py http://api my_service super_secret \
    fetch|fetch-all|fetch-generator|create|preview|template|all_templates|template_version|all_template_versions
"""

import json
import sys
from docopt import docopt
from pprint import pprint

from notifications_python_client.notifications import NotificationsAPIClient


def create_notification(notifications_client, **kwargs):
    notification_type = kwargs['--type'] or input(
        "enter type email|sms|letter|precompiled_letter: ")

    if notification_type == 'sms':
        return create_sms_notification(notifications_client, **kwargs)
    if notification_type == 'email':
        return create_email_notification(notifications_client, **kwargs)
    if notification_type == 'letter':
        return create_letter_notification(notifications_client, **kwargs)
    if notification_type == 'precompiled_letter':
        return create_precompiled_letter_notification(notifications_client, **kwargs)
    print("Invalid type: {}, exiting".format(notification_type))
    sys.exit(1)


def create_sms_notification(notifications_client, **kwargs):
    mobile_number = kwargs['--to'] or input("enter number (+441234123123): ")
    template_id = kwargs['--template'] or input("template id: ")
    personalisation = kwargs['--personalisation'] or input("personalisation (JSON string):")
    personalisation = personalisation and json.loads(personalisation)
    reference = kwargs['--reference'] if kwargs['--reference'] is not None else input("reference string for notification: ")  # noqa
    sms_sender_id = kwargs['--sms_sender_id'] or input("sms sender id: ")
    return notifications_client.send_sms_notification(
        mobile_number,
        template_id=template_id,
        personalisation=personalisation,
        reference=reference,
        sms_sender_id=sms_sender_id,
    )


def create_email_notification(notifications_client, **kwargs):
    email_address = kwargs['--to'] or input("enter email: ")
    template_id = kwargs['--template'] or input("template id: ")
    personalisation = kwargs['--personalisation'] or input("personalisation (as JSON):") or None
    personalisation = personalisation and json.loads(personalisation)
    reference = kwargs['--reference'] if kwargs['--reference'] is not None else input("reference string for notification: ")  # noqa
    email_reply_to_id = input("email reply to id:")
    return notifications_client.send_email_notification(
        email_address,
        template_id=template_id,
        personalisation=personalisation,
        reference=reference,
        email_reply_to_id=email_reply_to_id
    )


def create_letter_notification(notifications_client, **kwargs):
    template_id = kwargs['--template'] or input("template id: ")
    personalisation = json.loads(kwargs['--personalisation'] or input("personalisation (as JSON):"))
    reference = kwargs['--reference'] if kwargs['--reference'] is not None else input("reference string for notification: ")  # noqa
    return notifications_client.send_letter_notification(
        template_id=template_id, personalisation=personalisation, reference=reference
    )


def create_precompiled_letter_notification(notifications_client, **kwargs):
    reference = kwargs['--reference'] or input("reference string for notification: ")
    filename = kwargs['--filename'] or input("filename (pdf): ")
    with open(filename, "rb") as pdf_file:
        return notifications_client.send_precompiled_letter_notification(
            reference=reference, pdf_file=pdf_file
        )


def get_notification(notifications_client):
    id = input("Notification id: ")
    return notifications_client.get_notification_by_id(id)


def get_all_notifications_generator(notifications_client):
    status = input("Notification status: ")
    template_type = input("Notification template type: ")
    reference = input("Notification reference: ")
    older_than = input("Older than notification id: ")
    generator = notifications_client.get_all_notifications_iterator(
        status=status,
        template_type=template_type,
        reference=reference,
        older_than=older_than
    )
    return generator


def get_all_notifications(notifications_client):
    status = input("Notification status: ")
    template_type = input("Notification template type: ")
    reference = input("Notification reference: ")
    older_than = input("Older than id: ")
    return notifications_client.get_all_notifications(status=status, template_type=template_type,
                                                      reference=reference, older_than=older_than)


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


if __name__ == "__main__":  # noqa
    arguments = docopt(__doc__)

    client = NotificationsAPIClient(
        base_url=arguments['<base_url>'],
        api_key=arguments['<secret>']
    )

    if arguments['<call>'] == 'create':
        pprint(create_notification(
            notifications_client=client,
            **{k: arguments[k] for k in arguments if k.startswith('--')}
        ))

    if arguments['<call>'] == 'fetch':
        pprint(get_notification(
            notifications_client=client
        ))

    if arguments['<call>'] == 'fetch-all':
        pprint(get_all_notifications(
            notifications_client=client
        ))

    if arguments['<call>'] == 'fetch-generator':
        pprint(list(get_all_notifications_generator(
            notifications_client=client
        )))

    if arguments['<call>'] == 'preview':
        pprint(preview_template(notifications_client=client))

    if arguments['<call>'] == 'template':
        pprint(get_template(notifications_client=client))

    if arguments['<call>'] == 'all_templates':
        pprint(get_all_templates(notifications_client=client))

    if arguments['<call>'] == 'template_version':
        pprint(get_template_version(notifications_client=client))

    if arguments['<call>'] == 'all_template_versions':
        pprint(get_all_template_versions(notifications_client=client))

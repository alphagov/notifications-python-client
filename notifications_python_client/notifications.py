from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
import logging
import re

from notifications_python_client.base import BaseAPIClient

logger = logging.getLogger(__name__)


class NotificationsAPIClient(BaseAPIClient):
    def send_sms_notification(self, phone_number, template_id, personalisation=None, reference=None,
                              scheduled_for=None):
        notification = {
            "phone_number": phone_number,
            "template_id": template_id
        }
        if personalisation:
            notification.update({'personalisation': personalisation})
        if reference:
            notification.update({'reference': reference})
        if scheduled_for:
            notification.update({'scheduled_for': scheduled_for})

        return self.post(
            '/v2/notifications/sms',
            data=notification)

    def send_email_notification(self, email_address, template_id, personalisation=None, reference=None,
                                scheduled_for=None):
        notification = {
            "email_address": email_address,
            "template_id": template_id
        }
        if personalisation:
            notification.update({'personalisation': personalisation})
        if reference:
            notification.update({'reference': reference})
        if scheduled_for:
            notification.update({'scheduled_for': scheduled_for})
        return self.post(
            '/v2/notifications/email',
            data=notification)

    def get_notification_by_id(self, id):
        return self.get('/v2/notifications/{}'.format(id))

    def get_all_notifications(self, status=None, template_type=None, reference=None, older_than=None):
        data = {}
        if status:
            data.update({'status': status})
        if template_type:
            data.update({'template_type': template_type})
        if reference:
            data.update({'reference': reference})
        if older_than:
            data.update({'older_than': older_than})
        return self.get(
            '/v2/notifications',
            params=data
        )

    def get_all_notifications_iterator(self, status=None, template_type=None, reference=None, older_than=None):
        result = self.get_all_notifications(status, template_type, reference, older_than)
        notifications = result.get('notifications')
        while notifications:
            for notification in notifications:
                yield notification
            next_link = result['links'].get('next')
            notification_id = re.search("[0-F]{8}-[0-F]{4}-[0-F]{4}-[0-F]{4}-[0-F]{12}", next_link, re.I).group(0)
            result = self.get_all_notifications(status, template_type, reference, notification_id)
            notifications = result.get('notifications')

    def get_notification_statistics_for_day(self, day=None):
        data = {}
        if day:
            data.update({'day': day})
        return self.get(
            '/notifications/statistics',
            params=data
        )

    def post_template_preview(self, template_id, personalisation):
        template = {
            "personalisation": personalisation
        }
        return self.post('/v2/template/{}/preview'.format(template_id), data=template)

    def get_template(self, template_id):
        return self.get('/v2/template/{}'.format(template_id))

    def get_template_version(self, template_id, version):
        return self.get('/v2/template/{}/version/{}'.format(template_id, version))

    def get_all_template_versions(self, template_id):
        return self.get('service/{}/template/{}/versions'.format(self.service_id, template_id))

    def get_all_templates(self, template_type=None):
        _template_type = '?type={}'.format(template_type) if template_type else ''

        return self.get('/v2/templates{}'.format(_template_type))

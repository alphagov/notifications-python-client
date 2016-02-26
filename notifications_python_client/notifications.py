from notifications_python_client.base import BaseAPIClient


class NotificationsAPIClient(BaseAPIClient):
    def send_sms_notification(self, to, template_id=None):
        notification = {
            "to": to,
            "template": template_id
        }
        return self.post(
            '/notifications/sms',
            data=notification)

    def send_email_notification(self, to, template_id):
        notification = {
            "to": to,
            "template": template_id
        }
        return self.post(
            '/notifications/email',
            data=notification)

    def get_notification_by_id(self, id):
        return self.get('/notifications/{}'.format(id))

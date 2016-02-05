from notifications_python_client.base import BaseAPIClient


class NotificationsAPIClient(BaseAPIClient):
    def send_sms_notification(self, to, template_id=None, content=None):
        notification = {"to": to}
        if template_id:
            notification.update({
                "template": template_id
            })
        if content:
            notification.update({
                "content": content
            })
        return self.post(
            '/notifications/sms',
            data=notification)

    def send_email_notification(self, to, message, from_, subject):
        notification = {}
        notification.update({
            "to": to,
            "from": from_,
            "subject": subject,
            "message": message
        })
        return self.post(
            '/notifications/email',
            data=notification)

    def get_notification_by_id(self, id):
        return self.get('/notifications/{}'.format(id))

from client.base import BaseAPIClient


class NotificationsAPIClient(BaseAPIClient):
    def send_sms_notification(self, to, message):
        notification = {}
        notification.update({
            "to": to,
            "message": message
        })

        return self.post(
            '/notifications/sms',
            data={
                "notification": notification
            })

    def get_notification(self, id):
        return self.get('/notifications/{}'.format(id))

    def get_service(self, service_id, *params):
        """
        Retrieve a service.
        """
        return self.get(
            '/service/{0}'.format(service_id))

    def get_services(self, *params):
        """
        Retrieve a list of services.
        """
        return self.get('/service', *params)

    def get_service_template(self, service_id, template_id, *params):
        """
        Retrieve a service template.
        """
        endpoint = '/service/{service_id}/template/{template_id}'.format(
            service_id=service_id,
            template_id=template_id)
        return self.get(endpoint, *params)

    def get_service_templates(self, service_id, *params):
        """
        Retrieve all templates for service.
        """
        endpoint = '/service/{service_id}/template'.format(
            service_id=service_id)
        return self.get(endpoint, *params)

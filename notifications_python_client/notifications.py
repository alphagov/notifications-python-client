import base64
import logging
import re
from io import BytesIO

from notifications_python_client.base import BaseAPIClient

logger = logging.getLogger(__name__)


class NotificationsAPIClient(BaseAPIClient):
    def send_sms_notification(
        self, phone_number, template_id, personalisation=None, reference=None, sms_sender_id=None
    ):
        notification = {"phone_number": phone_number, "template_id": template_id}
        if personalisation:
            notification.update({"personalisation": personalisation})
        if reference:
            notification.update({"reference": reference})
        if sms_sender_id:
            notification.update({"sms_sender_id": sms_sender_id})
        return self.post("/v2/notifications/sms", data=notification)

    def send_email_notification(
        self,
        email_address,
        template_id,
        personalisation=None,
        reference=None,
        email_reply_to_id=None,
        one_click_unsubscribe_url=None,
    ):
        notification = {"email_address": email_address, "template_id": template_id}
        if personalisation:
            notification.update({"personalisation": personalisation})
        if reference:
            notification.update({"reference": reference})
        if email_reply_to_id:
            notification.update({"email_reply_to_id": email_reply_to_id})
        if one_click_unsubscribe_url:
            notification.update({"one_click_unsubscribe_url": one_click_unsubscribe_url})

        return self.post("/v2/notifications/email", data=notification)

    def send_letter_notification(self, template_id, personalisation, reference=None):
        notification = {"template_id": template_id, "personalisation": personalisation}
        if reference:
            notification.update({"reference": reference})
        return self.post("/v2/notifications/letter", data=notification)

    def send_precompiled_letter_notification(self, reference, pdf_file, postage=None):
        content = base64.b64encode(pdf_file.read()).decode("utf-8")
        notification = {"reference": reference, "content": content}

        if postage:
            notification["postage"] = postage

        return self.post("/v2/notifications/letter", data=notification)

    def get_received_texts(self, older_than=None):
        if older_than:
            query_string = f"?older_than={older_than}"
        else:
            query_string = ""

        return self.get(f"/v2/received-text-messages{query_string}")

    def get_received_texts_iterator(self, older_than=None):
        result = self.get_received_texts(older_than=older_than)
        received_texts = result.get("received_text_messages")
        while received_texts:
            yield from received_texts
            next_link = result["links"].get("next")
            received_text_id = re.search("[0-F]{8}-[0-F]{4}-[0-F]{4}-[0-F]{4}-[0-F]{12}", next_link, re.I).group(0)
            result = self.get_received_texts(older_than=received_text_id)
            received_texts = result.get("received_text_messages")

    def get_notification_by_id(self, id):
        return self.get(f"/v2/notifications/{id}")

    def get_pdf_for_letter(self, id):
        url = f"/v2/notifications/{id}/pdf"
        logger.debug("API request %s %s", "GET", url)
        url, kwargs = self._create_request_objects(url, data=None, params=None)

        response = self._perform_request("GET", url, kwargs)

        return BytesIO(response.content)

    def get_all_notifications(
        self, status=None, template_type=None, reference=None, older_than=None, include_jobs=None
    ):
        data = {}
        if status:
            data.update({"status": status})
        if template_type:
            data.update({"template_type": template_type})
        if reference:
            data.update({"reference": reference})
        if older_than:
            data.update({"older_than": older_than})
        if include_jobs:
            data.update({"include_jobs": include_jobs})
        return self.get("/v2/notifications", params=data)

    def get_all_notifications_iterator(self, status=None, template_type=None, reference=None, older_than=None):
        result = self.get_all_notifications(status, template_type, reference, older_than)
        notifications = result.get("notifications")
        while notifications:
            yield from notifications
            next_link = result["links"].get("next")
            notification_id = re.search("[0-F]{8}-[0-F]{4}-[0-F]{4}-[0-F]{4}-[0-F]{12}", next_link, re.I).group(0)
            result = self.get_all_notifications(status, template_type, reference, notification_id)
            notifications = result.get("notifications")

    def post_template_preview(self, template_id, personalisation):
        template = {"personalisation": personalisation}
        return self.post(f"/v2/template/{template_id}/preview", data=template)

    def get_template(self, template_id):
        return self.get(f"/v2/template/{template_id}")

    def get_template_version(self, template_id, version):
        return self.get(f"/v2/template/{template_id}/version/{version}")

    def get_all_template_versions(self, template_id):
        return self.get(f"service/{self.service_id}/template/{template_id}/versions")

    def get_all_templates(self, template_type=None):
        _template_type = f"?type={template_type}" if template_type else ""

        return self.get(f"/v2/templates{_template_type}")

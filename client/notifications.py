from client.base import BaseAPIClient


class NotificationsAPIClient(BaseAPIClient):

    def test_get(self):
        return self.get("/")

    def test_post(self):
        return self.post(
            "/",
            data={
                "a": "b"
            }
        )

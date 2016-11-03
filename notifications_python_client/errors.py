REQUEST_ERROR_STATUS_CODE = 503
REQUEST_ERROR_MESSAGE = "Request failed"


class TokenError(Exception):

    def __init__(self, message, token=None):
        self.message = message
        self.token = token


class TokenDecodeError(TokenError):
    def __init__(self, message=None):
        super().__init__(message or 'Invalid token: signature')


class TokenExpiredError(TokenError):
    pass


class TokenIssuerError(TokenDecodeError):
    def __init__(self):
        super().__init__('Invalid token: iss field not provided')


class TokenIssuedAtError(TokenDecodeError):
    def __init__(self):
        super().__init__('Invalid token: iat field not provided')


class APIError(Exception):
    def __init__(self, response=None, message=None):
        self.response = response
        self._message = message

    def __str__(self):
        return "{} - {}".format(self.status_code, self.message)

    @property
    def message(self):
        try:
            return self.response.json()['message']
        except (TypeError, ValueError, AttributeError, KeyError):
            return self._message or REQUEST_ERROR_MESSAGE

    @property
    def status_code(self):
        try:
            return self.response.status_code
        except AttributeError:
            return REQUEST_ERROR_STATUS_CODE


class HTTPError(APIError):
    @staticmethod
    def create(e):
        error = HTTPError(e.response)
        if error.status_code == 503:
            error = HTTP503Error(e.response)
        return error


class HTTP503Error(HTTPError):
    """Specific instance of HTTPError for 503 errors

    Used for detecting whether failed requests should be retried.
    """
    pass


class InvalidResponse(APIError):
    pass

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import super
from future import standard_library
standard_library.install_aliases()

REQUEST_ERROR_STATUS_CODE = 503
REQUEST_ERROR_MESSAGE = "Request failed"

TOKEN_ERROR_GUIDANCE = "See our requirements for JSON Web Tokens at https://docs.notifications.service.gov.uk/rest-api.html#authorisation-header"  # noqa
TOKEN_ERROR_DEFAULT_ERROR_MESSAGE = "Invalid token: " + TOKEN_ERROR_GUIDANCE


class TokenError(Exception):

    def __init__(self, message=None, token=None):
        self.message = message + ". " + TOKEN_ERROR_GUIDANCE if message else TOKEN_ERROR_DEFAULT_ERROR_MESSAGE
        self.token = token


class TokenExpiredError(TokenError):
    pass


class TokenAlgorithmError(TokenError):
    def __init__(self):
        super().__init__('Invalid token: algorithm used is not HS256')


class TokenDecodeError(TokenError):
    def __init__(self, message=None):
        super().__init__(message or 'Invalid token: signature')


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
            return self.response.json().get('message', self.response.json().get('errors'))
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

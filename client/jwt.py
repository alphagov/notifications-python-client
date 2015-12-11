import jwt
import hashlib
import hmac
import calendar
import time
import base64


def create_signature(original, secret_key):
    """
    Perform signing of object
    HMAC signature, using provided key
    SHA256 hashing algorithm

    :param original: String to sign
    :param secret_key: Signing secret
    :return: Base64 representation of signature
    """
    return base64.b64encode(
        hmac.new(
            secret_key.encode(),
            original.encode(),
            digestmod=hashlib.sha256
        ).digest()
    )


def create_jwt_token(request_method, request_path, secret_key, client_id, request_body):
    """
    Create JWT token for GOV.UK Notify

    Tokens have standard header:
    {
        "typ": "JWT",
        "alg": "HS256"
    }

    Claims consist of:
    iss: identifier for the client
    iat: issued at in epoch seconds (UTC)
    req: signed request, of the format METHOD PATH. Example POST /resource
    pay: signed payload. Must be the exact value as placed in to request, after any serialization.

    :param request_method: Method of request [GET|POST|etc]
    :param request_path: Path to requested resource
    :param secret_key: Application signing secret
    :param client_id: Identifier for the client
    :param request_body: Serialized request body, not required. If no request body claim is not set
    :return: JWT token for this request
    """

    assert request_method, "Missing request method"
    assert request_path, "Missing request path"
    assert secret_key, "Missing secret key"
    assert client_id, "Missing client id"

    # Format request for signing METHOD *space* RESOURCE
    request = "{} {}".format(request_method, request_path)

    signed_url = create_signature(request, secret_key)

    headers = {
        "typ": "JWT",
        "alg": "HS256"
    }

    claims = {
        'iss': client_id,
        'iat': calendar.timegm(time.gmtime()),
        'req': signed_url.decode()
    }

    if request_body:
        claims.update({
            'pay': create_signature(request_body, secret_key).decode()
        })

    return jwt.encode(payload=claims, key=secret_key, headers=headers).decode()

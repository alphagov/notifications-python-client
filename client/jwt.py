import jwt
import hashlib
import hmac
import calendar
import time
import base64
from client.errors import TokenDecodeError, TokenExpiredError, TokenRequestError, TokenPayloadError

__algorithm__ = "HS256"
__type__ = "JWT"
__bound__ = 5


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


def create_jwt_token(request_method, request_path, secret, client_id, request_body):
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
    assert secret, "Missing secret key"
    assert client_id, "Missing client id"

    # Format request for signing METHOD *space* RESOURCE
    signed_url = create_signed_request(request_method, request_path, secret)

    headers = {
        "typ": __type__,
        "alg": __algorithm__
    }

    claims = {
        'iss': client_id,
        'iat': epoch_seconds(),
        'req': signed_url.decode()
    }

    if request_body:
        claims.update({
            'pay': create_signature(request_body, secret).decode()
        })

    return jwt.encode(payload=claims, key=secret, headers=headers).decode()


def get_token_issuer(token):
    """
    Issuer of a token is the identifier used to recover the secret
    Need to extract this from token to ensure we can proceed to the signature validation stage
    Does not check validity of the token
    :param token: signed JWT token
    :return issuer: iss field of the JWT token
    :raises AssertionError: is iss field not present
    """
    unverified = decode_token(token)
    assert 'iss' in unverified
    return unverified['iss']


def decode_jwt_token(token, secret, request_method, request_path, request_payload=None):
    """
    Validates and decodes the JWT token
    Token checked for
        - signature of JWT token
        - token issued date is valid
        - token request path is valid
        - token request payload is valid [optional]

    :param token: jwt token
    :param secret: client specific secret
    :param request_method: HTTP method for the request
    :param request_path: Resource path for the request
    :param request_payload: Body of the request
    :return boolean: True if valid token, False otherwise
    :raises AssertionError: If any required fields are not present
    :raises jwt.DecodeError: If signature validation fails
    """
    try:
        # check signature of the token
        decoded_token = jwt.decode(token, key=secret.encode(), verify=True, algorithms=[__algorithm__])

        # token has all the required fields
        assert 'iss' in decoded_token, 'Missing iss field in token'
        assert 'iat' in decoded_token, 'Missing iat field in token'
        assert 'req' in decoded_token, 'Missing req field in token'
        if request_payload is not None:
            assert 'pay' in decoded_token, 'Missing pay field in token'

        # check iat time is within bounds
        now = epoch_seconds()
        iat = int(decoded_token['iat'])

        if now > (iat + __bound__):
            raise TokenExpiredError("Token has expired", decoded_token)

        # check request
        if decoded_token['req'] != create_signed_request(request_method, request_path, secret).decode():
            raise TokenRequestError("Token has invalid request", decoded_token)

        # check request payload
        if request_payload:
            if decoded_token['pay'] != create_signature(request_payload, secret).decode():
                raise TokenPayloadError("Token has an invalid payload", decoded_token)

        return True
    except jwt.InvalidIssuedAtError:
        raise TokenExpiredError("Token has invalid iat field", decode_token(token))
    except jwt.DecodeError:
        raise TokenDecodeError("Invalid token")


def decode_token(token):
    """
    Decode token but don;t check the signature
    :param token:
    :return decoded token:
    """
    return jwt.decode(token, verify=False, algorithms=[__algorithm__])


def create_signed_request(request_method, request_path, secret):
    return create_signature(
        "{} {}".format(request_method, request_path),
        secret
    )


def epoch_seconds():
    return calendar.timegm(time.gmtime())

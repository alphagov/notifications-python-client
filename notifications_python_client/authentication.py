from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import int
from future import standard_library
standard_library.install_aliases()
import calendar
import time

import jwt

from notifications_python_client.errors import (
    TokenDecodeError,
    TokenExpiredError,
    TokenIssuerError,
    TokenIssuedAtError
)

__algorithm__ = "HS256"
__type__ = "JWT"
__bound__ = 30


def create_jwt_token(secret, client_id):
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

    :param secret: Application signing secret
    :param client_id: Identifier for the client
    :return: JWT token for this request
    """
    assert secret, "Missing secret key"
    assert client_id, "Missing client id"

    headers = {
        "typ": __type__,
        "alg": __algorithm__
    }

    claims = {
        'iss': client_id,
        'iat': epoch_seconds()
    }

    return jwt.encode(payload=claims, key=secret, headers=headers).decode()


def get_token_issuer(token):
    """
    Issuer of a token is the identifier used to recover the secret
    Need to extract this from token to ensure we can proceed to the signature validation stage
    Does not check validity of the token
    :param token: signed JWT token
    :return issuer: iss field of the JWT token
    :raises TokenIssuerError: if iss field not present
    :raises TokenDecodeError: if token does not conform to JWT spec
    """
    try:
        unverified = decode_token(token)

        if 'iss' not in unverified:
            raise TokenIssuerError

        return unverified.get('iss')
    except jwt.DecodeError:
        raise TokenDecodeError


def decode_jwt_token(token, secret):
    """
    Validates and decodes the JWT token
    Token checked for
        - signature of JWT token
        - token issued date is valid

    :param token: jwt token
    :param secret: client specific secret
    :return boolean: True if valid token, False otherwise
    :raises TokenIssuerError: if iss field not present
    :raises TokenIssuedAtError: if iat field not present
    :raises jwt.DecodeError: If signature validation fails
    """
    try:
        # check signature of the token
        decoded_token = jwt.decode(
            token,
            key=secret.encode(),
            verify=True,
            algorithms=[__algorithm__],
            leeway=__bound__
        )
        # token has all the required fields
        if 'iss' not in decoded_token:
            raise TokenIssuerError
        if 'iat' not in decoded_token:
            raise TokenIssuedAtError

        # check iat time is within bounds
        now = epoch_seconds()
        iat = int(decoded_token['iat'])
        if now > (iat + __bound__):
            raise TokenExpiredError("Token has expired", decoded_token)
        if iat > (now + __bound__):
            raise TokenExpiredError("Token can not be in the future", decoded_token)

        return True
    except jwt.InvalidIssuedAtError:
        raise TokenExpiredError("Token has invalid iat field", decode_token(token))
    except jwt.DecodeError:
        raise TokenDecodeError


def decode_token(token):
    """
    Decode token but don;t check the signature
    :param token:
    :return decoded token:
    """
    return jwt.decode(token, verify=False, algorithms=[__algorithm__])


def epoch_seconds():
    return calendar.timegm(time.gmtime())

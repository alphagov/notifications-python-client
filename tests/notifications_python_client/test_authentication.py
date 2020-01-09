from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import str
from future import standard_library
standard_library.install_aliases()
import calendar
import time

import jwt
import pytest
import mock
from freezegun import freeze_time

from notifications_python_client.authentication import (
    create_jwt_token, decode_jwt_token, get_token_issuer)
from notifications_python_client.errors import (
    TokenExpiredError,
    TokenDecodeError,
    TokenIssuerError,
    TokenIssuedAtError,
    TokenAlgorithmError,
    TokenError,
    TOKEN_ERROR_DEFAULT_ERROR_MESSAGE,
)


# helper method to directly decode token
def decode_token(token, secret):
    return jwt.decode(token, key=secret.encode(), verify=True, algorithms=['HS256'])


def test_should_reject_token_request_if_missing_secret():
    with pytest.raises(AssertionError) as err:
        create_jwt_token(secret=None, client_id="client_id")
    assert str(err.value) == "Missing secret key"


def test_should_reject_token_request_if_missing_client_id():
    with pytest.raises(AssertionError) as err:
        create_jwt_token("key", None)
    assert str(err.value) == "Missing client id"


def test_token_should_contain_correct_headers():
    token = create_jwt_token("key", "client_id")
    headers = jwt.get_unverified_header(token)
    assert headers['typ'] == 'JWT'
    assert headers['alg'] == 'HS256'


def test_token_should_fail_to_decode_if_wrong_key():
    token = create_jwt_token("key", "client_id")
    with pytest.raises(jwt.DecodeError) as err:
        decode_token(token, "wrong key")
    assert str(err.value) == "Signature verification failed"


@pytest.mark.parametrize('exception_class', [
    jwt.InvalidAudienceError,
    jwt.ImmatureSignatureError,
    jwt.InvalidIssuerError,
    jwt.ExpiredSignatureError,

])
@mock.patch('notifications_python_client.authentication.jwt.decode')
def test_decode_jwt_token_raises_token_error_if_jwt_invalid_token_error_exception(decode_mock, exception_class):
    token = create_jwt_token("key", "client_id")
    decode_mock.side_effect = exception_class

    with pytest.raises(TokenError) as err:
        decode_jwt_token(token, "key")

    assert str(err.value.message) == TOKEN_ERROR_DEFAULT_ERROR_MESSAGE


def test_token_should_contain_correct_claim_keys():
    token = create_jwt_token("key", "client_id")
    decoded = decode_token(token, "key")
    assert 'iss' in decoded
    assert "client_id" == decoded['iss']
    assert 'iat' in decoded
    assert 'req' not in decoded
    assert 'pay' not in decoded


@freeze_time("2020-01-01 00:00:00")
def test_token_should_contain_correct_issued_at_claim():
    token = create_jwt_token("key", "client_id")
    decoded = decode_token(token, "key")
    assert decoded['iat'] == calendar.timegm(time.gmtime())


def test_should_reject_token_with_invalid_key():
    token = create_jwt_token("key", "client_id")
    with pytest.raises(TokenDecodeError) as e:
        decode_jwt_token(token=token, secret="wrong-key")

    assert "Invalid token: signature. See our requirements" in e.value.message


def test_should_reject_token_that_is_too_old():
    # make token 31 seconds ago
    with freeze_time('2001-01-01T12:00:00'):
        token = create_jwt_token("key", "client_id")

    with freeze_time('2001-01-01T12:00:31'), pytest.raises(TokenExpiredError) as e:
        decode_jwt_token(token, "key")

    assert "Token has expired. See our requirements" in e.value.message
    assert e.value.token['iss'] == "client_id"


def test_should_reject_token_that_is_just_out_of_bounds_future():
    # make token 31 seconds ago
    with freeze_time('2001-01-01T12:00:31'):
        token = create_jwt_token("key", "client_id")

    with freeze_time('2001-01-01T12:00:00'), pytest.raises(TokenExpiredError) as e:
        decode_jwt_token(token, "key")

    assert "Token can not be in the future. See our requirements" in e.value.message
    assert e.value.token['iss'] == "client_id"


def test_should_accept_token_that_just_within_bounds_old():
    # make token 31 seconds ago
    with freeze_time('2001-01-01T12:00:00'):
        token = create_jwt_token("key", "client_id")

    with freeze_time('2001-01-01T12:00:30'):
        assert decode_jwt_token(token, "key")


def test_should_accept_token_that_is_just_within_bounds_future():
    # make token 30 seconds in the future
    with freeze_time('2001-01-01T12:00:30'):
        token = create_jwt_token("key", "client_id")

    with freeze_time('2001-01-01T12:00:00'):
        assert decode_jwt_token(token, "key")


def test_should_handle_random_inputs():
    with pytest.raises(TokenDecodeError) as e:
        decode_jwt_token("token", "key")

    assert "Invalid token: signature. See our requirements" in e.value.message


def test_should_handle_invalid_token_for_issuer_lookup():
    with pytest.raises(TokenDecodeError) as e:
        get_token_issuer("token")

    assert "Invalid token: signature. See our requirements" in e.value.message


def test_get_token_issuer_should_handle_invalid_token_with_no_iss():
    token = create_jwt_token("key", "client_id")
    token = jwt.encode(
        payload={'iat': 1234},
        key='1234',
        headers={'typ': 'JWT', 'alg': 'HS256'}
    ).decode()

    with pytest.raises(TokenIssuerError) as e:
        get_token_issuer(token)

    assert "Invalid token: iss field not provided. See our requirements" in e.value.message


@pytest.mark.parametrize('missing_field,exception_class', [
    ('iss', TokenIssuerError),
    ('iat', TokenIssuedAtError),
])
def test_decode_should_handle_invalid_token_with_missing_field(missing_field, exception_class):
    payload = {'iss': '1234', 'iat': '1234'}
    payload.pop(missing_field)
    token = jwt.encode(
        payload=payload,
        key='bar',
        headers={'typ': 'JWT', 'alg': 'HS256'}
    )

    with pytest.raises(exception_class):
        decode_jwt_token(token, 'bar')


def test_decode_should_handle_invalid_token_with_non_hs256_algorithm():
    payload = {'iss': '1234', 'iat': '1234'}
    token = jwt.encode(
        payload=payload,
        key='bar',
        headers={'typ': 'JWT', 'alg': 'HS512'}
    )

    with pytest.raises(TokenAlgorithmError) as e:
        decode_jwt_token(token, 'bar')

    assert "Invalid token: algorithm used is not HS256. See our requirements" in e.value.message


def test_should_return_issuer_from_token():
    token = create_jwt_token("key", "client_id")

    issuer = get_token_issuer(token)

    assert issuer == "client_id"

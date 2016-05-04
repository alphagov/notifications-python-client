import calendar
import time
from datetime import datetime, timedelta

import jwt
import pytest
from freezegun import freeze_time

from notifications_python_client.authentication import (
    create_jwt_token, decode_jwt_token, get_token_issuer)
from notifications_python_client.errors import (
    TokenExpiredError, TokenDecodeError)


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
        assert decode_jwt_token(token=token, secret="wrong-key")

    assert e.value.message == "Invalid token"


def test_should_reject_token_that_is_old():
    # make token 31 seconds ago
    thirty_one_seconds_in_past = datetime.utcnow() - timedelta(seconds=31)
    freezer = freeze_time(thirty_one_seconds_in_past)
    freezer.start()
    token = create_jwt_token(secret="key", client_id="client_id")
    freezer.stop()

    with pytest.raises(TokenExpiredError) as e:
        assert decode_jwt_token(token, "key")

    assert e.value.token['iss'] == "client_id"


def test_should_reject_token_that_is_in_future():
    # make token 31 seconds ago
    thirty_one_seconds_in_future = datetime.utcnow() + timedelta(seconds=31)
    freezer = freeze_time(thirty_one_seconds_in_future)
    freezer.start()
    token = create_jwt_token("key", "client_id")
    freezer.stop()

    with pytest.raises(TokenExpiredError) as e:
        assert decode_jwt_token(token, "key")

    assert e.value.token['iss'] == "client_id"


def test_should_reject_token_that_just_within_bounds_old():
    # make token 31 seconds ago
    thirty_one_seconds_in_past = datetime.utcnow() - timedelta(seconds=30)
    freezer = freeze_time(thirty_one_seconds_in_past)
    freezer.start()
    token = create_jwt_token("key", "client_id")
    freezer.stop()

    assert decode_jwt_token(token, "key")


def test_should_reject_token_that_is_just_within_bounds_future():
    # make token 31 seconds ago
    thirty_one_seconds_in_future = datetime.utcnow() + timedelta(seconds=30)
    freezer = freeze_time(thirty_one_seconds_in_future)
    freezer.start()
    token = create_jwt_token("key", "client_id")
    freezer.stop()

    assert decode_jwt_token(token, "key")


def test_should_handle_random_inputs():
    with pytest.raises(TokenDecodeError) as e:
        assert decode_jwt_token("token", "key")

    assert e.value.message == "Invalid token"


def test_should_handle_invalid_token_for_issuer_lookup():
    with pytest.raises(TokenDecodeError) as e:
        assert get_token_issuer("token")

    assert e.value.message == "Invalid token"


def test_should_return_issuer_from_token():
    token = create_jwt_token("key", "client_id")

    issuer = get_token_issuer(token)

    assert issuer == "client_id"

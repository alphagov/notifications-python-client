import pytest


def test_get_behaves_as_expected(notifications_client, rmock):
    rmock.request(
        "GET",
        "http://test-host/",
        json={"result": "success"},
        status_code=200)

    result = notifications_client.test_get()

    assert rmock.called
    assert result == {'result': 'success'}


def test_post_behaves_as_expected(notifications_client, rmock):
    rmock.request(
        "POST",
        "http://test-host/",
        json={"result": "success"},
        status_code=200)

    result = notifications_client.test_post()

    assert rmock.called
    assert result == {'result': 'success'}

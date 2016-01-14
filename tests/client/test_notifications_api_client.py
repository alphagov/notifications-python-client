from ..conftest import TEST_HOST


def test_get_behaves_as_expected(notifications_client, rmock):
    rmock.request(
        "GET",
        TEST_HOST,
        json={"result": "success"},
        status_code=200)

    result = notifications_client.test_get()

    assert rmock.called
    assert result == {'result': 'success'}


def test_post_behaves_as_expected(notifications_client, rmock):
    rmock.request(
        "POST",
        TEST_HOST,
        json={"result": "success"},
        status_code=200)

    result = notifications_client.test_post()

    assert rmock.called
    assert result == {'result': 'success'}

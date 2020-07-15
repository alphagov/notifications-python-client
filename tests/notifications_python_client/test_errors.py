import mock

import pytest

from notifications_python_client.errors import HTTPError


@pytest.fixture
def make_mock_response():
    def factory(*, json, status_code):
        response = mock.Mock()
        response.json.return_value = json
        response.status_code = status_code
        return response

    return factory


@pytest.mark.parametrize('json, errors', (
    (
        {'errors': [{'error': 'AuthError', 'message': 'Invalid token: API key not found'}]},
        [{'error': 'AuthError', 'message': 'Invalid token: API key not found'}]
    ),
    (
        {'message': 'The requested URL was not found on the server'},
        [{'message': 'The requested URL was not found on the server'}]
    ),
    (
        None,
        [{'message': 'Request failed'}]
    )
))
def test_errors_is_list_of_objects(make_mock_response, json, errors):
    error = HTTPError(response=make_mock_response(
        json=json,
        status_code=400,
    ))

    assert len(error.errors)
    assert error.errors == errors


@pytest.mark.parametrize('json, error_message', (
    (
        {'errors': [{'error': 'AuthError', 'message': 'Invalid token: API key not found'}]},
        'Invalid token: API key not found'
    ),
    (
        {'message': 'The requested URL was not found on the server'},
        'The requested URL was not found on the server'
    ),
    (
        None,
        'Request failed'
    ),
))
def test_error_message_is_a_string(make_mock_response, json, error_message):
    error = HTTPError(response=make_mock_response(
        json=json,
        status_code=400,
    ))

    assert isinstance(error.error_message, str)
    assert error.error_message == error_message

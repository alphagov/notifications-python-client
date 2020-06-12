# Contributing

Pull requests welcome.

## Working on the client locally

This is a Python codebase, written to support Python 2 and 3.

If you’re using OS X and don’t have Python installed, run this command:
```shell
    brew install python3
```

## Dependency management

This is done through [pip](pip.readthedocs.org/) and
[virtualenv](https://virtualenv.readthedocs.org/en/latest/).
We recommend using [VirtualEnvWrapper](http://virtualenvwrapper.readthedocs.org/en/latest/command_ref.html).

Setting up a Virtualenv for python3

```shell
    mkvirtualenv -p /usr/local/bin/python3 notifications-python-client
```

Install the dependencies
```python
    python setup.py develop
```

## Tests

The `./scripts/run_tests.py` script will run all the tests.
[`py.test`](http://pytest.org/latest/) is used for testing.

Running the script will also check for conformance with
[`flake8`](https://pypi.org/project/flake8/).

Additionally code coverage is checked via `pytest-cov`.

## Integration tests

Before running tests please ensure that the environment variables are set up for the integration test.

```
NOTIFY_API_URL "https://example.notify-api.url"
API_KEY "example_API_test_key"
FUNCTIONAL_TEST_NUMBER "valid mobile number"
FUNCTIONAL_TEST_EMAIL "valid email address"
EMAIL_TEMPLATE_ID "valid email_template_id"
SMS_TEMPLATE_ID "valid sms_template_id"
LETTER_TEMPLATE_ID "valid letter_template_id"
EMAIL_REPLY_TO_ID "valid email reply to id"
SMS_SENDER_ID "valid sms_sender_id - to test sending to a receiving number, so needs to be a valid number"
API_SENDING_KEY "API_team_key for sending an SMS to a receiving number"
INBOUND_SMS_QUERY_KEY "API_test_key to get received text messages - leave blank for local development as cannot test locally"
```

The `./scripts/run_integration_tests.py` script will run the integration tests.
The integration tests will test the contract of the response to all the api calls,
ensuring the latest version of notifications-api do not break the contract of the notifications-python-client.

## Command line tool

Use this to test the client without having to create an application.

```
    PYTHONPATH=. python /utils/make_api_call.py <base_api_url> <api_key> [fetch|create]
```

This will use the API referred to in the base_api_url argument to send a text message.

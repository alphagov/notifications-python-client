# Contributing

Pull requests welcome.

## Working on the client locally

This is a Python codebase, written to support Python 3 only.

## Tests

The `./scripts/run_tests.py` script will run all the tests.
[`py.test`](http://pytest.org/latest/) is used for testing.

Running the script will also check for conformance with
[`flake8`](https://pypi.org/project/flake8/).

Additionally code coverage is checked via `pytest-cov`.

### tox

We use tox to ensure code works on all versions of python. You can run this using docker by calling:

```sh
make tox-with-docker
```

If you wish to run tox locally, you'll need to install a variety of
python versions. You should use [`pyenv`](https://github.com/pyenv/pyenv) for this.

You'll first want to install the latest versions of each minor python version. You'll need to use `pyenv install --list`
to see available versions

```sh
while read line; do pyenv install "$line" < /dev/null; done < .python-version
```

Then you'll need to install tox.
```sh
pip install tox
```

Then you can run `tox` to run the tests against each version of python.


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

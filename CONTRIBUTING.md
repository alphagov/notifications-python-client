# Contributing

Pull requests welcome.

This is a Python codebase, written to support Python 3 only.

## Setting Up

### Docker container

This app uses dependencies that are difficult to install locally. In order to make local development easy, we run app commands through a Docker container. Run the following to set this up:

```shell
make bootstrap-with-docker
```

Because the container caches things like packages, you will need to run this again if you change the package versions.

## Tests

There are unit and integration tests that can be run to test functionality of the client.

### Unit tests

To run the unit tests:

```
make test-with-docker
```

### tox

We use tox to ensure code works on all versions of python. You can run this using docker by calling:

```sh
make tox-with-docker
```

Because tox caches installed packages, you may need to run `rm -rf .tox` if you change package versions.

### Integration tests

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

To run the integration tests:

```
make integration-test-with-docker
```

## Running the client locally

If you wish to run tox locally, you'll need to install a variety of python versions. You should use [`pyenv`](https://github.com/pyenv/pyenv) for this.

```sh
while read line; do pyenv install "$line" < /dev/null; done < tox-python-versions
```

You may already have a `.python-version` file. In order to run tox you need to activate all the Python versions in `tox-python-versions`.

```sh
cp tox-python-versions .python-version
```

Then you'll need to install tox.

```sh
pip install tox
```

Then you can run `tox` to run the tests against each version of python.

## Command line tool

Use this to test the client without having to create an application.

```
    PYTHONPATH=. python /utils/make_api_call.py <base_api_url> <api_key> [fetch|create]
```

This will use the API referred to in the base_api_url argument to send a text message.

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

### `environment.sh`

In the root directory of the repo, run:

```
notify-pass credentials/client-integration-tests > environment.sh
```

Unless you're part of the GOV.UK Notify team, you won't be able to run this command or the Integration Tests. However, the file still needs to exist - run `touch environment.sh` instead.

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

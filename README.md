[![Build Status](https://api.travis-ci.org/alphagov/notifications-python-client.svg?branch=master)](https://api.travis-ci.org/alphagov/notifications-python-client.svg?branch=master)


# GOV.UK Notify - notifications-python-client [BETA]
Python client for notifications API

Python API client for the beta for the GOVUK Notify platform.

Provides client calls, response marchalling and authentication for the GOV.UK Notify API.

## Installing

This is a [python](https://www.python.org/) application.

#### Python version
This is a python 3 application. It has not been run against any version of python 2.x

    brew install python3

#### Dependency management

This is done through [pip](pip.readthedocs.org/) and [virtualenv](https://virtualenv.readthedocs.org/en/latest/). In practise we have used
[VirtualEnvWrapper](http://virtualenvwrapper.readthedocs.org/en/latest/command_ref.html) for our virtual environemnts.

Setting up a virtualenvwrapper for python3
    
    mkvirtualenv -p /usr/local/bin/python3 notifications-python-client

#### Setup

The boostrap script will set the application up. *Ensure you have activated the virtual environment first.*

    ./scripts/bootstrap.sh
    
This will

* Use pip to install dependencies.

#### Tests

The `./scripts/run_tests.py` script will run all the tests. [py.test](http://pytest.org/latest/) is used for testing.

Running tests will also apply syntax checking, using [pep8](https://www.python.org/dev/peps/pep-0008/).

Additionally code coverage is checked via pytest-cov:


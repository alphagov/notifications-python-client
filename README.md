[![Build Status](https://api.travis-ci.org/alphagov/notifications-python-client.svg?branch=master)](https://api.travis-ci.org/alphagov/notifications-python-client.svg?branch=master)


# GOV.UK Notify - notifications-python-client [BETA]
Python client for notifications API

Python API client for the beta for the GOVUK Notify platform.

Provides client calls, response marshalling and authentication for the GOV.UK Notify API.

This project is currently in an early beta phase and this client is presented as a work in progress
for discussions and conversations. It is not supported and is not to be used in production applications
at this stage.

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


Install the dependencies *Ensure you have activated the virtual environment first.*

    pip3 install -r requirements_for_test.txt
    
#### Tests

The `./scripts/run_tests.py` script will run all the tests. [py.test](http://pytest.org/latest/) is used for testing.

Running tests will also apply syntax checking, using [pep8](https://www.python.org/dev/peps/pep-0008/).

Additionally code coverage is checked via pytest-cov:


## Usage


Prior to usage an account must be created through the notify admin console. This will allow access to the API credentials you application.


Once credentials have been obtained the client is initialised as follows:

    from client.notifications import NotificationsAPIClient
    
Then to initialize the client:

    client = NotificationsAPIClient(<base_url>, <service_id>', '<secret>')

Creating a text message:

    notifications_client.send_sms_notification(mobile_number, template_id)

Where:

* "mobile-number" is the mobile phone number to deliver to
    * Only UK mobiles are supported
    * Must start with +44
    * Must not have leading zero
    * Must not have any whitespace, punctuation etc.
    * valid format is +447777111222
    
* "template_id" is the template to send
    * Must be an integer that identifies a valid template. Templates are created in the admin tools.
    

Checking the status of a text message:

    notifications_client.get_notification_by_id(notification_id)


## Errors

Errors are returned as subclasses of the APIError class.


## Testing

A test script is included, it is executed as follows:

    PYTHONPATH=. python /utils/make_api_call.py <base_api_url> <service_id> <api_key> [fetch|create]
    
This will use the API referred to in the base_api_url argument to send a text message.


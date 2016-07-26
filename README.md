[![Build Status](https://api.travis-ci.org/alphagov/notifications-python-client.svg?branch=master)](https://api.travis-ci.org/alphagov/notifications-python-client.svg?branch=master)

# GOV.UK Notify Python client


## Installation

```shell
pip install git+https://github.com/alphagov/notifications-python-client.git@1.0.0#egg=notifications-python-client==1.0.0
```

## Getting started

```python
from notifications_python_client.notifications import NotificationsAPIClient

notifications_client = NotificationsAPIClient(
    "https://api.notifications.service.gov.uk",
    <service_id>,
    <api_key>
)
```

Generate an API key by logging in to
[GOV.UK Notify](https://www.notifications.service.gov.uk) and going to
the _API integration_ page.

You will also find your service ID on the _API integration_ page.


## Send a message

```python
notifications_client.send_sms_notification(mobile_number, template_id)
```

```python
notifications_client.send_email_notification(email_address, template_id)
```

Find `template_id` by clicking _API info_ for the template you want to send.


### With personalisation

If a template has placeholders, you need to provide the values with which to fill them.

```python
notifications_client.send_sms_notification(
    mobile_number,
    template_id,
    personalisation={
        'name': 'Amala',
        'reference_number': '300241',
    }
)
```

## Get the status of one message

```python
notifications_client.get_notification_by_id(notification_id)
```

## Get the status of all messages

```python
notifications_client.get_all_notifications()
```

### Only email or text messages
```python
notifications_client.get_all_notifications(template_type=…)
```
Where `template_type` is one of:

* `email`
* `sms`


### By status
```python
notifications_client.get_all_notifications(status=…)
```

Where `status` is one of:

* `sending`
* `delivered`
* `permanent-failure`
* `temporary-failure`
* `technical-failure`


## Responses

The client will dump the JSON that it receives from the API, for
example:
```python
notifications_client.send_email_notification(
  email_address,
  template_id,
  personalisation={'name': 'Bill'}
)
```
```json
{
  "data":{
    "notification": {
      "id":1
    },
    "body": "Dear Bill, your licence is due for renewal…",
    "template_version": 1,
    "subject": "Licence renewal"
  }
}
```

All of the responses can be found in the
[API documentation](https://www.notifications.service.gov.uk/documentation#API_endpoints).


## Errors

The client will raise a `HTTPError` if it gets a non-`200` response from
the API.

Both the status code and error (dumped from the JSON response) are
available:

```python
try:
  notifications_client.send_email_notification(
    email_address,
    template_id
  )
except HTTPError as error:
  print(error.value.status_code)  # 400
  print(error.value.message)  # <json>
```

For full details of possible errors, see the
[API documentation](https://www.notifications.service.gov.uk/documentation#API_endpoints).

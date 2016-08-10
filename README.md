[![Build Status](https://api.travis-ci.org/alphagov/notifications-python-client.svg?branch=master)](https://travis-ci.org/alphagov/notifications-python-client)

# GOV.UK Notify Python client


## Installation

```shell
pip install git+https://github.com/alphagov/notifications-python-client.git
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
notifications_client.send_sms_notification(
    mobile_number,
    template_id
)
```

```python
notifications_client.send_email_notification(
    email_address,
    template_id
)
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

<details> 
    <summary>
        Response:
    </summary>
```
{
  "data":{
    "notification": {
      "id":1
    },
    "body": "Dear Bill, your licence is due for renewal on 3 January 2016.",
    "template_version": 1,
    "subject": "Licence renewal"
  }
}
```
</details> 


<details> 
    <summary>
        Response codes:
    </summary>
Status code | Body | Meaning
--- | --- | ---
429 | ??? | ???
429 | {"result": "error", <br> "message": "Exceeded send limits (50) for today"} | You have reached the maximum number of messages you can send per day
400 | {"result": "error", <br> "message": "id: required field"} | Post body is badly formed: missing `id` field
400 | {"result":"error", <br> "message":{"template": ["Missing personalisation: {template_placeholder_name}"]} | Post body is badly formed: missing personalisation data
400 | {"result":"error", <br> "message"={"to": ["Invalid {notification_type} for restricted service")]} | Service is in trial mode; you cannot send messages to email addresses or phone numbers not belonging to team members

</details> 

## Get the status of one message

```python
notifications_client.get_notification_by_id(notification_id)
```

<details> 
    <summary>
        Response:
    </summary>
```
{
  "notification": {
    "status": "delivered",
    "to": "07515 987 456",
    "template": {
      "id": "5e427b42-4e98-46f3-a047-32c4a87d26bb",
      "name": "First template",
      "template_type": "sms"
    },
    "created_at": "2016-04-26T15:29:36.891512+00:00",
    "updated_at": "2016-04-26T15:29:38.724808+00:00",
    "sent_at": "2016-04-26T15:29:37.230976+00:00",
    "job": {
      "id": "f9043884-acac-46db-b2ea-f08cd8ec6d67",
      "original_file_name": "Test run"
    },
    "sent_at": "2016-04-26T15:29:37.230976+00:00",
    "id": "f163deaf-2d3f-4ec6-98fc-f23fa511518f",
    "content_char_count": 490,
    "service": "5cf87313-fddd-4482-a2ea-48e37320efd1",
    "reference": None,
    "sent_by": "mmg",
    "body": "Dear Bill, your licence is due for renewal on 3 January 2016."
    "date": "3 January 2016"
  }
}
```

</details> 


## Get the status of all messages

```python
notifications_client.get_all_notifications()
```


<details> 
    <summary>
        Response:
    </summary>
```
{"notifications":
  [{
    "status": "delivered",
    "to": "07515 987 456",
    "template": {
      "id": "5e427b42-4e98-46f3-a047-32c4a87d26bb",
      "name": "First template",
      "template_type": "sms"
    },
    "job": {
      "id": "5cc9d7ae-ceb7-4565-8345-4931d71f8c2e",
      "original_file_name": "Test run"
    },
    "created_at": "2016-04-26T15:30:49.968969+00:00",
    "updated_at": "2016-04-26T15:30:50.853844+00:00",
    "sent_at": "2016-04-26T15:30:50.383634+00:00",
    "id": "04ae9bdc-92aa-4d6c-a0da-48587c03d4c7",
    "content_char_count": 446,
    "service": "5cf87313-fddd-4482-a2ea-48e37320efd1",
    "reference": None,
    "sent_by": "mmg"
    },
    {
    "status": "delivered",
    "to": "07515 987 456",
    "template": {
      "id": "5e427b42-4e98-46f3-a047-32c4a87d26bb",
      "name": "First template",
      "template_type": "sms"
    },
    "job": {
      "id": "f9043884-acac-46db-b2ea-f08cd8ec6d67",
      "original_file_name": "Test run"
    },
    "created_at": "2016-04-26T15:29:36.891512+00:00",
    "updated_at": "2016-04-26T15:29:38.724808+00:00",
    "sent_at": "2016-04-26T15:29:37.230976+00:00",
    "id": "f163deaf-2d3f-4ec6-98fc-f23fa511518f",
    "content_char_count": 490,
    "service": "5cf87313-fddd-4482-a2ea-48e37320efd1",
    "reference": None,
    "sent_by": "mmg"
    },
    …
  ],
  "links": {
    "last": "/notifications?page=3&template_type=sms&status=delivered",
    "next": "/notifications?page=2&template_type=sms&status=delivered"
  },
  "total": 162,
  "page_size": 50
}
```
</details> 


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





## Errors

The client will raise a `HTTPError` if it gets a non-`200` response from
the API.

Both the status code and error (dumped from the JSON response) are
available:

```python
from notifications_python_client.errors import HTTPError

try:
    notifications_client.send_email_notification(
        email_address,
        template_id
    )
except HTTPError as error:
    print(error.status_code)  # 400
    print(error.message)  # <json>
```



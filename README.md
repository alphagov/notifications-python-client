# GOV.UK Notify Python client

## Installation

```shell
pip install notifications-python-client
```

## Getting started

```python
from notifications_python_client.notifications import NotificationsAPIClient

notifications_client = NotificationsAPIClient(api_key)
```

Generate an API key by logging in to
[GOV.UK Notify](https://www.notifications.service.gov.uk) and going to
the **API integration** page.

## Send messages

### Text message

```python
response = notifications_client.send_sms_notification(
    phone_number='+447900900123',
    template_id='f33517ff-2a88-4f6e-b855-c550268ce08a',
    personalisation=None,
    reference=None
)
```
<details>
<summary>
Response
</summary>

If the request is successful, `response` will be a `dict`:

```python
{
  "id": "740e5834-3a29-46b4-9a6f-16142fde533a",
  "reference": None,
  "content": {
    "body": "Some words",
    "from_number": "40604"
  },
  "uri": "https://api.notifications.service.gov.uk/v2/notifications/740e5834-3a29-46b4-9a6f-16142fde533a",
  "template": {
    "id": "f33517ff-2a88-4f6e-b855-c550268ce08a",
    "version": 1,
    "uri": "https://api.notifications.service.gov.uk/v2/template/ceb50d92-100d-4b8b-b559-14fa3b091cd"
  }
}
```

Otherwise the client will raise a `HTTPError`:
<table>
<thead>
<tr>
<th>`error.status_code`</th>
<th>`error.message`</th>
</tr>
</thead>
<tbody>
<tr>
<td>
<pre>429</pre>
</td>
<td>
<pre>
[{
    "error": "RateLimitError",
    "message": "Exceeded rate limit for key type TEAM of 10 requests per 10 seconds"
}]
</pre>
</td>
</tr>
<tr>
<td>
<pre>429</pre>
</td>
<td>
<pre>
[{
    "error": "TooManyRequestsError",
    "message": "Exceeded send limits (50) for today"
}]
</pre>
</td>
</tr>
<tr>
<td>
<pre>400</pre>
</td>
<td>
<pre>
[{
    "error": "BadRequestError",
    "message": "Can"t send to this recipient using a team-only API key"
]}
</pre>
</td>
</tr>
<tr>
<td>
<pre>400</pre>
</td>
<td>
<pre>
[{
    "error": "BadRequestError",
    "message": "Can"t send to this recipient when service is in trial mode
                - see https://www.notifications.service.gov.uk/trial-mode"
}]
</pre>
</td>
</tr>
</tbody>
</table>
</details>

<details>
<summary>
Arguments
</summary>

#### `phone_number`

The phone number of the recipient, only required for sms notifications.

#### `template_id`

Find by clicking **API info** for the template you want to send.

#### `reference`

An optional identifier you generate. The `reference` can be used as a unique reference for the notification. Because Notify does not require this reference to be unique you could also use this reference to identify a batch or group of notifications.

You can omit this argument if you do not require a reference for the notification.


#### `personalisation`

If a template has placeholders, you need to provide their values, for example:

```python
personalisation={
    'first_name': 'Amala',
    'reference_number': '300241',
}
```

</details>

### Email

```python
response = notifications_client.send_email_notification(
    email_address='the_email_address@example.com',
    template_id='f33517ff-2a88-4f6e-b855-c550268ce08a'
    personalisation=None,
    reference=None
)
```

<details>
<summary>
Response
</summary>

If the request is successful, `response` will be a `dict`:

```python
{
  "id": "740e5834-3a29-46b4-9a6f-16142fde533a",
  "reference": None,
  "content": {
    "subject": "Licence renewal",
    "body": "Dear Bill, your licence is due for renewal on 3 January 2016.",
    "from_email": "the_service@gov.uk"
  },
  "uri": "https://api.notifications.service.gov.uk/v2/notifications/740e5834-3a29-46b4-9a6f-16142fde533a",
  "template": {
    "id": "f33517ff-2a88-4f6e-b855-c550268ce08a",
    "version": 1,
    "uri": "https://api.notifications.service.gov.uk/v2/template/f33517ff-2a88-4f6e-b855-c550268ce08a"
  }
}
```

Otherwise the client will raise a `HTTPError`:
<table>
<thead>
<tr>
<th>`error.status_code`</th>
<th>`error.message`</th>
</tr>
</thead>
<tbody>
<tr>
<td>
<pre>429</pre>
</td>
<td>
<pre>
[{
    "error": "RateLimitError",
    "message": "Exceeded rate limit for key type TEAM of 10 requests per 10 seconds"
}]
</pre>
</td>
</tr>
<tr>
<td>
<pre>429</pre>
</td>
<td>
<pre>
[{
    "error": "TooManyRequestsError",
    "message": "Exceeded send limits (50) for today"
}]
</pre>
</td>
</tr>
<tr>
<td>
<pre>400</pre>
</td>
<td>
<pre>
[{
    "error": "BadRequestError",
    "message": "Can"t send to this recipient using a team-only API key"
]}
</pre>
</td>
</tr>
<tr>
<td>
<pre>400</pre>
</td>
<td>
<pre>
[{
    "error": "BadRequestError",
    "message": "Can"t send to this recipient when service is in trial mode
                - see https://www.notifications.service.gov.uk/trial-mode"
}]
</pre>
</td>
</tr>
</tbody>
</table>
</details>

<details>
<summary>Arguments</summary>

#### `email_address`
The email address of the recipient, only required for email notifications.

#### `template_id`

Find by clicking **API info** for the template you want to send.

#### `reference`

An optional identifier you generate. The `reference` can be used as a unique reference for the notification. Because Notify does not require this reference to be unique you could also use this reference to identify a batch or group of notifications.

You can omit this argument if you do not require a reference for the notification.

#### `personalisation`

If a template has placeholders, you need to provide their values, for example:

```python
personalisation={
    'first_name': 'Amala',
    'reference_number': '300241',
}
```

</details>

### Letter

```python
response = notifications_client.send_letter_notification(
    template_id='f33517ff-2a88-4f6e-b855-c550268ce08a'
    personalisation={
      'address_line_1': 'The Occupier',  # required
      'address_line_2': '123 High Street', # required
      'address_line_3': 'London',
      'postcode': 'SW14 6BH',  # required

      ... # any other personalisation found in your template
    },
    reference=None
)
```

<details>
<summary>
Response
</summary>

If the request is successful, `response` will be a `dict`:

```python
{
  "id": "740e5834-3a29-46b4-9a6f-16142fde533a",
  "reference": None,
  "content": {
    "subject": "Licence renewal",
    "body": "Dear Bill, your licence is due for renewal on 3 January 2016.",
  },
  "uri": "https://api.notifications.service.gov.uk/v2/notifications/740e5834-3a29-46b4-9a6f-16142fde533a",
  "template": {
    "id": "f33517ff-2a88-4f6e-b855-c550268ce08a",
    "version": 1,
    "uri": "https://api.notifications.service.gov.uk/v2/template/f33517ff-2a88-4f6e-b855-c550268ce08a"
  }
  "scheduled_for": None
}
```

Otherwise the client will raise a `HTTPError`:
<table>
<thead>
<tr>
<th>`error.status_code`</th>
<th>`error.message`</th>
</tr>
</thead>
<tbody>
<tr>
<td>
<pre>429</pre>
</td>
<td>
<pre>
[{
    "error": "RateLimitError",
    "message": "Exceeded rate limit for key type TEAM of 10 requests per 10 seconds"
}]
</pre>
</td>
</tr>
<tr>
<td>
<pre>429</pre>
</td>
<td>
<pre>
[{
    "error": "TooManyRequestsError",
    "message": "Exceeded send limits (50) for today"
}]
</pre>
</td>
</tr>
<tr>
<td>
<pre>400</pre>
</td>
<td>
<pre>
[{
    "error": "BadRequestError",
    "message": "Can"t send to this recipient using a team-only API key"
]}
</pre>
</td>
</tr>
<tr>
<td>
<pre>400</pre>
</td>
<td>
<pre>
[{
    "error": "BadRequestError",
    "message": "Can"t send to this recipient when service is in trial mode
                - see https://www.notifications.service.gov.uk/trial-mode"
}]
</pre>
</td>
</tr>
<tr>
<td>
<pre>400</pre>
</td>
<td>
<pre>
[{
    "error": "ValidationError",
    "message": "personalisation address_line_1 is a required property"
}]
</pre>
</td>
</tr>
</tbody>
</table>
</details>

<details>
<summary>Arguments</summary>


#### `template_id`

Find by clicking **API info** for the template you want to send.

#### `reference`

An optional identifier you generate. The `reference` can be used as a unique reference for the notification. Because Notify does not require this reference to be unique you could also use this reference to identify a batch or group of notifications.

You can omit this argument if you do not require a reference for the notification.

#### `personalisation`

If you are sending a letter, you will need to provide the letter fields in the format `"address_line_#"`, for example:

```python
personalisation={
    'address_line_1': 'The Occupier',
    'address_line_2': '123 High Street',
    'address_line_3': 'London', # There can be up to six address_line fields
    'postcode': 'SW14 6BH',
    'first_name': 'Amala',
    'reference_number': '300241',
}
```

The fields `"address_line_1"`, `"address_line_2"` and `"postcode"` are required. We support up to six address lines.

</details>


## Get the status of one message

```python
response = notifications_client.get_notification_by_id(notification_id)
```

<details>
<summary>
Response
</summary>

If the request is successful, `response` will be a `dict`:

```python
{
  "id": "notify_id", # required
  "reference": "client reference", # optional
  "email_address": "email address",  # required for emails
  "phone_number": "phone number",  # required for sms
  "line_1": "full name of a person or company", # required for letter
  "line_2": "123 The Street", # required for letter
  "line_3": "Some Area", # optional
  "line_4": "Some Town", # optional
  "line_5": "Some county", # optional
  "line_6": "Something else", # optional
  "postcode": "postcode", # required for letter
  "type": "sms|letter|email", # required
  "status": "current status", # required
  "template": {
    "version": 1 # template version num # required
    "id": 1 # template id # required
    "uri": "/v2/template/{id}/{version}", # required
  },
  "body": "Body of the notification",
  "subject": "Subject of an email notification or None if an sms message"
	"created_at": "created at", # required
	"sent_at": " sent to provider at", # optional
	"completed_at:" "date the notification is delivered or failed" # optional
}
```

Otherwise the client will raise a `HTTPError`:
<table>
<thead>
<tr>
<th>`error.status_code`</th>
<th>`error.message`</th>
</tr>
</thead>
<tbody>
<tr>
<td>
<pre>404</pre>
</td>
<td>
<pre>
[{
    "error": "NoResultFound",
    "message": "No result found"
}]
</pre>
</td>
</tr>
<tr>
<td>
<pre>400</pre>
</td>
<td>
<pre>
[{
    "error": "ValidationError",
    "message": "id is not a valid UUID"
}]
</pre>
</td>
</tr>
</tbody>
</table>
</details>

## Get the status of all messages (with pagination)

_This will return one page of notifications (250) per call. Use the `get_all_notifications_iterator` to retrieve all notifications unpaginated._

```python
response = notifications_client.get_all_notifications(template_type, status, reference, older_than)
```
<details>
<summary>
Response
</summary>

If the request is successful, `response` will be a `dict`:

```python
{"notifications":
  [
    {
      "id": "notify_id", # required
      "reference": "client reference", # optional
      "email_address": "email address",  # required for emails
      "phone_number": "phone number",  # required for sms
      "line_1": "full name of a person or company", # required for letter
      "line_2": "123 The Street", # required for letter
      "line_3": "Some Area", # optional
      "line_4": "Some Town", # optional
      "line_5": "Some county", # optional
      "line_6": "Something else", # optional
      "postcode": "postcode", # required for letter
      "type": "sms | letter | email", # required
      "status": sending | delivered | permanent-failure | temporary-failure | technical-failure # required
      "template": {
        "version": 1 # template version num # required
        "id": 1 # template id # required
        "uri": "/v2/template/{id}/{version}", # required
      },
      "body": "Body of the notification",
      "subject": "Subject of an email notification or None if an sms message"
      "created_at": "created at", # required
      "sent_at": " sent to provider at", # optional
      "completed_at:" "date the notification is delivered or failed" # optional
    },
    …
  ],
  "links": {
    "current": "/notifications?template_type=sms&status=delivered",
    "next": "/notifications?other_than=last_id_in_list&template_type=sms&status=delivered"
  }
}
```

Otherwise the client will raise a `HTTPError`:
<table>
<thead>
<tr>
<th>`error.status_code`</th>
<th>`error.message`</th>
</tr>
</thead>
<tbody>
<tr>
<td>
<pre>400</pre>
</td>
<td>
<pre>
[{
    'error': 'ValidationError',
    'message': 'bad status is not one of [created, sending, delivered, pending, failed, technical-failure, temporary-failure, permanent-failure]'
}]
</pre>
</td>
</tr>
<tr>
<td>
<pre>400</pre>
</td>
<td>
<pre>
[{
    "error": "ValidationError",
    "message": "Apple is not one of [sms, email, letter]"
}]
</pre>
</td>
</tr>
</tbody>
</table>
</details>

### Arguments

#### `template_type`

You can filter by:

* `email`
* `sms`
* `letter`

You can omit this argument to ignore this filter.


#### `status`

##### email

You can filter by:

* `sending` - the message is queued to be sent by the provider.
* `delivered` - the message was successfully delivered.
* `failed` - this will return all failure statuses `permanent-failure`, `temporary-failure` and `technical-failure`.
* `permanent-failure` - the provider was unable to deliver message, email does not exist; remove this recipient from your list.
* `temporary-failure` - the provider was unable to deliver message, email box was full; you can try to send the message again.
* `technical-failure` - Notify had a technical failure; you can try to send the message again.

You can omit this argument to ignore this filter.

##### text message

You can filter by:

* `sending` - the message is queued to be sent by the provider.
* `delivered` - the message was successfully delivered.
* `failed` - this will return all failure statuses `permanent-failure`, `temporary-failure` and `technical-failure`.
* `permanent-failure` - the provider was unable to deliver message, phone number does not exist; remove this recipient from your list.
* `temporary-failure` - the provider was unable to deliver message, the phone was turned off; you can try to send the message again.
* `technical-failure` - Notify had a technical failure; you can try to send the message again.

You can omit this argument to ignore this filter.

##### letter

You can filter by:

* `created` - the message has been created
* `sending` - the message is queued to be sent by the provider.
* `failed` - this will return all failure statuses `permanent-failure`, `temporary-failure` and `technical-failure`.
* `technical-failure` - Notify had a technical failure; you can try to send the message again.

You can omit this argument to ignore this filter.

### `reference`

This is the `reference` you gave at the time of sending the notification. The `reference` can be a unique identifier for the notification or an identifier for a batch of notifications.

You can omit this argument to ignore the filter.

### `olderThanId`

You can get the notifications older than a given Notification.notificationId.

You can omit this argument to ignore the filter.

## Get the status of all messages (without pagination)

```python
response = get_all_notifications_iterator(status="sending")
```
<details>
<summary>
Response
</summary>

If the request is successful, `response` will be a `<generator object>` that will yield all messages:

```python
<generator object NotificationsAPIClient.get_all_notifications_iterator at 0x1026c7410>
```

Otherwise the client will raise a `HTTPError`:
<table>
<thead>
<tr>
<th>`error.status_code`</th>
<th>`error.message`</th>
</tr>
</thead>
<tbody>
<tr>
<td>
<pre>400</pre>
</td>
<td>
<pre>
[{
    'error': 'ValidationError',
    'message': 'bad status is not one of [created, sending, delivered, pending, failed, technical-failure, temporary-failure, permanent-failure]'
}]
</pre>
</td>
</tr>
<tr>
<td>
<pre>400</pre>
</td>
<td>
<pre>
[{
    "error": "ValidationError",
    "message": "Apple is not one of [sms, email, letter]"
}]
</pre>
</td>
</tr>
</tbody>
</table>
</details>

### Arguments

#### `template_type`

You can filter by:

* `email`
* `sms`
* `letter`

You can omit this argument to ignore this filter.


#### `status`

##### email

You can filter by:

* `sending` - the message is queued to be sent by the provider.
* `delivered` - the message was successfully delivered.
* `failed` - this will return all failure statuses `permanent-failure`, `temporary-failure` and `technical-failure`.
* `permanent-failure` - the provider was unable to deliver message, email does not exist; remove this recipient from your list.
* `temporary-failure` - the provider was unable to deliver message, email box was full; you can try to send the message again.
* `technical-failure` - Notify had a technical failure; you can try to send the message again.

You can omit this argument to ignore this filter.

##### text message

You can filter by:

* `sending` - the message is queued to be sent by the provider.
* `delivered` - the message was successfully delivered.
* `failed` - this will return all failure statuses `permanent-failure`, `temporary-failure` and `technical-failure`.
* `permanent-failure` - the provider was unable to deliver message, phone number does not exist; remove this recipient from your list.
* `temporary-failure` - the provider was unable to deliver message, the phone was turned off; you can try to send the message again.
* `technical-failure` - Notify had a technical failure; you can try to send the message again.

You can omit this argument to ignore this filter.

##### letter

You can filter by:

* `created` - the message has been created
* `sending` - the message is queued to be sent by the provider.
* `failed` - this will return all failure statuses `permanent-failure`, `temporary-failure` and `technical-failure`.
* `technical-failure` - Notify had a technical failure; you can try to send the message again.

You can omit this argument to ignore this filter.

### `reference`

This is the `reference` you gave at the time of sending the notification. The `reference` can be a unique identifier for the notification or an identifier for a batch of notifications.

## Get a template by ID

_This will return the latest version of the template. Use [get_template_version](#get-a-template-by-id-and-version) to retrieve a specific template version_

```python
response = notifications_client.get_template(
    'template_id'
)
```

<details>
<summary>
Response
</summary>

If the request is successful, `response` will be a `dict`:

```python
{
    "id": "template_id", # required
    "type": "sms" | "email" | "letter", # required
    "created_at": "created at", # required
    "updated_at": "updated at", # required
    "version": "version", # integer required
    "created_by": "someone@example.com", # email required
    "body": "Body of the notification", # required
    "subject": "Subject of an email or letter notification or None if an sms message"
}
```

Otherwise the client will raise a `HTTPError`:
<table>
<thead>
<tr>
<th>`error.status_code`</th>
<th>`error.message`</th>
</tr>
</thead>
<tbody>
<tr>
<td>
<pre>404</pre>
</td>
<td>
<pre>
[{
    "error": "NoResultFound",
    "message": "No result found"
]}
</pre>
</td>
</tr>
</tbody>
</table>
</details>

## Get a template by ID and version

```python
response = notifications_client.get_template_version(
    'template_id',
    1   # integer required for version number
)
```

<details>
<summary>
Response
</summary>

If the request is successful, `response` will be a `dict`:

```python
{
    "id": "template_id", # required
    "type": "sms" | "email" | "letter", # required
    "created_at": "created at", # required
    "updated_at": "updated at", # required
    "version": "version", # integer required
    "created_by": "someone@example.com", # email required
    "body": "Body of the notification", # required
    "subject": "Subject of an email or letter notification, or None if an sms message"
}
```

Otherwise the client will raise a `HTTPError`:
<table>
<thead>
<tr>
<th>`error.status_code`</th>
<th>`error.message`</th>
</tr>
</thead>
<tbody>
<tr>
<td>
<pre>404</pre>
</td>
<td>
<pre>
[{
    "error": "NoResultFound",
    "message": "No result found"
]}
</pre>
</td>
</tr>
</tbody>
</table>
</details>

## Get all templates

```python
response = notifications_client.get_all_templates(
    template_type=None # optional
)
```
_This will return the latest version for each template_

[See available template types](#template_type)

<details>
<summary>
Response
</summary>

If the request is successful, `response` will be a `dict`:

```python
{
    "templates" : [
        {
            "id": "template_id", # required
            "type": "sms" | "email" | "letter", # required
            "created_at": "created at", # required
            "updated_at": "updated at", # required
            "version": "version", # integer required
            "created_by": "someone@example.com", # email required
            "body": "Body of the notification", # required
            "subject": "Subject of an email or letter notification, or None if an sms message"
        },
        {
            ... another template
        }
    ]
}
```

If no templates exist for a template type or there no templates for a service, the `response` will be a `dict` with an empty `templates` list element:

```python
{
    "templates" : []
}
```

</details>

## Generate a preview template

```
response = notifications_client.post_template_preview(
    'template_id',
    personalisation={'name': 'chris'}
)
```

<details>
<summary>
Response
</summary>

If the request is successful, `response` will be a `dict`:

```python
{
    "id": "notify_id", # required
    "type": "sms" | "email" | "letter", # required
    "version": "version", # integer required
    "body": "Body of the notification", # required
    "subject": "Subject of an email or letter notification, or None if an sms message"
}
```

Otherwise the client will raise a `HTTPError`:
<table>
<thead>
<tr>
<th>`error.status_code`</th>
<th>`error.message`</th>
</tr>
</thead>
<tbody>
<tr>
<td>
<pre>400</pre>
</td>
<td>
<pre>
[{
    "error": "BadRequestError",
    "message": "Missing personalisation: [name]"
]}
</pre>
</td>
</tr>
<tr>
<td>
<pre>404</pre>
</td>
<td>
<pre>
[{
    "error": "NoResultFound",
    "message": "No result found"
]}
</pre>
</td>
</tr>
</tbody>
</table>
</details>

# GOV.UK Notify Python client

This documentation is for developers interested in using this Python client to integrate their government service with GOV.UK Notify.

## Table of Contents

* [Installation](#installation)
* [Getting started](#getting-started)
* [Send messages](#send-messages)
* [Get the status of one message](#get-the-status-of-one-message)
* [Get the status of all messages with pagination](#get-the-status-of-all-messages-with-pagination)
* [Get the status of all messages without pagination](#get-the-status-of-all-messages-without-pagination)
* [Get a template by ID](#get-a-template-by-id)
* [Get a template by ID and version](#get-a-template-by-id-and-version)
* [Get all templates](#get-all-templates)
* [Generate a preview template](#generate-a-preview-template)
* [Get received text messages with pagination](#get-received-text-messages-with-pagination)
* [Get received text messages without pagination](#get-received-text-messages-without-pagination)

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

#### Method 

<details>
<summary>
Click here to expand for more information.
</summary>

```python
response = notifications_client.send_sms_notification(
    phone_number='+447900900123',
    template_id='f33517ff-2a88-4f6e-b855-c550268ce08a',
    personalisation=None,
    reference=None
    sms_sender_id=None
)
```
</details>

#### Response

If the request is successful, `response` will be a `dict`. 
<details>
<summary>
Click here to expand for more information.
</summary>

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


|`error.status_code`|`error.message`|
|:---|:---|
|`429`|`[{`<br>`"error": "RateLimitError",`<br>`"message": "Exceeded rate limit for key type TEAM of 10 requests per 10 seconds"`<br>`}]`|
|`429`|`[{`<br>`"error": "TooManyRequestsError",`<br>`"message": "Exceeded send limits (50) for today"`<br>`}]`|
|`400`|`[{`<br>`"error": "BadRequestError",`<br>`"message": "Can"t send to this recipient using a team-only API key"`<br>`]}`|
|`400`|`[{`<br>`"error": "BadRequestError",`<br>`"message": "Can"t send to this recipient when service is in trial mode - see https://www.notifications.service.gov.uk/trial-mode"`<br>`}]`|

</details>

#### Arguments

<details>
<summary>
Click here to expand for more information.
</summary>

##### `phone_number`

The phone number of the recipient, only required for sms notifications.

##### `template_id`

Find by clicking **API info** for the template you want to send.

##### `reference`

An optional identifier you generate. The `reference` can be used as a unique reference for the notification. Because Notify does not require this reference to be unique you could also use this reference to identify a batch or group of notifications.

You can omit this argument if you do not require a reference for the notification.


##### `personalisation`

If a template has placeholders, you need to provide their values, for example:

```python
personalisation={
    'first_name': 'Amala',
    'reference_number': '300241',
}
```
##### `sms_sender_id`

Optional. Specifies the identifier of the sms sender to set for the notification. The identifiers are found in your service Settings, when you 'Manage' your 'Text message sender'.

If you omit this argument your default sms sender will be set for the notification.

</details>

### Email

#### Method

<details>
<summary>
Click here to expand for more information.
</summary>

```python
response = notifications_client.send_email_notification(
    email_address='the_email_address@example.com',
    template_id='f33517ff-2a88-4f6e-b855-c550268ce08a'
    personalisation=None,
    reference=None,
    email_reply_to_id=None
)
```
</details>

#### Response

If the request is successful, `response` will be a `dict`. 
<details>
<summary>
Click here to expand for more information.
</summary>


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

|`error.status_code`|`error.message`|
|:---|:---|
|`429`|`[{`<br>`"error": "RateLimitError",`<br>`"message": "Exceeded rate limit for key type TEAM of 10 requests per 10 seconds"`<br>`}]`|
|`429`|`[{`<br>`"error": "TooManyRequestsError",`<br>`"message": "Exceeded send limits (50) for today"`<br>`}]`|
|`400`|`[{`<br>`"error": "BadRequestError",`<br>`"message": "Can"t send to this recipient using a team-only API key"`<br>`]}`|
|`400`|`[{`<br>`"error": "BadRequestError",`<br>`"message": "Can"t send to this recipient when service is in trial mode - see https://www.notifications.service.gov.uk/trial-mode"`<br>`}]`|

</details>

#### Arguments

<details>
<summary>Click here to expand for more information</summary>

##### `email_address`
The email address of the recipient, only required for email notifications.

##### `template_id`

Find by clicking **API info** for the template you want to send.

##### `reference`

An optional identifier you generate. The `reference` can be used as a unique reference for the notification. Because Notify does not require this reference to be unique you could also use this reference to identify a batch or group of notifications.

You can omit this argument if you do not require a reference for the notification.

##### `personalisation`

If a template has placeholders, you need to provide their values, for example:

```python
personalisation={
    'first_name': 'Amala',
    'application_number': '300241',
}
```

##### `email_reply_to_id`

An optional identifier that you can get from the service email_reply_to ids found in the service settings / manage email reply to addresses page.

You can omit this argument if you want to use the default service email reply to otherwise add the id from the list of email_reply_to ids associated with the service.

</details>

### Letter

#### Method

<details>
<summary>
Click here to expand for more information.
</summary>

```python
response = notifications_client.send_letter_notification(
    template_id='f33517ff-2a88-4f6e-b855-c550268ce08a',
    personalisation={
      'address_line_1': 'The Occupier',  # required
      'address_line_2': '123 High Street', # required
      'address_line_3': 'London',
      'postcode': 'SW14 6BH',  # required

      ... # any other optional address lines, or personalisation fields found in your template
    },
    reference=None
)
```
</details>

#### Response

If the request is successful, `response` will be a `dict`. 
<details>
<summary>
Click here to expand for more information.
</summary>

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

|`error.status_code`|`error.message`|
|:---|:---|
|`429`|`[{`<br>`"error": "RateLimitError",`<br>`"message": "Exceeded rate limit for key type live of 10 requests per 20 seconds"`<br>`}]`|
|`429`|`[{`<br>`"error": "TooManyRequestsError",`<br>`"message": "Exceeded send limits (50) for today"`<br>`}]`|
|`400`|`[{`<br>`"error": "BadRequestError",`<br>`"message": "Cannot send letters with a team api key"`<br>`]}`|
|`400`|`[{`<br>`"error": "BadRequestError",`<br>`"message": "Cannot send letters when service is in trial mode - see https://www.notifications.service.gov.uk/trial-mode"`<br>`}]`|
|`400`|`[{`<br>`"error": "ValidationError",`<br>`"message": "personalisation address_line_1 is a required property"`<br>`}]`|

</details>

#### Arguments

<details>
<summary>Click here to expand for more information.</summary>

##### `template_id`

Find by clicking **API info** for the template you want to send.

##### `reference`

An optional identifier you generate. The `reference` can be used as a unique reference for the notification. Because Notify does not require this reference to be unique you could also use this reference to identify a batch or group of notifications.

You can omit this argument if you do not require a reference for the notification.

##### `personalisation`

The letter must contain:

- mandatory address fields
- optional address fields if applicable
- fields from template

```python
personalisation={
    'address_line_1': 'The Occupier', 		# mandatory address field
    'address_line_2': 'Flat 2', 		# mandatory address field
    'address_line_3': '123 High Street', 	# optional address field
    'address_line_4': 'Richmond upon Thames', 	# optional address field
    'address_line_5': 'London', 		# optional address field
    'address_line_6': 'Middlesex', 		# optional address field
    'postcode': 'SW14 6BH', 			# mandatory address field
    'application_id': '1234', 			# field from template
    'application_date': '2017-01-01', 		# field from template
}
```

</details>


## Get the status of one message

#### Method

<details>
<summary>
Click here to expand for more information.
</summary>

```python
response = notifications_client.get_notification_by_id(notification_id)
```
</details>

#### Response

If the request is successful, `response` will be a `dict`. 
<details>
<summary>
Click here to expand for more information.
</summary>


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

|`error.status_code`|`error.message`|
|:---|:---|
|`404`|`[{`<br>`"error": "NoResultFound",`<br>`"message": "No result found"`<br>`}]`|
|`400`|`[{`<br>`"error": "ValidationError",`<br>`"message": "id is not a valid UUID"`<br>`}]`|

</details>

#### Arguments

<details>
<summary>
Click here to expand for more information.
</summary>

##### `notification_id`

The ID of the notification.

</details>

## Get the status of all messages with pagination

#### Method

This will return one page of notifications (250) per call. Use the `get_all_notifications_iterator` to retrieve all notifications unpaginated. 
<details>

<summary>
Click here to expand for more information.
</summary>


```python
response = notifications_client.get_all_notifications(template_type, status, reference, older_than)
```

</details>

#### Response

If the request is successful, `response` will be a `dict`. 
<details>
<summary>
Click here to expand for more information.
</summary>



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
      "type": "sms" | "letter" | "email", # required
      "status": "sending" | "delivered" | "permanent-failure" | "temporary-failure" | "technical-failure" # required
      "template": {
        "version": 1 # template version num # required
        "id": 1 # template id # required
        "uri": "/v2/template/{id}/{version}", # required
      },
      "body": "Body of the notification",
      "subject": "Subject of an email notification or None if an sms message"
      "created_at": "created at", # required
      "sent_at": "sent to provider at", # optional
      "completed_at": "date the notification is delivered or failed" # optional
    },
    …
  ],
  "links": {
    "current": "/notifications?template_type=sms&status=delivered",
    "next": "/notifications?older_than=last_id_in_list&template_type=sms&status=delivered"
  }
}
```

Otherwise the client will raise a `HTTPError`:

|`error.status_code`|`error.message`|
|:---|:---|
|`400`|`[{`<br>`"error": "ValidationError",`<br>`"message": "bad status is not one of [created, sending, delivered, pending, failed, technical-failure, temporary-failure, permanent-failure]"`<br>`}]`|
|`400`|`[{`<br>`"error": "ValidationError",`<br>`"message": "Apple is not one of [sms, email, letter]"`<br>`}]`|


</details>


#### Arguments

<details>
<summary>Click here to expand for more information.</summary>

##### `template_type`

You can filter by:

* `email`
* `sms`
* `letter`

You can omit this argument to ignore this filter.

##### `status`

__email__

You can filter by:

* `sending` - the message is queued to be sent by the provider.
* `delivered` - the message was successfully delivered.
* `failed` - this will return all failure statuses `permanent-failure`, `temporary-failure` and `technical-failure`.
* `permanent-failure` - the provider was unable to deliver message, email does not exist; remove this recipient from your list.
* `temporary-failure` - the provider was unable to deliver message, email box was full; you can try to send the message again.
* `technical-failure` - Notify had a technical failure; you can try to send the message again.

You can omit this argument to ignore this filter.

__text message__

You can filter by:

* `sending` - the message is queued to be sent by the provider.
* `delivered` - the message was successfully delivered.
* `failed` - this will return all failure statuses `permanent-failure`, `temporary-failure` and `technical-failure`.
* `permanent-failure` - the provider was unable to deliver message, phone number does not exist; remove this recipient from your list.
* `temporary-failure` - the provider was unable to deliver message, the phone was turned off; you can try to send the message again.
* `technical-failure` - Notify had a technical failure; you can try to send the message again.

You can omit this argument to ignore this filter.

__letter__

You can filter by:

* `accepted` -  Notify is in the process of printing and posting the letter
* `technical-failure` - Notify had an unexpected error while sending to our printing provider

You can omit this argument to ignore this filter.

##### `reference`

This is the `reference` you gave at the time of sending the notification. The `reference` can be a unique identifier for the notification or an identifier for a batch of notifications.

You can omit this argument to ignore the filter.

##### `older_than`

If omitted first 250 notifications are returned. Otherwise you can filter to retrieve the next 250 notifications older than the given Notification.notificationId.

</details>

## Get the status of all messages without pagination

#### Method

<details>
<summary>
Click here to expand for more information.
</summary>

```python
response = get_all_notifications_iterator(status="sending")
```
</details>

#### Response

If the request is successful, `response` will be a `<generator object>` that will yield all messages. 
<details>
<summary>
Click here to expand for more information.
</summary>

```python
<generator object NotificationsAPIClient.get_all_notifications_iterator at 0x1026c7410>
```

Otherwise the client will raise a `HTTPError`:

|`error.status_code`|`error.message`|
|:---|:---|
|`400`|`[{`<br>`"error": "ValidationError",`<br>`"message": "bad status is not one of [created, sending, delivered, pending, failed, technical-failure, temporary-failure, permanent-failure]"`<br>`}]`|
|`400`|`[{`<br>`"error": "ValidationError",`<br>`"message": "Apple is not one of [sms, email, letter]"`<br>`}]`|

</details>

#### Arguments

<details>
<summary>Click here to expand for more information.</summary>

##### `template_type`

You can filter by:

* `email`
* `sms`
* `letter`

You can omit this argument to ignore this filter.

##### `status`

__email__

You can filter by:

* `sending` - the message is queued to be sent by the provider.
* `delivered` - the message was successfully delivered.
* `failed` - this will return all failure statuses `permanent-failure`, `temporary-failure` and `technical-failure`.
* `permanent-failure` - the provider was unable to deliver message, email does not exist; remove this recipient from your list.
* `temporary-failure` - the provider was unable to deliver message, email box was full; you can try to send the message again.
* `technical-failure` - Notify had a technical failure; you can try to send the message again.

You can omit this argument to ignore this filter.

__text message__

You can filter by:

* `sending` - the message is queued to be sent by the provider.
* `delivered` - the message was successfully delivered.
* `failed` - this will return all failure statuses `permanent-failure`, `temporary-failure` and `technical-failure`.
* `permanent-failure` - the provider was unable to deliver message, phone number does not exist; remove this recipient from your list.
* `temporary-failure` - the provider was unable to deliver message, the phone was turned off; you can try to send the message again.
* `technical-failure` - Notify had a technical failure; you can try to send the message again.

You can omit this argument to ignore this filter.

__letter__

You can filter by:

* `accepted` - the letter has been generated.
* `technical-failure` - Notify had an unexpected error while sending to our printing provider

You can omit this argument to ignore this filter.

##### `reference`

This is the `reference` you gave at the time of sending the notification. The `reference` can be a unique identifier for the notification or an identifier for a batch of notifications.

</details>

## Get a template by ID

#### Method 

This will return the latest version of the template. Use [get_template_version](#get-a-template-by-id-and-version) to retrieve a specific template version. 

<details>
<summary>
Click here to expand for more information.
</summary>


```python
response = notifications_client.get_template(
    'template_id'
)
```
</details>

#### Response

If the request is successful, `response` will be a `dict`. 
<details>
<summary>
Click here to expand for more information.
</summary>


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

|`error.status_code`|`error.message`|
|:---|:---|
|`404`|`[{`<br>`"error": "NoResultFound",`<br>`"message": "No Result Found"`<br>`}]`|

</details>

#### Arguments

<details>
<summary>Click here to expand for more information.</summary>

##### `template_id`

Find by clicking **API info** for the template you want to send.

</details>


## Get a template by ID and version

#### Method

<details>
<summary>
Click here to expand for more information.
</summary>

```python
response = notifications_client.get_template_version(
    'template_id',
    1   # integer required for version number
)
```
</details>

#### Response

If the request is successful, `response` will be a `dict`. 
<details>
<summary>
Click here to expand for more information.
</summary>

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

|`error.status_code`|`error.message`|
|:---|:---|
|`404`|`[{`<br>`"error": "NoResultFound",`<br>`"message": "No Result Found"`<br>`}]`|

</details>

#### Arguments

<details>
<summary>Click here to expand for more information.</summary>

##### `template_id`

Find by clicking **API info** for the template you want to send.

##### `version`

The version number of the template.

</details>

## Get all templates

#### Method

This will return the latest version for each template. 
<details>
<summary>
Click here to expand for more information.
</summary>


```python
response = notifications_client.get_all_templates(
    template_type=None # optional
)
```

[See available template types](#template_type)

</details>

#### Response

If the request is successful, `response` will be a `dict`. 
<details>
<summary>
Click here to expand for more information.
</summary>

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

#### Arguments

<details>
<summary>Click here to expand for more information.</summary>

##### `template_type`

If omitted all messages are returned. Otherwise you can filter by:

- `email`
- `sms`
- `letter`

</details>

## Generate a preview template

#### Method

<details>
<summary>
Click here to expand for more information.
</summary>


```
response = notifications_client.post_template_preview(
    'template_id',
    personalisation={'name': 'chris'}
)
```

</details>

#### Response

If the request is successful, `response` will be a `dict`. 
<details>
<summary>
Click here to expand for more information.
</summary>


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

|`error.status_code`|`error.message`|
|:---|:---|
|`400`|`[{`<br>`"error": "BadRequestError",`<br>`"message": "Missing personalisation: [name]"`<br>`}]`|
|`400`|`[{`<br>`"error": "NoResultFound",`<br>`"message": "No result found"`<br>`}]`|

</details>

#### Arguments

<details>
<summary>Click here to expand for more information.</summary>

##### `template_id`

Find by clicking **API info** for the template you want to send.

##### `personalisation`

If a template has placeholders, you need to provide their values, for example:

```python
personalisation={
    'first_name': 'Amala',
    'reference_number': '300241',
}
```

</details>

## Get received text messages with pagination

This will return 250 of the most recently received text messages. Use the `get_received_texts_iterator` to retrieve all received texts unpaginated. 
#### Method

<details>
<summary>
Click here to expand for more information.
</summary>

```python

response = client.get_received_texts(older_than)

```
</details>

#### Response

If the request is successful, `response` will be a `dict`.
<details>
<summary>
Click here to expand for more information.
</summary>

```python
{
  "received_text_messages":
  [
    {
      "id": "notify_id", # required
      "user_number": "user number", # required user number
      "notify_number": "notify number", # receiving number 
      "created_at": "created at", # required
      "service_id": "service id", # required service id
      "content": "text content" # required text content
    },
    …
  ],
  "links": {
    "current": "/received-text-messages",
    "next": "/received-text-messages?older_than=last_id_in_list"
  }
}
```

</details>

#### Arguments

<details>
<summary>
Click here to expand for more information.
</summary>
	
#### `older_than`

If omitted 250 of the most recently received text messages are returned. Otherwise the next 250 received text messages older than the given id are returned.

</details>

## Get received text messages without pagination

#### Method

<details>
<summary>
Click here to expand for more information.
</summary>

```python
response = get_received_texts_iterator()
```
</details>

#### Response

If the request is successful, `response` will be a `<generator object>` that will yield all received texts. 
<details>
<summary>
Click here to expand for more information.
</summary>

```python
<generator object NotificationsAPIClient.get_received_texts_iterator at 0x1026c7410>
```
</details>

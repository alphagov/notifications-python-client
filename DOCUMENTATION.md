# Python client documentation

This documentation is for Python developers interested in using GOV.UK Notify to send emails, text messages or letters. Notify supports Python 3.x and 2.7.

# Set up the client

## Install the client

Run the following code in the command line:

```shell
pip install notifications-python-client
```

Refer to the [client change log](https://github.com/alphagov/notifications-python-client/blob/master/CHANGELOG.md) for the client version number and the latest updates.

## Create a new instance of the client

Add this code to your application:

```python
from notifications_python_client.notifications import NotificationsAPIClient

notifications_client = NotificationsAPIClient(api_key)
```

To get an API key, [sign in to GOV.UK Notify](https://www.notifications.service.gov.uk/) and go to the _API integration_ page. You can find more information in the [API keys](#api-keys) section.

# Send a message

You can use GOV.UK Notify to send text messages, emails and letters.

## Send a text message

### Method

```python
response = notifications_client.send_email_notification(
    phone_number='+447900900123', # required string
    template_id='f33517ff-2a88-4f6e-b855-c550268ce08a', # required UUID string
)
```

### Arguments

#### phone_number (required)

The phone number of the recipient of the text message. This number can be UK or international.

#### template_id (required)

The ID of the template. You can find this by signing into [GOV.UK Notify](https://www.notifications.service.gov.uk/) and going to the __Templates__ page.

#### personalisation (optional)

If a template has placeholder fields for personalised information such as name or reference number, you need to provide their values in a dictionary with key value pairs. For example:

```python
personalisation={
    'first_name': 'Amala',
    'application_date': '2018-01-01',
}
```

#### reference (optional)

A unique identifier. This reference can identify a single unique notification or a batch of multiple notifications.

```python
reference='STRING', # optional string - identifies notification(s)
```

#### sms_sender_id (optional)

A unique identifier of the sender of the text message notification. To set this up:

1. Sign into your GOV.UK Notify account.
1. Go to __Settings__.
1. Go to the __Text Messages__ section and select __Manage__ on the "Text Message sender" row.
1. You can do one of the following:
  - copy the ID of the sender you want to use and paste it into the method
  - select __Change__ to change the default sender that the service will use, and select __Save__

```python
sms_sender_id='8e222534-7f05-4972-86e3-17c5d9f894e2' # optional UUID string
```

If you omit this argument from your method, the client will set the default `sms_sender_id` for the notification.

### Response

If the request to the client is successful, you will receive the following `dict` response:

```python
{
  "id": "740e5834-3a29-46b4-9a6f-16142fde533a",
  "reference": "STRING",
  "content": {
    "body": "MESSAGE TEXT",
    "from_number": "SENDER"
  },
  "uri": "https://api.notifications.service.gov.uk/v2/notifications/740e5834-3a29-46b4-9a6f-16142fde533a",
  "template": {
    "id": 'f33517ff-2a88-4f6e-b855-c550268ce08a',
    "version": INTEGER,
    "uri": "https://api.notifications.service.gov.uk/v2/template/ceb50d92-100d-4b8b-b559-14fa3b091cd"
  }
}
```

If you are using the [test API key](#test), all your messages will come back as delivered.

All successfully delivered messages will appear on your dashboard.

### Error codes

If the request is not successful, the client will raise an `HTTPError`.

|`error.status_code`|`error.message`|How to fix|
|:---|:---|:---|
|`400`|`[{`<br>`"error": "BadRequestError",`<br>`"message": "Can't send to this recipient using a team-only API key"`<br>`]}`|Use the correct type of API key. Refer to [API keys](#api-keys) for more information|
|`400`|`[{`<br>`"error": "BadRequestError",`<br>`"message": "Can't send to this recipient when service is in trial mode - see https://www.notifications.service.gov.uk/trial-mode"`<br>`}]`|Refer to [trial mode](https://www.notifications.service.gov.uk/features/using-notify#trial-mode) for more information|
|`403`|`[{`<br>`"error": "AuthError",`<br>`"message": "Error: Your system clock must be accurate to within 30 seconds"`<br>`}]`|Check your system clock|
|`403`|`[{`<br>`"error": "AuthError",`<br>`"message": "Invalid token: signature, api token not found"`<br>`}]`|Use the correct API key. Refer to [API keys](#api-keys) for more information|
|`429`|`[{`<br>`"error": "RateLimitError",`<br>`"message": "Exceeded rate limit for key type TEAM/TEST/LIVE of 3000 requests per 60 seconds"`<br>`}]`|Refer to [API rate limits](#api-rate-limits) for more information|
|`429`|`[{`<br>`"error": "TooManyRequestsError",`<br>`"message": "Exceeded send limits (LIMIT NUMBER) for today"`<br>`}]`|Refer to [service limits](#service-limits) for the limit number|
|`500`|`[{`<br>`"error": "Exception",`<br>`"message": "Internal server error"`<br>`}]`|Notify was unable to process the request, resend your notification.|

## Send an email

### Method

```python
response = notifications_client.send_email_notification(
    email_address='sender@something.com', # required string
    template_id='f33517ff-2a88-4f6e-b855-c550268ce08a', # required UUID string
)
```

### Arguments

#### email_address (required)

The email address of the recipient.

#### template_id (required)

The ID of the template. You can find this by signing into GOV.UK Notify and going to the __Templates__ page.

#### personalisation (optional)

If a template has placeholder fields for personalised information such as name or reference number, you need to provide their values in a dictionary with key value pairs. For example:

```python
personalisation={
    'first_name': 'Amala',
    'application_date': '2018-01-01',
}
```

#### reference (optional)

A unique identifier. This reference can identify a single unique notification or a batch of multiple notifications.

```python
reference='STRING', # optional string - identifies notification(s)
```

#### email_reply_to_id (optional)

This is an email reply-to address specified by you to receive replies from your users. Your service cannot go live until at least one email address has been set up for this. To set up:

1. Sign into your GOV.UK Notify account.
1. Go to __Settings__.
1. Go to the Email section and select __Manage__ on the "Email reply to addresses" row.
1. Select __Change__ to specify the email address to receive replies, and select __Save__.

```python
email_reply_to_id='8e222534-7f05-4972-86e3-17c5d9f894e2' # optional UUID string
```

If you omit this argument, the client will set your default email reply-to address for the notification.

### Response

If the request to the client is successful, you will receive the following `dict` response:

```python
{
  "id": "740e5834-3a29-46b4-9a6f-16142fde533a",
  "reference": "STRING",
  "content": {
    "subject": "SUBJECT TEXT",
    "body": "MESSAGE TEXT",
    "from_email": "SENDER EMAIL"
  },
  "uri": "https://api.notifications.service.gov.uk/v2/notifications/740e5834-3a29-46b4-9a6f-16142fde533a",
  "template": {
    "id": "f33517ff-2a88-4f6e-b855-c550268ce08a",
    "version": INTEGER,
    "uri": "https://api.notifications.service.gov.uk/v2/template/f33517ff-2a88-4f6e-b855-c550268ce08a"
  }
}
```


### Error codes

If the request is not successful, the client will raise an `HTTPError`.

|`error.status_code`|`error.message`|How to fix|
|:---|:---|:---|
|`400`|`[{`<br>`"error": "BadRequestError",`<br>`"message": "Can't send to this recipient using a team-only API key"`<br>`]}`|Use the correct type of API key. Refer to [API keys](#api-keys) for more information|
|`400`|`[{`<br>`"error": "BadRequestError",`<br>`"message": "Can't send to this recipient when service is in trial mode - see https://www.notifications.service.gov.uk/trial-mode"`<br>`}]`|Refer to [trial mode](https://www.notifications.service.gov.uk/features/using-notify#trial-mode) for more information|
|`403`|`[{`<br>`"error": "AuthError",`<br>`"message": "Error: Your system clock must be accurate to within 30 seconds"`<br>`}]`|Check your system clock|
|`403`|`[{`<br>`"error": "AuthError",`<br>`"message": "Invalid token: signature, api token not found"`<br>`}]`|Use the correct API key. Refer to [API keys](#api-keys) for more information|
|`429`|`[{`<br>`"error": "RateLimitError",`<br>`"message": "Exceeded rate limit for key type TEAM/TEST/LIVE of 3000 requests per 60 seconds"`<br>`}]`|Refer to [API rate limits](#api-rate-limits) for more information|
|`429`|`[{`<br>`"error": "TooManyRequestsError",`<br>`"message": "Exceeded send limits (LIMIT NUMBER) for today"`<br>`}]`|Refer to [service limits](#service-limits) for the limit number|
|`500`|`[{`<br>`"error": "Exception",`<br>`"message": "Internal server error"`<br>`}]`|Notify was unable to process the request, resend your notification.|

## Send a letter

When your service first signs up to GOV.UK Notify, you’ll start in trial mode. You can only send letters in live mode.

### Method

```python
    response = notifications_client.send_letter_notification(
        template_id='f33517ff-2a88-4f6e-b855-c550268ce08a', # required UUID string
        personalisation={
          'address_line_1': 'The Occupier' # required string,
          'address_line_2': '123 High Street' # required string,
          'postcode': 'SW14 6BH' # required string,
        },
    )
```

### Arguments

#### template_id (required)

The ID of the template. You can find this by signing into GOV.UK Notify and going to the __Templates__ page.

#### personalisation (required)

The personalisation argument always contains the following required parameters for the letter recipient's address:

- `address_line_1`
- `address_line_2`
- `postcode`

Any other placeholder fields included in the letter template also count as required parameters. You need to provide their values in a dictionary with key value pairs. For example:

```python
personalisation={
  'address_line_1': 'The Occupier',
  'address_line_2': '123 High Street',
  'postcode': 'SW14 6BF',
  'name': 'John Smith',
  'application_id': '4134325'
}
```

#### reference (optional)

A unique identifier. This reference can identify a single unique notification or a batch of multiple notifications.

```python
reference='STRING' # optional string - identifies notification(s)
```

#### personalisation (optional)

The following parameters in the letter recipient's address are optional:

```python
personalisation={
    'address_line_3': '123 High Street', 	
    'address_line_4': 'Richmond upon Thames', 	
    'address_line_5': 'London', 		
    'address_line_6': 'Middlesex',
}
```

### Response

If the request to the client is successful, you will receive the following `dict` response:

```python
{
  "id": "740e5834-3a29-46b4-9a6f-16142fde533a",
  "reference": 'STRING',
  "content": {
    "subject": "SUBJECT TEXT",
    "body": "LETTER TEXT",
  },
  "uri": "https://api.notifications.service.gov.uk/v2/notifications/740e5834-3a29-46b4-9a6f-16142fde533a",
  "template": {
    "id": "f33517ff-2a88-4f6e-b855-c550268ce08a",
    "version": INTEGER,
    "uri": "https://api.notifications.service.gov.uk/v2/template/f33517ff-2a88-4f6e-b855-c550268ce08a"
  }
  "scheduled_for": None
}
```

### Error codes

If the request is not successful, the client will raise an `HTTPError`.

|`error.status_code`|`error.message`|How to fix|
|:---|:---|:---|
|`400`|`[{`<br>`"error": "BadRequestError",`<br>`"message": "Cannot send letters with a team api key"`<br>`]}`|Use the correct type of API key. Refer to [API keys](#api-keys) for more information|
|`400`|`[{`<br>`"error": "BadRequestError",`<br>`"message": "Cannot send letters when service is in trial mode - see https://www.notifications.service.gov.uk/trial-mode"`<br>`}]`|Refer to [trial mode](https://www.notifications.service.gov.uk/features/using-notify#trial-mode) for more information|
|`400`|`[{`<br>`"error": "ValidationError",`<br>`"message": "personalisation address_line_1 is a required property"`<br>`}]`|Ensure that your template has a field for the first line of the address, check [personlisation](#send-a-letter-arguments-personalisation-optional) for more information.|
|`403`|`[{`<br>`"error": "AuthError",`<br>`"message": "Error: Your system clock must be accurate to within 30 seconds"`<br>`}]`|Check your system clock|
|`403`|`[{`<br>`"error": "AuthError",`<br>`"message": "Invalid token: signature, api token not found"`<br>`}]`|Use the correct API key. Refer to [API keys](#api-keys) for more information|
|`429`|`[{`<br>`"error": "RateLimitError",`<br>`"message": "Exceeded rate limit for key type TEAM/TEST/LIVE of 3000 requests per 60 seconds"`<br>`}]`|Refer to [API rate limits](#api-rate-limits) for more information|
|`429`|`[{`<br>`"error": "TooManyRequestsError",`<br>`"message": "Exceeded send limits (LIMIT NUMBER) for today"`<br>`}]`|Refer to [service limits](#service-limits) for the limit number|
|`500`|`[{`<br>`"error": "Exception",`<br>`"message": "Internal server error"`<br>`}]`|Notify was unable to process the request, resend your notification.|


# Get message status

The possible status of a message depends on the message type.

## Status - text and email

### Sending

The message is queued to be sent by the provider.

### Delivered

The message was successfully delivered.

### Failed

This covers all failure statuses:

- `permanent-failure` - "The provider was unable to deliver message, email or phone number does not exist; remove this recipient from your list"
- `temporary-failure` - "The provider was unable to deliver message, email inbox was full or phone was turned off; you can try to send the message again"
- `technical-failure` - "Notify had a technical failure; you can try to send the message again"

## Status - letter

### Failed

The only failure status that applies to letters is `technical-failure` - Notify had an unexpected error while sending to our printing provider.

### Accepted

Notify is printing and posting the letter.

## Get the status of one message

### Method

```python
response = notifications_client.get_notification_by_id(notification_id)
```

### Arguments

#### notification_id (required)

The ID of the notification.

### Response

If the request to the client is successful, you will receive the following `dict` response:

```python
{
  "id": "740e5834-3a29-46b4-9a6f-16142fde533a", # required string - notification ID
  "reference": "STRING", # optional string
  "email_address": "sender@something.com",  # required string for emails
  "phone_number": "+447900900123",  # required string for text messages
  "line_1": "ADDRESS LINE 1", # required string for letter
  "line_2": "ADDRESS LINE 2", # required string for letter
  "line_3": "ADDRESS LINE 3", # optional string for letter
  "line_4": "ADDRESS LINE 4", # optional string for letter
  "line_5": "ADDRESS LINE 5", # optional string for letter
  "line_6": "ADDRESS LINE 6", # optional string for letter
  "postcode": "STRING", # required string for letter
  "type": "sms / letter / email", # required string
  "status": "sending / delivered / permanent-failure / temporary-failure / technical-failure", # required string
  "template": {
    "Version": INTEGER
    "id": 'f33517ff-2a88-4f6e-b855-c550268ce08a' # required string - template ID
    "uri": "/v2/template/{id}/{version}", # required
  },
  "body": "STRING", # required string - body of notification
  "subject": "STRING" # required string for email - subject of email
  "created_at": "STRING", # required string - date and time notification created
  "sent_at": "STRING", # optional string - date and time notification sent to provider
  "completed_at:" "STRING" # optional string - date and time notification delivered or failed
}
```

### Error codes

If the request is not successful, the client will raise an `HTTPError`:

|`error.status_code`|`error.message`|How to fix|
|:---|:---|:---|
|`400`|`[{`<br>`"error": "ValidationError",`<br>`"message": "id is not a valid UUID"`<br>`}]`|Check the notification ID|
|`403`|`[{`<br>`"error": "AuthError",`<br>`"message": "Error: Your system clock must be accurate to within 30 seconds"`<br>`}]`|Check your system clock|
|`403`|`[{`<br>`"error": "AuthError",`<br>`"message": "Invalid token: signature, api token not found"`<br>`}]`|Use the correct API key. Refer to [API keys](#api-keys) for more information|
|`404`|`[{`<br>`"error": "NoResultFound",`<br>`"message": "No result found"`<br>`}]`|Check the notification ID|


## Get the status of all messages

This API call returns the status of all messages. You can either get the status of all messages in one call, or one page of up to 250 messages.

### Method

#### All messages

This will return all your messages with statuses. They will display in pages of up to 250 messages each.

```python
response = notifications_client.get_all_notifications(template_type, status, reference, older_than)
```

You can filter the returned messages by including the following optional arguments in the method:

- [`template_type`](#template-type-optional)
- [`status`](#status-optional)
- [`reference`](#get-the-status-of-all-messages-arguments-reference-optional)
- [`older_than`](#older-than-optional)


#### One page of up to 250 messages

This will return one page of up to 250 messages and statuses. You can get either the most recent messages, or get older messages by specifying a particular notification ID in the [`older_than`](#older-than-optional) argument.

##### Most recent messages

```python
response = get_all_notifications_iterator(status="sending")
```

You must set the [`status`](#status-optional) argument to `sending`.

##### Older messages

To get older messages:

1. Get the ID of an older notification.
1. Add the following code to your application, with the older notification ID in the [`older_than`](#older-than-optional) argument.

```python
response = get_all_notifications_iterator(status="sending",older_than="NOTIFICATION ID")
```

You must set the [`status`](#status-optional) argument to `sending`.

This method will return the next oldest messages from the specified notification ID.

### Arguments

You can omit any of these arguments to ignore these filters.

#### template_type (optional)

You can filter by:

* `email`
* `sms`
* `letter`

#### status (optional)

| status | description | text | email | letter |
|:--- |:--- |:--- |:--- |:--- |
|`sending` |The message is queued to be sent by the provider|Yes|Yes||
|`delivered`|The message was successfully delivered|Yes|Yes||
|`failed`|This will return all failure statuses:<br>- `permanent-failure`<br>- `temporary-failure`<br>- `technical-failure`|Yes|Yes||
|`permanent-failure`|The provider was unable to deliver message, email or phone number does not exist; remove this recipient from your list|Yes|Yes||
|`temporary-failure`|The provider was unable to deliver message, email inbox was full or phone was turned off; you can try to send the message again|Yes|Yes||
|`technical-failure`|Email or text message: Notify had a technical failure; you can try to send the message again. <br><br>Letter: Notify had an unexpected error while sending to our printing provider. <br><br>You can omit this argument to ignore this filter.|Yes|Yes||
|`accepted`|Notify is printing and posting the letter|||Yes|

#### reference (optional)

A unique identifier. This reference can identify a single unique notification or a batch of multiple notifications.

```python
reference='STRING' # optional string - identifies notification(s)
```

#### older_than (optional)

Input the ID of a notification into this argument. If you use this argument, the method returns the next 250 received notifications older than the given ID.

```python
older_than='740e5834-3a29-46b4-9a6f-16142fde533a' # optional string - notification ID
```

If this argument is omitted, the method returns the most recent 250 notifications.

### Response

If the request to the client is successful, you will receive a `dict` response.

#### All messages

```python
{"notifications":
  [
    {
      "id": "740e5834-3a29-46b4-9a6f-16142fde533a", # required string - notification ID
      "reference": "STRING", # optional string - client reference
      "email_address": "sender@something.com",  # required string for emails
      "phone_number": "+447900900123",  # required string for text messages
      "line_1": "ADDRESS LINE 1", # required string for letter
      "line_2": "ADDRESS LINE 2", # required string for letter
      "line_3": "ADDRESS LINE 3", # optional string for letter
      "line_4": "ADDRESS LINE 4", # optional string for letter
      "line_5": "ADDRESS LINE 5", # optional string for letter
      "line_6": "ADDRESS LINE 6", # optional string for letter
      "postcode": "STRING", # required for string letter
      "type": "sms / letter / email", # required string
      "status": "sending / delivered / permanent-failure / temporary-failure / technical-failure", # required string
      "template": {
        "version": INTEGER
        "id": 'f33517ff-2a88-4f6e-b855-c550268ce08a' # required string - template ID
        "uri": "/v2/template/{id}/{version}", # required
      },
      "body": "STRING", # required string - body of notification
      "subject": "STRING" # required string for email - subject of email
      "created_at": "STRING", # required string - date and time notification created
      "sent_at": " STRING", # optional string - date and time notification sent to provider
      "Completed_at": "STRING" # optional string - date and time notification delivered or failed
    },
    …
  ],
  "links": {
    "current": "/notifications?template_type=sms&status=delivered",
    "next": "/notifications?other_than=last_id_in_list&template_type=sms&status=delivered"
  }
}
```

#### One page of up to 250 messages

```python
<generator object NotificationsAPIClient.get_all_notifications_iterator at 0x1026c7410>
```

### Error codes

If the request is not successful, the client will raise an `HTTPError`:

|`error.status_code`|`error.message`|How to fix|
|:---|:---|:---|
|`400`|`[{`<br>`"error": "ValidationError",`<br>`"message": "bad status is not one of [created, sending, delivered, pending, failed, technical-failure, temporary-failure, permanent-failure]"`<br>`}]`|Contact the Notify team|
|`400`|`[{`<br>`"error": "ValidationError",`<br>`"message": "Apple is not one of [sms, email, letter]"`<br>`}]`|Contact the Notify team|
|`403`|`[{`<br>`"error": "AuthError",`<br>`"message": "Error: Your system clock must be accurate to within 30 seconds"`<br>`}]`|Check your system clock|
|`403`|`[{`<br>`"error": "AuthError",`<br>`"message": "Invalid token: signature, api token not found"`<br>`}]`|Use the correct API key. Refer to [API keys](#api-keys) for more information|


# Get a template

## Get a template by ID

### Method

This will return the latest version of the template.

```python
response = notifications_client.get_template(
  'f33517ff-2a88-4f6e-b855-c550268ce08a' # required string - template ID
)
```

### Arguments

#### template_id (required)

The ID of the template. You can find this by signing into GOV.UK Notify and going to the __Templates__ page.

### Response

If the request to the client is successful, you will receive a `dict` response.

```python
{
    "id": 'f33517ff-2a88-4f6e-b855-c550268ce08a' # required string - template ID
    "type": "sms / email / letter" , # required string
    "created_at": "STRING", # required string - date and time template created
    "updated_at": "STRING", # required string - date and time template last updated
    "version": INTEGER,
    "created_by": "someone@example.com", # required string
    "body": "STRING", # required string - body of notification
    "subject": "STRING" # required string for email - subject of email
}
```

### Error codes

If the request is not successful, the client will raise an `HTTPError`:

|`error.status_code`|`error.message`|How to fix|
|:---|:---|:---|
|`403`|`[{`<br>`"error": "AuthError",`<br>`"message": "Error: Your system clock must be accurate to within 30 seconds"`<br>`}]`|Check your system clock|
|`403`|`[{`<br>`"error": "AuthError",`<br>`"message": "Invalid token: signature, api token not found"`<br>`}]`|Use the correct API key. Refer to [API keys](#api-keys) for more information|
|`404`|`[{`<br>`"error": "NoResultFound",`<br>`"message": "No Result Found"`<br>`}]`|Check your [template ID](#get-a-template-by-id-arguments-template-id-required)|


## Get a template by ID and version

### Method

This will return the latest version of the template.

```python
response = notifications_client.get_template_version(
    'f33517ff-2a88-4f6e-b855-c550268ce08a' # required string - template ID
    'version': INTEGER,
)
```

### Arguments

#### template_id (required)

The ID of the template. You can find this by signing into GOV.UK Notify and going to the __Templates__ page.

#### version (required)

The version number of the template.

### Response

If the request to the client is successful, you will receive a `dict` response.

```python
{
    "id": 'f33517ff-2a88-4f6e-b855-c550268ce08a' # required string - template ID
    "type": "sms / email / letter" , # required string
    "created_at": "STRING", # required string - date and time template created
    "updated_at": "STRING", # required string - date and time template last updated
    "version": INTEGER,
    "created_by": "someone@example.com", # required string
    "body": "STRING", # required string - body of notification
    "subject": "STRING" # required string for email - subject of email
}
```

### Error codes

If the request is not successful, the client will raise an `HTTPError`:

|`error.status_code`|`error.message`|How to fix|
|:---|:---|:---|
|`403`|`[{`<br>`"error": "AuthError",`<br>`"message": "Error: Your system clock must be accurate to within 30 seconds"`<br>`}]`|Check your system clock|
|`403`|`[{`<br>`"error": "AuthError",`<br>`"message": "Invalid token: signature, api token not found"`<br>`}]`|Use the correct API key. Refer to [API keys](#api-keys) for more information|
|`404`|`[{`<br>`"error": "NoResultFound",`<br>`"message": "No Result Found"`<br>`}]`|Check your [template ID](#get-a-template-by-id-and-version-arguments-template-id-required) and [version](#version-required)|


## Get all templates

### Method

This will return the latest version of all templates.

```python
response = notifications_client.get_all_templates(
    template_type="sms / letter / email" # optional string
)
```

### Arguments

#### template_type (optional)

If omitted, the method returns all templates. Otherwise you can filter by:

- `email`
- `sms`
- `letter`

### Response

If the request to the client is successful, you will receive a `dict` response.

```python
{
    "templates": [
        {
            "id": 'f33517ff-2a88-4f6e-b855-c550268ce08a' # required string - template ID
    		"type": "sms / email / letter" , # required string
    		"created_at": "STRING", # required string - date and time template created
    		"updated_at": "STRING", # required string - date and time template last updated
    		"version": NUMBER, # required string - template version
    		"created_by": "someone@example.com", # required string
    		"body": "STRING", # required string - body of notification
    		"subject": "STRING" # required string for email - subject of email
        },
        {
            ...another template
        }
    ]
}
```

If no templates exist for a template type or there no templates for a service, you will receive a `dict` response with an empty `templates` list element:

```python
{
    "templates": []
}
```

## Generate a preview template

### Method

This will generate a preview version of a template.

```python
response = notifications_client.post_template_preview(
    'template_id'='f33517ff-2a88-4f6e-b855-c550268ce08a', # required UUID string
    personalisation={
        'KEY': 'VALUE',
        'KEY': 'VALUE',
        ...
        }, # required dict - specifies template parameters
)
```

The parameters in the personalisation argument must match the placeholder fields in the actual template. The API notification client will ignore any extra fields in the method.

### Arguments

#### template_id (required)

The ID of the template. You can find this by signing into GOV.UK Notify and going to the __Templates__ page.

#### personalisation (required)

If a template has placeholder fields for personalised information such as name or reference number, you need to provide their values in a dictionary with key value pairs. For example:

```python
personalisation={
    'first_name': 'Amala',
    'application_date': '2018-01-01',
}
```

### Response

If the request to the client is successful, you will receive a `dict` response.

```python
{
    "id": "740e5834-3a29-46b4-9a6f-16142fde533a", # required string - notification ID
    "type": "sms / email / letter" , # required string
    "version": INTEGER,
    "body": "STRING", # required string - body of notification
    "subject": "STRING" # required string for email - subject of email
}
```

### Error codes

If the request is not successful, the client will raise an `HTTPError`:

|`error.status_code`|`error.message`|Notes|
|:---|:---|:---|
|`400`|`[{`<br>`"error": "BadRequestError",`<br>`"message": "Missing personalisation: [PERSONALISATION FIELD]"`<br>`}]`|Check that the personalisation arguments in the method match the placeholder fields in the template|
|`400`|`[{`<br>`"error": "NoResultFound",`<br>`"message": "No result found"`<br>`}]`|Check the [template ID](#generate-a-preview-template-arguments-template-id-required)|
|`403`|`[{`<br>`"error": "AuthError",`<br>`"message": "Error: Your system clock must be accurate to within 30 seconds"`<br>`}]`|Check your system clock|
|`403`|`[{`<br>`"error": "AuthError",`<br>`"message": "Invalid token: signature, api token not found"`<br>`}]`|Use the correct API key. Refer to [API keys](#api-keys) for more information|


# Get received text messages

This API call returns received text messages. Depending on which method you use, you can either get all received text messages, or a page of up to 250 text messages.

## Get all received text messages

This method will return a `<generator object>` with all received text messages.

### Method

```python
response = get_received_texts_iterator()
```

### Response

If the request to the client is successful, you will receive a `<generator object>` response that will return all received text messages.

```python
<generator object NotificationsAPIClient.get_received_texts_iterator at 0x1026c7410>
```

## Get one page of received text messages

This will return one page of up to 250 text messages.  

### Method

```python
response = client.get_received_texts(older_than)
```

You can specify which text messages to receive by inputting the ID of a received text message into the [`older_than`](#get-one-page-of-received-text-messages-arguments-older-than-optional) argument.

### Arguments

#### older_than (optional)

Input the ID of a received text message into this argument. If you use this argument, the method returns the next 250 received text messages older than the given ID.

```python
older_than='740e5834-3a29-46b4-9a6f-16142fde533a' # optional string - notification ID
```

If this argument is omitted, the method returns the most recent 250 text messages.

### Response

If the request to the client is successful, you will receive a `dict` response.

```python
{
  "received_text_messages":
  [
    {
      "id": "STRING", # required string - ID of received text message
      "user_number": "STRING", # required string
      "notify_number": "STRING", # required string - receiving number
      "created_at": "STRING", # required string - date and time template created
      "service_id": "STRING", # required string - service ID
      "content": "STRING" # required string - text content
    },
    …
  ],
  "links": {
    "current": "/received-text-messages",
    "next": "/received-text-messages?other_than=last_id_in_list"
  }
}
```

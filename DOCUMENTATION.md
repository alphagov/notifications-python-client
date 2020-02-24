# Python client documentation

This documentation is for developers interested in using the GOV.UK Notify Python client to send emails, text messages or letters. Notify supports Python 3.x and 2.7.

# Set up the client

## Install the client

Run the following code in the command line:

```shell
pip install notifications-python-client
```

Refer to the [client changelog](https://github.com/alphagov/notifications-python-client/blob/master/CHANGELOG.md) for the client version number and the latest updates.

## Create a new instance of the client

Add this code to your application:

```python
from notifications_python_client.notifications import NotificationsAPIClient

notifications_client = NotificationsAPIClient(api_key)
```

To get an API key, [sign in to GOV.UK Notify](https://www.notifications.service.gov.uk/sign-in) and go to the __API integration__ page. You can find more information in the [API keys](#api-keys) section of this documentation.

# Send a message

You can use GOV.UK Notify to send text messages, emails and letters.

## Send a text message

### Method

```python
response = notifications_client.send_sms_notification(
    phone_number='+447900900123', # required string
    template_id='f33517ff-2a88-4f6e-b855-c550268ce08a', # required UUID string
)
```

### Arguments

#### phone_number (required)

The phone number of the recipient of the text message. This can be a UK or international number.

#### template_id (required)

To find the template ID:

1. [Sign in to GOV.UK Notify](https://www.notifications.service.gov.uk/sign-in).
1. Go to the __Templates__ page and select the relevant template.
1. Select __Copy template ID to clipboard__.

#### personalisation (optional)

If a template has placeholder fields for personalised information such as name or reference number, you must provide their values in a dictionary with key value pairs. For example:

```python
personalisation={
    'first_name': 'Amala',
    'application_date': '2018-01-01',
}
```

You can leave out this argument if a template does not have any placeholder fields for personalised information.

#### reference (optional)

A unique identifier you can create if necessary. This reference identifies a single unique notification or a batch of notifications. It must not contain any personal information such as name or postal address. For example:

```python
reference='STRING', # optional string - identifies notification(s)
```
You can leave out this argument if you do not have a reference.

#### sms_sender_id (optional)

A unique identifier of the sender of the text message notification.

To find the text message sender:

1. [Sign in to GOV.UK Notify](https://www.notifications.service.gov.uk/sign-in).
1. Go to the __Settings__ page.
1. In the __Text Messages__ section, select __Manage__ on the __Text Message sender__ row.

You can then either:

- copy the sender ID that you want to use and paste it into the method
- select __Change__ to change the default sender that the service will use, and select __Save__

```python
sms_sender_id='8e222534-7f05-4972-86e3-17c5d9f894e2' # optional UUID string
```

You can leave out this argument if your service only has one text message sender, or if you want to use the default sender.

### Response

If the request to the client is successful, the client returns a `dict`:

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

If you are using the [test API key](#test), all your messages will come back with a `delivered` status.

All messages sent using the [team and whitelist](#team-and-whitelist) or [live](#live) keys will appear on your dashboard.

### Error codes

If the request is not successful, the client returns an `HTTPError` containing the relevant error code.

|error.status_code|error.message|How to fix|
|:---|:---|:---|
|`400`|`[{`<br>`"error": "BadRequestError",`<br>`"message": "Can't send to this recipient using a team-only API key"`<br>`]}`|Use the correct type of [API key](#api-keys)|
|`400`|`[{`<br>`"error": "BadRequestError",`<br>`"message": "Can't send to this recipient when service is in trial mode - see https://www.notifications.service.gov.uk/trial-mode"`<br>`}]`|Your service cannot send this notification in [trial mode](https://www.notifications.service.gov.uk/features/using-notify#trial-mode)|
|`403`|`[{`<br>`"error": "AuthError",`<br>`"message": "Error: Your system clock must be accurate to within 30 seconds"`<br>`}]`|Check your system clock|
|`403`|`[{`<br>`"error": "AuthError",`<br>`"message": "Invalid token: API key not found"`<br>`}]`|Use the correct API key. Refer to [API keys](#api-keys) for more information|
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

To find the template ID:

1. [Sign in to GOV.UK Notify](https://www.notifications.service.gov.uk/sign-in).
1. Go to the __Templates__ page and select the relevant template.
1. Select __Copy template ID to clipboard__.

#### personalisation (optional)

If a template has placeholder fields for personalised information such as name or reference number, you need to provide their values in a dictionary with key value pairs. For example:

```python
personalisation={
    'first_name': 'Amala',
    'application_date': '2018-01-01',
}
```
You can leave out this argument if a template does not have any placeholder fields for personalised information.

#### reference (optional)

A unique identifier you can create if necessary. This reference identifies a single unique notification or a batch of notifications. It must not contain any personal information such as name or postal address. For example:

```python
reference='STRING', # optional string - identifies notification(s)
```

You can leave out this argument if you do not have a reference.

#### email_reply_to_id (optional)

This is an email address specified by you to receive replies from your users. You must add at least one reply-to email address before your service can go live.

To add a reply-to email address:

1. [Sign in to GOV.UK Notify](https://www.notifications.service.gov.uk/sign-in).
1. Go to the __Settings__ page.
1. In the __Email__ section, select __Manage__ on the __Reply-to email addresses__ row.
1. Select __Add reply-to address__.
1. Enter the email address you want to use, and select __Add__.

For example:

```python
email_reply_to_id='8e222534-7f05-4972-86e3-17c5d9f894e2' # optional UUID string
```

You can leave out this argument if your service only has one reply-to email address, or you want to use the default email address.

## Send a file by email

To send a file by email, add a placeholder to the template then upload a file. The placeholder will contain a secure link to download the file.

The links are unique and unguessable. GOV.UK Notify cannot access or decrypt your file.

#### Add contact details to the file download page

1. [Sign in to GOV.UK Notify](https://www.notifications.service.gov.uk/sign-in).
1. Go to the __Settings__ page.
1. In the __Email__ section, select __Manage__ on the __Send files by email__ row.
1. Enter the contact details you want to use, and select __Save__.

#### Add a placeholder to the template

1. [Sign in to GOV.UK Notify](https://www.notifications.service.gov.uk/sign-in).
1. Go to the __Templates__ page and select the relevant email template.
1. Select __Edit__.
1. Add a placeholder to the email template using double brackets. For example:

"Download your file at: ((link_to_file))"

#### Upload your file

The file you upload must be a PDF, CSV, text file or Microsoft Word document smaller than 2MB. [Contact the GOV.UK Notify team](https://www.notifications.service.gov.uk/support/ask-question-give-feedback) if you need to send other file types.

Pass the file object as a value into the personalisation argument. For example:

```python
from notifications_python_client import prepare_upload

with open('file.pdf', 'rb') as f:
    ...
    personalisation={
      'first_name': 'Amala',
      'application_date': '2018-01-01',
      'link_to_file': prepare_upload(f),
    }
```

### Response

If the request to the client is successful, the client returns a `dict`:

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

If the request is not successful, the client returns an `HTTPError` containing the relevant error code.

|error.status_code|error.message|How to fix|
|:---|:---|:---|
|`400`|`[{`<br>`"error": "BadRequestError",`<br>`"message": "Can't send to this recipient using a team-only API key"`<br>`]}`|Use the correct type of [API key](#api-keys)|
|`400`|`[{`<br>`"error": "BadRequestError",`<br>`"message": "Can't send to this recipient when service is in trial mode - see https://www.notifications.service.gov.uk/trial-mode"`<br>`}]`|Your service cannot send this notification in [trial mode](https://www.notifications.service.gov.uk/features/using-notify#trial-mode)|
|`400`|`[{`<br>`"error": "BadRequestError",`<br>`"message": "Unsupported file type '(FILE TYPE)'. Supported types are: '(ALLOWED TYPES)'"`<br>`}]`|Wrong file type. You can only upload .pdf, .csv, .txt, .doc or .docx files|
|`400`|`[{`<br>`"error": "BadRequestError",`<br>`"message": "File did not pass the virus scan"`<br>`}]`|The file contains a virus|
|`400`|`[{`<br>`"error": "BadRequestError",`<br>`"message": "Service is not allowed to send documents"`<br>`}]`|Contact the GOV.UK Notify team|
|`403`|`[{`<br>`"error": "AuthError",`<br>`"message": "Error: Your system clock must be accurate to within 30 seconds"`<br>`}]`|Check your system clock|
|`403`|`[{`<br>`"error": "AuthError",`<br>`"message": "Invalid token: API key not found"`<br>`}]`|Use the correct API key. Refer to [API keys](#api-keys) for more information|
|`429`|`[{`<br>`"error": "RateLimitError",`<br>`"message": "Exceeded rate limit for key type TEAM/TEST/LIVE of 3000 requests per 60 seconds"`<br>`}]`|Refer to [API rate limits](#api-rate-limits) for more information|
|`429`|`[{`<br>`"error": "TooManyRequestsError",`<br>`"message": "Exceeded send limits (LIMIT NUMBER) for today"`<br>`}]`|Refer to [service limits](#service-limits) for the limit number|
|`500`|`[{`<br>`"error": "Exception",`<br>`"message": "Internal server error"`<br>`}]`|Notify was unable to process the request, resend your notification.|
|-|`ValueError('File is larger than 2MB')`|The file is too big. Files must be smaller than 2MB.|

## Send a letter

When you add a new service it will start in [trial mode](https://www.notifications.service.gov.uk/features/trial-mode). You can only send letters when your service is live.

To send Notify a request to go live:

1. [Sign in to GOV.UK Notify](https://www.notifications.service.gov.uk/sign-in).
1. Go to the __Settings__ page.
1. In the __Your service is in trial mode__ section, select __request to go live__.

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

To find the template ID:

1. [Sign in to GOV.UK Notify](https://www.notifications.service.gov.uk/sign-in).
1. Go to the __Templates__ page and select the relevant template.
1. Select __Copy template ID to clipboard__.

#### personalisation (required)

The personalisation argument always contains the following required parameters for the letter recipient’s address:

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

A unique identifier you can create if necessary. This reference identifies a single unique notification or a batch of notifications. It must not contain any personal information such as name or postal address. For example:

```python
reference='STRING' # optional string - identifies notification(s)
```

#### personalisation (optional)

The following parameters in the letter recipient’s address are optional:

```python
personalisation={
    'address_line_3': '123 High Street',
    'address_line_4': 'Richmond upon Thames',
    'address_line_5': 'London',
    'address_line_6': 'Middlesex',
}
```

### Response

If the request to the client is successful, the client returns a `dict`:

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

If the request is not successful, the client returns an `HTTPError` containing the relevant error code.

|error.status_code|error.message|How to fix|
|:---|:---|:---|
|`400`|`[{`<br>`"error": "BadRequestError",`<br>`"message": "Cannot send letters with a team api key"`<br>`]}`|Use the correct type of [API key](#api-keys)|
|`400`|`[{`<br>`"error": "BadRequestError",`<br>`"message": "Cannot send letters when service is in trial mode - see https://www.notifications.service.gov.uk/trial-mode"`<br>`}]`|Your service cannot send this notification in  [trial mode](https://www.notifications.service.gov.uk/features/using-notify#trial-mode)|
|`400`|`[{`<br>`"error": "ValidationError",`<br>`"message": "personalisation address_line_1 is a required property"`<br>`}]`|Ensure that your template has a field for the first line of the address, check [personalisation](#send-a-letter-arguments-personalisation-optional) for more information.|
|`403`|`[{`<br>`"error": "AuthError",`<br>`"message": "Error: Your system clock must be accurate to within 30 seconds"`<br>`}]`|Check your system clock|
|`403`|`[{`<br>`"error": "AuthError",`<br>`"message": "Invalid token: API key not found"`<br>`}]`|Use the correct API key. Refer to [API keys](#api-keys) for more information|
|`429`|`[{`<br>`"error": "RateLimitError",`<br>`"message": "Exceeded rate limit for key type TEAM/TEST/LIVE of 3000 requests per 60 seconds"`<br>`}]`|Refer to [API rate limits](#api-rate-limits) for more information|
|`429`|`[{`<br>`"error": "TooManyRequestsError",`<br>`"message": "Exceeded send limits (LIMIT NUMBER) for today"`<br>`}]`|Refer to [service limits](#service-limits) for the limit number|
|`500`|`[{`<br>`"error": "Exception",`<br>`"message": "Internal server error"`<br>`}]`|Notify was unable to process the request, resend your notification.|


## Send a precompiled letter

### Method

```python
response = notifications_client.send_precompiled_letter_notification(
    reference,      # Reference to identify the notification
    pdf_file,       # PDF File object
    postage         # set postage on your precompiled letter
)
```

### Arguments

#### reference (required)

A unique identifier you create. This reference identifies a single unique notification or a batch of notifications. It must not contain any personal information such as name or postal address.

#### pdf_file (required)

The precompiled letter must be a PDF file which meets [the GOV.UK Notify PDF letter specification](https://docs.notifications.service.gov.uk/documentation/images/notify-pdf-letter-spec-v2.4.pdf).

```python
with open("path/to/pdf_file", "rb") as pdf_file:
    notification = notifications_client.send_precompiled_letter_notification(
        reference="your reference", pdf_file=pdf_file
    )
```

#### postage (optional)

You can choose first or second class postage for your precompiled letter. Set the value to `first` for first class, or `second` for second class. If you do not pass in this argument, the postage will default to second class.



### Response

If the request to the client is successful, the client returns a `dict`:

```python
{
  "id": "740e5834-3a29-46b4-9a6f-16142fde533a",
  "reference": "your-letter-reference",
  "postage": "postage-you-have-set-or-None"
}
```

### Error codes

If the request is not successful, the client returns an HTTPError containing the relevant error code.

|error.status_code|error.message|How to fix|
|:---|:---|:---|
|`400`|`[{`<br>`"error": "BadRequestError",`<br>`"message": "Cannot send letters with a team api key"`<br>`]}`|Use the correct type of [API key](#api-keys)|
|`400`|`[{`<br>`"error": "BadRequestError",`<br>`"message": "Letter content is not a valid PDF"`<br>`]}`|PDF file format is required|
|`400`|`[{`<br>`"error": "BadRequestError",`<br>`"message": "Cannot send letters when service is in trial mode - see https://www.notifications.service.gov.uk/trial-mode"`<br>`}]`|Your service cannot send this notification in [trial mode](https://www.notifications.service.gov.uk/features/using-notify#trial-mode)|
|`400`|`[{`<br>`"error": "ValidationError",`<br>`"message": "reference is a required property"`<br>`}]`|Add a `reference` argument to the method call|
|`400`|`[{`<br>`"error": "ValidationError",`<br>`"message": "postage invalid. It must be either first or second."`<br>`}]`|Change the value of `postage` argument in the method call to either 'first' or 'second'|
|`429`|`[{`<br>`"error": "RateLimitError",`<br>`"message": "Exceeded rate limit for key type live of 10 requests per 20 seconds"`<br>`}]`|Use the correct API key. Refer to [API keys](#api-keys) for more information|
|`429`|`[{`<br>`"error": "TooManyRequestsError",`<br>`"message": "Exceeded send limits (50) for today"`<br>`}]`|Refer to [service limits](#service-limits) for the limit number|

# Get message status

Message status depends on the type of message you have sent.

You can only get the status of messages that are 7 days old or newer.

## Status - text and email

|Status|Information|
|:---|:---|
|Created|GOV.UK Notify has placed the message in a queue, ready to be sent to the provider. It should only remain in this state for a few seconds.|
|Sending|GOV.UK Notify has sent the message to the provider. The provider will try to deliver the message to the recipient for up to 72 hours. GOV.UK Notify is waiting for delivery information.|
|Delivered|The message was successfully delivered.|
|Failed|This covers all failure statuses:<br>- `permanent-failure` - "The provider could not deliver the message because the email address or phone number was wrong. You should remove these email addresses or phone numbers from your database. You’ll still be charged for text messages to numbers that do not exist."<br>- `temporary-failure` - "The provider could not deliver the message. This can happen when the recipient’s inbox is full or their phone is off. You can try to send the message again. You’ll still be charged for text messages to phones that are not accepting messages."<br>- `technical-failure` - "Your message was not sent because there was a problem between Notify and the provider.<br>You’ll have to try sending your messages again. You will not be charged for text messages that are affected by a technical failure."|

## Status - text only

|Status|Information|
|:---|:---|
|Pending|GOV.UK Notify is waiting for more delivery information.<br>GOV.UK Notify received a callback from the provider but the recipient's device has not yet responded. Another callback from the provider determines the final status of the notification.|
|Sent / Sent internationally|The message was sent to an international number. The mobile networks in some countries do not provide any more delivery information. The GOV.UK Notify client API returns this status as `sent`. The GOV.UK Notify client app returns this status as `Sent internationally`.|

## Status - letter

|Status|information|
|:---|:---|
|Failed|The only failure status that applies to letters is `technical-failure`. GOV.UK Notify had an unexpected error while sending to our printing provider.|
|Accepted|GOV.UK Notify has sent the letter to the provider to be printed.|
|Received|The provider has printed and dispatched the letter.|

## Status - precompiled letter

|Status|information|
|:---|:---|
|Pending virus check|GOV.UK Notify has not completed a virus scan of the precompiled letter file.|
|Virus scan failed|GOV.UK Notify found a potential virus in the precompiled letter file.|
|Validation failed|Content in the precompiled letter file is outside the printable area. See the [GOV.UK Notify PDF letter specification](https://docs.notifications.service.gov.uk/documentation/images/notify-pdf-letter-spec-v2.3.pdf) for more information.|

## Get the status of one message

### Method

```python
response = notifications_client.get_notification_by_id(notification_id)
```

### Arguments

#### notification_id (required)

The ID of the notification. You can find the notification ID in the response to the [original notification method call](#get-the-status-of-one-message-response).

You can also find it by [signing in to GOV.UK Notify](https://www.notifications.service.gov.uk/sign-in) and going to the __API integration__ page.

### Response

If the request to the client is successful, the client will return a `dict`:

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
  "created_by_name": "STRING", # optional string - name of the person who sent the notification if sent manually
  "sent_at": "STRING", # optional string - date and time notification sent to provider
  "completed_at:" "STRING" # optional string - date and time notification delivered or failed
}
```

### Error codes

If the request is not successful, the client will return an `HTTPError` containing the relevant error code:

|error.status_code|error.message|How to fix|
|:---|:---|:---|
|`400`|`[{`<br>`"error": "ValidationError",`<br>`"message": "id is not a valid UUID"`<br>`}]`|Check the notification ID|
|`403`|`[{`<br>`"error": "AuthError",`<br>`"message": "Error: Your system clock must be accurate to within 30 seconds"`<br>`}]`|Check your system clock|
|`403`|`[{`<br>`"error": "AuthError",`<br>`"message": "Invalid token: API key not found"`<br>`}]`|Use the correct API key. Refer to [API keys](#api-keys) for more information|
|`404`|`[{`<br>`"error": "NoResultFound",`<br>`"message": "No result found"`<br>`}]`|Check the notification ID|


## Get the status of multiple messages

This API call returns one page of up to 250 messages and statuses. You can get either the most recent messages, or get older messages by specifying a particular notification ID in the `older_than` argument.

You can only get the status of messages that are 7 days old or newer.

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

| status | description | text | email | letter |Precompiled letter|
|:--- |:--- |:--- |:--- |:--- |:--- |
|created|GOV.UK Notify has placed the message in a queue, ready to be sent to the provider. It should only remain in this state for a few seconds.|Yes|Yes|||
|sending|GOV.UK Notify has sent the message to the provider. The provider will try to deliver the message to the recipient for up to 72 hours. GOV.UK Notify is waiting for delivery information.|Yes|Yes|||
|delivered|The message was successfully delivered|Yes|Yes|||
|sent / sent internationally|The message was sent to an international number. The mobile networks in some countries do not provide any more delivery information.|Yes||||
|pending|GOV.UK Notify is waiting for more delivery information.<br>GOV.UK Notify received a callback from the provider but the recipient's device has not yet responded. Another callback from the provider determines the final status of the notification.|Yes||||
|failed|This returns all failure statuses:<br>- permanent-failure<br>- temporary-failure<br>- technical-failure|Yes|Yes|||
|permanent-failure|The provider could not deliver the message because the email address or phone number was wrong. You should remove these email addresses or phone numbers from your database. You’ll still be charged for text messages to numbers that do not exist.|Yes|Yes|||
|temporary-failure|The provider could not deliver the message. This can happen when the recipient’s inbox is full or their phone is off. You can try to send the message again. You’ll still be charged for text messages to phones that are not accepting messages.|Yes|Yes|||
|technical-failure|Email / Text: Your message was not sent because there was a problem between Notify and the provider.<br>You’ll have to try sending your messages again. You will not be charged for text messages that are affected by a technical failure. <br><br>Letter: Notify had an unexpected error while sending to our printing provider. <br><br>You can leave out this argument to ignore this filter.|Yes|Yes|||
|accepted|GOV.UK Notify has sent the letter to the provider to be printed.|||Yes||
|received|The provider has printed and dispatched the letter.|||Yes||
|pending-virus-check|GOV.UK Notify is scanning the precompiled letter file for viruses.||||Yes|
|virus-scan-failed|GOV.UK Notify found a potential virus in the precompiled letter file.||||Yes|
|validation-failed|Content in the precompiled letter file is outside the printable area.||||Yes|

#### reference (optional)

A unique identifier you can create if necessary. This reference identifies a single unique notification or a batch of notifications. It must not contain any personal information such as name or postal address. For example:

```python
reference='STRING' # optional string - identifies notification(s)
```

#### older_than (optional)

Input the ID of a notification into this argument. If you use this argument, the method returns the next 250 received notifications older than the given ID.

```python
older_than='740e5834-3a29-46b4-9a6f-16142fde533a' # optional string - notification ID
```

If you leave out this argument, the method returns the most recent 250 notifications.

The client only returns notifications that are 7 days old or newer. If the notification specified in this argument is older than 7 days, the client returns an empty response.

### Response

If the request to the client is successful, the client returns a `dict`.

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
      "created_by_name": "STRING", # optional string - name of the person who sent the notification if sent manually
      "sent_at": " STRING", # optional string - date and time notification sent to provider
      "completed_at": "STRING" # optional string - date and time notification delivered or failed
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

If the request is not successful, the client returns an `HTTPError` containing the relevant error code:

|error.status_code|error.message|How to fix|
|:---|:---|:---|
|`400`|`[{`<br>`"error": "ValidationError",`<br>`"message": "bad status is not one of [created, sending, delivered, pending, failed, technical-failure, temporary-failure, permanent-failure]"`<br>`}]`|Contact the GOV.UK Notify team|
|`400`|`[{`<br>`"error": "ValidationError",`<br>`"message": "Apple is not one of [sms, email, letter]"`<br>`}]`|Contact the GOV.UK Notify team|
|`403`|`[{`<br>`"error": "AuthError",`<br>`"message": "Error: Your system clock must be accurate to within 30 seconds"`<br>`}]`|Check your system clock|
|`403`|`[{`<br>`"error": "AuthError",`<br>`"message": "Invalid token: API key not found"`<br>`}]`|Use the correct API key. Refer to [API keys](#api-keys) for more information|


## Get a PDF for a letter notification

### Method

This returns the PDF contents of a letter notification.

```python
pdf_file = notifications_client.get_pdf_for_letter(
  'f33517ff-2a88-4f6e-b855-c550268ce08a' # required string - notification ID
)
```

### Arguments

#### notification_id (required)

The ID of the notification. You can find the notification ID in the response to the [original notification method call](#get-the-status-of-one-message-response).

You can also find it by [signing in to GOV.UK Notify](https://www.notifications.service.gov.uk/sign-in) and going to the __API integration__ page.

### Response

If the request to the client is successful, the client will return a `io.BytesIO` object containing the raw PDF data.

### Error codes

If the request is not successful, the client will return an `HTTPError` containing the relevant error code:

|error.status_code|error.message|How to fix|
|:---|:---|:---|
|`400`|`[{`<br>`"error": "ValidationError",`<br>`"message": "id is not a valid UUID"`<br>`}]`|Check the notification ID|
|`400`|`[{`<br>`"error": "PDFNotReadyError",`<br>`"message": "PDF not available yet, try again later"`<br>`}]`|Wait for the notification to finish processing. This usually takes a few seconds|
|`400`|`[{`<br>`"error": "BadRequestError",`<br>`"message": "File did not pass the virus scan"`<br>`}]`|You cannot retrieve the contents of a letter notification that contains a virus|
|`400`|`[{`<br>`"error": "BadRequestError",`<br>`"message": "PDF not available for letters in technical-failure"`<br>`}]`|You cannot retrieve the contents of a letter notification in technical-failure|
|`400`|`[{`<br>`"error": "ValidationError",`<br>`"message": "Notification is not a letter"`<br>`}]`|Check that you are looking up the correct notification|
|`403`|`[{`<br>`"error": "AuthError",`<br>`"message": "Error: Your system clock must be accurate to within 30 seconds"`<br>`}]`|Check your system clock|
|`403`|`[{`<br>`"error": "AuthError",`<br>`"message": "Invalid token: API key not found"`<br>`}]`|Use the correct API key. Refer to [API keys](#api-keys) for more information|
|`404`|`[{`<br>`"error": "NoResultFound",`<br>`"message": "No result found"`<br>`}]`|Check the notification ID|

# Get a template

## Get a template by ID

### Method

This returns the latest version of the template.

```python
response = notifications_client.get_template(
  'f33517ff-2a88-4f6e-b855-c550268ce08a' # required string - template ID
)
```

### Arguments

#### template_id (required)

The ID of the template. [Sign in to GOV.UK Notify](https://www.notifications.service.gov.uk/sign-in) and go to the __Templates__ page to find it.

### Response

If the request to the client is successful, the client returns a `dict`.

```python
{
    "id": 'f33517ff-2a88-4f6e-b855-c550268ce08a', # required string - template ID
    "name": "STRING", # required string - template name
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

If the request is not successful, the client returns an `HTTPError` containing the relevant error code:

|error.status_code|error.message|How to fix|
|:---|:---|:---|
|`403`|`[{`<br>`"error": "AuthError",`<br>`"message": "Error: Your system clock must be accurate to within 30 seconds"`<br>`}]`|Check your system clock|
|`403`|`[{`<br>`"error": "AuthError",`<br>`"message": "Invalid token: API key not found"`<br>`}]`|Use the correct API key. Refer to [API keys](#api-keys) for more information|
|`404`|`[{`<br>`"error": "NoResultFound",`<br>`"message": "No Result Found"`<br>`}]`|Check your [template ID](#get-a-template-by-id-arguments-template-id-required)|


## Get a template by ID and version

### Method

```python
response = notifications_client.get_template_version(
    'f33517ff-2a88-4f6e-b855-c550268ce08a' # required string - template ID
    'version': INTEGER,
)
```

### Arguments

#### template_id (required)

The ID of the template. [Sign in to GOV.UK Notify](https://www.notifications.service.gov.uk/sign-in) and go to the __Templates__ page to find it.

#### version (required)

The version number of the template.

### Response

If the request to the client is successful, the client returns a `dict`.

```python
{
    "id": 'f33517ff-2a88-4f6e-b855-c550268ce08a', # required string - template ID
    "name": "STRING", # required string - template name
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

If the request is not successful, the client returns an `HTTPError` containing the relevant error code:

|error.status_code|error.message|How to fix|
|:---|:---|:---|
|`403`|`[{`<br>`"error": "AuthError",`<br>`"message": "Error: Your system clock must be accurate to within 30 seconds"`<br>`}]`|Check your system clock|
|`403`|`[{`<br>`"error": "AuthError",`<br>`"message": "Invalid token: API key not found"`<br>`}]`|Use the correct API key. Refer to [API keys](#api-keys) for more information|
|`404`|`[{`<br>`"error": "NoResultFound",`<br>`"message": "No Result Found"`<br>`}]`|Check your [template ID](#get-a-template-by-id-and-version-arguments-template-id-required) and [version](#version-required)|


## Get all templates

### Method

This returns the latest version of all templates.

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

If the request to the client is successful, the client returns a `dict`.

```python
{
    "templates": [
        {
            "id": 'f33517ff-2a88-4f6e-b855-c550268ce08a', # required string - template ID
            "name": "STRING", # required string - template name
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

If no templates exist for a template type or there no templates for a service, the client returns a `dict` with an empty `templates` list element:

```python
{
    "templates": []
}
```

## Generate a preview template

### Method

This generates a preview version of a template.

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

The ID of the template. [Sign in to GOV.UK Notify](https://www.notifications.service.gov.uk/sign-in) and go to the __Templates__ page to find it.

#### personalisation (required)

If a template has placeholder fields for personalised information such as name or reference number, you need to provide their values in a dictionary with key value pairs. For example:

```python
personalisation={
    'first_name': 'Amala',
    'application_date': '2018-01-01',
}
```

### Response

If the request to the client is successful, you receive a `dict` response.

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

If the request is not successful, the client returns an `HTTPError` containing the relevant error code:

|error.status_code|error.message|Notes|
|:---|:---|:---|
|`400`|`[{`<br>`"error": "BadRequestError",`<br>`"message": "Missing personalisation: [PERSONALISATION FIELD]"`<br>`}]`|Check that the personalisation arguments in the method match the placeholder fields in the template|
|`400`|`[{`<br>`"error": "NoResultFound",`<br>`"message": "No result found"`<br>`}]`|Check the [template ID](#generate-a-preview-template-arguments-template-id-required)|
|`403`|`[{`<br>`"error": "AuthError",`<br>`"message": "Error: Your system clock must be accurate to within 30 seconds"`<br>`}]`|Check your system clock|
|`403`|`[{`<br>`"error": "AuthError",`<br>`"message": "Invalid token: API key not found"`<br>`}]`|Use the correct API key. Refer to [API keys](#api-keys) for more information|


# Get received text messages

This API call returns one page of up to 250 received text messages. You can get either the most recent messages, or get older messages by specifying a particular notification ID in the older_than argument.

You can only get the status of messages that are 7 days old or newer.

## Get all received text messages

This method returns a `<generator object>` with all received text messages.

### Method

```python
response = get_received_texts_iterator()
```

### Response

If the request to the client is successful, the client will return a `<generator object>` that will return all received text messages.

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

If the request to the client is successful, the client returns a `dict`.

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

### Error codes

If the request is not successful, the client returns an `HTTPError` containing the relevant error code.

|error.status_code|error.message|How to fix|
|:---|:---|:---|
|`403`|`[{`<br>`"error": "AuthError",`<br>`"message": "Error: Your system clock must be accurate to within 30 seconds"`<br>`}]`|Check your system clock|
|`403`|`[{`<br>`"error": "AuthError",`<br>`"message": "Invalid token: API key not found"`<br>`}]`|Use the correct API key. Refer to [API keys](#api-keys) for more information|

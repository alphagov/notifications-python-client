# Python client documentation

This documentation is for developers interested in using the GOV.UK Notify Python client to send emails, text messages or letters. Notify supports Python 3.x and 2.7.

## Set up the client

### Install the client

Run the following code in the command line:

```shell
pip install notifications-python-client
```

Refer to the [client changelog](https://github.com/alphagov/notifications-python-client/blob/master/CHANGELOG.md) for the client version number and the latest updates.

### Create a new instance of the client

Add this code to your application:

```python
from notifications_python_client.notifications import NotificationsAPIClient

notifications_client = NotificationsAPIClient(api_key)
```

To get an API key, [sign in to GOV.UK Notify](https://www.notifications.service.gov.uk/sign-in) and go to the __API integration__ page. You can find more information in the [API keys](#api-keys) section of this documentation.

## Send a message

You can use GOV.UK Notify to send text messages, emails and letters.

### Send a text message

#### Method

```python
response = notifications_client.send_sms_notification(
    phone_number='+447900900123', # required string
    template_id='f33517ff-2a88-4f6e-b855-c550268ce08a', # required UUID string
)
```

#### Arguments

##### phone_number (required)

The phone number of the recipient of the text message. This can be a UK or international number.

##### template_id (required)

To find the template ID:

1. [Sign in to GOV.UK Notify](https://www.notifications.service.gov.uk/sign-in).
1. Go to the __Templates__ page and select the relevant template.
1. Select __Copy template ID to clipboard__.

##### personalisation (optional)

If a template has placeholder fields for personalised information such as name or reference number, you must provide their values in a dictionary with key value pairs. For example:

```python
personalisation={
    'first_name': 'Amala',
    'application_date': '2018-01-01',
}
```

You can leave out this argument if a template does not have any placeholder fields for personalised information.

##### reference (optional)

A unique identifier you can create if necessary. This reference identifies a single unique message or a batch of messages. It must not contain any personal information such as name or postal address. For example:

```python
reference='STRING', # optional string - identifies notification(s)
```
You can leave out this argument if you do not have a reference.

##### sms_sender_id (optional)

A unique identifier of the sender of the text message.

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

#### Response

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

All messages sent using the [team and guest list](#team-and-guest-list) or [live](#live) keys will appear on your dashboard.

#### Error codes

If the request is not successful, the client returns an `HTTPError` containing the relevant error code.

|error.status_code|error.message|How to fix|
|:---|:---|:---|
|`400`|`[{`<br>`"error": "BadRequestError",`<br>`"message": "Can't send to this recipient using a team-only API key"`<br>`}]`|Use the correct type of [API key](#api-keys)|
|`400`|`[{`<br>`"error": "BadRequestError",`<br>`"message": "Can't send to this recipient when service is in trial mode - see https://www.notifications.service.gov.uk/trial-mode"`<br>`}]`|Your service cannot send this text message in [trial mode](https://www.notifications.service.gov.uk/features/using-notify#trial-mode)|
|`403`|`[{`<br>`"error": "AuthError",`<br>`"message": "Error: Your system clock must be accurate to within 30 seconds"`<br>`}]`|Check your system clock|
|`403`|`[{`<br>`"error": "AuthError",`<br>`"message": "Invalid token: API key not found"`<br>`}]`|Use the correct API key. Refer to [API keys](#api-keys) for more information|
|`429`|`[{`<br>`"error": "RateLimitError",`<br>`"message": "Exceeded rate limit for key type TEAM/TEST/LIVE of 3000 requests per 60 seconds"`<br>`}]`|Refer to [API rate limits](#rate-limits) for more information|
|`429`|`[{`<br>`"error": "TooManyRequestsError",`<br>`"message": "Exceeded send limits (LIMIT NUMBER) for today"`<br>`}]`|Refer to [service limits](#daily-limits) for the limit number|
|`500`|`[{`<br>`"error": "Exception",`<br>`"message": "Internal server error"`<br>`}]`|Notify was unable to process the request, resend your text message.|

### Send an email

#### Method

```python
response = notifications_client.send_email_notification(
    email_address='sender@something.com', # required string
    template_id='f33517ff-2a88-4f6e-b855-c550268ce08a', # required UUID string
)
```

#### Arguments

##### email_address (required)

The email address of the recipient.

##### template_id (required)

To find the template ID:

1. [Sign in to GOV.UK Notify](https://www.notifications.service.gov.uk/sign-in).
1. Go to the __Templates__ page and select the relevant template.
1. Select __Copy template ID to clipboard__.

##### personalisation (optional)

If a template has placeholder fields for personalised information such as name or reference number, you need to provide their values in a dictionary with key value pairs. For example:

```python
personalisation={
    'first_name': 'Amala',
    'application_date': '2018-01-01',
}
```
You can leave out this argument if a template does not have any placeholder fields for personalised information.

##### reference (optional)

A unique identifier you can create if necessary. This reference identifies a single unique email or a batch of emails. It must not contain any personal information such as name or postal address. For example:

```python
reference='STRING', # optional string - identifies notification(s)
```

You can leave out this argument if you do not have a reference.

##### email_reply_to_id (optional)

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

### Send a file by email

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

You can upload PDF, CSV, .odt, .txt, .rtf and MS Word Document files. Your file must be smaller than 2MB. [Contact the GOV.UK Notify team](https://www.notifications.service.gov.uk/support/ask-question-give-feedback) if you need to send other file types.

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

##### CSV Files

Uploads for CSV files should use the `is_csv` parameter
on the `prepare_upload()` utility.  For example:

```python
from notifications_python_client import prepare_upload

with open('file.csv', 'rb') as f:
    ...
    personalisation={
      'first_name': 'Amala',
      'application_date': '2018-01-01',
      'link_to_file': prepare_upload(f, is_csv=True),
    }
```

#### Response

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

#### Error codes

If the request is not successful, the client returns an `HTTPError` containing the relevant error code.

|error.status_code|error.message|How to fix|
|:---|:---|:---|
|`400`|`[{`<br>`"error": "BadRequestError",`<br>`"message": "Can't send to this recipient using a team-only API key"`<br>`}]`|Use the correct type of [API key](#api-keys)|
|`400`|`[{`<br>`"error": "BadRequestError",`<br>`"message": "Can't send to this recipient when service is in trial mode - see https://www.notifications.service.gov.uk/trial-mode"`<br>`}]`|Your service cannot send this email in [trial mode](https://www.notifications.service.gov.uk/features/using-notify#trial-mode)|
|`400`|`[{`<br>`"error": "BadRequestError",`<br>`"message": "Unsupported file type '(FILE TYPE)'. Supported types are: '(ALLOWED TYPES)'"`<br>`}]`|Wrong file type. You can only upload .pdf, .csv, .txt, .doc, .docx, .rtf or .odt files|
|`400`|`[{`<br>`"error": "BadRequestError",`<br>`"message": "File did not pass the virus scan"`<br>`}]`|The file contains a virus|
|`400`|`[{`<br>`"error": "BadRequestError",`<br>`"message": "Send files by email has not been set up - add contact details for your service at https://www.notifications.service.gov.uk/services/(SERVICE ID)/service-settings/send-files-by-email"`<br>`}]`|See how to [add contact details to the file download page](#add-contact-details-to-the-file-download-page)|
|`403`|`[{`<br>`"error": "AuthError",`<br>`"message": "Error: Your system clock must be accurate to within 30 seconds"`<br>`}]`|Check your system clock|
|`403`|`[{`<br>`"error": "AuthError",`<br>`"message": "Invalid token: API key not found"`<br>`}]`|Use the correct API key. Refer to [API keys](#api-keys) for more information|
|`429`|`[{`<br>`"error": "RateLimitError",`<br>`"message": "Exceeded rate limit for key type TEAM/TEST/LIVE of 3000 requests per 60 seconds"`<br>`}]`|Refer to [API rate limits](#rate-limits) for more information|
|`429`|`[{`<br>`"error": "TooManyRequestsError",`<br>`"message": "Exceeded send limits (LIMIT NUMBER) for today"`<br>`}]`|Refer to [service limits](#daily-limits) for the limit number|
|`500`|`[{`<br>`"error": "Exception",`<br>`"message": "Internal server error"`<br>`}]`|Notify was unable to process the request, resend your email.|
|-|`ValueError('File is larger than 2MB')`|The file is too big. Files must be smaller than 2MB.|

### Send a letter

When you add a new service it will start in [trial mode](https://www.notifications.service.gov.uk/features/trial-mode). You can only send letters when your service is live.

To send Notify a request to go live:

1. [Sign in to GOV.UK Notify](https://www.notifications.service.gov.uk/sign-in).
1. Go to the __Settings__ page.
1. In the __Your service is in trial mode__ section, select __request to go live__.

#### Method

```python
    response = notifications_client.send_letter_notification(
        template_id='f33517ff-2a88-4f6e-b855-c550268ce08a', # required UUID string
        personalisation={
          'address_line_1': 'The Occupier' # required string,
          'address_line_2': '123 High Street' # required string,
          'address_line_3': 'SW14 6BH' # required string,
        },
    )
```

#### Arguments

##### template_id (required)

To find the template ID:

1. [Sign in to GOV.UK Notify](https://www.notifications.service.gov.uk/sign-in).
1. Go to the __Templates__ page and select the relevant template.
1. Select __Copy template ID to clipboard__.

##### personalisation (required)

The personalisation argument always contains the following parameters for the letter recipient’s address:

- `address_line_1`
- `address_line_2`
- `address_line_3`
- `address_line_4`
- `address_line_5`
- `address_line_6`
- `address_line_7`

The address must have at least 3 lines.

The last line needs to be a real UK postcode or the name of a country outside the UK.

Notify checks for international addresses and will automatically charge you the correct postage.

The `postcode` personalisation argument has been replaced. If your template still uses `postcode`, Notify will treat it as the last line of the address.

Any other placeholder fields included in the letter template also count as required parameters. You need to provide their values in a dictionary with key value pairs. For example:

```python
personalisation={
  'address_line_1': 'The Occupier',
  'address_line_2': '123 High Street',
  'address_line_3': 'Richmond upon Thames',
  'address_line_4': 'Middlesex',
  'address_line_5': 'SW14 6BF',
  'name': 'John Smith',
  'application_id': '4134325'
}
```

##### reference (optional)

A unique identifier you can create if necessary. This reference identifies a single unique letter or a batch of letters. It must not contain any personal information such as name or postal address. For example:

```python
reference='STRING' # optional string - identifies notification(s)
```

#### Response

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

#### Error codes

If the request is not successful, the client returns an `HTTPError` containing the relevant error code.

|error.status_code|error.message|How to fix|
|:---|:---|:---|
|`400`|`[{`<br>`"error": "BadRequestError",`<br>`"message": "Cannot send letters with a team api key"`<br>`}]`|Use the correct type of [API key](#api-keys)|
|`400`|`[{`<br>`"error": "BadRequestError",`<br>`"message": "Cannot send letters when service is in trial mode - see https://www.notifications.service.gov.uk/trial-mode"`<br>`}]`|Your service cannot send this letter in  [trial mode](https://www.notifications.service.gov.uk/features/using-notify#trial-mode).|
|`400`|`[{`<br>`"error": "ValidationError",`<br>`"message": "personalisation address_line_1 is a required property"`<br>`}]`|Ensure that your template has a field for the first line of the address, check [personalisation](#personalisation-required) for more information.|
|`400`|`[{`<br>`"error": "ValidationError",`<br>`"message": "Must be a real UK postcode"`<br>`}]`|Ensure that the value for the last line of the address is a real UK postcode.|
|`400`|`[{`<br>`"error": "ValidationError",`<br>`"message": "Last line of address must be a real UK postcode or another country"`<br>`}]`|Ensure that the value for the last line of the address is a real UK postcode or the name of a country outside the UK.|
|`403`|`[{`<br>`"error": "AuthError",`<br>`"message": "Error: Your system clock must be accurate to within 30 seconds"`<br>`}]`|Check your system clock.|
|`403`|`[{`<br>`"error": "AuthError",`<br>`"message": "Invalid token: API key not found"`<br>`}]`|Use the correct API key. Refer to [API keys](#api-keys) for more information.|
|`429`|`[{`<br>`"error": "RateLimitError",`<br>`"message": "Exceeded rate limit for key type TEAM/TEST/LIVE of 3000 requests per 60 seconds"`<br>`}]`|Refer to [API rate limits](#rate-limits) for more information.|
|`429`|`[{`<br>`"error": "TooManyRequestsError",`<br>`"message": "Exceeded send limits (LIMIT NUMBER) for today"`<br>`}]`|Refer to [service limits](#daily-limits) for the limit number.|
|`500`|`[{`<br>`"error": "Exception",`<br>`"message": "Internal server error"`<br>`}]`|Notify was unable to process the request, resend your letter.|


### Send a precompiled letter

#### Method

```python
response = notifications_client.send_precompiled_letter_notification(
    reference,      # Reference to identify the notification
    pdf_file,       # PDF File object
    postage         # set postage on your precompiled letter
)
```

#### Arguments

##### reference (required)

A unique identifier you create. This reference identifies a single unique precompiled letter or a batch of precompiled letters. It must not contain any personal information such as name or postal address.

##### pdf_file (required)

The precompiled letter must be a PDF file which meets [the GOV.UK Notify letter specification](https://www.notifications.service.gov.uk/using-notify/guidance/letter-specification).

```python
with open("path/to/pdf_file", "rb") as pdf_file:
    notification = notifications_client.send_precompiled_letter_notification(
        reference="your reference", pdf_file=pdf_file
    )
```

##### postage (optional)

You can choose first or second class postage for your precompiled letter. Set the value to `first` for first class, or `second` for second class. If you do not pass in this argument, the postage will default to second class.



#### Response

If the request to the client is successful, the client returns a `dict`:

```python
{
  "id": "740e5834-3a29-46b4-9a6f-16142fde533a",
  "reference": "your-letter-reference",
  "postage": "postage-you-have-set-or-None"
}
```

#### Error codes

If the request is not successful, the client returns an HTTPError containing the relevant error code.

|error.status_code|error.message|How to fix|
|:---|:---|:---|
|`400`|`[{`<br>`"error": "BadRequestError",`<br>`"message": "Cannot send letters with a team api key"`<br>`}]`|Use the correct type of [API key](#api-keys)|
|`400`|`[{`<br>`"error": "BadRequestError",`<br>`"message": "Letter content is not a valid PDF"`<br>`}]`|PDF file format is required|
|`400`|`[{`<br>`"error": "BadRequestError",`<br>`"message": "Cannot send letters when service is in trial mode - see https://www.notifications.service.gov.uk/trial-mode"`<br>`}]`|Your service cannot send this precompiled letter in [trial mode](https://www.notifications.service.gov.uk/features/using-notify#trial-mode)|
|`400`|`[{`<br>`"error": "ValidationError",`<br>`"message": "reference is a required property"`<br>`}]`|Add a `reference` argument to the method call|
|`400`|`[{`<br>`"error": "ValidationError",`<br>`"message": "postage invalid. It must be either first or second."`<br>`}]`|Change the value of `postage` argument in the method call to either 'first' or 'second'|
|`429`|`[{`<br>`"error": "RateLimitError",`<br>`"message": "Exceeded rate limit for key type live of 10 requests per 20 seconds"`<br>`}]`|Use the correct API key. Refer to [API keys](#api-keys) for more information|
|`429`|`[{`<br>`"error": "TooManyRequestsError",`<br>`"message": "Exceeded send limits (50) for today"`<br>`}]`|Refer to [service limits](#daily-limits) for the limit number|

## Get message status

### Get the status of one message

You can only get the status of messages sent within the retention period. The default retention period is 7 days.

#### Method

```python
response = notifications_client.get_notification_by_id(notification_id)
```

#### Arguments

##### notification_id (required)

The ID of the notification. To find the notification ID, you can either:

* check the response to the [original notification method call](#response)
* [sign in to GOV.UK Notify](https://www.notifications.service.gov.uk/sign-in) and go to the __API integration__ page

#### Response

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
  "line_7": "ADDRESS LINE 7", # required string for letter
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

For more information, see the:

* [email status descriptions](#email-status-descriptions)
* [text message status descriptions](#text-message-status-descriptions)
* [letter status descriptions](#letter-status-descriptions)
* [precompiled letter status descriptions](#precompiled-letter-status-descriptions)

#### Error codes

If the request is not successful, the client will return an `HTTPError` containing the relevant error code:

|error.status_code|error.message|How to fix|
|:---|:---|:---|
|`400`|`[{`<br>`"error": "ValidationError",`<br>`"message": "id is not a valid UUID"`<br>`}]`|Check the notification ID|
|`403`|`[{`<br>`"error": "AuthError",`<br>`"message": "Error: Your system clock must be accurate to within 30 seconds"`<br>`}]`|Check your system clock|
|`403`|`[{`<br>`"error": "AuthError",`<br>`"message": "Invalid token: API key not found"`<br>`}]`|Use the correct API key. Refer to [API keys](#api-keys) for more information|
|`404`|`[{`<br>`"error": "NoResultFound",`<br>`"message": "No result found"`<br>`}]`|Check when your message was sent. If it was sent before the retention period, it has been deleted. You can no longer get the status of this message. The default retention period is 7 days.|


### Get the status of multiple messages

This API call returns one page of up to 250 messages and statuses. You can get either the most recent messages, or get older messages by specifying a particular notification ID in the `older_than` argument.

You can only get the status of messages sent within the retention period. The default retention period is 7 days.

#### Method

##### All messages

This will return all your messages with statuses. They will display in pages of up to 250 messages each.

```python
response = notifications_client.get_all_notifications(template_type, status, reference, older_than)
```

You can filter the returned messages by including the following optional arguments in the method:

- [`template_type`](#template-type-optional)
- [`status`](#status-optional)
- [`reference`](#get-the-status-of-multiple-messages-arguments-reference-optional)
- [`older_than`](#older-than-optional)


##### One page of up to 250 messages

This will return one page of up to 250 messages and statuses. You can get either the most recent messages, or get older messages by specifying a particular notification ID in the [`older_than`](#older-than-optional) argument.

To get the most recent messages, add the following code to your application:

```python
response = get_all_notifications_iterator(status="sending")
```

You must set the [`status`](#status-optional) argument to `sending`.

To get older messages:

1. Get the ID of an older message.
1. Add the following code to your application, with the older notification ID in the [`older_than`](#older-than-optional) argument.

```python
response = get_all_notifications_iterator(status="sending",older_than="NOTIFICATION ID")
```

You must set the [`status`](#status-optional) argument to `sending`.

This method will return the next oldest messages from the specified notification ID.

#### Arguments

##### template_type (optional)

You can filter by:

* `email`
* `sms`
* `letter`

You can leave out this argument to ignore this filter.

##### status (optional)

You can filter by each:

* [email status](#email-status-descriptions)
* [text message status](#text-message-status-descriptions)
* [letter status](#letter-status-descriptions)
* [precompiled letter status](#precompiled-letter-status-descriptions)

If you filter by `failed` it will return all 3 failure statuses: `permanent-failure`, `temporary-failure` and `technical-failure`.

You can leave out this argument to ignore this filter.

##### reference (optional)

A unique identifier you can create if necessary. This reference identifies a single unique message or a batch of messages. It must not contain any personal information such as name or postal address. For example:

```python
reference='STRING' # optional string - identifies notification(s)
```

You can leave out this argument to ignore this filter.

##### older_than (optional)

Input a notification ID into this argument. If you use this argument, the method returns the next 250 received messages older than the given ID.

```python
older_than='740e5834-3a29-46b4-9a6f-16142fde533a' # optional string - notification ID
```

If you leave out this argument, the method returns the most recent 250 messages.

The client only returns messages sent within the retention period. The default retention period is 7 days. If the message specified in this argument was sent before the retention period, the client returns an empty response.

#### Response

If the request to the client is successful, the client returns a `dict`.

##### All messages

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
      "postcode": "A REAL UK POSTCODE", # required string for letter
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

##### One page of up to 250 messages

```python
<generator object NotificationsAPIClient.get_all_notifications_iterator at 0x1026c7410>
```

For more information, see the:

* [email status descriptions](#email-status-descriptions)
* [text message status descriptions](#text-message-status-descriptions)
* [letter status descriptions](#letter-status-descriptions)
* [precompiled letter status descriptions](#precompiled-letter-status-descriptions)

#### Error codes

If the request is not successful, the client returns an `HTTPError` containing the relevant error code:

|error.status_code|error.message|How to fix|
|:---|:---|:---|
|`400`|`[{`<br>`"error": "ValidationError",`<br>`"message": "status ‘elephant’ is not one of [cancelled, created, sending, sent, delivered, pending, failed, technical-failure, temporary-failure, permanent-failure, pending-virus-check, validation-failed, virus-scan-failed, returned-letter, accepted, received]"`<br>`}]`|Change the [status argument](#status-optional)|
|`400`|`[{`<br>`"error": "ValidationError",`<br>`"message": "‘Apple’ is not one of [sms, email, letter]"`<br>`}]`|Change the [template_type argument](#template-type-optional)|

### Email status descriptions

|Status|Description|
|:---|:---|
|`created`|GOV.UK Notify has placed the message in a queue, ready to be sent to the provider. It should only remain in this state for a few seconds.|
|`sending`|GOV.UK Notify has sent the message to the provider. The provider will try to deliver the message to the recipient for up to 72 hours. GOV.UK Notify is waiting for delivery information.|
|`delivered`|The message was successfully delivered.|
|`permanent-failure`|The provider could not deliver the message because the email address was wrong. You should remove these email addresses from your database.|
|`temporary-failure`|The provider could not deliver the message. This can happen when the recipient’s inbox is full. You can try to send the message again.|
|`technical-failure`|Your message was not sent because there was a problem between Notify and the provider.<br>You’ll have to try sending your messages again.|

### Text message status descriptions

|Status|Description|
|:---|:---|
|`created`|GOV.UK Notify has placed the message in a queue, ready to be sent to the provider. It should only remain in this state for a few seconds.|
|`sending`|GOV.UK Notify has sent the message to the provider. The provider will try to deliver the message to the recipient for up to 72 hours. GOV.UK Notify is waiting for delivery information.|
|`pending`|GOV.UK Notify is waiting for more delivery information.<br>GOV.UK Notify received a callback from the provider but the recipient’s device has not yet responded. Another callback from the provider determines the final status of the text message.|
|`sent`|The message was sent to an international number. The mobile networks in some countries do not provide any more delivery information. The GOV.UK Notify website displays this status as 'Sent to an international number'.|
|`delivered`|The message was successfully delivered.|
|`permanent-failure`|The provider could not deliver the message. This can happen if the phone number was wrong or if the network operator rejects the message. If you’re sure that these phone numbers are correct, you should [contact GOV.UK Notify support](https://www.notifications.service.gov.uk/support). If not, you should remove them from your database. You’ll still be charged for text messages that cannot be delivered.
|`temporary-failure`|The provider could not deliver the message. This can happen when the recipient’s phone is off, has no signal, or their text message inbox is full. You can try to send the message again. You’ll still be charged for text messages to phones that are not accepting messages.|
|`technical-failure`|Your message was not sent because there was a problem between Notify and the provider.<br>You’ll have to try sending your messages again. You will not be charged for text messages that are affected by a technical failure.|

### Letter status descriptions

|Status|Description|
|:---|:---|
|`accepted`|GOV.UK Notify has sent the letter to the provider to be printed.|
|`cancelled`|Sending cancelled. The letter will not be printed or dispatched.|
|`received`|The provider has printed and dispatched the letter.|
|`technical-failure`|GOV.UK Notify had an unexpected error while sending the letter to our printing provider.|

### Precompiled letter status descriptions

|Status|Description|
|:---|:---|
|`pending-virus-check`|GOV.UK Notify has not completed a virus scan of the precompiled letter file.|
|`virus-scan-failed`|GOV.UK Notify found a potential virus in the precompiled letter file.|
|`validation-failed`|Content in the precompiled letter file is outside the printable area. See the [GOV.UK Notify letter specification](https://www.notifications.service.gov.uk/using-notify/guidance/letter-specification) for more information.|
|`accepted`|GOV.UK Notify has sent the letter to the provider to be printed.|
|`cancelled`|Sending cancelled. The letter will not be printed or dispatched.|
|`received`|The provider has printed and dispatched the letter.|
|`technical-failure`|GOV.UK Notify had an unexpected error while sending the letter to our printing provider.|

### Get a PDF for a letter

#### Method

This returns the PDF contents of a letter.

```python
pdf_file = notifications_client.get_pdf_for_letter(
  'f33517ff-2a88-4f6e-b855-c550268ce08a' # required string - notification ID
)
```

#### Arguments

##### notification_id (required)

The ID of the notification. To find the notification ID, you can either:

* check the response to the [original notification method call](#get-the-status-of-one-message-response)
* [sign in to GOV.UK Notify](https://www.notifications.service.gov.uk/sign-in) and go to the __API integration__ page

#### Response

If the request to the client is successful, the client will return a `io.BytesIO` object containing the raw PDF data.

#### Error codes

If the request is not successful, the client will return an `HTTPError` containing the relevant error code:

|error.status_code|error.message|How to fix|
|:---|:---|:---|
|`400`|`[{`<br>`"error": "ValidationError",`<br>`"message": "id is not a valid UUID"`<br>`}]`|Check the notification ID|
|`400`|`[{`<br>`"error": "PDFNotReadyError",`<br>`"message": "PDF not available yet, try again later"`<br>`}]`|Wait for the letter to finish processing. This usually takes a few seconds|
|`400`|`[{`<br>`"error": "BadRequestError",`<br>`"message": "File did not pass the virus scan"`<br>`}]`|You cannot retrieve the contents of a letter that contains a virus|
|`400`|`[{`<br>`"error": "BadRequestError",`<br>`"message": "PDF not available for letters in technical-failure"`<br>`}]`|You cannot retrieve the contents of a letter in technical-failure|
|`400`|`[{`<br>`"error": "ValidationError",`<br>`"message": "Notification is not a letter"`<br>`}]`|Check that you are looking up the correct notification|
|`403`|`[{`<br>`"error": "AuthError",`<br>`"message": "Error: Your system clock must be accurate to within 30 seconds"`<br>`}]`|Check your system clock|
|`403`|`[{`<br>`"error": "AuthError",`<br>`"message": "Invalid token: API key not found"`<br>`}]`|Use the correct API key. Refer to [API keys](#api-keys) for more information|
|`404`|`[{`<br>`"error": "NoResultFound",`<br>`"message": "No result found"`<br>`}]`|Check the notification ID|

## Get a template

### Get a template by ID

#### Method

This returns the latest version of the template.

```python
response = notifications_client.get_template(
  'f33517ff-2a88-4f6e-b855-c550268ce08a' # required string - template ID
)
```

#### Arguments

##### template_id (required)

The ID of the template. [Sign in to GOV.UK Notify](https://www.notifications.service.gov.uk/sign-in) and go to the __Templates__ page to find it.

#### Response

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
    "letter_contact_block": "STRING" # optional string - None if not a letter template or contact block not set
}
```

#### Error codes

If the request is not successful, the client returns an `HTTPError` containing the relevant error code:

|error.status_code|error.message|How to fix|
|:---|:---|:---|
|`403`|`[{`<br>`"error": "AuthError",`<br>`"message": "Error: Your system clock must be accurate to within 30 seconds"`<br>`}]`|Check your system clock|
|`403`|`[{`<br>`"error": "AuthError",`<br>`"message": "Invalid token: API key not found"`<br>`}]`|Use the correct API key. Refer to [API keys](#api-keys) for more information|
|`404`|`[{`<br>`"error": "NoResultFound",`<br>`"message": "No Result Found"`<br>`}]`|Check your [template ID](#get-a-template-by-id-arguments-template-id-required)|


### Get a template by ID and version

#### Method

```python
response = notifications_client.get_template_version(
    'f33517ff-2a88-4f6e-b855-c550268ce08a' # required string - template ID
    'version': INTEGER,
)
```

#### Arguments

##### template_id (required)

The ID of the template. [Sign in to GOV.UK Notify](https://www.notifications.service.gov.uk/sign-in) and go to the __Templates__ page to find it.

##### version (required)

The version number of the template.

#### Response

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
    "letter_contact_block": "STRING" # optional string - None if not a letter template or contact block not set
}
```

#### Error codes

If the request is not successful, the client returns an `HTTPError` containing the relevant error code:

|error.status_code|error.message|How to fix|
|:---|:---|:---|
|`403`|`[{`<br>`"error": "AuthError",`<br>`"message": "Error: Your system clock must be accurate to within 30 seconds"`<br>`}]`|Check your system clock|
|`403`|`[{`<br>`"error": "AuthError",`<br>`"message": "Invalid token: API key not found"`<br>`}]`|Use the correct API key. Refer to [API keys](#api-keys) for more information|
|`404`|`[{`<br>`"error": "NoResultFound",`<br>`"message": "No Result Found"`<br>`}]`|Check your [template ID](#get-a-template-by-id-and-version-arguments-template-id-required) and [version](#version-required)|


### Get all templates

#### Method

This returns the latest version of all templates.

```python
response = notifications_client.get_all_templates(
    template_type="sms / letter / email" # optional string
)
```

#### Arguments

##### template_type (optional)

If you leave out this argument, the method returns all templates. Otherwise you can filter by:

- `email`
- `sms`
- `letter`

#### Response

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
            "letter_contact_block": "STRING" # optional string - None if not a letter template or contact block not set
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

### Generate a preview template

#### Method

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

#### Arguments

##### template_id (required)

The ID of the template. [Sign in to GOV.UK Notify](https://www.notifications.service.gov.uk/sign-in) and go to the __Templates__ page to find it.

##### personalisation (required)

If a template has placeholder fields for personalised information such as name or reference number, you need to provide their values in a dictionary with key value pairs. For example:

```python
personalisation={
    'first_name': 'Amala',
    'application_date': '2018-01-01',
}
```

#### Response

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

#### Error codes

If the request is not successful, the client returns an `HTTPError` containing the relevant error code:

|error.status_code|error.message|Notes|
|:---|:---|:---|
|`400`|`[{`<br>`"error": "BadRequestError",`<br>`"message": "Missing personalisation: [PERSONALISATION FIELD]"`<br>`}]`|Check that the personalisation arguments in the method match the placeholder fields in the template|
|`400`|`[{`<br>`"error": "NoResultFound",`<br>`"message": "No result found"`<br>`}]`|Check the [template ID](#generate-a-preview-template-arguments-template-id-required)|
|`403`|`[{`<br>`"error": "AuthError",`<br>`"message": "Error: Your system clock must be accurate to within 30 seconds"`<br>`}]`|Check your system clock|
|`403`|`[{`<br>`"error": "AuthError",`<br>`"message": "Invalid token: API key not found"`<br>`}]`|Use the correct API key. Refer to [API keys](#api-keys) for more information|


## Get received text messages

This API call returns one page of up to 250 received text messages. You can get either the most recent messages, or get older messages by specifying a particular notification ID in the older_than argument.

You can only get the status of messages that are 7 days old or newer.

### Get all received text messages

This method returns a `<generator object>` with all received text messages.

#### Method

```python
response = get_received_texts_iterator()
```

#### Response

If the request to the client is successful, the client will return a `<generator object>` that will return all received text messages.

```python
<generator object NotificationsAPIClient.get_received_texts_iterator at 0x1026c7410>
```

### Get one page of received text messages

This will return one page of up to 250 text messages.

#### Method

```python
response = client.get_received_texts(older_than)
```

You can specify which text messages to receive by inputting the ID of a received text message into the [`older_than`](#get-one-page-of-received-text-messages-arguments-older-than-optional) argument.

#### Arguments

##### older_than (optional)

Input the ID of a received text message into this argument. If you use this argument, the method returns the next 250 received text messages older than the given ID.

```python
older_than='740e5834-3a29-46b4-9a6f-16142fde533a' # optional string - notification ID
```

If you leave out this argument, the method returns the most recent 250 text messages.

#### Response

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

#### Error codes

If the request is not successful, the client returns an `HTTPError` containing the relevant error code.

|error.status_code|error.message|How to fix|
|:---|:---|:---|
|`403`|`[{`<br>`"error": "AuthError",`<br>`"message": "Error: Your system clock must be accurate to within 30 seconds"`<br>`}]`|Check your system clock|
|`403`|`[{`<br>`"error": "AuthError",`<br>`"message": "Invalid token: API key not found"`<br>`}]`|Use the correct API key. Refer to [API keys](#api-keys) for more information|

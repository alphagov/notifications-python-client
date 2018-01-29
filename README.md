# Set up the client

## Install the client

Run the following code in the command line:

```shell
pip install notifications-python-client
```

The client supports both Python 3.x and 2.7. Refer to the [client change log](https://github.com/alphagov/notifications-python-client/blob/master/CHANGELOG.md) for the version number and the latest updates.

## Create a new instance of the client

Add this code to your application:

```python
from notifications_python_client.notifications import NotificationsAPIClient

notifications_client = NotificationsAPIClient(api_key)
```

To get an API key, [log in to GOV.UK Notify](https://www.notifications.service.gov.uk/) and go to the _API integration_ page. More information can be found in the [API keys](/#api-keys) section.

[Back to top](/#gov-uk-notify-technical-documentation-python)

# Send a message

GOV.UK Notify enables you to send text messages, emails and letters.

## Send a text message

### Method

1. Add the following method to your application code:

    ```python
    response = notifications_client.send_sms_notification(
        phone_number='07XXXXXXXXX', # required string - for example 07967346238
        template_id='XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX', # required string - for example 2956cbb0-5e1f-4341-9334-cbc097b86d8a
        personalisation={
            'KEY': 'VALUE',
            'KEY': 'VALUE',
            ...
            }, # optional dict
        reference='REFERENCE', # optional string - identifies the notification(s)
        sms_sender_id='XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX' # £ optional string - for example 8e222534-7f05-4972-86e3-17c5d9f894e2
    )
    ```

1. Complete the required [`phone_number`](/#phone-number) and [`template_id`](#template-id) arguments.

1. Complete the optional [`personalisation`](/#personalisation), [`reference`](/#reference) and [`sms_sender_id`](/#sms-sender-id) arguments if required.

1. You are now ready to send a text message notification. Run your application to send a request to the API Notification client.

[Back to top](/#gov-uk-notify-technical-documentation-python)

### Required arguments

#### phone_number

The phone number of the recipient of the text message. This number can be UK or international.

#### template_id

The ID of the template. You can find this by logging into [GOV.UK Notify](https://www.notifications.service.gov.uk/) and going to the _Templates_ page.

[Back to top](/#gov-uk-notify-technical-documentation-python)

### Optional arguments

#### personalisation

If a template has placeholder fields for personalised information such as name or reference number, you need to provide their values in a dictionary with key value pairs. For example:

```python
personalisation={
    'first_name': 'Amala',
    'application_date': '2018-01-01',
}
```

#### reference

A unique identifier. This reference can identify a single unique notification or a batch of multiple notifications.

#### sms_sender_id

A unique identifier of the sender of the text message notification. To set this up:

1. Log into your GOV.UK Notify account.
1. Go to _Settings_.
1. Check that you are in the correct service. If you are not, click _Switch service_ in the top right corner of the screen and select the correct one.
1. Go to the _Text Messages_ section and click _Manage_ on the "Text Message sender" row.
1. You can do one of the following:
  - copy the ID of the sender you want to use and paste it into the method
  - click _Change_ to change the default sender that the service will use, and click _Save_

If you omit this argument from your method, the default `sms_sender_id` will be set for the notification.

[Back to top](/#gov-uk-notify-technical-documentation-python)

### Response

If the request to the client is successful, you will receive the following `dict` response:

```python
{
  "id": "NOTIFICATION_ID",
  "reference": "REFERENCE",
  "content": {
    "body": "MESSAGE TEXT",
    "from_number": "SENDER"
  },
  "uri": "https://api.notifications.service.gov.uk/v2/notifications/NOTIFICATION_ID",
  "template": {
    "id": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
    "version": 1,
    "uri": "https://api.notifications.service.gov.uk/v2/template/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
  }
}
```

If you are using the [test API key](/#test), all your messages will come back as delivered.

All successfully delivered messages will appear on your dashboard.

[Back to top](/#gov-uk-notify-technical-documentation-python)

### Error codes

If the request is not successful, the client will raise an `HTTPError`:

|`error.status_code`|`error.message`|Notes|
|:---|:---|:---|
|`429`|`[{`<br>`"error": "RateLimitError",`<br>`"message": "Exceeded rate limit for key type TEAM/TEST/LIVE of 3000 requests per 60 seconds"`<br>`}]`||
|`429`|`[{`<br>`"error": "TooManyRequestsError",`<br>`"message": "Exceeded send limits (LIMIT NUMBER) for today"`<br>`}]`|Refer to [service limits](/#service-limits) for the limit number|
|`400`|`[{`<br>`"error": "BadRequestError",`<br>`"message": "Can"t send to this recipient using a team-only API key"`<br>`]}`||
|`400`|`[{`<br>`"error": "BadRequestError",`<br>`"message": "Can"t send to this recipient when service is in trial mode - see https://www.notifications.service.gov.uk/trial-mode"`<br>`}]`||

[Back to top](/#gov-uk-notify-technical-documentation-python)

## Send an email

### Method

1. Add the following method to your application:

	   ```python
	    response = notifications_client.send_email_notification(
		email_address='EMAIL ADDRESS', # for example sender@something.com
		template_id='XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX', # for example 2956cbb0-5e1f-4341-9334-cbc097b86d8a
		personalisation={
		    'KEY': 'VALUE',
		    'KEY': 'VALUE',
		    ...
		    },,
		reference='REFERENCE', #???
		email_reply_to_id='XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX' # for example 8e222534-7f05-4972-86e3-17c5d9f894e2
	    )
	    ```
	    
1. Complete the required [`email_address`](/#email-address) and [`template_id`](#send-an-email-required-arguments-template-id) arguments.

1. Complete the optional  [`personalisation`](/#send-an-email-optional-arguments-personalisation), [`reference`](/#send-an-email-optional-arguments-reference) and [`email_reply_to_id`](/#email-reply-to-id) arguments if required.

You are now ready to send an email notification. Run your application to send a request to the API notification client.

[Back to top](/#gov-uk-notify-technical-documentation-python)

### Required arguments

#### email_address

The email address of the recipient, only required for email notifications.

#### template_id

The ID of the template. You can find this by logging into GOV.UK Notify and going to the _Templates_ page.

[Back to top](/#gov-uk-notify-technical-documentation-python)

### Optional arguments

#### personalisation

If a template has placeholder fields for personalised information such as name or reference number, you need to provide their values in a dictionary with key value pairs. For example:

```python
personalisation={
    'first_name': 'Amala',
    'reference_number': '300241',
}
```

#### reference

A unique identifier. This reference can identify a single unique notification or a batch of multiple notifications.

#### email_reply_to_id

This is an email reply-to address specified by you to receive replies from your users. Your service cannot go live until at least one email address has been set up for this. To set up:

1. Log into your GOV.UK Notify account.
1. Go to _Settings_.
1. Check that you are in the correct service. If you are not, click _Switch service_ in the top right corner of the screen and select the correct one.
1. Go to the Email section and click _Manage_ on the "Email reply to addresses" row.
1. Click _Change_ to specify the email address to receive replies, and click _Save_.

If you omit this argument, your default email reply-to address will be set for the notification.

[Back to top](/#gov-uk-notify-technical-documentation-python)

### Response

If the request to the client is successful, you will receive the following `dict` response:

```python
{
  "id": "NOTIFICATION ID",
  "reference": "REFERENCE",
  "content": {
    "subject": "SUBJECT TEXT",
    "body": "MESSAGE TEXT",
    "from_email": "FROM EMAIL ADDRESS"
  },
  "uri": "https://api.notifications.service.gov.uk/v2/notifications/NOTIFICATION_ID",
  "template": {
    "id": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
    "version": 1,
    "uri": "https://api.notifications.service.gov.uk/v2/template/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
  }
}
```

[Back to top](/#gov-uk-notify-technical-documentation-python)

### Error codes

If the request is not successful, the client will raise an `HTTPError`:

|`error.status_code`|`error.message`|Notes|
|:---|:---|:---|
|`429`|`[{`<br>`"error": "RateLimitError",`<br>`"message": "Exceeded rate limit for key type TEAM/TEST/LIVE of 3000 requests per 60 seconds"`<br>`}]`||
|`429`|`[{`<br>`"error": "TooManyRequestsError",`<br>`"message": "Exceeded send limits (LIMIT) for today"`<br>`}]`|Refer to [service limits](/#service-limits) for the limit number|
|`400`|`[{`<br>`"error": "BadRequestError",`<br>`"message": "Can"t send to this recipient using a team-only API key"`<br>`]}`||
|`400`|`[{`<br>`"error": "BadRequestError",`<br>`"message": "Can"t send to this recipient when service is in trial mode - see https://www.notifications.service.gov.uk/trial-mode"`<br>`}]`||

[Back to top](/#gov-uk-notify-technical-documentation-python)

## Send a letter

When your service first signs up to GOV.UK Notify, you’ll start in trial mode. You can only send letters in live mode.

### Method

1. Add the following method to your application:

    ```python
    response = notifications_client.send_letter_notification(
        template_id='XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX', #2956cbb0-5e1f-4341-9334-cbc097b86d8a
        personalisation={
          'address_line_1': 'ADDRESS LINE 1' #The Occupuier',
          'address_line_2': 'ADDRESS LINE 2' #123 High Street',
          'postcode': 'POSTCODE' #SW14 6BH',
          ...
        },
        reference='REFERENCE' #???
    )
    ```

1. Complete the required [`template_id`](/#send-a-letter-required-arguments-template-id) argument.
1. Complete the required [`personalisation`](/#send-a-letter-required-arguments-personalisation) arguments (the code example above only includes the required parameters).
1. Complete the optional [`reference`](/#send-a-letter-optional-arguments-reference) and [`personalisation`](/#send-a-letter-optional-arguments-personalisation) arguments if required.

You are now ready to send a letter notification. Run your application to send a request to the API notification client.

[Back to top](/#gov-uk-notify-technical-documentation-python)

### Required arguments

#### template_id

The ID of the template. You can find this by logging into GOV.UK Notify and going to the _Templates_ page.

#### personalisation

The personalisation argument always contains the following required parameters for the letter recipient's address:

- `address_line_1`
- `address_line_2`
- `postcode`

Any variables / placeholders (_QP: Which one?_) included in the letter template also count as required parameters. You need to provide their values in a dictionary with key value pairs:

```python
personalisation={
  'address_line_1': 'The Occupier',
  'address_line_2': '123 High Street',
  'postcode': 'SW14 6BF',
  'name': 'John Smith',
  'application_id': '4134325'
}
```

[Back to top](/#gov-uk-notify-technical-documentation-python)

### Optional arguments

#### reference

A unique identifier. This reference can identify a single unique notification or a batch of multiple notifications.

#### personalisation

The following parameters in the letter recipient's address are optional:

```python
personalisation={
    'address_line_3': '123 High Street', 	
    'address_line_4': 'Richmond upon Thames', 	
    'address_line_5': 'London', 		
    'address_line_6': 'Middlesex',
}
```

_QP: parameter? variable? placeholder?_

[Back to top](/#gov-uk-notify-technical-documentation-python)

### Response

If the request to the client is successful, you will receive the following `dict` response:

```python
{
  "id": "NOTIFICATION_ID",
  "reference": 'REFERENCE',
  "content": {
    "subject": "SUBJECT TEXT",
    "body": "LETTER TEXT",
  },
  "uri": "https://api.notifications.service.gov.uk/v2/notifications/NOTIFICATION_ID",
  "template": {
    "id": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
    "version": 1,
    "uri": "https://api.notifications.service.gov.uk/v2/template/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
  }
  "scheduled_for": None
}
```

[Back to top](/#gov-uk-notify-technical-documentation-python)

### Error codes

If the request is not successful, the client will raise an `HTTPError`:

|`error.status_code`|`error.message`|Notes|
|:---|:---|:---|
|`429`|`[{`<br>`"error": "RateLimitError",`<br>`"message": "Exceeded rate limit for key type TEAM/TEST/LIVE of 3000 requests per 60 seconds"`<br>`}]`||
|`429`|`[{`<br>`"error": "TooManyRequestsError",`<br>`"message": "Exceeded send limits (LIMIT) for today"`<br>`}]`|Refer to [service limits](/#service-limits) for the limit number|
|`400`|`[{`<br>`"error": "BadRequestError",`<br>`"message": "Cannot send letters with a team api key"`<br>`]}`||
|`400`|`[{`<br>`"error": "BadRequestError",`<br>`"message": "Cannot send letters when service is in trial mode - see https://www.notifications.service.gov.uk/trial-mode"`<br>`}]`||
|`400`|`[{`<br>`"error": "ValidationError",`<br>`"message": "personalisation address_line_1 is a required property"`<br>`}]`||

# Get message status

The possible status of a message depends on the message type.

## Status - text and email

### Sending

The message is queued to be sent by the provider.

### Delivered

The message was successfully delivered.

### Failed

This covers all failure statuses:

- permanent-failure - "The provider was unable to deliver message, email or phone number does not exist; remove this recipient from your list"
- temporary-failure - "The provider was unable to deliver message, email inbox was full or phone was turned off; you can try to send the message again"
- technical-failure - "Notify had a technical failure; you can try to send the message again"

## Status - letter

### Failed

The only failure status that applies to letters is __technical-failure__ - Notify had an unexpected error while sending to our printing provider.

### Accepted

Notify is printing and posting the letter.

## Get the status of one message

### Method

1. Add the following method to your application code:

    ```python
    response = notifications_client.get_notification_by_id(notification_id)
    ```

1. Complete the required [`notification_id`](/#notification-id) argument with the ID of the notification that you want the status of.

You are now ready to get the status of the notification. Run your application to send a request to the API Notification client.

[Back to top](/#gov-uk-notify-technical-documentation-python)

### Required arguments

#### notification_id

The ID of the notification.

[Back to top](/#gov-uk-notify-technical-documentation-python)

### Response

If the request to the client is successful, you will receive the following `dict` response:

```python
{
  "id": "NOTIFICATION ID", # required
  "reference": "CLIENT REFERENCE", # optional
  "email_address": "EMAIL ADDRESS",  # required for emails
  "phone_number": "PHONE NUMBER",  # required for sms
  "line_1": "ADDRESS LINE 1", # required for letter - name of person or company
  "line_2": "ADDRESS LINE 2", # required for letter
  "line_3": "ADDRESS LINE 3", # optional
  "line_4": "ADDRESS LINE 4", # optional
  "line_5": "ADDRESS LINE 5", # optional
  "line_6": "ADDRESS LINE 6", # optional
  "postcode": "POSTCODE", # required for letter
  "type": "TYPE", # required - sms / letter / email
  "status": "CURRENT STATUS", # required - sending / delivered / permanent-failure / temporary-failure / technical-failure
  "template": {
    "version": X # required template version number
    "id": `XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX` # required template id
    "uri": "/v2/template/{id}/{version}", # required
  },
  "body": "Body of the notification",
  "subject": "Subject of an email notification or None if an sms message"
	"created_at": "created at", # required
	"sent_at": " sent to provider at", # optional
	"completed_at:" "date the notification is delivered or failed" # optional
}
```

[Back to top](/#gov-uk-notify-technical-documentation-python)

### Error codes

If the request is not successful, the client will raise an `HTTPError`:

|`error.status_code`|`error.message`|
|:---|:---|
|`404`|`[{`<br>`"error": "NoResultFound",`<br>`"message": "No result found"`<br>`}]`|
|`400`|`[{`<br>`"error": "ValidationError",`<br>`"message": "id is not a valid UUID"`<br>`}]`|

[Back to top](/#gov-uk-notify-technical-documentation-python)

## Get the status of all messages

This API call returns the status of all messages. You can either get the status of all messages in one call, or one page of up to 250 messages.

### Method

#### All messages

This will return all your messages with statuses; they will be displayed in pages of up to 250 messages each.

Add the following method to your application code:

```python
response = notifications_client.get_all_notifications(template_type, status, reference, older_than)
```

You can filter the returned messages by including the following optional arguments in the method:

- [`template_type`](/#template-type)
- [`status`](/#status)
- [`reference`](/#get-the-status-of-all-messages-optional-arguments-reference)
- [`older_than`](/#older-than)

Run your application to send a request to the API notification client.

#### One page of up to 250 messages

This will return one page of up to 250 messages and statuses. You can get either the most recent messages, or get older messages by specifying a particular notification ID in the [`older_than`](/#older-than) argument.

##### Most recent messages

Add the following method to your application code:

```python
response = get_all_notifications_iterator(status="sending")
```

You must set the [`status`](/#status) argument to "sending".

Run your application to send a request to the API notification client.

##### Older messages

To get older messages:

1. Get the ID of an older notification.
1. Add the following code to your application, with the older notification ID in the [`older_than`](/#older-than) argument.

    ```python
    response = get_all_notifications_iterator(status="sending",older_than="NOTIFICATION ID")
    ```

You must set the [`status`](/#status) argument to "sending".

Run your application to send a request to the API notification client. It will return the next oldest messages from the specified notification ID.

[Back to top](/#gov-uk-notify-technical-documentation-python)

### Optional arguments

You can omit any of these arguments to ignore these filters.

#### template_type

You can filter by:

* email
* sms
* letter

#### status

| status | description | text | email | letter |
|:--- |:--- |:--- |:--- |:--- |
|sending |The message is queued to be sent by the provider|Yes|Yes||
|delivered|The message was successfully delivered|Yes|Yes||
|failed|This will return all failure statuses:<br>- `permanent-failure`<br>- `temporary-failure`<br>- `technical-failure`|Yes|Yes||
|permanent-failure|The provider was unable to deliver message, email or phone number does not exist; remove this recipient from your list|Yes|Yes||
|temporary-failure|The provider was unable to deliver message, email inbox was full or phone was turned off; you can try to send the message again|Yes|Yes||
|technical-failure|Email / Text: Notify had a technical failure; you can try to send the message again. <br><br>Letter: Notify had an unexpected error while sending to our printing provider. <br><br>You can omit this argument to ignore this filter.|Yes|Yes||
|accepted|Notify is printing and posting the letter|||Yes|

#### reference

A unique identifier. This reference can identify a single unique notification or a batch of multiple notifications.

#### older_than

Input the ID of a notification into this argument. If you use this argument, the next 250 received notifications older than the given ID are returned.

If this argument is omitted, the most recent 250 notifications are returned.

[Back to top](/#gov-uk-notify-technical-documentation-python)

### Response

If the request to the client is successful, you will receive a `dict` response.

#### All messages

```python
{"notifications":
  [
    {
      "id": "NOTIFICATION ID", # required
      "reference": "CLIENT REFERENCE", # optional
      "email_address": "EMAIL ADDRESS",  # required for emails
      "phone_number": "PHONE NUMBER",  # required for sms
      "line_1": "ADDRESS LINE 1", # required for letter - name of person or company
      "line_2": "ADDRESS LINE 2", # required for letter
      "line_3": "ADDRESS LINE 3", # optional
      "line_4": "ADDRESS LINE 4", # optional
      "line_5": "ADDRESS LINE 5", # optional
      "line_6": "ADDRESS LINE 6", # optional
      "postcode": "POSTCODE", # required for letter
      "type": "TYPE", # required - sms / letter / email
      "status": "CURRENT STATUS", # required - sending / delivered / permanent-failure / temporary-failure / technical-failure
      "template": {
        "version": x # required template version number
        "id": `XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX` # required template id
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


#### One page of up to 250 messages

```python
<generator object NotificationsAPIClient.get_all_notifications_iterator at 0x1026c7410>
```

[Back to top](/#gov-uk-notify-technical-documentation-python)

### Error codes

If the request is not successful, the client will raise an `HTTPError`:

|`error.status_code`|`error.message`|
|:---|:---|
|`400`|`[{`<br>`"error": "ValidationError",`<br>`"message": "bad status is not one of [created, sending, delivered, pending, failed, technical-failure, temporary-failure, permanent-failure]"`<br>`}]`|
|`400`|`[{`<br>`"error": "ValidationError",`<br>`"message": "Apple is not one of [sms, email, letter]"`<br>`}]`|

[Back to top](/#gov-uk-notify-technical-documentation-python)

# Get a template

## Get a template by ID

### Method

This will return the latest version of the template.

Add the following method to your application code, completing the required [`template_id`](/#arguments-template-id) argument:

```python
response = notifications_client.get_template(
  'template_id'
)
```

Run your application to send a request to the API Notification client.

[Back to top](/#gov-uk-notify-technical-documentation-python)


#### template_id

The ID of the template. You can find this by logging into GOV.UK Notify and going to the _Templates_ page.

[Back to top](/#gov-uk-notify-technical-documentation-python)

### Response

If the request to the client is successful, you will receive a `dict` response.

```python
{
    "id": "template_id", # required - XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
    "type": "TYPE" , # required - sms / email / letter
    "created_at": "CREATED AT", # required
    "updated_at": "UPDATED AT", # required
    "version": "VERSION", # integer required
    "created_by": "someone@example.com", # email required
    "body": "Body of the notification", # required
    "subject": "Subject of an email or letter notification or None if an sms message"
}
```

[Back to top](/#gov-uk-notify-technical-documentation-python)

### Error codes

If the request is not successful, the client will raise an `HTTPError`:

|`error.status_code`|`error.message`|
|:---|:---|
|`404`|`[{`<br>`"error": "NoResultFound",`<br>`"message": "No Result Found"`<br>`}]`|

[Back to top](/#gov-uk-notify-technical-documentation-python)


## Get a template by ID and version

### Method

This will return the latest version of the template.

Add the following method to your application code, completing the [`template_id`](/#get-a-template-by-id-and-version-required-arguments-template-id) and [`version`](/#version) arguments:


```python
response = notifications_client.get_template_version(
    'template_id',
    'version' # integer required for version number
)
```

Run your application to send a request to the API notification client.

[Back to top](/#gov-uk-notify-technical-documentation-python)

### Required arguments

#### template_id

The ID of the template. You can find this by logging into GOV.UK Notify and going to the _Templates_ page.

#### version

The version number of the template.

[Back to top](/#gov-uk-notify-technical-documentation-python)

### Response

If the request to the client is successful, you will receive a `dict` response.

```python
{
    "id": "template_id", # XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
    "type": "TYPE", # required - "sms" / "email" / "letter"
    "created_at": "created at", # required
    "updated_at": "updated at", # required
    "version": "VERSION", # integer required
    "created_by": "EMAIL", # email required
    "body": "Body of the notification", # required
    "subject": "Subject of an email or letter notification, or None if an sms message"
}
```

[Back to top](/#gov-uk-notify-technical-documentation-python)

### Error codes

If the request is not successful, the client will raise an `HTTPError`:

|`error.status_code`|`error.message`|
|:---|:---|
|`404`|`[{`<br>`"error": "NoResultFound",`<br>`"message": "No Result Found"`<br>`}]`|

[Back to top](/#gov-uk-notify-technical-documentation-python)


## Get all templates

### Method

This will return the latest version of all templates.

Add the following method to your application code:

```python
response = notifications_client.get_all_templates(
    template_type="TYPE" # optional - "email" / "sms" / "letter"
)
```

Run your application to send a request to the API notification client.

[Back to top](/#gov-uk-notify-technical-documentation-python)

### Optional arguments

#### template_type

If omitted all templates are returned. Otherwise you can filter by:

- email
- sms
- letter

[Back to top](/#gov-uk-notify-technical-documentation-python)

### Response

If the request to the client is successful, you will receive a `dict` response.

```python
{
    "templates": [
        {
            "id": "template_id", # required - XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
            "type": "TYPE", # required - "sms" / "email" / "letter"
            "created_at": "CREATED AT", # required
            "updated_at": "UPDATED AT", # required
            "version": "VERSION", # integer required
            "created_by": "EMAIL", # email required
            "body": "Body of the notification", # required
            "subject": "Subject of an email or letter notification, or None if an sms message"
        },
        {
            ... another template
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

[Back to top](/#gov-uk-notify-technical-documentation-python)


## Generate a preview template

### Method

This will generate a preview version of a template.

Add the following method to your application code, completing the required [`template_id`](/#generate-a-preview-template-required-arguments-template-id) and [`personalisation`](/#generate-a-preview-template-required-arguments-personalisation) arguments:

```Python
response = notifications_client.post_template_preview(
    'template_id',
    personalisation={
        'KEY': 'VALUE',
        'KEY': 'VALUE',
        ...
        },
)
```

The parameters in the personalisation argument must match the placeholder fields in the actual template. The API notification client will ignore any extra fields in the method.

Run your application to send a request to the API notification client

[Back to top](/#gov-uk-notify-technical-documentation-python)

### Required arguments

#### template_id

The ID of the template. You can find this by logging into GOV.UK Notify and going to the _Templates_ page.

#### personalisation

If a template has placeholder fields for personalised information such as name or reference number, you need to provide their values in a dictionary with key value pairs. For example:

```python
personalisation={
    'first_name': 'Amala',
    'reference_number': '300241',
}
```

[Back to top](/#gov-uk-notify-technical-documentation-python)

### Response

If the request to the client is successful, you will receive a `dict` response.

```python
{
    "id": "notification_id", # required
    "type": "TYPE", # required - "sms" / "email" / "letter"
    "version": "VERSION", # integer required
    "body": "Body of the notification", # required
    "subject": "Subject of an email or letter notification, or None if an sms message"
}
```

[Back to top](/#gov-uk-notify-technical-documentation-python)

### Error codes

If the request is not successful, the client will raise an `HTTPError`:

|`error.status_code`|`error.message`|
|:---|:---|
|`400`|`[{`<br>`"error": "BadRequestError",`<br>`"message": "Missing personalisation: [PERSONALISATION FIELD]"`<br>`}]`|
|`400`|`[{`<br>`"error": "NoResultFound",`<br>`"message": "No result found"`<br>`}]`|

[Back to top](/#gov-uk-notify-technical-documentation-python)


# Get received text messages

This API call returns received text messages. Depending on which method you use, you can either get all received text messages, or a page of up to 250 text messages.

## Get all received text messages

This method will return a `<generator object>` with all received text messages.

### Method

To return all received text messages, add the following method to your application code:

```python
response = get_received_texts_iterator()
```

Run your application to send a request to the API Notification client.

[Back to top](/#gov-uk-notify-technical-documentation-python)

### Response

If the request to the client is successful, you will receive a `<generator object>` response that will return all received texts.

```python
<generator object NotificationsAPIClient.get_received_texts_iterator at 0x1026c7410>
```

[Back to top](/#gov-uk-notify-technical-documentation-python)

## Get one page of received text messages

This will return one page of up to 250 text messages.  

### Method

Add the following method to your application code:

```python
response = client.get_received_texts(older_than)
```

You can specify which texts to receive by inputting the ID of a received text message into the [`older_than`](/#get-one-page-of-received-text-messages-optional-arguments-older-than) argument.

Run your application to send a request to the API notification client.

[Back to top](/#gov-uk-notify-technical-documentation-python)

### Optional arguments

#### older_than

Input the ID of a received text message into this argument. If you use this argument, the next 250 received text messages older than the given ID are returned.

If this argument is omitted, the most recent 250 text messages are returned.

[Back to top](/#gov-uk-notify-technical-documentation-python)

### Response

If the request to the client is successful, you will receive a `dict` response.


```python
{
  "received_text_messages":
  [
    {
      "id": "ID of the received text message", # required
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
    "next": "/received-text-messages?other_than=last_id_in_list"
  }
}
```

[Back to top](/#gov-uk-notify-technical-documentation-python)

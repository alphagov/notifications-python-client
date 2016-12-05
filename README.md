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
    template_id='ceb50d92-100d-4b8b-b559-14fa3b091cda', 
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
        "id": "bfb50d92-100d-4b8b-b559-14fa3b091cda",
        "reference": None,
        "content": {
                    "body": "Some words", 
                    "from_number": "40604"
                    },
        "uri": "https://api.notifications.service.gov.uk/v2/notifications/ceb50d92-100d-4b8b-b559-14fa3b091cd",
        "template": {
                     "id": "ceb50d92-100d-4b8b-b559-14fa3b091cda",
                     "version": 1,
                     "uri": "https://api.notifications.service.gov.uk/v2/templates/bfb50d92-100d-4b8b-b559-14fa3b091cda"
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
    "message": "Can"t send to this recipient when service is in trial mode - see https://www.notifications.service.gov.uk/trial-mode"
}]
</pre>
</td>
</tr>
</tbody>
</table>
</details>


### Email

```python
response = notifications_client.send_email_notification(
    email_address='the_email_address@example.com',
    template_id='bfb50d92-100d-4b8b-b559-14fa3b091cda'
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
        "id": "bfb50d92-100d-4b8b-b559-14fa3b091cda",
        "reference": None,
        "content": {"subject": "Licence renewal",
                    "body": "Dear Bill, your licence is due for renewal on 3 January 2016.",
                    "from_email": "the_service@gov.uk"
                    },
        "uri": "https://api.notifications.service.gov.uk/v2/notifications/ceb50d92-100d-4b8b-b559-14fa3b091cd",
        "template": {
                     "id": "ceb50d92-100d-4b8b-b559-14fa3b091cda",
                     "version": 1,
                     "uri": "https://api.notificaitons.service.gov.uk/service/your_service_id/templates/bfb50d92-100d-4b8b-b559-14fa3b091cda"
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


### Arguments


#### `template_id`

Find by clicking **API info** for the template you want to send.

#### `reference`

An optional identifier you generate if you don’t want to use Notify’s `id`.


#### `personalisation`

If a template has placeholders, you need to provide their values, for example:

```python
personalisation={
    'first_name': 'Amala',
    'reference_number': '300241',
}
```
      
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
    "line_2": "123 The Street", # optional
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
                    "uri": "/template/{id}/{version}", # required
                },
	"created_at": "created at", # required
	"sent_at": " sent to provider at", # optional
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

## Get the status of all messages

```python
response = notifications_client.get_all_notifications(template_type="email", status="sending")
```
<details>
<summary>
Response
</summary>

If the request is successful, `response` will be a `dict`:

```python
{"notifications":
  [{
         "id": "notify_id", # required
         "reference": "client reference", # optional
         "email_address": "email address",  # required for emails
         "phone_number": "phone number",  # required for sms
         "line_1": "full name of a person or company", # required for letter
         "line_2": "123 The Street", # optional
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
                         "uri": "/template/{id}/{version}", # required
                     },
         "created_at": "created at", # required
         "sent_at": " sent to provider at", # optional
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

If omitted all messages are returned. Otherwise you can filter by: 

* `email`
* `sms`
* `letter`


#### `status`

If omitted all messages are returned. Otherwise you can filter by: 

* `sending` - the message is queued to be sent by the provider.
* `delivered` - the message was successfully delivered.
* `failed` - this will return all failure statuses `permanent-failure`, `temporary-failure` and `technical-failure`.
* `permanent-failure` - the provider was unable to deliver message, email or phone number does not exist; remove this recipient from your list. 
* `temporary-failure` - the provider was unable to deliver message, email box was full or the phone was turned off; you can try to send the message again.
* `technical-failure` - Notify had a technical failure; you can try to send the message again.
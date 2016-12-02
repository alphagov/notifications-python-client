# GOV.UK Notify Python client
This client provides an interface to version 2 of the notifications-api. If this is your first time using the client continue using this version to integrate with Notify. 
If you have used the client before and your version of notification-python-client is less than 4.0.0, then you will need to read this document to see the changes to the api requests and responses.

## Installation

```shell
pip install git+https://github.com/alphagov/notifications-python-client.git
```

## Getting started

```python
from notifications_python_client.notifications import NotificationsAPIClient

notifications_client = NotificationsAPIClient(api_key)
```

Generate an API key by logging in to
[GOV.UK Notify](https://www.notifications.service.gov.uk) and going to
the **API integration** page.

## Send a message

Text message:

```python
notifications_client.send_sms_notification(
    phone_number='the_phone_number', 
    template_id='the_template_id', 
    personalisation=None, 
    reference=None
)
```
Email:

```python
notifications_client.send_email_notification(
    email_address='the_email_address',
    template_id='the_template_id'
    personalisation=None, 
    reference=None
)
```

Find `template_id` by clicking **API info** for the template you want to send.

The `reference` is option, it is an identifier that you want to use to identify the notification, rather than use our id of the notification.

If a template has placeholders, you need to provide their values in `personalisation`,
for example:

```python
notifications_client.send_email_notification(
    email_address,
    template_id,
    personalisation={
        'first_name': 'Amala',
        'reference_number': '300241',
    }
)
```

<details> 
    <summary>
        Response (expand this section for more details):
    </summary>

<table>
  <thead>
    <tr>
        <td>Status
        </td>
        <td>Body
        </td>
    </tr>
  </thead>
  <tbody>
    <tr>
        <td>201
        </td>
        <td>
<pre>
{
  "id":"unique_id"
  "reference": None or "the reference you gave"
  "content": {
        "body": "Dear Bill, your licence is due for renewal on 3 January 2016.",
        "from_email": "your from email address",
        "subject": "Licence renewal"
        }
  "uri": "https://api.notifications.service.gov.uk/v2/notifications/unique_id"
  "template": {
        "id": "unique_id_of_template",
        "version": 1,
        "uri": "https://api.notificaitons.service.gov.uk/service/your_service_id/templates/unique_id_of_template"
        }
  }
}
</pre> 
        </td>
    </tr>
  </tbody>
<thead>
    <tr>
        <td>Exception
        </td>
        <td>Attributes available on the exception
        </td>
    </tr>
  </thead>
  <tbody>
    <tr>
    <tr>
        <td>HTTPError 
        </td>
        <td>
<pre>
status_code: 429
message: [{
            "error": "TooManyRequestsError",
            "message": "Exceeded send limits (50) for today"
           }
          ]
response: {
            "status_code": 429,
            "errors": [{
                        "error": "TooManyRequestsError",
                        "message": "Exceeded send limits (50) for today"
                       }
                     ]
          }
</pre>
        </td>
    </tr>
        <tr>
        <td>HTTPError
        </td>
        <td>
<pre>
status_code: 400
message: [{
             "error": "BadRequestError",
             "message": "Can"t send to this recipient using a team-only API key"
          ]}
response: {
            "status_code":"400",
            "errors":[{
                         "error": "BadRequestError",
                         "message": "Can"t send to this recipient using a team-only API key"
                      ]}
           }
</pre>
</td>
    </tr>
  </tbody>
<thead>
    <tr>
        <td>Exception
        </td>
        <td>Attributes available on the exception
        </td>
    </tr>
  </thead>
  <tbody>
        </td>
    </tr>
        </tr>
        <tr>
        <td>HTTPError
        </td>
        <td>
<pre>
status_code: 400
message: [{
             "error": "BadRequestError",
             "message": "Can"t send to this recipient when service is in trial mode - see https://www.notifications.service.gov.uk/trial-mode"
         ]
response: {   
            "status_code":"400",
            "errors":[{
                         "error": "BadRequestError",
                         "message": "Can"t send to this recipient when service is in trial mode - see https://www.notifications.service.gov.uk/trial-mode"
                     ]
          }
</pre>
        </td>
    </tr>
  </tbody>
</table>

</details> 


## Get the status of one message

```python
notifications_client.get_notification_by_id(notification_id)
```

<details> 
    <summary>
        Response (expand this section for more details):
    </summary>
<table>
  <thead>
    <tr>
        <td>Status
        </td>
        <td>Body
        </td>
    </tr>
  </thead>
  <tbody>
    <tr>
        <td>200
        </td>
        <td>

<pre>
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
</pre> 
</td>
    </tr>
  </tbody>
<thead>
    <tr>
        <td>Exception
        </td>
        <td>Attributes available on the exception
        </td>
    </tr>
  </thead>
  <tbody>
 </td>
 </tr>
 <tr>
   <td>HTTPError</td>
    <td>
<pre>
status_code: 400
message: [
    {
        "error": "ValidationError",
        "message": "id is a required"
     }
]
response: {
               "status_code":"400",
                "errors":[
                    {
                        "error": "ValidationError",
                        "message": "id is a required"
                     }
                ]
            }    
</pre>
        </td>
    </tr>
        <tr>
        <td>HTTPError
        </td>
        <td>
<pre>
status_code: 400
message: [
            {
              "error": "NoResultFound",
              "message": "No result found"
            }
         ]
response: {
              "status_code": 404
              "errors": [
                {
                  "error": "NoResultFound",
                  "message": "No result found"
                }
              ]
            }
</pre>
        </td>
    </tr>

  </tbody>
</table>


</details> 



## Get the status of all messages

```python
notifications_client.get_all_notifications(template_type="email", status="sending")
```
Optional `template_type` can be one of, if left empty all template_types are returned:

* `email`
* `sms`
* `letter`

Optional `status` can be one of, if not included then all status types are returned:

* `sending` - the message is queued to be sent by the provider.
* `delivered` - the message was successfully delivered.
* `failed` - this will return all failure statuses `permanent-failure`, `temporary-failure` and `technical-failure`.
* `permanent-failure` - the provider was unable to deliver message, email or phone number does not exist; remove this recipient from your list. 
* `temporary-failure` - the provider was unable to deliver message, email box was full or the phone was turned off; you can try to send the message again.
* `technical-failure` - Notify had a technical failure; you can try to send the message again.



<details> 
    <summary>
        Response (expand this section for more details):
    </summary>
<table>
  <thead>
    <tr>
        <td>Status
        </td>
        <td>Body
        </td>
    </tr>
  </thead>
  <tbody>
    <tr>
        <td>201
        </td>
        <td>
<pre>
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
</pre> 
        </td>
    </tr>
 </td>
    </tr>
  </tbody>
<thead>
    <tr>
        <td>Exception
        </td>
        <td>Attributes available on the exception
        </td>
    </tr>
  </thead>
  <tbody>
     <tr>
        <td>HTTPError
        </td>
        <td>
<pre>
status_code: 404
message: [
            {
              "error": "NoResultFound",
              "message": "No result found"
            }
          ]
response: {
              "status_code": 404
              "errors": [
                {
                  "error": "NoResultFound",
                  "message": "No result found"
                }
              ]
           }
</pre>
        </td>
        <tr>
        <td>HTTPError
        </td>
        <td>
<pre>
status_code: 400
message: [
            {'error': 'ValidationError',
             'message': 'bad status is not one of [created, sending, delivered, pending, failed, technical-failure, temporary-failure, permanent-failure]'
             }
          ]
response: {
                "status_code": 400,
                "errors": [
                            {'error': 'ValidationError',
                             'message': 'bad status is not one of [created, sending, delivered, pending, failed, technical-failure, temporary-failure, permanent-failure]'
                             }
                             ]
           }
</pre>
        </td>
    </tr>
    </tr>

  </tbody>
</table>

</details> 

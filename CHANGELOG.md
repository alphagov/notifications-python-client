## 4.4.0
* Added an optional parameter to `NotificationsAPIClient.send_sms_notification()` and `NotificationsAPIClient.send_email_notification()`.
  • the `schedule_for` parameter will schedule the notification to be delivered at the given time. 
  • `YYYY-MM-DD HH`  is the accepted format where the date time is in BST.
  * the `scheduled_for` is returned in the response of the  `NotificationsAPIClient.send_sms_notification()` and `NotificationsAPIClient.send_email_notification()`
    and in the  `NotificationsAPIClient.get_notification_by_id()` and `NotificationsAPIClient.get_all_notifications()`

## 4.3.0

### Changed

* Update to `NotificationsAPIClient.get_template(id)`: 
    * the `dict` returned has changed, learn more from the [README](https://github.com/alphagov/notifications-python-client#get-a-template-by-id).
* Update to `NotificationsAPIClient.get_template_version(id, version)`: 
    * the `dict` returned has changed, learn more from the [README](https://github.com/alphagov/notifications-python-client#get-a-template-by-id-and-version).
* Update to `NotificationsAPIClient.get_all_templates(template_type=None)`: 
    * the `dict` returned has changed, learn more from the [README](https://github.com/alphagov/notifications-python-client#get-all-templates)
* Replaced `NotificationsAPIClient.get_template_preview(id)` function with `NotificationsAPIClient.post_template_preview(id, persionalisation)`: 
    * See more details here [README](https://github.com/alphagov/notifications-python-client#generate-a-preview-template)

## 4.2.0

### Changed

* `NotificationsAPIClient.get_all_notifications()` 
    * Notifications can be now be filtered by `reference`, see the README for details.
    * NotificationList response has changed, see the [README](https://github.com/alphagov/notifications-python-client#get-the-status-of-all-messages-with-pagination) for details.

## 4.1.0

### Changed

* Python 2.7 supported

## 4.0.0 

### Changed
* Using version 2 of the notification-api.
* When creating a new NotificationsAPIClient the optional parameter of service_id has been removed. The api_key is a combined string contain the api_key and the service_id
* Update to `NotificationsAPIClient.send_sms_notification()`: 
    * added `reference`: an optional unique identifier for the notification or an identifier for a batch of notifications. `reference` can be omitted.
    * the `dict` returned has changed, learn more from the [README](https://github.com/alphagov/notifications-python-client#text-message). 
* Update to `NotificationClient.send_email_notification()`: 
    * added `reference`: an optional unique identifier for the notification or an identifier for a batch of notifications. `reference` can be omitted.
    * the `dict` returned has changed, learn more from the [README](https://github.com/alphagov/notifications-python-client#email). 
* Update to the response of `NotificationsAPIClient.get_notification_by_id(id)`, see the [README](https://github.com/alphagov/notifications-python-client#get-the-status-of-one-message) for details.

## 3.0.0 (2016-11-14)

### Changed
* `BaseClient` method signature: `base_url` is now optional. See [#41](https://github.com/alphagov/notifications-python-client/pull/41)
* `BaseClient` method signature: `api_key` is now a positional argument. See [#41](https://github.com/alphagov/notifications-python-client/pull/41)

## 2.0.0 (2016-11-09)

### Changed
* Replace asserts with proper exceptions in jwt token code. See [#40](https://github.com/alphagov/notifications-python-client/pull/40)

# Prior versions

Changelog not recorded - please see pull requests on github.

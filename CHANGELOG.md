## 4.0.0 
* Using version 2 of the notification-api.
* Update to `NotificationsAPIClient.send_sms_notification()`: 
    * added `reference`: an optional unique identifier for the notification or an identifier for a batch of notifications. `reference` can be omitted.
    * the `dict` returned has changed, learn more from the README. 
* Update to `NotificationClient.send_email_notification()`: 
    * added `reference`: an optional unique identifier for the notification or an identifier for a batch of notifications. `reference` can be omitted.
    * the `dict` returned has changed, learn more from the README. 
* Update to the response of `NotificationsAPIClient.get_notification_by_id(id)`, see the README for details.
* `NotificationsAPIClient.get_all_notifications()` 
    * Notifications can be now be filtered by `reference`, see the README for details.
    * NotificationList response has changed, see the README for details.


## 3.0.0 (2016-11-14)

### Changed
* `BaseClient` method signature: `base_url` is now optional. See [#41](https://github.com/alphagov/notifications-python-client/pull/41)
* `BaseClient` method signature: `api_key` is now a positional argument. See [#41](https://github.com/alphagov/notifications-python-client/pull/41)

## 2.0.0 (2016-11-09)

### Changed
* Replace asserts with proper exceptions in jwt token code. See [#40](https://github.com/alphagov/notifications-python-client/pull/40)

# Prior versions

Changelog not recorded - please see pull requests on github.

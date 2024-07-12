## 10.0.0

* Drop support for end-of-life Python 3.7
* Chain `RequestExceptions` when raising an `HTTPError` so users can view the full context in stack traces etc.

## 9.1.0

* Adds `one_click_unsubscribe_url` parameter to `send_email_notification`

## 9.0.0

* Removes the `is_csv` parameter to `prepare_upload`.
* Adds the `filename` parameter to `prepare_upload`. See [our documentation](https://docs.notifications.service.gov.uk/python.html#send-a-file-by-email) for guidance on how to use this.

## 8.2.0

* Add support for python 3.12

## 8.1.0

* Reuse the same `requests.session` between requests to increase performance through HTTP Keepalive

## 8.0.1

* Some minor non-functional code reformatting.
* Changing emitted logs to use lazy %-based evaluation rather than upfront "".format
* Changing an error-level log to a warning-level log (request failures). These still throw the actual exception to be caught and handled by the calling code.

# 8.0.0

* Add support for python 3.10 and 3.11
* Drop support for end-of-lifed python 3.6

# 7.0.0

* PyPI distribution no longer includes `integration_test`, `tests` and `utils` modules which were not intended for client use.

## 6.4.1

* Fix authentication when using PyJWT 2.6.0 - which now more strictly validates tokens with `iat` in the future.

## 6.4.0

* Added support for `confirm_email_before_download` and `retention_period` security features for sending files by email.

## 6.3.0

* Added a default timeout of 30s to the `BaseAPIClient`

## 6.2.1

* Auto-convert sets to lists in API calls

## 6.2.0

* Optionally include job notifications in `get_all_notifications`

## 6.1.0

* Add type hints for errors

## 6.0.2

* Remove two dependencies that are now not needed, `monotonic` and `future`

## 6.0.1

* Properly block old versions of python from installing the new version

## 6.0.0

* Removed support for old versions of python.
    * Drop support for Python 2.7, and versions of Python 3 below 3.6.

## 5.7.1
* Support PyJWT 2.0

## 5.7.0

* We added `letter_contact_block` to our template object serialization, which means it will be added to responses for `get_template_by_id` requests and also `get_template_version` and `get_all_templates` . This version adds this new `letter_contact_block` attribute to Documentation and tests.

## 5.6.0

* Add support for an optional `is_csv` parameter in the `prepare_upload()` function. This fixes a bug when sending a CSV file by email. This ensures that the file is downloaded as a CSV rather than a TXT file.

## 5.5.1

* change error message to refer to file rather than document

## 5.5.0

* Improve error messages for errors related to JSON Web Tokens

## 5.4.0

* Add `NotificationsAPIClient.get_pdf_for_letter(id)`
    * Returns a `BytesIO`
    * Will raise a BadRequestError if the PDF is not available


## 5.3.0

* Add an optional `postage` argument to `send_precompiled_letter_notification` method.
* Add postage to the response of `send_precompiled_letter_notification`

## 5.2.0

* Add a document size check to `prepare_upload`. Will raise `ValueError` when trying to upload a document larger than 2MB.

## 5.1.0

* Added `name` to the response for `NotificationsAPIClient.get_template_by_id()` and `NotificationsAPIClient.get_template_version()`
    * These functions now return the template name

## 5.0.1

* Change `BaseAPIClient.request` method to only add use the `data` and `params` arguments if they are not `None`, in order to avoid sending GET requests with a body of `'null'`, since these are rejected by Cloudfront.

## 5.0.0

* Changed the way documents are added to the personalisation data. A new `prepare_upload` function has to be called for each document upload to prepare the file data to be sent to the Notify API.

## 4.10.0

* Added `created_by_name` to the response for `NotificationsAPIClient.get_notification_by_id()` and `NotificationsAPIClient.get_all_notifications()`
    * If the notification was sent manually, this will be the name of the sender. If the notification was sent through the API this will be `None`.

## 4.9.0

* Add support for document uploads in `send_email_notification`

## 4.8.2

* Fix issues when installing with pip 10.0.0

## 4.8.1

* Added post_precompiled_letter_response and updated integration tests
    * The API now only returns notification id and client reference, so updated the response scheme to match

## 4.8.0

* Added `NotificationsAPIClient.send_precompiled_letter_notification()`
    * The client can now send PDF files which conform to the Notify printing template
    * Send a File object
    * 'reference' must be provided to identify the document

## 4.7.2
* Use Flake 8 rather than Pep 8

## 4.7.1

* Fixed PyJWT security issue. [#91](https://github.com/alphagov/notifications-python-client/pull/91)

## 4.7.0

* Added `NotificationsAPIClient.get_received_texts()`
    * an optional `older_than` argument can be specified to retrieve all received texts older than the last
    received text id. If omitted the first 250, the api limit, received texts will be returned, with links indicating how to retrieve the next page of results.
* Added `NotificationsAPIClient.get_received_texts_iterator()`
    * returns all received texts by a generator object.

## 4.6.0

### Changed

* Update to `NotificationsAPIClient.send_sms_notification()`
    * added `sms_sender_id`: an optional `sms_sender_id` specified when adding SMS senders under service settings. If this is not provided, the SMS sender will be the service default SMS sender. `sms_sender_id` can be omitted.

## 4.5.0

* Update to `NotificationsAPIClient.send_email_notification()`
    * added `email_reply_to_id`: an optional email_reply_to_id specified when adding Email reply to addresses under service settings, if this is not provided the reply to email will be the service default reply to email. `email_reply_to_id` can be omitted.

## 4.4.0

### Added

* Added `NotificationsAPIClient.send_letter_notification()`:
  * functions similarly to `send_sms_notification` and `send_email_notification`, however, address details are provided
    in the personalisation dict
  * See more details in the [README](https://github.com/alphagov/notifications-python-client#letter)

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

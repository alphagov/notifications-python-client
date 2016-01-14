from ..conftest import TEST_HOST


def test_get_service(notifications_client, rmock, service_json):
    endpoint = "{0}/service/{1}".format(TEST_HOST, service_json['id'])
    rmock.request(
        "GET",
        endpoint,
        json=service_json,
        status_code=200)

    result = notifications_client.get_service(service_json['id'])

    assert rmock.called
    assert result == service_json


def test_get_services(notifications_client, rmock, services_json):
    endpoint = "{0}/service".format(TEST_HOST)
    rmock.request(
        "GET",
        endpoint,
        json=services_json,
        status_code=200)

    result = notifications_client.get_services()

    assert rmock.called
    assert result == services_json


def test_get_service_template(notifications_client, rmock, service_template_json):
    endpoint = "{0}/service/{1}/template/{2}".format(
        TEST_HOST,
        service_template_json['service'],
        service_template_json['id'])
    rmock.request(
        "GET",
        endpoint,
        json=service_template_json,
        status_code=200)

    result = notifications_client.get_service_template(
        service_template_json['service'], service_template_json['id'])

    assert rmock.called
    assert result == service_template_json


def test_get_service_templates(notifications_client, rmock, service_templates_json):
    endpoint = "{0}/service/{1}/template".format(
        TEST_HOST,
        service_templates_json[0]['service'])
    rmock.request(
        "GET",
        endpoint,
        json=service_templates_json,
        status_code=200)

    result = notifications_client.get_service_templates(
        service_templates_json[0]['service'])

    assert rmock.called
    assert result == service_templates_json

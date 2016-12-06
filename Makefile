.DEFAULT_GOAL := help
SHELL := /bin/bash

PIP_ACCEL_CACHE ?= ${CURDIR}/.cache/pip-accel

DOCKER_BUILDER_IMAGE_NAME = govuk/notify-python-client-runner

BUILD_TAG ?= notifications-python-client-manual

DOCKER_CONTAINER_PREFIX = ${USER}-${BUILD_TAG}

PYPI_REPOSITORY_NAME = pypi
PYPI_REPOSITORY_URL = https://pypi.python.org/pypi/
# pypi's test repository, for testing changes to .rst or packaging. Note: you'll need different credentials for testpypi
# PYPI_REPOSITORY_NAME = testpypi
# PYPI_REPOSITORY_URL = https://testpypi.python.org/pypi

.PHONY: help
help:
	@cat $(MAKEFILE_LIST) | grep -E '^[a-zA-Z_-]+:.*?## .*$$' | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: venv
venv: venv/bin/activate ## Create virtualenv if it does not exist

venv/bin/activate:
	test -d venv || virtualenv venv -p python3
	./venv/bin/pip install pip-accel

.PHONY: dependencies
dependencies: venv ## Install build dependencies
	mkdir -p ${PIP_ACCEL_CACHE}
	PIP_ACCEL_CACHE=${PIP_ACCEL_CACHE} ./venv/bin/pip-accel install -r requirements_for_test.txt

.PHONY: build
build: dependencies ## Build project

.PHONY: test
test: venv ## Run tests
	./scripts/run_tests.sh

.PHONY: integration-test
integration-test: ## Run integration tests
	./scripts/run_integration_tests.sh

.PHONY: build-wheel
build-wheel: venv ## build distributable wheel
	./venv/bin/pip install wheel
	./venv/bin/python setup.py bdist_wheel

.PHONY: publish-to-pypi
publish-to-pypi: build-wheel ## upload distributable wheel to pypi
	./venv/bin/pip install twine
	twine upload dist/*.whl \
		--repository=${PYPI_REPOSITORY_NAME} \
		--repository-url=${PYPI_REPOSITORY_URL} \
		--username=${PYPI_USERNAME} \
		--password=${PYPI_PASSWORD} \
		--skip-existing # if you haven't run `make clean` there may be old wheels - don't try and re-upload them

.PHONY: generate-env-file
generate-env-file: ## Generate the environment file for running the tests inside a Docker container
	scripts/generate_docker_env.sh

.PHONY: prepare-docker-runner-image
prepare-docker-runner-image: ## Prepare the Docker builder image
	make -C docker build

.PHONY: build-with-docker
build-with-docker: prepare-docker-runner-image ## Build inside a Docker container
	docker run -i --rm \
		--name "${DOCKER_CONTAINER_PREFIX}-build" \
		-v `pwd`:/var/project \
		-e http_proxy="${HTTP_PROXY}" \
		-e HTTP_PROXY="${HTTP_PROXY}" \
		-e https_proxy="${HTTPS_PROXY}" \
		-e HTTPS_PROXY="${HTTPS_PROXY}" \
		-e NO_PROXY="${NO_PROXY}" \
		${DOCKER_BUILDER_IMAGE_NAME} \
		make build

.PHONY: test-with-docker
test-with-docker: prepare-docker-runner-image generate-env-file ## Run tests inside a Docker container
	docker run -i --rm \
		--name "${DOCKER_CONTAINER_PREFIX}-test" \
		-v `pwd`:/var/project \
		-e http_proxy="${HTTP_PROXY}" \
		-e HTTP_PROXY="${HTTP_PROXY}" \
		-e https_proxy="${HTTPS_PROXY}" \
		-e HTTPS_PROXY="${HTTPS_PROXY}" \
		-e NO_PROXY="${NO_PROXY}" \
		--env-file docker.env \
		${DOCKER_BUILDER_IMAGE_NAME} \
		make test

.PHONY: integration-test-with-docker
integration-test-with-docker: prepare-docker-runner-image generate-env-file ## Run integration tests inside a Docker container
	docker run -i --rm \
		--name "${DOCKER_CONTAINER_PREFIX}-integration-test" \
		-v `pwd`:/var/project \
		-e http_proxy="${HTTP_PROXY}" \
		-e HTTP_PROXY="${HTTP_PROXY}" \
		-e https_proxy="${HTTPS_PROXY}" \
		-e HTTPS_PROXY="${HTTPS_PROXY}" \
		-e NO_PROXY="${NO_PROXY}" \
		--env-file docker.env \
		${DOCKER_BUILDER_IMAGE_NAME} \
		make integration-test

.PHONY: publish-to-pypi-with-docker
publish-to-pypi-with-docker: prepare-docker-runner-image generate-env-file ## publish wheel to pypi inside a docker container
	docker run -i --rm \
		--name "${DOCKER_CONTAINER_PREFIX}-publish-to-pypi" \
		-v `pwd`:/var/project \
		-e http_proxy="${HTTP_PROXY}" \
		-e HTTP_PROXY="${HTTP_PROXY}" \
		-e https_proxy="${HTTPS_PROXY}" \
		-e HTTPS_PROXY="${HTTPS_PROXY}" \
		-e NO_PROXY="${NO_PROXY}" \
		-e PYPI_USERNAME="${PYPI_USERNAME}" \
		-e PYPI_PASSWORD="${PYPI_PASSWORD}" \
		--env-file docker.env \
		${DOCKER_BUILDER_IMAGE_NAME} \
		make publish-to-pypi

.PHONY: clean-docker-containers
clean-docker-containers: ## Clean up any remaining docker containers
	docker rm -f $(shell docker ps -q -f "name=${DOCKER_CONTAINER_PREFIX}") 2> /dev/null || true

clean:
	rm -rf .cache venv dist .eggs build

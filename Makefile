.DEFAULT_GOAL := help
SHELL := /bin/bash

DOCKER_BUILDER_IMAGE_NAME = govuk/notify-python-client-runner

BUILD_TAG ?= notifications-python-client-manual

DOCKER_CONTAINER_PREFIX = ${USER}-${BUILD_TAG}

.PHONY: help
help:
	@cat $(MAKEFILE_LIST) | grep -E '^[a-zA-Z_-]+:.*?## .*$$' | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: dependencies
dependencies: ## Install build dependencies
	pip install -r requirements_for_test.txt

.PHONY: build
build: dependencies ## Build project

.PHONY: test
test: ## Run tests
	flake8 .
	pytest

.PHONY: integration-test
integration-test: ## Run integration tests
	python integration_test/integration_tests.py

.PHONY: build-wheel
build-wheel: ## build distributable wheel
	pip install wheel
	python setup.py bdist_wheel

.PHONY: publish-to-pypi
publish-to-pypi: build-wheel ## upload distributable wheel to pypi
	pip install --upgrade twine
	@twine upload dist/*.whl \
		--username="${PYPI_USERNAME}" \
		--password="${PYPI_PASSWORD}" \
		--skip-existing # if you haven't run `make clean` there may be old wheels - don't try and re-upload them

.PHONY: generate-env-file
generate-env-file: ## Generate the environment file for running the tests inside a Docker container
	scripts/generate_docker_env.sh

.PHONY: prepare-docker-runner-image
prepare-docker-runner-image: ## Prepare the Docker builder image
	docker build -t ${DOCKER_BUILDER_IMAGE_NAME} .

.PHONY: build-with-docker
build-with-docker: prepare-docker-runner-image ## Build inside a Docker container
	docker run -i --rm \
		--name "${DOCKER_CONTAINER_PREFIX}-build" \
		-v "`pwd`:/var/project" \
		-v "`pwd`/tox-python-versions:/var/project/.python-version" \
		${DOCKER_BUILDER_IMAGE_NAME} \
		make build

.PHONY: test-with-docker
test-with-docker: prepare-docker-runner-image generate-env-file ## Run tests inside a Docker container
	docker run -i --rm \
		--name "${DOCKER_CONTAINER_PREFIX}-test" \
		-v "`pwd`:/var/project" \
		-v "`pwd`/tox-python-versions:/var/project/.python-version" \
		--env-file docker.env \
		${DOCKER_BUILDER_IMAGE_NAME} \
		make test

.PHONY: integration-test-with-docker
integration-test-with-docker: prepare-docker-runner-image generate-env-file ## Run integration tests inside a Docker container
	docker run -i --rm \
		--name "${DOCKER_CONTAINER_PREFIX}-integration-test" \
		-v "`pwd`:/var/project" \
		-v "`pwd`/tox-python-versions:/var/project/.python-version" \
		--env-file docker.env \
		${DOCKER_BUILDER_IMAGE_NAME} \
		make integration-test

.PHONY: publish-to-pypi-with-docker
publish-to-pypi-with-docker: prepare-docker-runner-image generate-env-file ## publish wheel to pypi inside a docker container
	@docker run -i --rm \
		--name "${DOCKER_CONTAINER_PREFIX}-publish-to-pypi" \
		-v "`pwd`:/var/project" \
		-v "`pwd`/tox-python-versions:/var/project/.python-version" \
		-e PYPI_USERNAME="${PYPI_USERNAME}" \
		-e PYPI_PASSWORD="${PYPI_PASSWORD}" \
		--env-file docker.env \
		${DOCKER_BUILDER_IMAGE_NAME} \
		make publish-to-pypi

.PHONY: clean-docker-containers
clean-docker-containers: ## Clean up any remaining docker containers
	docker rm -f $(shell docker ps -q -f "name=${DOCKER_CONTAINER_PREFIX}") 2> /dev/null || true

clean:
	rm -rf .cache dist .eggs build .tox

.PHONY: tox-with-docker
tox-with-docker: prepare-docker-runner-image generate-env-file
	docker run -i --rm \
		--name "${DOCKER_CONTAINER_PREFIX}-integration-test" \
		-v "`pwd`:/var/project" \
		-v "`pwd`/tox-python-versions:/var/project/.python-version" \
		--env-file docker.env \
		${DOCKER_BUILDER_IMAGE_NAME} \
		tox

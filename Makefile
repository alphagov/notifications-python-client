.DEFAULT_GOAL := help
SHELL := /bin/bash

.PHONY: help
help:
	@cat $(MAKEFILE_LIST) | grep -E '^[a-zA-Z_-]+:.*?## .*$$' | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: bootstrap
bootstrap: ## Install build dependencies
	pip install -r requirements_for_test.txt

.PHONY: build
build: bootstrap ## Build project (dummy task for CI)

.PHONY: test
test: ## Run tests
	flake8 .
	isort --check-only ./notifications_python_client ./utils ./integration_test ./tests
	black --check .
	pytest

.PHONY: integration-test
integration-test: ## Run integration tests
	python -m integration_test.integration_tests

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

.PHONY: bootstrap-with-docker
bootstrap-with-docker: ## Prepare the Docker builder image
	docker build -t notifications-python-client .

.PHONY: test-with-docker
test-with-docker: ## Run tests inside a Docker container
	./scripts/run_with_docker.sh make test

.PHONY: integration-test-with-docker
integration-test-with-docker: ## Run integration tests inside a Docker container
	./scripts/run_with_docker.sh make integration-test

.PHONY: tox-with-docker
tox-with-docker:
	./scripts/run_with_docker.sh tox

clean:
	rm -rf .cache dist .eggs build .tox

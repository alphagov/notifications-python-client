.DEFAULT_GOAL := help
SHELL := /bin/bash

.PHONY: help
help:
	@cat $(MAKEFILE_LIST) | grep -E '^[a-zA-Z_-]+:.*?## .*$$' | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: freeze-requirements
freeze-requirements: ## Freeze requirements files
	pip install -r requirements.txt
	python -c "from notifications_utils.version_tools import copy_config; copy_config()"
	pip-compile -o requirements_for_test.txt setup.py requirements_for_test.in

.PHONY: bootstrap
bootstrap: ## Install build dependencies
	pip install --upgrade pip-tools
	pip install -r requirements_for_test.txt

.PHONY: build
build: bootstrap ## Build project (dummy task for CI)

.PHONY: bump-utils
bump-utils:  # Bump notifications-utils package to latest version
	python -c "from notifications_utils.version_tools import upgrade_version; upgrade_version()"

.PHONY: test
test: ## Run tests
	ruff check .
	ruff format --check .
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

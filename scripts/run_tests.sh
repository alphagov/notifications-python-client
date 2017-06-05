#!/bin/bash
#
# Run project tests
#
# NOTE: This script expects to be run from the project root with
# ./scripts/run_tests.sh

# Use default environment vars for localhost if not already set

set -o pipefail

[ "$IGNORE_ENVIRONMENT_SH" = "1" ] || source environment.sh 2> /dev/null

function display_result {
  RESULT=$1
  EXIT_STATUS=$2
  TEST=$3

  if [ $RESULT -ne 0 ]; then
    echo -e "\033[31m$TEST failed\033[0m"
    exit $EXIT_STATUS
  else
    echo -e "\033[32m$TEST passed\033[0m"
  fi
}

if [ -d venv ]; then
  source ./venv/bin/activate
fi

pep8 --exclude=venv,.tox .

display_result $? 1 "Code style check"

## Code coverage
#py.test --cov=client tests/
#display_result $? 2 "Code coverage"

py.test -v -x tests/
display_result $? 3 "Unit tests"

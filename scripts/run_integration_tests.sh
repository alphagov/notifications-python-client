#!/bin/bash
#
# Run project tests
#
# NOTE: This script expects to be run from the project root with
# ./scripts/run_integration_tests.sh

# Use default environment vars for localhost if not already set

set -o pipefail

[ "$IGNORE_ENVIRONMENT_SH" = "1" ] || source environment.sh 2> /dev/null

if [ -d venv ]; then
  source ./venv/bin/activate
fi

PYTHONPATH=. python integration_test/integration_tests.py

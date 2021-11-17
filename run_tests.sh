#!/bin/bash
#
# Run Python unit tests

# Exit on first error
set -o errexit

# Activate our virtual environment
# shellcheck disable=SC1091
source venv/bin/activate

# Run our unit tests with code coverage
# shellcheck disable=SC2140
python -m coverage run --omit="venv/*","tests/*" -m unittest discover tests/

# Show the lines our tests miss
python -m coverage report --show-missing

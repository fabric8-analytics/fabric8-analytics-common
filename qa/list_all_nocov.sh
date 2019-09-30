#!/bin/bash

# Lists all "pragma:s" in all Python source codes

SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"

pushd "${SCRIPT_DIR}/.."

grep -r --include "*.py" "pragma: " .

popd

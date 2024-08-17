#!/bin/bash
SCRIPT_PATH=$(readlink -f "$0")
SCRIPT_FOLDER=$(dirname "$SCRIPT_PATH")
pushd "$SCRIPT_FOLDER" > /dev/null

PYTHON_FILE="./src/HOMFLY-PT-indexer/src/HOMFLY-PT-solver/src/x86_64-sage-minimal/src/bin/portable_sage/sage/bin/python3.11"
chmod +x "$PYTHON_FILE"

echo -e "\033[1;34mINFO\033[0m: using python3.11 packed in sagemath." 1>&2
"$PYTHON_FILE" "$@"

popd > /dev/null

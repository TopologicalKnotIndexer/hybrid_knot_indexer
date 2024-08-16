#!/bin/bash
SCRIPT_PATH=$(readlink -f "$0")
SCRIPT_FOLDER=$(dirname "$SCRIPT_PATH")
pushd "$SCRIPT_FOLDER" > /dev/null

bash ./src/HOMFLY-PT-indexer/src/HOMFLY-PT-solver/src/x86_64-sage-minimal/src/bin/portable_sage/test_all.sh
bash ./python3.sh ./src/main.py --test

popd > /dev/null

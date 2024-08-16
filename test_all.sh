#!/bin/bash
SCRIPT_PATH=$(readlink -f "$0")
SCRIPT_FOLDER=$(dirname "$SCRIPT_PATH")
pushd "$SCRIPT_FOLDER" > /dev/null

# 删除压缩包中原先自带的二进制版本
KNOT_PDCODE_BIN="./src/che_data_to_pd_code/src/spatial_coord_to_pd_code/src/knot-pdcode"
if [ -f "$KNOT_PDCODE_BIN" ]; then
    echo -e "\033[1;34mINFO\033[0m: erasing original knot-pdcode binary." 1>&2
    rm "$KNOT_PDCODE_BIN"
fi

bash ./src/HOMFLY-PT-indexer/src/HOMFLY-PT-solver/src/x86_64-sage-minimal/src/bin/portable_sage/test_all.sh
bash ./python3.sh ./src/main.py --test

popd > /dev/null

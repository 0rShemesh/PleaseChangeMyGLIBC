#!/usr/bin/env bash

ELF_TO_INJECT="$(realpath $1)"

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
ORIGINAL_DIR=$(pwd)
cd $SCRIPT_DIR

python3 patch_binary_to_glibc.py $ELF_TO_INJECT

cd $ORIGINAL_DIR

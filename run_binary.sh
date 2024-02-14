#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
GLIBC_TAG="glibc-2.39"

GLIBC_DIRECTORY=$(realpath ./glibc)

LD_LIBRARY_PATH="$SCRIPT_DIR/builds/$GLIBC_TAG/elf/ld.so" $*

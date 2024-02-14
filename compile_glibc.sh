#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
ORIGINAL_DIR=$(pwd)
cd $SCRIPT_DIR

# in case of diffrent toolchain
# DIFFRENT_TOOLCHAIN=/opt/external_compiler
# source $DIFFRENT_TOOLCHAIN/activate

# checkout to the relevant version
GLIBC_TAG="glibc-2.39"

# Enable malloc debug things
# export CPPFLAGS="-DMALLOC_DEBUG=1"
GLIBC_DIRECTORY=$(realpath ./glibc)


cd $GLIBC_DIRECTORY
git checkout $GLIBC_TAG
cd ..
export glibc_install="$(pwd)/install"

mkdir -p ./builds/$GLIBC_TAG
cd ./builds/$GLIBC_TAG
$GLIBC_DIRECTORY/configure --prefix "$glibc_install" --enable-debug
make -j $(nproc)


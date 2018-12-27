#!/bin/bash -e

pushd $(dirname $0) &>/dev/null

./download.sh
./process.sh

popd &>/dev/null


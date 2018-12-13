#!/bin/bash -e

pushd $(dirname $0) &>/dev/null

./download.sh
./process_sbdb.py
./process_close_approach.py

popd &>/dev/null


#!/bin/bash -e

pushd $(dirname $0) &>/dev/null

./download.sh
./process_sbdb.py
./process_close_approach.py
./process_sentry.py

popd &>/dev/null


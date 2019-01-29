#!/bin/bash -e

pushd $(dirname $0) &>/dev/null

./process_sbdb.py
./process_close_approach.py
./process_sentry.py
./process_nhats.py
./process_damit.py

popd &>/dev/null

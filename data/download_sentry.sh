#!/bin/bash -e

pushd $(dirname $0) &>/dev/null

curl -o rawdata/sentry.json https://ssd-api.jpl.nasa.gov/sentry.api?all=1

popd &>/dev/null

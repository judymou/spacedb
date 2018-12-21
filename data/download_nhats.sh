#!/bin/bash -e

pushd $(dirname $0) &>/dev/null

curl -o rawdata/nhats.json https://ssd-api.jpl.nasa.gov/nhats.api

popd &>/dev/null

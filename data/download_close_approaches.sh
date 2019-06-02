#!/bin/bash -e

pushd $(dirname $0) &>/dev/null

curl 'https://ssd-api.jpl.nasa.gov/cad.api?date-min=2019-01-01&date-max=2200-01-01&dist-max=0.2&fullname=true' -o rawdata/close_approach.json

popd &>/dev/null

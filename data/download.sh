#!/bin/bash -e

pushd $(dirname $0) &>/dev/null

mkdir -p rawdata

echo 'Downloading SBDB...'
./download_sbdb.sh

echo 'Downloading close approaches...'
./download_close_approaches.sh

echo 'Downloading sentry...'
./download_sentry.sh

echo 'Downloading nhats...'
./download_nhats.sh

echo 'Downloading damit...'
./download_damit.sh

echo 'Done.'

popd &>/dev/null

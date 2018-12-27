#!/bin/bash -e

pushd $(dirname $0) &>/dev/null

cd ..
git pull
docker-compose build
docker-compose down
docker-compose up -d

popd &>/dev/null

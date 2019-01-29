#!/bin/bash -e

pushd $(dirname $0) &>/dev/null

mkdir -p rawdata/shapes
rm -rf rawdata/shapes/*
cd rawdata/shapes

# Download complete flush from
# http://astro.troja.mff.cuni.cz/projects/asteroids3D/web.php?page=db_export
curl -o damit.tar.gz http://www.ianww.com/damit.tar.gz

# Decompress
tar xzvf damit.tar.gz
# Put everything into one directory instead of breaking it up every thousand
# Use find instead of mv because on mac mv limits the number of arguments.
find archive/ -name '*.*' -exec mv {} archive/. \;

popd &>/dev/null

#!/bin/bash -e

pushd $(dirname $0) &>/dev/null

mkdir -p rawdata/shapes
#rm -rf rawdata/shapes/*
cd rawdata/shapes

echo 'Download complete flush from'
echo 'http://astro.troja.mff.cuni.cz/projects/asteroids3D/web.php?page=db_export'

echo '...'

# Decompress
tar xzvf damit_flush_complete*
# Put everything into one directory instead of breaking it up every thousand
# Use find instead of mv because on mac mv limits the number of arguments.
find archive/ -name '*.*' -exec mv {} archive/. \;

popd &>/dev/null

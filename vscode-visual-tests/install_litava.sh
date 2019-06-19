#!/bin/bash -ex

# Script to install the Litava executable that can be used to fuzzy pattern matching in raster images

rm -f ./litava
rm -rf ./litava.git
git clone https://github.com/tisnik/litava.git litava.git
pushd litava.git
make clean
make
mv ./litava ../
popd

#!/bin/bash

# Load environment variables from the .env file
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

echo "Python: $(which python)"
echo "Python version: $(python --version)"
echo "Cmake: $(which cmake)"

# clean the build folder
rm -rf build

# Configuring cmake
cmake -D KRISP_SDK_PATH=${KRISP_SDK_PATH} \
      -D Python3_FIND_VIRTUALENV=ONLY \
      -S lib/cmake -B build

# Building the main C++ sample, look inside makefile to learn how to build the other sample apps
cmake --build build
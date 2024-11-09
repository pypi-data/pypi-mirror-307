#!/bin/bash

# Clear all the files that we are not supposed to bundle
sh ./scripts/clear.sh

# Build the dist
python setup.py sdist

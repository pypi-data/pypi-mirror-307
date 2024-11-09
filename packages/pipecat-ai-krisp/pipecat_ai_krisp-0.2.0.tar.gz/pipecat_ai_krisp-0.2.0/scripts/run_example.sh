#!/bin/bash

mkdir -p ./output

# Load environment variables from the .env file
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

python example/process_wav_file.py \
  -i example/sample-nc-test-pcm16.wav \
  -o output/out-pcm16.wav \
  -m ${KRISP_MODEL_PATH}
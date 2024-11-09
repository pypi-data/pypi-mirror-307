# Pipecat Krisp

This module provides a Python wrapper around Krisp's C++ SDK, enabling its integration with Pipecat. 
Krisp offers a Desktop SDK (in C++) that supports Linux, Windows, and macOS, allowing applications to leverage noise suppression capabilities.

## Prerequisites

1. **Krisp Desktop SDK**: Download Krisp's Desktop SDK and the model you wish to use from [Krisp's desktop SDKs](https://sdk.krisp.ai/sdk/desktop).
2. **Environment Configuration**:
   - Copy the provided `env_template` file to a new file named `.env`.
   - In `.env`, set the paths to the downloaded Krisp SDK and model files.
3. **CPython Module Dependencies**
   - In addition to above dependencies you will need the pybind11 library to build CPython modules using C++.
   - On Ubuntu Linux: `sudo apt-get install pybind11-dev`
   - On Mac: `brew install pybind11`

### Environment Template

Below is the format for the `.env` file. Replace the placeholders with the actual paths where the Krisp SDK and model are located:

```env
KRISP_SDK_PATH=/PATH/TO/KRISP/SDK
KRISP_MODEL_PATH=/PATH/TO/KRISP/MODEL
```

## Installation and Setup

Follow these steps to set up and build the Pipecat Krisp Module:

- Set up a Virtual Environment:
```shell
python3 -m venv venv
source venv/bin/activate
```

- Install Dependencies:
```shell
pip install -r requirements.txt
```

- Build and Install the Local Python wrapper Library:
```shell
pip install --editable .
```

## Running the Example

- Install Dependencies:
```shell
pip install -r example/requirements.txt
```

After setup, you can run an example script to test the Krisp integration:

```shell
./scripts/run_example.sh
```
> An output folder will be created, containing the processed file with noise suppression applied by Krisp.

## Publishing

- Prepare to dist:
```shell
./scripts/prepare_dist.sh
```

- Test the build using TestPyPI with Twine:

Upload to TestPyPI using twine
```shell
twine upload --repository testpypi dist/*
```

Test using pip to download packages from TestPyPI instead of PyPI
```shell
pip install --index-url https://test.pypi.org/simple/ pipecat-ai-krisp
```

Once you are happy, publish it to production.
```shell
twine upload dist/*
```

> Use twine upload dist/* to upload your package and enter your credentials for the account you registered on the real PyPI.
> In this case you don’t need to specify --repository.

## References
- Krisp getting started:  https://sdk-docs.krisp.ai/docs/getting-started-js
- Krisp Sample Apps: https://github.com/krispai/Krisp-SDK-Sample-Apps/tree/krisp-sdk-v9
- Python packaging guide: https://packaging.python.org/en/latest/guides/using-testpypi/

## Getting help

➡️ [Join our Discord](https://discord.gg/pipecat)

➡️ [Reach us on X](https://x.com/pipecat_ai)

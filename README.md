# OpenHexa Python SDK

## Running the examples

Clone the repo and install the dependencies, including the ones required to run the examples:

```shell
git checkout https://github.com/BLSQ/openhexa-sdk-python.git
pip install ".[examples]"
```

Run a pipeline:

```shell
cd examples/pipelines/logistic_stats
python pipeline.py -c '{"deg":"qfxEYY9xAl6","periods":["2022Q1","2022Q2"]}'
```

Or using a config file:

```shell
cd examples/pipelines/logistic_stats
python pipeline.py -f example_conf.json
```

## Development & testing

Install the SDK in editable mode:

```shell
python -m venv venv # Create a virtual environment for this project
source venv/bin/activate # Activate the venv
pip install -r requirements.txt
```

Run the tests using pytest:

```shell
pytest
```


## Publishing the pipelines image

The docker image `openhexa-pipelines` is still build and published manually. Follow the steps below to publish a new docker image.

```shell
cd openhexa-sdk-python
python -m build .
mv dist/*.whl docker/
cd docker
docker build -t openhexa-pipelines .
docker tag openhexa-pipelines blsq/openhexa-pipelines:latest
docker push blsq/openhexa-pipelines:latest
```

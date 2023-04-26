# OpenHexa Python SDK

The OpenHexa Python SDK is a tool that helps you write code for the OpenHexa platform.

It is particularly useful to write OpenHexa data pipelines, but can also be used in the OpenHexa notebooks environment.

## Writing data pipelines

TBC

## Using the SDK in the notebooks environment

TBC

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

## Using the CLI

Now that your pipeline is functional, you can push it to the OpenHexa backend so that it can run online.

As code and data are organized with workspaces, the first think to do is to activate a workspace using the CLI.

Using the OpenHexa interface, chose a workspace, click on the "Pipelines" section and then on the "Create" 
call-to-action at the top-right of the header. You will find ready-to use instructions on how to activate 
the workspace, as well as the API token you need to use.

The command looks as follows:

```shell
openhexa workspaces add <workspace_slug>
```

You can then push your pipeline:

```shell
openhexa pipelines push <pipeline_directory>
```

## Development & testing

### Development setup

Install the SDK in editable mode:

```shell
python -m venv venv # Create a virtual environment for this project
source venv/bin/activate # Activate the venv
pip install -r requirements.txt
pip install -e ".[dev]"  # Necessary to be able to run the openhexa CLI
```

### Using a local installation of the OpenHexa backend to run pipelines

```shell
openhexa config set_url http://localhost:8000
```

Notes: you can monitor the status of your pipelines using http://localhost:8000/pipelines/status

### Running the tests

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

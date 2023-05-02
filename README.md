# OpenHexa Python SDK

The OpenHexa Python SDK is a tool that helps you write code for the OpenHexa platform.

It is particularly useful to write OpenHexa data pipelines, but can also be used in the OpenHexa notebooks environment.

## Quickstart

### Writing and deploying pipelines

Here's a super minimal example to get you started. First, create a new directory and a virtual environment:

```shell
mkdir openhexa-pipelines-quickstart
cd openhexa-pipelines-quickstart
virtualenv venv
source venv/bin/activate
```

You can then install the OpenHexa SDK:

```shell
pip install --upgrade openhexa.sdk
```

Now that the SDK is installed withing your virtual environmentYou can now use the `openhexa` CLI utility to create 
a new pipeline:

```shell
openhexa pipelines init "My awesome pipeline"
```

Great! As you can see in the console output, the OpenHexa CLI has created a new directory, which contains the basic 
structure required for an OpenHexa pipeline. You can now `cd` in the new pipeline directory and run the pipeline:

```shell
cd my_awesome_pipeline
python pipeline.py
```

Congratulations! You have successfully run your first pipeline locally.

If you inspect the actual pipeline code, you will see that it doesn't do a lot of things, but it is still a perfectly 
valid OpenHexa pipeline.

Let's publish to an actual OpenHexa workspace so that it can run online.

Using the OpenHexa web interface, within a workspace, navigate to the Pipelines tab and click on "Create".

Copy the command displayed in the popup in your terminal:

```shell
openhexa workspaces add <workspace>
```

You will be prompted for an authentication token, you can find it in the popup as well.

After adding the workspace using the CLI, you can now push your pipeline:

```shell
openhexa pipelines push 
```

As it is the first time, the CLI will ask you to confirm the creation operation. After confirmation the console will 
output the link to the pipeline screen in the OpenHexa interface.

You can now open the link and run the pipeline using the OpenHexa web interface.

### Using the SDK in the notebooks environment

TBC

## Contributing

The following sections explain how you can setup a local development environment if you want to participate to the 
development of the SDK

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

### Publishing the pipelines image

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

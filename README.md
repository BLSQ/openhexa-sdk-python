<div align="center">
   <img alt="OpenHEXA Logo" src="https://raw.githubusercontent.com/BLSQ/openhexa-app/main/hexa/static/img/logo/logo_with_text_grey.svg" height="80">
</div>
<p align="center">
    <em>Open-source Data integration platform</em>
</p>
<p align="center">
   <a href="https://github.com/BLSQ/openhexa-app/actions/workflows/test.yml">
      <img alt="Test Suite" src="https://github.com/BLSQ/openhexa-sdk-python/actions/workflows/ci.yml/badge.svg">
   </a>
</p>

OpenHEXA Python SDK
===================

OpenHEXA is an open-source data integration platform developed by [Bluesquare](https://bluesquarehub.com).

Its goal is to facilitate data integration and analysis workflows, in particular in the context of public health 
projects.

Please refer to the [OpenHEXA wiki](https://github.com/BLSQ/openhexa/wiki/Home) for more information about OpenHEXA.

This repository contains the code of the OpenHEXA SDK, a library allows you to write code for the OpenHEXA platform. 
It is particularly useful to write OpenHEXA data pipelines, but can also be used in the OpenHEXA notebooks environment.

The OpenHEXA wiki has a section dedicated to the SDK: 
[Using the OpenHEXA SDK](https://github.com/BLSQ/openhexa/wiki/Using-the-OpenHEXA-SDK).

Requirements
------------

The OpenHEXA SDK requires Python version 3.9 or newer, but it is not yet compatible with Python 3.12 or later versions.

If you want to be able to run pipeline in a containerized environment on your machine, you will need 
[Docker](https://www.docker.com/).

Quickstart
----------

Here's a super minimal example to get you started. First, create a new directory and a virtual environment:

```shell
mkdir openhexa-pipelines-quickstart
cd openhexa-pipelines-quickstart
python -m venv venv
source venv/bin/activate
```

You can then install the OpenHEXA SDK:

```shell
pip install --upgrade openhexa.sdk
```

💡New OpenHEXA SDK versions are released on a regular basis. Don't forget to update your local installations with 
`pip install --upgrade` from times to times!

Now that the SDK is installed withing your virtual environmentYou can now use the `openhexa` CLI utility to create 
a new pipeline:

```shell
openhexa pipelines init "My awesome pipeline"
```

Great! As you can see in the console output, the OpenHEXA CLI has created a new directory, which contains the basic 
structure required for an OpenHEXA pipeline. You can now `cd` in the new pipeline directory and run the pipeline:

```shell
cd my_awesome_pipeline
python pipeline.py
```

Congratulations! You have successfully run your first pipeline locally.

If you inspect the actual pipeline code, you will see that it doesn't do a lot of things, but it is still a perfectly 
valid OpenHEXA pipeline.

Let's publish to an actual OpenHEXA workspace so that it can run online.

Using the OpenHEXA web interface, within a workspace, navigate to the Pipelines tab and click on "Create".

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
output the link to the pipeline screen in the OpenHEXA interface.

You can now open the link and run the pipeline using the OpenHEXA web interface.

Contributing
------------

The following sections explain how you can set up a local development environment if you want to participate to the 
development of the SDK.

### SDK development setup

Install the SDK in editable mode:

```shell
python -m venv venv # Create a virtual environment for this project
source venv/bin/activate # Activate the venv
pip install -e ".[dev]"  # Necessary to be able to run the openhexa CLI
```

### Using a local installation of OpenHEXA to run pipelines

While it is possible to run pipelines locally using only the SDK, if you want to run OpenHEXA in a more realistic 
setting you will need to install the OpenHEXA app and frontend components. Please refer to the 
[installation instructions](https://github.com/BLSQ/openhexa/wiki/Installation-instructions) for more information.

You can then configure the OpenHEXA CLI to connect to your local backend:

```shell
openhexa config set_url http://localhost:8000
```

Notes: you can monitor the status of your pipelines using http://localhost:8000/pipelines/status

### Running the tests

You can run the tests using pytest:

```shell
pytest
```
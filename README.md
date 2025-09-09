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

The OpenHEXA SDK requires Python version 3.11, 3.12 or 3.13.

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
openhexa pipelines run ./my_awesome_pipeline
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

### Using a local version of the SDK to run pipelines

If you want to use a local version of the SDK to run pipelines, you can build a docker image with the local version of the SDK installed in it :

```shell
docker build --platform linux/amd64 -t local_image:v1 -f images/Dockerfile .
```

Then reference the image name and tag in the `.env` file of your OpenHexa app :

```dotenv
DEFAULT_WORKSPACE_IMAGE=local_image:v1
```

Or you can set the following in your `workspace.yaml` configuration file in your pipeline directory:

```yaml
env:
  WORKSPACE_DOCKER_IMAGE: local_image:v1
```


### Running the tests

You can run the tests using pytest:

```shell
pytest
```

### Codegen from the GraphQL schema

We use code generation to create Python client code from our GraphQL schema. This involves one tools:

- [**ariadne-codegen**](https://github.com/mirumee/ariadne-codegen): Generates typed Python GraphQL client code from GraphQL files

The code generation process:

1. The GraphQL schema is manually taken from the [Openhexa Monorepo](https://github.com/BLSQ/openhexa-app/blob/main/frontend/schema.generated.graphql) and saved in [`openhexa/graphql/schema.generated.graphql`](https://github.com/BLSQ/openhexa-sdk-python/blob/main/openhexa/graphql/schema.generated.graphql)
2. `ariadne-codegen` uses both the schema and queries to generate typed Python client code

To run code generation manually:

```shell
pip install ariadne-codegen
python -m ariadne_codegen
```

ariadne-codegen runs automatically via pre-commit hooks and CI/CD when GraphQL files are modified.

You can add new queries or mutations in the [`openhexa/graphql/queries.graphql`](https://github.com/BLSQ/openhexa-sdk-python/blob/main/openhexa/graphql/queries.graphql) directory, and they will be picked up by the code generation process.

Example of usage of the generated code:

```python
from sdk import OpenHexaClient

# connect to OpenHEXA backend using environment variables
OpenHexaClient().get_countries(workspace_slug="workspace_slug_example")

# or explicitly pass the URL and token
OpenHexaClient(server_url="app.demo.openhexa.org", token="supersecuretoken")
 ```

## Release

This project uses [release-please](https://github.com/googleapis/release-please) to manage releases using conventional commits.

To release a new version:

1. You need to have a least a commit with a conventional commit message (`feat|fix`) since the last release.
2. release-please will create a new release PR on GitHub.
3. Once the PR is merged, release-please will create a new release on GitHub.
4. A GitHub action will build the package on github release creation and upload it to PyPI and Anaconda.

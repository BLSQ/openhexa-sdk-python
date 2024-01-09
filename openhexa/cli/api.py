"""Collection of functions that interacts with the OpenHEXA API."""

import base64
import enum
import io
import os
import typing
from configparser import ConfigParser
from importlib.metadata import version
from pathlib import Path
from zipfile import ZipFile

import click
import requests

from openhexa.sdk.pipelines import get_local_workspace_config, import_pipeline

CONFIGFILE_PATH = os.path.expanduser("~") + "/.openhexa.ini"


class InvalidDefinitionError(Exception):
    """Raised whenever pipeline parameters and/or pipeline options are incompatible."""

    pass


class PipelineDefinitionErrorCode(enum.Enum):
    """Enumeration of possible pipeline definition error codes."""

    PIPELINE_DOES_NOT_SUPPORT_PARAMETERS = "PIPELINE_DOES_NOT_SUPPORT_PARAMETERS"
    INVALID_TIMEOUT_VALUE = "INVALID_TIMEOUT_VALUE"


def is_debug(config: ConfigParser) -> bool:
    """Determine whether the provided configuration has the debug flag."""
    return config.getboolean("openhexa", "debug", fallback=False)


def open_config():
    """Open the local configuration file using configparser.

    A default configuration file will be generated if the file does not exist.
    """
    config = ConfigParser()
    if os.path.exists(CONFIGFILE_PATH):
        config.read(CONFIGFILE_PATH)
    else:
        config.read_string(
            """
        [openhexa]
        url=https://api.openhexa.org

        [workspaces]
        """
        )
    return config


def save_config(config: ConfigParser):
    """Save the provided configparser local configuration to disk."""
    with open(CONFIGFILE_PATH, "w") as configfile:
        config.write(configfile)


def graphql(config, query: str, variables=None, token=None):
    """Perform a GraphQL request."""
    url = config["openhexa"]["url"] + "/graphql/"
    if token is None:
        current_workspace = config["openhexa"]["current_workspace"]
        token = config["workspaces"].get(current_workspace)

    if not token:
        raise Exception("No token found for workspace")

    if is_debug(config):
        click.echo("")
        click.echo("Graphql Query:")
        click.echo(f"URL: {url}")
        click.echo(f"Query: {query}")
        click.echo(f"Variables: {variables}")

    response = requests.post(
        url,
        headers={
            "User-Agent": f"openhexa-cli/{version('openhexa.sdk')}",
            "Authorization": f"Bearer {token}",
        },
        json={"query": query, "variables": variables},
    )
    response.raise_for_status()
    data = response.json()

    if is_debug(config):
        click.echo("Graphql Response:")
        click.echo(data)
        click.echo("")

    if data.get("errors"):
        if data.get("errors")[0].get("extensions", {}).get("code") == "UNAUTHENTICATED":
            raise Exception("Token is invalid, please update the token")
        raise Exception(data["errors"])
    return data["data"]


def get_skeleton_dir():
    """Get the path to the skeleton directory."""
    return Path(__file__).parent / "skeleton"


def get_workspace(config, slug: str, token: str):
    """Get a single workspace."""
    return graphql(
        config,
        """
            query getWorkspace($slug: String!) {
                workspace(slug: $slug) {
                    name
                    slug
                }
            }
            """,
        {"slug": slug},
        token,
    )["workspace"]


def list_pipelines(config):
    """List all pipelines in the workspace."""
    data = graphql(
        config,
        """
    query getWorkspacePipelines($workspaceSlug: String!) {
        pipelines(workspaceSlug: $workspaceSlug) {
            items {
                id
                code
                name
                currentVersion {
                    number
                }
            }
        }
    }
    """,
        {"workspaceSlug": config["openhexa"]["current_workspace"]},
    )
    return data["pipelines"]["items"]


def get_pipeline(config, pipeline_code: str) -> dict[str, typing.Any]:
    """Get a single pipeline."""
    data = graphql(
        config,
        """
    query getWorkspacePipeline($workspaceSlug: String!, $pipelineCode: String!) {
        pipelineByCode (workspaceSlug: $workspaceSlug, code: $pipelineCode) {
            id
            code
            currentVersion {
                number
            }
        }
    }
    """,
        {
            "workspaceSlug": config["openhexa"]["current_workspace"],
            "pipelineCode": pipeline_code,
        },
    )
    return data["pipelineByCode"]


def create_pipeline(config, pipeline_code: str, pipeline_name: str):
    """Create a pipeline using the API."""
    data = graphql(
        config,
        """
    mutation createPipeline($input: CreatePipelineInput!) {
        createPipeline(input: $input) {
            success
            errors
            pipeline {
                id
                code
                name
            }
        }
    }
    """,
        {
            "input": {
                "workspaceSlug": config["openhexa"]["current_workspace"],
                "code": pipeline_code,
                "name": pipeline_name,
            }
        },
    )

    if not data["createPipeline"]["success"]:
        raise Exception(data["createPipeline"]["errors"])

    return data["createPipeline"]["pipeline"]


def delete_pipeline(config, pipeline_id: str):
    """Delete a single pipeline."""
    data = graphql(
        config,
        """
    mutation deletePipeline($input: DeletePipelineInput!) {
                    deletePipeline(input: $input) {
                        success
                        errors
                    }
                }
    """,
        {"input": {"id": pipeline_id}},
    )

    if not data["deletePipeline"]["success"]:
        raise Exception(data["deletePipeline"]["errors"])

    return data["deletePipeline"]["success"]


def ensure_is_pipeline_dir(pipeline_path: str):
    """Ensure that there is a pipeline.py file in the directory."""
    if not os.path.isdir(pipeline_path):
        raise Exception(f"Path {pipeline_path} is not a directory")
    if not os.path.exists(pipeline_path):
        raise Exception(f"Directory {pipeline_path} does not exist")
    if not os.path.exists(os.path.join(pipeline_path, "pipeline.py")):
        raise Exception(f"Directory {pipeline_path} does not contain a pipeline.py file")

    return True


# This is easier to mock in the tests than trying to mock click.confirm
def ask_pipeline_config_creation():
    """Mockable function to ask the user if he wants to create a pipeline config file.

    Returns
    -------
        bool: True if the user wants to create a pipeline config file, False otherwise.

    """
    return click.confirm(
        "No workspace.yaml file found. Do you want to create one?",
        default=True,
    )


def ensure_pipeline_config_exists(pipeline_path: Path):
    """Ensure that there is a workspace.yaml file in the directory. If it does not exist, it asks the user if he wants to create it.

    Args:
        pipeline_path (Path): Base directory of the pipeline
    """
    if (pipeline_path / "workspace.yaml").exists():
        return True

    if ask_pipeline_config_creation():
        content = open(get_skeleton_dir() / "workspace.yaml").read()
        with open(pipeline_path / "workspace.yaml", "w") as f:
            f.write(content)
        return True
    else:
        raise Exception("No workspace.yaml file found")


def upload_pipeline(config, pipeline_directory_path: typing.Union[str, Path]):
    """Upload the pipeline contained in the provided directory using the GraphQL API.

    The pipeline code will be zipped and base64-encoded before being sent to the backend.
    """
    pipeline = import_pipeline(pipeline_directory_path)
    directory = Path(os.path.abspath(pipeline_directory_path))

    zip_file = io.BytesIO(b"")

    if is_debug(config):
        click.echo("Generating ZIP file:")
    files = []
    env_vars = get_local_workspace_config(Path(pipeline_directory_path))

    # We exclude the workspace directory since it can break the mount of the bucket on /home/hexa/workspace
    # This is also the default value of the WORKSPACE_FILES_PATH env var
    excluded_paths = [directory / "workspace"]
    if env_vars.get("WORKSPACE_FILES_PATH") and Path(env_vars["WORKSPACE_FILES_PATH"]) not in excluded_paths:
        excluded_paths.append(Path(env_vars["WORKSPACE_FILES_PATH"]))

    with ZipFile(zip_file, "w") as zipObj:
        for path in directory.glob("**/*"):
            if path.name == "python":
                # We are in a virtual environment
                excluded_paths.append(path.parent.parent)  # ./<venv>/bin/python -> ./<venv>

            if path.suffix not in (".py", ".ipynb", ".txt", ".md"):
                continue

            files.append(path)

        if is_debug(config):
            click.echo(f"Excluded dirs: {[p.absolute() for p in excluded_paths]}")

        for file_path in files:
            # Do not include files from the excluded paths
            if any([file_path.is_relative_to(excluded_dir) for excluded_dir in excluded_paths]):
                if is_debug(config):
                    click.echo(f"\t{file_path.name} (excluded)")
                continue
            if is_debug(config):
                click.echo(f"\t{file_path.name}")
            zipObj.write(file_path, file_path.relative_to(directory))

    zip_file.seek(0)

    if is_debug(config):
        # Write zip_file to disk for debugging
        with open("pipeline.zip", "wb") as debug_file:
            debug_file.write(zip_file.read())
        zip_file.seek(0)

    base64_content = base64.b64encode(zip_file.read()).decode("ascii")

    data = graphql(
        config,
        """
            mutation uploadPipeline($input: UploadPipelineInput!) {
                uploadPipeline(input: $input) {
                    success
                    errors
                    version
                }
            }
        """,
        {
            "input": {
                "workspaceSlug": config["openhexa"]["current_workspace"],
                "code": pipeline.code,
                "zipfile": base64_content,
                "parameters": pipeline.parameters_spec(),
                "timeout": pipeline.timeout,
            }
        },
    )

    if not data["uploadPipeline"]["success"]:
        if PipelineDefinitionErrorCode.PIPELINE_DOES_NOT_SUPPORT_PARAMETERS.value in data["uploadPipeline"]["errors"]:
            raise InvalidDefinitionError(
                "Cannot push a new version : this pipeline has a schedule and the new version cannot be scheduled "
                "(all parameters must be optional or have default values)."
            )
        elif PipelineDefinitionErrorCode.INVALID_TIMEOUT_VALUE.value in data["uploadPipeline"]["errors"]:
            raise InvalidDefinitionError(
                "Timeout value is invalid : ensure that it's no negative and inferior to 12 hours."
            )
        else:
            raise Exception(data["uploadPipeline"]["errors"])

    return data["uploadPipeline"]["version"]

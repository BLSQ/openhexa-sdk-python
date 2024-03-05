"""Collection of functions that interacts with the OpenHEXA API."""

import base64
import enum
import io
import os
import typing
from dataclasses import asdict
from importlib.metadata import version
from pathlib import Path
from zipfile import ZipFile

import click
import requests
import stringcase

from openhexa.cli.settings import settings
from openhexa.sdk.pipelines import get_local_workspace_config
from openhexa.sdk.pipelines.runtime import get_pipeline_metadata


class InvalidDefinitionError(Exception):
    """Raised whenever pipeline parameters and/or pipeline options are incompatible."""

    pass


class NoActiveWorkspaceError(Exception):
    """Raised when no workspace is currently active in the configuration."""

    pass


class OutputDirectoryError(Exception):
    """Raised when the output directory is not a directory or is not empty."""

    pass


class APIError(Exception):
    """Raised when an error occurs while interacting with the API."""

    pass


class InvalidTokenError(APIError):
    """Raised when the token is invalid."""

    pass


class GraphQLError(APIError):
    """Raised when a GraphQL request returns an error."""

    pass


class PipelineDefinitionErrorCode(enum.Enum):
    """Enumeration of possible pipeline definition error codes."""

    PIPELINE_DOES_NOT_SUPPORT_PARAMETERS = "PIPELINE_DOES_NOT_SUPPORT_PARAMETERS"
    INVALID_TIMEOUT_VALUE = "INVALID_TIMEOUT_VALUE"


def graphql(query: str, variables=None, token=None):
    """Perform a GraphQL request."""
    url = settings.api_url + "/graphql/"
    if token is None:
        token = settings.access_token

    if token is None:
        raise InvalidTokenError("No token found for workspace")

    if settings.debug:
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
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise GraphQLError(str(e))

    data = response.json()

    if settings.debug:
        click.echo("Graphql Response:")
        click.echo(data)
        click.echo("")

    if data.get("errors"):
        if data.get("errors")[0].get("extensions", {}).get("code") == "UNAUTHENTICATED":
            raise InvalidTokenError
        raise GraphQLError(data["errors"])
    return data["data"]


def get_skeleton_dir():
    """Get the path to the skeleton directory."""
    return Path(__file__).parent / "skeleton"


def get_workspace(slug: str, token: str):
    """Get a single workspace."""
    return graphql(
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


def list_pipelines():
    """List all pipelines in the workspace."""
    if settings.current_workspace is None:
        raise NoActiveWorkspaceError
    data = graphql(
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
        {"workspaceSlug": settings.current_workspace},
    )
    return data["pipelines"]["items"]


def get_pipeline(pipeline_code: str) -> dict[str, typing.Any]:
    """Get a single pipeline."""
    if settings.current_workspace is None:
        raise NoActiveWorkspaceError
    data = graphql(
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
            "workspaceSlug": settings.current_workspace,
            "pipelineCode": pipeline_code,
        },
    )
    return data["pipelineByCode"]


def create_pipeline(pipeline_code: str, pipeline_name: str):
    """Create a pipeline using the API."""
    if settings.current_workspace is None:
        raise NoActiveWorkspaceError
    data = graphql(
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
                "workspaceSlug": settings.current_workspace,
                "code": pipeline_code,
                "name": pipeline_name,
            }
        },
    )

    if not data["createPipeline"]["success"]:
        raise Exception(data["createPipeline"]["errors"])

    return data["createPipeline"]["pipeline"]


def download_pipeline_sourcecode(pipeline_code, output_path: Path = None, force_overwrite=False):
    """Download the source code of a pipeline."""
    if settings.current_workspace is None:
        raise NoActiveWorkspaceError
    if output_path.exists() and not output_path.is_dir():
        raise OutputDirectoryError(f"{output_path.absolute()} is not a directory")
    if output_path.exists() and output_path.is_dir() and any(output_path.iterdir()) and not force_overwrite:
        raise OutputDirectoryError(f"{output_path.absolute()} is not empty")
    r = graphql(
        """
        query getPipelineVersionSourceCode($workspaceSlug: String!, $pipelineCode: String!)  {
            pipelineByCode(workspaceSlug: $workspaceSlug, code: $pipelineCode) {
                currentVersion {
                    zipfile
                }
            }
        }
    """,
        {
            "workspaceSlug": settings.current_workspace,
            "pipelineCode": pipeline_code,
        },
    )
    if r["pipelineByCode"] is None:
        raise Exception(f"No pipeline exists in {settings.current_workspace} with code {pipeline_code}")
    if r["pipelineByCode"]["currentVersion"] is None:
        raise Exception(f"No version found for pipeline {pipeline_code}")

    zip_file = base64.b64decode(r["pipelineByCode"]["currentVersion"]["zipfile"].encode("ascii"))
    with ZipFile(io.BytesIO(zip_file)) as zf:
        zf.extractall(output_path)


def delete_pipeline(pipeline_id: str):
    """Delete a single pipeline."""
    data = graphql(
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


def create_pipeline_structure(pipeline_name: str, base_path: Path) -> Path:
    """Create the structure of a pipeline in the provided directory based on a skeleton.

    Args
    -----
        pipeline_name (str): Name of the pipeline.
        base_path (Path): Base directory of the pipeline.

    Returns
    -------
        Path: Path to the created pipeline directory.
    """
    output_directory = base_path / stringcase.snakecase(pipeline_name.lower())
    sample_directory_path = get_skeleton_dir()

    if output_directory.exists():
        raise ValueError(f"Directory {output_directory} already exists")
    with open(sample_directory_path / Path(".gitignore")) as sample_ignore_file:
        sample_ignore_content = sample_ignore_file.read()
    with open(sample_directory_path / Path("pipeline.py")) as sample_pipeline_file:
        sample_pipeline_content = (
            sample_pipeline_file.read()
            .replace("skeleton-pipeline-code", stringcase.spinalcase(pipeline_name.lower()))
            .replace("skeleton_pipeline_name", stringcase.snakecase(pipeline_name.lower()))
            .replace("Skeleton pipeline name", pipeline_name)
        )
    with open(sample_directory_path / Path("workspace.yaml")) as sample_workspace_file:
        sample_workspace_content = sample_workspace_file.read()

    # Create directory
    output_directory.mkdir(exist_ok=False)
    (output_directory / "workspace").mkdir(exist_ok=False)
    with open(output_directory / ".gitignore", "w") as ignore_file:
        ignore_file.write(sample_ignore_content)
    with open(output_directory / "pipeline.py", "w") as pipeline_file:
        pipeline_file.write(sample_pipeline_content)
    with open(output_directory / "workspace.yaml", "w") as workspace_file:
        workspace_file.write(sample_workspace_content)

    return output_directory


def upload_pipeline(pipeline_directory_path: typing.Union[str, Path]):
    """Upload the pipeline contained in the provided directory using the GraphQL API.

    The pipeline code will be zipped and base64-encoded before being sent to the backend.
    """
    if settings.current_workspace is None:
        raise NoActiveWorkspaceError

    directory = pipeline_directory_path.absolute()
    pipeline = get_pipeline_metadata(directory)

    zip_file = io.BytesIO(b"")

    if settings.debug:
        click.echo("Generating ZIP file:")
    files = []

    # We exclude the workspace directory since it can break the mount of the bucket on /home/hexa/workspace
    # This is also the default value of the WORKSPACE_FILES_PATH env var
    excluded_paths = [directory / "workspace"]
    try:
        env_vars = get_local_workspace_config(pipeline_directory_path)
        if env_vars.get("WORKSPACE_FILES_PATH") and Path(env_vars["WORKSPACE_FILES_PATH"]) not in excluded_paths:
            excluded_paths.append(Path(env_vars["WORKSPACE_FILES_PATH"]))
    except FileNotFoundError:
        # No workspace.yaml file found, we can ignore this error and assume the default value of WORKSPACE_FILES_PATH
        pass

    with ZipFile(zip_file, "w") as zipObj:
        for path in directory.glob("**/*"):
            if path.name == "python":
                # We are in a virtual environment
                excluded_paths.append(path.parent.parent)  # ./<venv>/bin/python -> ./<venv>

            if path.suffix not in (".py", ".ipynb", ".txt", ".md"):
                continue

            files.append(path)

        if settings.debug:
            click.echo(f"Excluded dirs: {[p.absolute() for p in excluded_paths]}")

        for file_path in files:
            # Do not include files from the excluded paths
            if any([file_path.is_relative_to(excluded_dir) for excluded_dir in excluded_paths]):
                if settings.debug:
                    click.echo(f"\t{file_path.name} (excluded)")
                continue
            if settings.debug:
                click.echo(f"\t{file_path.name}")
            zipObj.write(file_path, file_path.relative_to(directory))

    zip_file.seek(0)

    if settings.debug:
        # Write zip_file to disk for debugging
        with open("pipeline.zip", "wb") as debug_file:
            debug_file.write(zip_file.read())
        zip_file.seek(0)

    base64_content = base64.b64encode(zip_file.read()).decode("ascii")
    data = graphql(
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
                "workspaceSlug": settings.current_workspace,
                "code": pipeline.code,
                "zipfile": base64_content,
                "parameters": [asdict(p) for p in pipeline.parameters],
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

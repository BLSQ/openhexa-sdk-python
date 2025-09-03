"""Collection of functions that interacts with the OpenHEXA API."""

import base64
import enum
import io
import json
import logging
import os
import tempfile
import typing
from datetime import datetime
from importlib.metadata import version
from pathlib import Path
from typing import Any
from zipfile import ZipFile

import click
import docker
import httpx
import requests
from docker.models.containers import Container
from graphql import build_client_schema, build_schema, get_introspection_query
from graphql.utilities import find_breaking_changes
from jinja2 import Template

from openhexa.cli.settings import settings
from openhexa.graphql import BaseOpenHexaClient
from openhexa.sdk.pipelines import get_local_workspace_config
from openhexa.sdk.pipelines.runtime import get_pipeline
from openhexa.utils import create_requests_session, stringcase


def handle_ssl_error(e):
    """Handle SSL certificate verification errors with helpful message."""
    if "SSL certificate verification failed" in str(e) or "CERTIFICATE_VERIFY_FAILED" in str(e):
        raise GraphQLError(
            "SSL certificate verification failed. "
            "If you want to disable SSL verification, set the environment variable: HEXA_VERIFY_SSL=false"
        )


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


class PipelineDirectoryError(Exception):
    """Raised when the pipeline directory is not a directory or does not exist."""

    pass


class DockerError(Exception):
    """Raised when Docker is not running or is not installed."""

    pass


class PipelineDefinitionErrorCode(enum.Enum):
    """Enumeration of possible pipeline definition error codes."""

    PIPELINE_DOES_NOT_SUPPORT_PARAMETERS = "PIPELINE_DOES_NOT_SUPPORT_PARAMETERS"
    INVALID_TIMEOUT_VALUE = "INVALID_TIMEOUT_VALUE"
    DUPLICATE_PIPELINE_VERSION_NAME = "DUPLICATE_PIPELINE_VERSION_NAME"


class PermissionDenied(Exception):
    """Raised whenever an operation on a pipeline is denied by the backend."""

    pass


def get_library_versions() -> tuple[str, str]:
    """Return the current version and the one on PyPi."""
    # Get the currently installed version
    installed_version = version("openhexa.sdk")

    # Get the latest version available on PyPI
    try:
        response = requests.get("https://pypi.org/pypi/openhexa.sdk/json")
        latest_version = response.json()["info"]["version"]
        return installed_version, latest_version
    except requests.RequestException:
        logging.error(
            "Could not check for the latest version of the openhexa.sdk package.",
            exc_info=True,
        )
        return installed_version, installed_version


def _detect_graphql_breaking_changes_if_needed(token):
    """Detect breaking changes if not done recently between the schema referenced in the SDK and the server using graphql-core."""
    ONE_HOUR = 60 * 60
    now_timestamp = int(datetime.now().timestamp())
    if not settings.last_breaking_change_check or now_timestamp - settings.last_breaking_change_check > ONE_HOUR:
        _detect_graphql_breaking_changes(token)
        settings.last_breaking_change_check = now_timestamp


def _detect_graphql_breaking_changes(token):
    """Detect breaking changes between the schema referenced in the SDK and the server using graphql-core."""
    stored_schema_obj = build_schema(
        (Path(__file__).parent.parent / "graphql" / "schema.generated.graphql").open().read()
    )
    server_schema_obj = build_client_schema(
        _query_graphql(get_introspection_query(input_value_deprecation=True), token=token)
    )

    breaking_changes = find_breaking_changes(stored_schema_obj, server_schema_obj)
    if breaking_changes:
        current_version, latest_version = get_library_versions()
        click.secho(
            f"⚠️ Breaking changes detected between the SDK (version {current_version}) and the server:",
            fg="red",
        )
        for change in breaking_changes:
            click.secho(f"- {change.description}", fg="yellow")
        click.secho(
            "This could lead to unexpected results.\n"
            f"Please update the SDK to the latest version {latest_version} "
            f"(using `pip install openhexa-sdk=={latest_version}`) or use a version of the SDK compatible with the server.",
            fg="red",
        )


def graphql(query: str, variables=None, token=None):
    """Check that there is no breaking change and perform a GraphQL request."""
    _detect_graphql_breaking_changes_if_needed(token)
    return _query_graphql(query, variables, token)


def _query_graphql(query: str, variables=None, token=None):
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

    session = create_requests_session(verify=settings.verify_ssl)

    try:
        response = session.post(
            url,
            headers={
                "User-Agent": f"openhexa-cli/{version('openhexa.sdk')}",
                "Authorization": f"Bearer {token}",
            },
            json={"query": query, "variables": variables},
        )
        response.raise_for_status()
    except requests.exceptions.SSLError as e:
        handle_ssl_error(e)
        raise
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


def get_pipelines_pages(name=None):
    """Get the first page of pipelines in the workspace optionally ranked by name similarity."""
    if settings.current_workspace is None:
        raise NoActiveWorkspaceError
    data = graphql(
        """
    query getWorkspacePipelines($workspaceSlug: String!, $name: String, $page: Int = 1, $perPage: Int = 10) {
        pipelines(workspaceSlug: $workspaceSlug, name: $name, page: $page, perPage: $perPage) {
            totalPages
            items {
                id
                code
                name
                type
                currentVersion {
                    id
                    name
                }
            }
        }
    }
    """,
        {"workspaceSlug": settings.current_workspace, "name": name},
    )
    return data["pipelines"]


def get_pipelines(name=None):
    """Get pipelines in the workspace optionally ranked by name similarity."""
    return get_pipelines_pages(name)["items"]


def get_pipeline_from_code(pipeline_code: str) -> dict[str, typing.Any]:
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
                id
                name
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


def create_pipeline(pipeline_name: str):
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
        if "PERMISSION_DENIED" in data["deletePipeline"]["errors"]:
            raise Exception(
                "Check that you have the correct permission or the pipeline is not in a queued/running state."
            )

        raise Exception(data["deletePipeline"]["errors"])

    return data["deletePipeline"]["success"]


def ensure_is_pipeline_dir(pipeline_path: str):
    """Ensure that there is a pipeline.py file in the directory."""
    if not os.path.isdir(pipeline_path):
        raise PipelineDirectoryError(f"Path {pipeline_path} is not a directory")
    if not os.path.exists(pipeline_path):
        raise PipelineDirectoryError(f"Directory {pipeline_path} does not exist")
    if not os.path.exists(os.path.join(pipeline_path, "pipeline.py")):
        raise PipelineDirectoryError(f"Directory {pipeline_path} does not contain a pipeline.py file")

    return True


def run_pipeline(path: Path, config: dict, image: str = None, debug: bool = False) -> Container:
    """Run a pipeline using the provided configuration."""
    ensure_is_pipeline_dir(path)
    ensure_pipeline_config_exists(path)
    env_vars = get_local_workspace_config(path)
    # # Prepare the mount for the workspace's files
    mount_files_path = Path(env_vars.pop("WORKSPACE_FILES_PATH")).absolute()
    try:
        docker_client = docker.from_env()
        docker_client.ping()
    except docker.errors.DockerException:
        raise DockerError(
            "Docker is not running or is not installed. Please install Docker Desktop and start the service."
        )

    if image is None:
        image = env_vars.get("WORKSPACE_DOCKER_IMAGE", "blsq/openhexa-blsq-environment:latest")

    zip_file = generate_zip_file(path)
    tmp_dir = tempfile.mkdtemp()
    with ZipFile(zip_file) as zf:
        zf.extractall(tmp_dir)

    volumes = {
        tmp_dir: {"bind": "/home/hexa/pipeline", "mode": "rw"},
        mount_files_path: {
            "bind": "/home/hexa/workspace",
            "mode": "rw",
        },
    }

    environment = {
        "HEXA_ENVIRONMENT": "local_pipeline",
        "HEXA_WORKSPACE": settings.current_workspace,
        "REMOTE_DEBUGGER": "true" if debug else None,
        **env_vars,
    }

    command = f"pipeline run --config {base64.b64encode(json.dumps(config).encode('utf-8')).decode('utf-8')}"
    try:
        docker_client.images.get(image)
    except docker.errors.ImageNotFound:
        logging.info("Pulling image %s...", image)
        docker_client.images.pull(image)
        logging.info("Image %s pulled", image)
    try:
        logging.info(f"Creating pipeline container with image '{image}'...")
        return docker_client.containers.run(
            image,
            command,
            remove=True,
            auto_remove=True,
            tty=debug,
            stdin_open=True,
            platform="linux/amd64",
            volumes=volumes,
            ports={"5678": 5678} if debug else None,
            environment=environment,
            healthcheck={"test": ["NONE"]},  # Disable health checks
            detach=True,
        )
    except docker.errors.ContainerError as e:
        raise DockerError(f"Error while running the pipeline: {e}")
    except docker.errors.ImageNotFound:
        raise DockerError("Docker image not found")


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


def create_pipeline_structure(pipeline_name: str, base_path: Path, workspace: str, workflow_mode: str = None) -> Path:
    """Create the structure of a pipeline in the provided directory based on a skeleton.

    Args
    -----
        pipeline_name (str): Name of the pipeline.
        base_path (Path): Base directory of the pipeline.
        workspace (str): Slug of the workspace.
        workflow_mode (str): If provided, a GitHub workflow will be created in the pipeline directory. Accepted values are "push", "manual" and "release".

    Returns
    -------
        Path: Path to the created pipeline directory.
    """
    output_directory = base_path / stringcase.snakecase(pipeline_name.lower())

    if output_directory.exists():
        raise ValueError(f"Directory {output_directory} already exists")

    sample_directory_path = get_skeleton_dir()
    templates = [
        "pipeline.py.j2",
        "workspace.yaml",
        ".gitignore",
        ".vscode/launch.json.j2",
    ]
    if workflow_mode is not None:
        templates.append(".github/workflows/push-pipeline.yml.j2")

    vars = {
        "pipeline_code": stringcase.spinalcase(pipeline_name.lower()),
        "pipeline_human_name": pipeline_name,
        "pipeline_snake_name": stringcase.snakecase(pipeline_name.lower()),
        "workspace_slug": workspace,
        "workflow_mode": workflow_mode,
    }
    jinja_options = {
        "variable_start_string": "[[",
        "variable_end_string": "]]",
    }

    for tpl_file in templates:
        out_path = output_directory / Path(tpl_file.rstrip(".j2"))
        template = Template(open(sample_directory_path / Path(tpl_file)).read(), **jinja_options)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w") as f:
            f.write(template.render(**vars))

    (output_directory / "workspace").mkdir(parents=True, exist_ok=True)
    return output_directory


def generate_zip_file(pipeline_directory_path: str | Path) -> io.BytesIO:
    """Generate a ZIP file containing the pipeline code.

    Args:
        pipeline_directory_path (str | Path): The path to the pipeline directory.

    Returns
    -------
        io.BytesIO: A BytesIO object containing the ZIP file.
    """
    if settings.debug:
        click.echo("Generating ZIP file:")
    zip_file = io.BytesIO(b"")
    files = []

    # We exclude the workspace directory since it can break the mount of the bucket on /home/hexa/workspace
    # This is also the default value of the WORKSPACE_FILES_PATH env var
    excluded_paths = [pipeline_directory_path / "workspace"]
    try:
        env_vars = get_local_workspace_config(pipeline_directory_path)
        if env_vars.get("WORKSPACE_FILES_PATH") and Path(env_vars["WORKSPACE_FILES_PATH"]) not in excluded_paths:
            excluded_paths.append(Path(env_vars["WORKSPACE_FILES_PATH"]))
    except FileNotFoundError:
        # No workspace.yaml file found, we can ignore this error and assume the default value of WORKSPACE_FILES_PATH
        pass
    with ZipFile(zip_file, "w") as zipObj:
        for path in pipeline_directory_path.glob("**/*"):
            if path.name == "python":
                # We are in a virtual environment
                excluded_paths.append(path.parent.parent)  # ./<venv>/bin/python -> ./<venv>

            if path.suffix not in (".py", ".ipynb", ".txt", ".md", ".R", ".r"):
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
            zipObj.write(file_path, file_path.relative_to(pipeline_directory_path))
    zip_file.seek(0)
    return zip_file


def upload_pipeline(
    target_pipeline_code: str,
    pipeline_directory_path: str | Path,
    name: str = None,
    description: str = None,
    link: str = None,
):
    """Upload the pipeline contained in the provided directory using the GraphQL API.

    The pipeline code will be zipped and base64-encoded before being sent to the backend.
    The target pipeline will be updated with the new version.
    """
    if settings.current_workspace is None:
        raise NoActiveWorkspaceError

    directory = pipeline_directory_path.absolute()
    pipeline = get_pipeline(directory)
    zip_file = generate_zip_file(directory)

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
                    pipelineVersion {
                        id
                        versionName
                        pipeline {
                            id
                            permissions {
                                createTemplateVersion {
                                    isAllowed
                                }
                            }
                            template {
                                id
                                code
                                name
                            }
                        }
                    }
                }
            }
        """,
        {
            "input": {
                "workspaceSlug": settings.current_workspace,
                "code": target_pipeline_code,
                "name": name,
                "description": description,
                "externalLink": link,
                "zipfile": base64_content,
                "parameters": [p.to_dict() for p in pipeline.parameters],
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
        elif PipelineDefinitionErrorCode.DUPLICATE_PIPELINE_VERSION_NAME.value in data["uploadPipeline"]["errors"]:
            raise InvalidDefinitionError("The pipeline version name is already used. Please choose another name.")
        else:
            raise Exception(data["uploadPipeline"]["errors"])

    return data["uploadPipeline"]["pipelineVersion"]


class PipelineTemplateVersionCreateErrorCode(enum.Enum):
    """Enumeration of possible pipeline template version create error codes."""

    PERMISSION_DENIED = "PERMISSION_DENIED"
    WORKSPACE_NOT_FOUND = "WORKSPACE_NOT_FOUND"
    PIPELINE_NOT_FOUND = "PIPELINE_NOT_FOUND"
    PIPELINE_VERSION_NOT_FOUND = "PIPELINE_VERSION_NOT_FOUND"


def create_pipeline_template_version(
    workspace_slug: str, pipeline_id: str, pipeline_version_id: str, changelog: str = None
):
    """Create a pipeline template version using the API."""
    data = graphql(
        """
    mutation createPipelineTemplateVersion($input: CreatePipelineTemplateVersionInput!) {
        createPipelineTemplateVersion(input: $input) {
            success
            errors
            pipelineTemplate {
                id
                name
                code
                currentVersion {
                    id
                    versionNumber
                }
            }
        }
    }
    """,
        {
            "input": {
                "workspaceSlug": workspace_slug,
                "pipelineId": pipeline_id,
                "pipelineVersionId": pipeline_version_id,
                "changelog": changelog,
            }
        },
    )
    if not data["createPipelineTemplateVersion"]["success"]:
        if (
            PipelineTemplateVersionCreateErrorCode.PERMISSION_DENIED.value
            in data["createPipelineTemplateVersion"]["errors"]
        ):
            raise PermissionDenied("Permission denied")
        elif (
            PipelineTemplateVersionCreateErrorCode.WORKSPACE_NOT_FOUND.value
            in data["createPipelineTemplateVersion"]["errors"]
        ):
            raise Exception("Workspace not found")
        elif (
            PipelineTemplateVersionCreateErrorCode.PIPELINE_NOT_FOUND.value
            in data["createPipelineTemplateVersion"]["errors"]
        ):
            raise Exception("Pipeline not found")
        elif (
            PipelineTemplateVersionCreateErrorCode.PIPELINE_VERSION_NOT_FOUND.value
            in data["createPipelineTemplateVersion"]["errors"]
        ):
            raise Exception("Pipeline version not found for this pipeline")
        else:
            raise Exception(data["createPipelineTemplateVersion"]["errors"])

    return data["createPipelineTemplateVersion"]["pipelineTemplate"]


def is_dhis2_connection_up(workspace_slug: str, connection_slug: str) -> bool:
    """DHIS2 connection status."""
    response = graphql(
        """
        query getConnectionBySlug($workspaceSlug: String!, $connectionSlug: String!) {
        connectionBySlug(workspaceSlug:$workspaceSlug, connectionSlug: $connectionSlug){
            ... on DHIS2Connection {
                    status
                }
        }
        }
        """,
        variables={
            "workspaceSlug": workspace_slug,
            "connectionSlug": connection_slug,
        },
    )
    return response["data"]["connectionBySlug"]["status"] == "UP"


class OpenHexaClient(BaseOpenHexaClient):
    """OpenHexaClient is a class that provides methods to interact with the OpenHexa GraphQL API."""

    def __init__(self, token=None):
        """Initialize the OpenHexaClient with the OpenHexa API URL and headers."""
        super().__init__(url=settings.api_url + "/graphql/", token=settings.access_token, verify=settings.verify_ssl)

    def execute(self, query, **kwargs):
        """Decorate parent execute method to log the GraphQL query and response."""
        _detect_graphql_breaking_changes(token=self.token)

        if self.token is None:
            raise InvalidTokenError("No token found for workspace")

        if settings.debug:
            click.echo("")
            click.echo("Graphql Query:")
            click.echo(f"URL: {self.url}")
            click.echo(f"Query: {query}")
            variables = kwargs.get("variables", {})
            click.echo(f"Variables: {variables}")

        try:
            response = super().execute(query=query, **kwargs)
        except Exception as e:
            handle_ssl_error(e)
            raise

        if settings.debug:
            click.echo("")
            click.echo("Graphql Response:")
            click.echo(f"Response: {response}")

        return response

    def get_data(self, response: httpx.Response) -> dict[str, Any]:
        """Get the data from the response, handling errors and authentication issues."""
        try:
            data = super().get_data(response)
        except Exception as e:
            handle_ssl_error(e)
            if "Resolver requires an authenticated user" in str(e):
                raise InvalidTokenError("No or invalid token found for workspace, please check your configuration.")
            raise
        return data

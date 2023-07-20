import base64
import configparser
import enum
import io
import os
from pathlib import Path
from zipfile import ZipFile

import click
import requests

from openhexa.sdk import __version__
from openhexa.sdk.pipelines import import_pipeline

CONFIGFILE_PATH = os.path.expanduser("~") + "/.openhexa.ini"


class InvalidDefinitionError(Exception):
    pass


class PipelineErrorEnum(enum.Enum):
    PIPELINE_DOES_NOT_SUPPORT_PARAMETERS = "PIPELINE_DOES_NOT_SUPPORT_PARAMETERS"


def is_debug(config: configparser.ConfigParser):
    return config.getboolean("openhexa", "debug", fallback=False)


def open_config():
    config = configparser.ConfigParser()
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


def save_config(config):
    with open(CONFIGFILE_PATH, "w") as configfile:
        config.write(configfile)


def graphql(config, query: str, variables=None, token=None):
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
            "User-Agent": f"openhexa-cli/{__version__}",
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


def get_workspace(config, slug: str, token: str):
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


def get_pipelines(config):
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


def get_pipeline(config, pipeline_code: str):
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


def ensure_is_pipeline_dir(pipeline_path: str):
    # Ensure that there is a pipeline.py file in the directory
    if not os.path.isdir(pipeline_path):
        raise Exception(f"Path {pipeline_path} is not a directory")
    if not os.path.exists(pipeline_path):
        raise Exception(f"Directory {pipeline_path} does not exist")
    if not os.path.exists(os.path.join(pipeline_path, "pipeline.py")):
        raise Exception(
            f"Directory {pipeline_path} does not contain a pipeline.py file"
        )

    return True


def upload_pipeline(config, pipeline_directory_path: str):
    pipeline = import_pipeline(pipeline_directory_path)
    directory = Path(os.path.abspath(pipeline_directory_path))

    zipFile = io.BytesIO(b"")

    if is_debug(config):
        click.echo("Generating ZIP file:")
    files = []
    venv_path = None
    with ZipFile(zipFile, "w") as zipObj:
        for path in directory.glob("**/*"):
            if path.name == "python":
                # We are in a virtual environment
                venv_path = path.parent.parent  # ./<venv>/bin/python -> ./<venv>

            if path.suffix not in (".py", ".ipynb", ".txt"):
                continue

            files.append(path)
        if is_debug(config):
            click.echo(f"Venv path: {venv_path}")

        for file_path in files:
            # Do not include files from the virtual environment if we found one
            if venv_path and file_path.is_relative_to(venv_path):
                continue
            if is_debug(config):
                click.echo(f"\t{file_path.name}")
            zipObj.write(file_path, file_path.relative_to(directory))
    zipFile.seek(0)

    if is_debug(config):
        # Write zipFile to disk for debugging
        with open("pipeline.zip", "wb") as debug_file:
            debug_file.write(zipFile.read())
        zipFile.seek(0)

    base64_content = base64.b64encode(zipFile.read()).decode("ascii")

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
            }
        },
    )

    if not data["uploadPipeline"]["success"]:
        if (
            PipelineErrorEnum.PIPELINE_DOES_NOT_SUPPORT_PARAMETERS.value
            in data["uploadPipeline"]["errors"]
        ):
            raise InvalidDefinitionError(
                "A pipeline with a schedule can't have parameters"
            )
        else:
            raise Exception(data["uploadPipeline"]["errors"])

    return data["uploadPipeline"]["version"]

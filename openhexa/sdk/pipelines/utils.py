"""Utilities for running local pipelines."""

import re
from pathlib import Path
from tempfile import mkdtemp

import stringcase
import yaml

from openhexa.sdk.pipelines.exceptions import InvalidParameterError


class LocalWorkspaceConfigError(Exception):
    """Raised whenever the local workspace config file does not exist or is invalid."""

    pass


def validate_pipeline_parameter_code(code: str):
    """Validate a pipeline parameter code."""
    if re.match("^[a-z_][a-z_0-9]+$", code) is None:
        raise InvalidParameterError(
            f"Invalid parameter code provided ({code}). Parameter must start with a letter or an underscore, "
            f"and can only contain lower case letters, numbers and underscores."
        )


def get_local_workspace_config(path: Path):
    """Get local workspace config for development/testing purposes.

    As of now, this function attempts to make the local run context looks like an online run context by
    filling environment variables.

    This is obviously brittle as it relies on setting the correct env variables keys, any changes upstream must
    be reflected here.
    """
    env_vars = {}

    # This will only work when running the pipeline using "python pipeline.py"
    # (We will have to find another approach for tests or running the pipeline using the CLI)
    local_workspace_config_path = path / Path("workspace.yaml")
    if not local_workspace_config_path.exists():
        raise FileNotFoundError(
            "To work with pipelines locally, you need a workspace.yaml file in the same directory as your pipeline file"
        )

    with open(local_workspace_config_path.resolve()) as local_workspace_config_file:
        local_workspace_config = yaml.safe_load(local_workspace_config_file)
        # Database config
        if "database" in local_workspace_config:
            try:
                env_vars["WORKSPACE_DATABASE_USERNAME"] = local_workspace_config["database"]["username"]
                password = local_workspace_config["database"].get("password")
                if password is not None:
                    env_vars["WORKSPACE_DATABASE_PASSWORD"] = password
                env_vars["WORKSPACE_DATABASE_HOST"] = local_workspace_config["database"]["host"]
                env_vars["WORKSPACE_DATABASE_PORT"] = str(local_workspace_config["database"]["port"])
                env_vars["WORKSPACE_DATABASE_DB_NAME"] = local_workspace_config["database"]["dbname"]
            except KeyError:
                exception_message = (
                    "Invalid local workspace database config. Please make sure you provide the following "
                    "keys: database.username, database.password, database.host, database.port, "
                    "database.dbname."
                )
                raise LocalWorkspaceConfigError(exception_message)

        # Files config
        if "files" in local_workspace_config:
            try:
                files_path = path / Path(local_workspace_config["files"]["path"])
                if not files_path.exists():
                    # Let's create the folder if it doesn't exist
                    files_path.mkdir(parents=True)
                env_vars["WORKSPACE_FILES_PATH"] = str(files_path.resolve())
            except KeyError:
                exception_message = (
                    "Invalid local workspace database config. Please make sure you provide the following "
                    "keys: username, password, host, port, name."
                )
                raise LocalWorkspaceConfigError(exception_message)

            # Create temp dir to simulate /home/hexa/tmp locally
            env_vars["WORKSPACE_TMP_PATH"] = mkdtemp()

        # Connections
        if "connections" in local_workspace_config:
            for slug, connection_config in local_workspace_config["connections"].items():
                slug = slug.lower()
                if "type" not in connection_config:
                    raise LocalWorkspaceConfigError("Each connection must have a type key.")

                # DHIS2 connection
                if connection_config["type"] == "dhis2":
                    try:
                        env_vars[f"{stringcase.constcase(slug)}_URL"] = connection_config["url"]
                        env_vars[f"{stringcase.constcase(slug)}_USERNAME"] = connection_config["username"]
                        env_vars[f"{stringcase.constcase(slug)}_PASSWORD"] = connection_config["password"]
                    except KeyError:
                        exception_message = (
                            "Invalid local workspace dhis2 connection config. Please make sure you provide "
                            "the following keys: url, username, password."
                        )
                        raise LocalWorkspaceConfigError(exception_message)
                # PostgreSQL connection
                elif connection_config["type"] == "postgresql":
                    try:
                        env_vars[f"{stringcase.constcase(slug)}_HOST"] = connection_config["host"]
                        env_vars[f"{stringcase.constcase(slug)}_PORT"] = str(connection_config["port"])
                        env_vars[f"{stringcase.constcase(slug)}_USERNAME"] = str(connection_config["username"])
                        env_vars[f"{stringcase.constcase(slug)}_PASSWORD"] = connection_config["password"]
                        env_vars[f"{stringcase.constcase(slug)}_DB_NAME"] = connection_config["database_name"]
                    except KeyError:
                        exception_message = (
                            "Invalid local workspace PostgreSQL connection config. Please make sure you provide "
                            "the following keys: url, username, password."
                        )
                        raise LocalWorkspaceConfigError(exception_message)
                # S3 connection
                elif connection_config["type"] == "s3":
                    try:
                        env_vars[f"{stringcase.constcase(slug)}_SECRET_ACCESS_KEY"] = connection_config[
                            "secret_access_key"
                        ]
                        env_vars[f"{stringcase.constcase(slug)}_ACCESS_KEY_ID"] = str(
                            connection_config["access_key_id"]
                        )
                        env_vars[f"{stringcase.constcase(slug)}_BUCKET_NAME"] = str(connection_config["bucket_name"])
                    except KeyError:
                        exception_message = (
                            "Invalid local workspace S3 connection config. Please make sure you provide "
                            "the following keys: secret_key, access_key_id, bucket_name."
                        )
                        raise LocalWorkspaceConfigError(exception_message)
                # GCS connection
                elif connection_config["type"] == "gcs":
                    try:
                        env_vars[f"{stringcase.constcase(slug)}_SERVICE_ACCOUNT_KEY"] = connection_config[
                            "service_account_key"
                        ]
                        env_vars[f"{stringcase.constcase(slug)}_BUCKET_NAME"] = str(connection_config["bucket_name"])
                    except KeyError:
                        exception_message = (
                            "Invalid local workspace GCS connection config. Please make sure you provide "
                            "the following keys: service_account_key, bucket_name."
                        )
                        raise LocalWorkspaceConfigError(exception_message)
                    # IASO connection
                elif connection_config["type"] == "iaso":
                    try:
                        env_vars[f"{stringcase.constcase(slug)}_URL"] = connection_config["url"]
                        env_vars[f"{stringcase.constcase(slug)}_USERNAME"] = connection_config["username"]
                        env_vars[f"{stringcase.constcase(slug)}_PASSWORD"] = connection_config["password"]
                    except KeyError:
                        exception_message = (
                            "Invalid local workspace iaso connection config. Please make sure you provide "
                            "the following keys: url, username, password."
                        )
                        raise LocalWorkspaceConfigError(exception_message)
                # Custom connection
                else:
                    for key, value in connection_config.items():
                        if key != "type":
                            env_vars[stringcase.constcase(f"{slug}_{key.lower()}")] = str(value)
        # Workspace docker image
        if "image" in local_workspace_config:
            env_vars["WORKSPACE_DOCKER_IMAGE"] = local_workspace_config["image"]

    return env_vars

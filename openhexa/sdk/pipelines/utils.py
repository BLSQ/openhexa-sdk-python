import os
import sys
from pathlib import Path

import stringcase
import yaml


class LocalWorkspaceConfigError(Exception):
    pass


def load_local_workspace_config():
    """Load local workspace config for development/testing purposes.

    As of now, this function attempts to make the local run context looks like an online run context by
    filling environment variables.

    This is obviously brittle as it relies on setting the correct env variables keys, any changes upstream must
    be reflected here.
    """

    # This will only work when running the pipeline using "python pipeline.py"
    # (We will have to find another approach for tests or running the pipeline using the CLI)
    pipeline_directory_path = Path(sys.argv[0]).parent
    local_workspace_config_path = Path(sys.argv[0]).parent / Path("workspace.yaml")
    if not local_workspace_config_path.exists():
        return

    with open(
        local_workspace_config_path.resolve(), "r"
    ) as local_workspace_config_file:
        local_workspace_config = yaml.safe_load(local_workspace_config_file)
        # Database config
        if "database" in local_workspace_config:
            try:
                os.environ["WORKSPACE_DATABASE_USERNAME"] = local_workspace_config[
                    "database"
                ]["username"]
                password = local_workspace_config["database"].get("password")
                if password is not None:
                    os.environ["WORKSPACE_DATABASE_PASSWORD"] = password
                os.environ["WORKSPACE_DATABASE_HOST"] = local_workspace_config[
                    "database"
                ]["host"]
                os.environ["WORKSPACE_DATABASE_PORT"] = str(
                    local_workspace_config["database"]["port"]
                )
                os.environ["WORKSPACE_DATABASE_DB_NAME"] = local_workspace_config[
                    "database"
                ]["dbname"]
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
                files_path = pipeline_directory_path / Path(
                    local_workspace_config["files"]["path"]
                )
                if not files_path.exists():
                    raise LocalWorkspaceConfigError(
                        f"The {files_path} files path does not exist. "
                        f"Did you forget to create it?"
                    )
                os.environ["WORKSPACE_FILES_PATH"] = str(files_path.resolve())
            except KeyError:
                exception_message = (
                    "Invalid local workspace database config. Please make sure you provide the following "
                    "keys: username, password, host, port, name."
                )
                raise LocalWorkspaceConfigError(exception_message)

        # Connections
        if "connections" in local_workspace_config:
            for slug, connection_config in local_workspace_config[
                "connections"
            ].items():
                if "type" not in connection_config:
                    raise LocalWorkspaceConfigError(
                        "Each connection must have a type key."
                    )

                # DHIS2 connections
                if connection_config["type"] == "dhis2":
                    try:
                        os.environ[
                            f"{stringcase.constcase(slug)}_URL"
                        ] = connection_config["url"]
                        os.environ[
                            f"{stringcase.constcase(slug)}_USERNAME"
                        ] = connection_config["username"]
                        os.environ[
                            f"{stringcase.constcase(slug)}_PASSWORD"
                        ] = connection_config["password"]
                    except KeyError:
                        exception_message = (
                            "Invalid local workspace dhis2 connection config. Please make sure you provide "
                            "the following keys: url, username, password."
                        )
                        raise LocalWorkspaceConfigError(exception_message)
                # PostgreSQL connections
                elif connection_config["type"] == "postgresql":
                    try:
                        os.environ[
                            f"{stringcase.constcase(slug)}_HOST"
                        ] = connection_config["host"]
                        os.environ[f"{stringcase.constcase(slug)}_PORT"] = str(
                            connection_config["port"]
                        )
                        os.environ[f"{stringcase.constcase(slug)}_USERNAME"] = str(
                            connection_config["username"]
                        )
                        os.environ[
                            f"{stringcase.constcase(slug)}_PASSWORD"
                        ] = connection_config["password"]
                        os.environ[
                            f"{stringcase.constcase(slug)}_DB_NAME"
                        ] = connection_config["database_name"]
                    except KeyError:
                        exception_message = (
                            "Invalid local workspace PostgreSQL connection config. Please make sure you provide "
                            "the following keys: url, username, password."
                        )
                        raise LocalWorkspaceConfigError(exception_message)
                # S3 connections
                elif connection_config["type"] == "s3":
                    try:
                        os.environ[
                            f"{stringcase.constcase(slug)}_SECRET_ACCESS_KEY"
                        ] = connection_config["secret_access_key"]
                        os.environ[f"{stringcase.constcase(slug)}_ACCESS_KEY_ID"] = str(
                            connection_config["access_key_id"]
                        )
                        os.environ[f"{stringcase.constcase(slug)}_BUCKET_NAME"] = str(
                            connection_config["bucket_name"]
                        )
                    except KeyError:
                        exception_message = (
                            "Invalid local workspace S3 connection config. Please make sure you provide "
                            "the following keys: secret_key, access_key_id, bucket_name."
                        )
                        raise LocalWorkspaceConfigError(exception_message)
                # GCS connections
                elif connection_config["type"] == "gcs":
                    try:
                        os.environ[
                            f"{stringcase.constcase(slug)}_SERVICE_ACCOUNT_KEY"
                        ] = connection_config["service_account_key"]
                        os.environ[f"{stringcase.constcase(slug)}_BUCKET_NAME"] = str(
                            connection_config["bucket_name"]
                        )
                    except KeyError:
                        exception_message = (
                            "Invalid local workspace GCS connection config. Please make sure you provide "
                            "the following keys: service_account_key, bucket_name."
                        )
                        raise LocalWorkspaceConfigError(exception_message)
                # Custom connection
                else:
                    for key, value in connection_config.items():
                        if key != "type":
                            os.environ[stringcase.constcase(f"{slug}_{key}")] = str(
                                value
                            )

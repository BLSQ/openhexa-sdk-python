"""API interactions test module."""

import configparser
import os
import shutil
import uuid
from pathlib import Path
from unittest import mock
from zipfile import ZipFile

import pytest
import yaml
from click.testing import CliRunner

from openhexa.cli.api import upload_pipeline
from openhexa.cli.cli import pipelines_delete, pipelines_init


def test_upload_pipeline():
    """Test upload API call."""
    # to enable zip file creation
    config = configparser.ConfigParser()
    config["openhexa"] = {"debug": True, "current_workspace": "test_workspace"}

    runner = CliRunner()
    runner.invoke(pipelines_init, ["test_pipelines"])  # NOQA
    pipeline_dir = Path.cwd() / "test_pipelines"
    pipeline_zip_file_dir = Path.cwd() / "pipeline.zip"

    # create a sample file inside workspace dir
    with open(pipeline_dir / Path("workspace/dummy.txt"), "w") as test_file:
        test_file.write("Test upload")

    with mock.patch("openhexa.cli.api.graphql") as mocked_graphql_client:
        upload_pipeline(config=config, pipeline_directory_path=pipeline_dir)
        mocked_graphql_client.return_value = {"success": True, "errors": []}

        with ZipFile(pipeline_zip_file_dir) as zip_file:
            with pytest.raises(KeyError):
                zip_file.getinfo("workspace")

    shutil.rmtree(pipeline_dir)
    os.remove(pipeline_zip_file_dir)


def test_upload_pipeline_custom_files_path():
    """Test upload API call (custom file path)."""
    # to enable zip file creation
    config = configparser.ConfigParser()
    config["openhexa"] = {"debug": True, "current_workspace": "test_workspace"}

    runner = CliRunner()
    runner.invoke(pipelines_init, ["test_pipelines"])  # NOQA
    pipeline_dir = Path.cwd() / "test_pipelines"
    pipeline_zip_file_dir = Path.cwd() / "pipeline.zip"

    (pipeline_dir / Path("data")).mkdir()
    # set up a custom path for files location in workspace.yaml
    pipeline_configs = {"files": {"path": "./data"}}

    with open(pipeline_dir / Path("workspace.yaml"), "w") as pipeline_configs_file:
        pipeline_configs_file.write(yaml.dump(pipeline_configs))

    # create a sample file inside custom dir
    with open(pipeline_dir / Path("data/dummy.txt"), "w") as test_file:
        test_file.write("Test upload with custom files path")

    with mock.patch("openhexa.cli.api.graphql") as mocked_graphql_client:
        upload_pipeline(config=config, pipeline_directory_path=pipeline_dir)
        mocked_graphql_client.return_value = {"success": True, "errors": []}

        with ZipFile(pipeline_zip_file_dir) as zip_file:
            with pytest.raises(KeyError):
                zip_file.getinfo("data")

    shutil.rmtree(pipeline_dir)
    os.remove(pipeline_zip_file_dir)


def test_delete_pipeline_not_in_workspace():
    """Test delete pipeline (pipeline does not exist)."""
    config = configparser.ConfigParser()
    config["openhexa"] = {"debug": True, "current_workspace": "test_workspace"}

    with mock.patch("openhexa.cli.api.graphql") as mocked_graphql_client, mock.patch(
        "openhexa.cli.cli.open_config"
    ) as mocked_config:
        runner = CliRunner()
        mocked_config.return_value = config
        mocked_graphql_client.return_value = {"pipelineByCode": None}
        r = runner.invoke(pipelines_delete, ["test_pipelines"], input="test_pipelines")  # NOQA

        assert r.output == "Pipeline test_pipelines does not exist in workspace test_workspace\n"


def test_delete_pipeline_confirm_code_invalid():
    """Test delete pipeline with an invalid confirmation code."""
    config = configparser.ConfigParser()
    config["openhexa"] = {"debug": True, "current_workspace": "test_workspace"}

    with mock.patch("openhexa.cli.api.graphql") as mocked_graphql_client, mock.patch(
        "openhexa.cli.cli.open_config"
    ) as mocked_config:
        runner = CliRunner()
        mocked_config.return_value = config

        mocked_graphql_client.return_value = {
            "pipelineByCode": {
                "id": uuid.uuid4(),
                "code": "test_pipelines",
                "currentVersion": {"number": 1},
            }
        }
        r = runner.invoke(pipelines_delete, ["test_pipelines"], input="test_pipeline")  # NOQA
        # "Pipeline code and confirmation are different
        assert r.exit_code == 1


def test_delete_pipeline():
    """Happy path for delete pipeline API call."""
    config = configparser.ConfigParser()
    config["openhexa"] = {"debug": True, "current_workspace": "test_workspace"}

    with mock.patch("openhexa.cli.cli.get_pipeline") as mocked_get_pipeline, mock.patch(
        "openhexa.cli.cli.delete_pipeline"
    ) as mocked_delete_pipeline, mock.patch("openhexa.cli.cli.open_config") as mocked_config:
        runner = CliRunner()
        mocked_config.return_value = config

        mocked_get_pipeline.return_value = {
            "id": uuid.uuid4(),
            "code": "test_pipelines",
            "currentVersion": {"number": 1},
        }
        mocked_delete_pipeline.return_value = True
        r = runner.invoke(pipelines_delete, ["test_pipelines"], input="test_pipelines")  # NOQA

        assert r.exit_code == 0

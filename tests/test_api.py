import configparser
import os
import pytest
import shutil
import yaml

from click.testing import CliRunner
from openhexa.cli.api import upload_pipeline
from openhexa.cli.cli import pipelines_init
from pathlib import Path

from unittest import mock
from zipfile import ZipFile


def test_upload_pipeline():
    # to enable zip file creation
    config = configparser.ConfigParser()
    config["openhexa"] = {"debug": True, "current_workspace": "test_workspace"}

    runner = CliRunner()
    runner.invoke(pipelines_init, ["test_pipelines"])
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
    # to enable zip file creation
    config = configparser.ConfigParser()
    config["openhexa"] = {"debug": True, "current_workspace": "test_workspace"}

    runner = CliRunner()
    runner.invoke(pipelines_init, ["test_pipelines"])
    pipeline_dir = Path.cwd() / "test_pipelines"
    pipeline_zip_file_dir = Path.cwd() / "pipeline.zip"

    (pipeline_dir / Path("data")).mkdir()
    # setup a custom path for files location in workspace.yaml
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

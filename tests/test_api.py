import configparser
import os
import pytest
import shutil

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
    pipeline_dir = os.path.join(Path.cwd(), "test_pipelines")
    pipeline_zip_file_dir = os.path.join(Path.cwd(), "pipeline.zip")

    with mock.patch("openhexa.cli.api.graphql") as mocked_graphql_client:
        upload_pipeline(config=config, pipeline_directory_path=pipeline_dir)
        mocked_graphql_client.return_value = {"success": True, "errors": []}

        with ZipFile(pipeline_zip_file_dir) as zip_file:
            with pytest.raises(KeyError):
                zip_file.getinfo("workspace")

    shutil.rmtree(pipeline_dir)
    os.remove(pipeline_zip_file_dir)

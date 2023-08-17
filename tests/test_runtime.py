import configparser
import shutil

from click.testing import CliRunner
from openhexa.sdk.pipelines.runtime import get_pipeline_specs
from openhexa.cli.cli import pipelines_init
from pathlib import Path

from unittest import mock


def test_upload_pipeline():
    config = configparser.ConfigParser()
    config["openhexa"] = {"debug": True, "current_workspace": "test_workspace"}
    pipeline_code = "test_pipeline"

    runner = CliRunner()
    runner.invoke(pipelines_init, [pipeline_code])
    pipeline_dir = Path.cwd() / pipeline_code

    with mock.patch("openhexa.cli.api.graphql") as mocked_graphql_client:
        pipeline_specs, pipeline_parameters_specs = get_pipeline_specs(pipeline_dir_path=pipeline_dir)
        mocked_graphql_client.return_value = {"success": True, "errors": []}

        assert len(pipeline_parameters_specs) == 0
        assert pipeline_specs.code == pipeline_code
        assert pipeline_specs.name == pipeline_code
        assert pipeline_specs.timeout is None

    shutil.rmtree(pipeline_dir)

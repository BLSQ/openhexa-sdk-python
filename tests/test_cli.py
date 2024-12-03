"""CLI test module."""

import base64
import os
from io import BytesIO
from pathlib import Path
from tempfile import mkdtemp
from unittest import TestCase
from unittest.mock import MagicMock, patch
from zipfile import ZipFile

import pytest
from click.testing import CliRunner

from openhexa.cli.cli import pipelines_download, pipelines_push, pipelines_run, workspaces_add
from openhexa.sdk.pipelines import Pipeline

python_file_name = "pipeline.py"
python_code = "print('pipeline.py file')"
version = "v1.0"
pipeline_name = "MyPipeline"


def create_zip_with_pipeline():
    """Create a zip file containing the pipeline.py file."""
    zip_buffer = BytesIO()
    fake_zipfile = ZipFile(zip_buffer, "w")
    fake_zipfile.writestr(python_file_name, python_code)
    fake_zipfile.close()
    return zip_buffer


def setup_graphql_response(zip_buffer=create_zip_with_pipeline()):
    """Set up the mock GraphQL response pipelines."""
    return {
        "pipelineByCode": {"currentVersion": {"zipfile": base64.b64encode(zip_buffer.getvalue()).decode()}},
        "pipelines": {"items": []},  # (empty workspace initially)
    }


@pytest.mark.usefixtures("settings")
class CliRunTest(TestCase):
    """Test the CLI."""

    runner = None

    def setUp(self):
        """Configure the CLI runner and the user config."""
        self.runner = CliRunner()
        return super().setUp()

    def tearDown(self) -> None:
        """Tear down the CLI runner and the user config.

        Returns
        -------
            None
        """
        return super().tearDown()

    @patch("openhexa.cli.api.ask_pipeline_config_creation", return_value=True)
    def test_no_pipeline(self, *args):
        """Test running a pipeline without a pipeline.py file."""
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(pipelines_run, [mkdtemp()])
            assert result.exit_code == 1
            self.assertTrue("does not contain a pipeline.py file" in str(result.exception))

    @patch("openhexa.cli.api.graphql")
    def test_download_pipeline_no_pipeline(self, mock_graphql):
        """Test the download pipeline command."""
        with self.runner.isolated_filesystem() as tmp:
            # Unknown pipeline
            mock_graphql.return_value = {"pipelineByCode": None}
            result = self.runner.invoke(pipelines_download, ["test_pipeline", tmp])
            self.assertIn(
                "No pipeline exists in workspace-slug with code test_pipeline",
                str(result.exception),
            )

    @patch("openhexa.cli.api.graphql")
    def test_download_pipeline_overwrite(self, mock_graphql):
        """Test the download pipeline command with an existing director with and without content."""
        with self.runner.isolated_filesystem() as tmp:
            # Known Pipeline & non-empty directory
            with open(Path(tmp) / python_file_name, "w") as f:
                f.write("<content>")

            mock_graphql.return_value = setup_graphql_response()

            result = self.runner.invoke(pipelines_download, ["test_pipeline", tmp], input="N\n")
            self.assertIn("Overwrite the files?", result.output)
            self.assertIn(f"{tmp} is not empty", result.output)
            self.assertEqual(open(Path(tmp) / python_file_name).read(), "<content>")

            # Overwrite the files in the directory
            mock_graphql.return_value = setup_graphql_response()

            result = self.runner.invoke(pipelines_download, ["test_pipeline", tmp], input="y\n")
            self.assertIn("Overwrite the files?", result.output)
            self.assertEqual(open(Path(tmp) / python_file_name).read(), python_code)

    @patch("openhexa.cli.api.graphql")
    def test_download_pipeline(self, mock_graphql):
        """Test the download pipeline command."""
        with self.runner.isolated_filesystem() as tmp:
            # Create a zipfile with a pipeline.py file in a buffer
            mock_graphql.return_value = setup_graphql_response()

            result = self.runner.invoke(pipelines_download, ["test_pipeline", tmp])
            self.assertEqual(result.exit_code, 0)
            path = Path(tmp) / python_file_name
            self.assertTrue(path.exists())
            self.assertEqual(open(path).read(), python_code)

    @patch("openhexa.cli.api.graphql")
    @patch("openhexa.cli.cli.get_pipeline")
    @patch("openhexa.cli.cli.upload_pipeline")
    @patch.dict(os.environ, {"HEXA_API_URL": "https://www.bluesquarehub.com/", "HEXA_WORKSPACE": "workspace"})
    def test_push_pipeline(self, mock_upload_pipeline, mock_get_pipeline, mock_graphql):
        """Test pushing a pipeline."""
        with self.runner.isolated_filesystem() as tmp:
            with open(Path(tmp) / python_file_name, "w") as f:
                f.write(python_code)
            mock_graphql.return_value = setup_graphql_response()
            mock_pipeline = MagicMock(spec=Pipeline)
            mock_pipeline.code = pipeline_name
            mock_get_pipeline.return_value = mock_pipeline
            mock_upload_pipeline.return_value = {"versionName": version}

            result = self.runner.invoke(pipelines_push, [tmp, "--name", version])
            self.assertEqual(result.exit_code, 0)
            self.assertIn(
                (
                    f"✅ New version '{version}' created! "
                    f"You can view the pipeline in OpenHEXA on https://www.bluesquarehub.com/workspaces/workspace/pipelines/{pipeline_name}"
                ),
                result.output,
            )
            self.assertTrue(mock_upload_pipeline.called)

    @patch("openhexa.cli.api.graphql")
    def test_workspaces_add_not_found(self, mock_graphql):
        """Test the add workspace command when the workspace doesn't exist on the current server."""
        with self.runner.isolated_filesystem():
            mock_graphql.return_value = {"workspace": None}
            result = self.runner.invoke(workspaces_add, ["test_workspace"], input="random_token \n")
            self.assertEqual(result.exit_code, 1)
            self.assertIn(
                "Workspace test_workspace does not exist",
                str(result.stdout),
            )

    @patch("openhexa.cli.api.graphql")
    def test_workspaces_add(self, mock_graphql):
        """Test the add workspace command."""
        with self.runner.isolated_filesystem():
            mock_graphql.return_value = {"workspace": {"name": "test_workspace", "slug": "test_workspace_0000"}}
            result = self.runner.invoke(workspaces_add, ["test_workspace"], input="random_token \n")
            self.assertEqual(result.exit_code, 0)

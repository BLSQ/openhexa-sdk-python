"""CLI test module."""

import base64
from io import BytesIO
from pathlib import Path
from tempfile import mkdtemp
from unittest import TestCase
from unittest.mock import patch
from zipfile import ZipFile

import pytest
from click.testing import CliRunner

from openhexa.cli.cli import pipelines_download, pipelines_run, workspaces_add


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
            # Create a zipfile with a pipeline.py file in a buffer
            zip_buffer = BytesIO()
            fake_zipfile = ZipFile(zip_buffer, "w")
            fake_zipfile.writestr("pipeline.py", "print('pipeline.py file')")
            fake_zipfile.close()

            # Known Pipeline & non empty directory
            with open(tmp + "/pipeline.py", "w") as f:
                f.write("<content>")
            mock_graphql.return_value = {
                "pipelineByCode": {"currentVersion": {"zipfile": base64.b64encode(zip_buffer.getvalue()).decode()}}
            }
            result = self.runner.invoke(pipelines_download, ["test_pipeline", tmp], input="N\n")
            self.assertIn("Overwrite the files?", result.output)
            self.assertIn(f"{tmp} is not empty", result.output)
            self.assertEqual(open(tmp + "/pipeline.py").read(), "<content>")

            # Overwrite the files in the directory
            mock_graphql.return_value = {
                "pipelineByCode": {"currentVersion": {"zipfile": base64.b64encode(zip_buffer.getvalue()).decode()}}
            }
            result = self.runner.invoke(pipelines_download, ["test_pipeline", tmp], input="y\n")
            self.assertIn("Overwrite the files?", result.output)
            self.assertEqual(open(tmp + "/pipeline.py").read(), "print('pipeline.py file')")

    @patch("openhexa.cli.api.graphql")
    def test_download_pipeline(self, mock_graphql):
        """Test the download pipeline command."""
        with self.runner.isolated_filesystem() as tmp:
            # Create a zipfile with a pipeline.py file in a buffer
            zip_buffer = BytesIO()
            fake_zipfile = ZipFile(zip_buffer, "w")
            fake_zipfile.writestr("pipeline.py", "print('pipeline.py file')")
            fake_zipfile.close()

            mock_graphql.return_value = {
                "pipelineByCode": {"currentVersion": {"zipfile": base64.b64encode(zip_buffer.getvalue()).decode()}}
            }
            result = self.runner.invoke(pipelines_download, ["test_pipeline", tmp])
            self.assertEqual(result.exit_code, 0)
            self.assertTrue((Path(tmp) / "pipeline.py").exists())
            self.assertEqual(open(tmp + "/pipeline.py").read(), "print('pipeline.py file')")

    @patch("openhexa.cli.api.graphql")
    def test_workspaces_add_not_found(self, mock_graphql):
        """Test the add workspace command when the workspae doesn't exist on the current server."""
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

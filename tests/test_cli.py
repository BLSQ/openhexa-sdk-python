"""CLI test module."""

import base64
from configparser import ConfigParser
from io import BytesIO
from pathlib import Path
from tempfile import mkdtemp
from unittest import TestCase
from unittest.mock import MagicMock, patch
from zipfile import ZipFile

from click.testing import CliRunner

from openhexa.cli.cli import pipelines_download, pipelines_run


class CliRunTest(TestCase):
    """Test the CLI."""

    runner = None
    user_config = None

    def setUp(self):
        """Configure the CLI runner and the user config."""
        self.runner = CliRunner()
        self.user_config = ConfigParser()
        self.user_config.read_string(
            """
            [openhexa]
            url=https://test.openhexa.org
            current_workspace=test_workspace

            [workspaces]
            test_workspace = WORKSPACE_TOKEN
            """
        )
        self.patch_user_config = patch("openhexa.cli.cli.open_config", return_value=self.user_config)
        self.patch_user_config.start()
        return super().setUp()

    def tearDown(self) -> None:
        """Tear down the CLI runner and the user config.

        Returns
        -------
            None
        """
        self.patch_user_config.stop()
        return super().tearDown()

    @patch("openhexa.cli.api.ask_pipeline_config_creation", return_value=True)
    def test_no_pipeline(self, *args):
        """Test running a pipeline without a pipeline.py file."""
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(pipelines_run, [mkdtemp()])
            assert result.exit_code == 1
            self.assertTrue("does not contain a pipeline.py file" in str(result.exception))

    @patch("openhexa.cli.api.ask_pipeline_config_creation", return_value=True)
    def test_no_config_file(self, mock_ask_config):
        """Test running a pipeline without a workspace.yaml file.

        It should ask the user if they want to create the config file.
        Two tests are performed:
        - The user accepts the config creation
        - The user refuses the config creation
        """
        with self.runner.isolated_filesystem() as tmp:
            with open("pipeline.py", "w") as f:
                f.write("")

            self.assertFalse((Path(tmp) / "workspace.yaml").exists())
            with patch("subprocess.Popen") as mock_popen:
                mock_process = MagicMock()
                mock_process.wait.return_value = MagicMock()

                mock_popen.return_value = mock_process

                # First without accepting the config creation
                mock_ask_config.return_value = False
                result = self.runner.invoke(pipelines_run, [tmp])
                self.assertEqual(result.exit_code, 1)
                self.assertFalse((Path(tmp) / "workspace.yaml").exists())
                mock_popen.assert_not_called()

                # This time we accept the config creation
                mock_ask_config.return_value = True
                result = self.runner.invoke(pipelines_run, [tmp])
                self.assertEqual(result.exit_code, 0)
                self.assertTrue((Path(tmp) / "workspace.yaml").exists())
                mock_popen.assert_called_once()

    @patch("openhexa.cli.api.graphql")
    def test_download_pipeline_no_pipeline(self, mock_graphql):
        """Test the download pipeline command."""
        with self.runner.isolated_filesystem() as tmp:
            # Unknown pipeline
            mock_graphql.return_value = {"pipelineByCode": None}
            result = self.runner.invoke(pipelines_download, ["test_pipeline", tmp])
            self.assertIn(
                "No pipeline exists in test_workspace with code test_pipeline",
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

"""CLI test module."""

from configparser import ConfigParser
from pathlib import Path
from tempfile import mkdtemp
from unittest import TestCase
from unittest.mock import MagicMock, patch

from click.testing import CliRunner

from openhexa.cli.cli import pipelines_run


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

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

from openhexa.cli.api import GraphQLError
from openhexa.cli.cli import (
    pipelines_download,
    pipelines_list,
    pipelines_push,
    pipelines_run,
    select_pipeline,
    workspaces_add,
)
from openhexa.sdk.pipelines import Pipeline

python_file_name = "pipeline.py"
python_code = "print('pipeline.py file')"
version = "v1.0"
pipeline_name = "MyPipeline"
pipeline_id = "pipeline_id"
pipeline_version_id = "pipeline_version_id"
template = {
    "id": "template_id",
    "name": "test_template",
    "code": "template_code",
    "currentVersion": {"versionNumber": "1.0"},
}
changelog = "Changelog for the new version"


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
        "pipelineByCode": {
            "code": "pipeline-1234",
            "currentVersion": {"zipfile": base64.b64encode(zip_buffer.getvalue()).decode()},
        },
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
    @patch("openhexa.cli.cli.get_pipelines_pages")
    @patch("openhexa.cli.cli.upload_pipeline")
    @patch("openhexa.cli.cli.create_pipeline_template_version")
    @patch.dict(os.environ, {"HEXA_API_URL": "https://www.bluesquarehub.com/", "HEXA_WORKSPACE": "workspace"})
    def test_push_pipeline(
        self, mock_create_template, mock_upload_pipeline, mock_get_pipelines_pages, mock_get_pipeline, mock_graphql
    ):
        """Test pushing a pipeline."""
        with self.runner.isolated_filesystem() as tmp:
            with open(Path(tmp) / python_file_name, "w") as f:
                f.write(python_code)
            mock_graphql.return_value = setup_graphql_response()
            mock_pipeline = MagicMock(spec=Pipeline)
            mock_pipeline.name = pipeline_name
            mock_get_pipeline.return_value = mock_pipeline
            mock_get_pipelines_pages.return_value = {
                "items": [
                    {"name": "Pipeline1", "code": "code1"},
                    {"name": "Pipeline2", "code": "code2"},
                ],
                "totalPages": 2,
            }
            mock_upload_pipeline.return_value = {
                "versionName": version,
                "pipeline": {
                    "id": pipeline_id,
                    "permissions": {"createTemplateVersion": {"isAllowed": True}},
                    "template": template,
                },
                "id": pipeline_version_id,
            }
            mock_create_template.return_value = template

            result = self.runner.invoke(
                pipelines_push,
                [tmp, "--name", version],
                input="\n".join(["4", "pipeline_code", "Y", "Y", changelog]) + "\n",
            )
            self.assertEqual(result.exit_code, 0)
            self.assertIn("Which pipeline do you want to update?", result.output)
            self.assertIn("Insert a pipeline code", result.output)
            self.assertIn(
                (
                    f"✅ New version '{version}' created! "
                    f"You can view the pipeline in OpenHEXA on https://www.bluesquarehub.com/workspaces/workspace/pipelines/pipeline-1234"
                ),
                result.output,
            )
            self.assertTrue(mock_upload_pipeline.called)
            mock_create_template.assert_called_with("workspace", pipeline_id, pipeline_version_id, changelog)
            self.assertIn(
                (
                    f"✅ New version '{template['currentVersion']['versionNumber']}' of the template '{template['name']}' created! "
                    f"You can view the new template version in OpenHEXA on https://www.bluesquarehub.com/workspaces/workspace/templates/{template['code']}/versions"
                ),
                result.output,
            )

    @patch("openhexa.cli.api.graphql")
    @patch.dict(os.environ, {"HEXA_API_URL": "https://www.bluesquarehub.com/", "HEXA_WORKSPACE": "workspace"})
    def test_push_pipeline_with_yes_flag_without_code(self, mock_graphql):
        """Test pushing a pipeline with the --yes flag without providing a --code."""
        with self.runner.isolated_filesystem() as tmp:
            with open(Path(tmp) / python_file_name, "w") as f:
                f.write(python_code)
            mock_graphql.return_value = setup_graphql_response()

            result = self.runner.invoke(
                pipelines_push,
                [tmp, "--yes"],
            )
            self.assertEqual(result.exit_code, 1)
            self.assertIn(
                "❌ You must provide a pipeline code (using -c or --code) when using the --yes flag.", result.output
            )

    @patch("openhexa.cli.api.graphql")
    @patch("openhexa.cli.cli.get_pipeline")
    @patch("openhexa.cli.cli.get_pipelines_pages")
    @patch("openhexa.cli.cli.get_pipeline_from_code")
    @patch.dict(os.environ, {"HEXA_API_URL": "https://www.bluesquarehub.com/", "HEXA_WORKSPACE": "workspace"})
    def test_push_pipeline_with_non_existing_code(
        self, mock_get_pipeline_from_code, mock_get_pipelines_pages, mock_get_pipeline, mock_graphql
    ):
        """Test pushing a pipeline with a non-existing --code flag."""
        with self.runner.isolated_filesystem() as tmp:
            with open(Path(tmp) / python_file_name, "w") as f:
                f.write(python_code)
            mock_graphql.return_value = setup_graphql_response()
            mock_pipeline = MagicMock(spec=Pipeline)
            mock_pipeline.name = pipeline_name
            mock_get_pipeline.return_value = mock_pipeline
            mock_get_pipelines_pages.return_value = {
                "items": [
                    {"name": "Pipeline1", "code": "code1"},
                    {"name": "Pipeline2", "code": "code2"},
                ],
                "totalPages": 2,
            }
            mock_get_pipeline_from_code.return_value = None  # Simulate non-existing pipeline code

            result = self.runner.invoke(
                pipelines_push,
                [tmp, "--code", "non_existing_code"],
            )
            self.assertEqual(result.exit_code, 1)
            self.assertIn("❌ Pipeline with code 'non_existing_code' not found.", result.output)

    @patch("openhexa.cli.api.graphql")
    @patch("openhexa.cli.cli.get_pipeline")
    @patch("openhexa.cli.cli.get_pipelines_pages")
    @patch("openhexa.cli.cli.upload_pipeline")
    @patch.dict(os.environ, {"HEXA_API_URL": "https://www.bluesquarehub.com/", "HEXA_WORKSPACE": "workspace"})
    def test_push_pipeline_with_code_flag(
        self, mock_upload_pipeline, mock_get_pipelines_pages, mock_get_pipeline, mock_graphql
    ):
        """Test pushing a pipeline using the --code flag."""
        code = "code1"
        with self.runner.isolated_filesystem() as tmp:
            with open(Path(tmp) / python_file_name, "w") as f:
                f.write(python_code)
            mock_graphql.return_value = {
                "pipelineByCode": {
                    "code": code,
                    "currentVersion": {"zipfile": ""},
                },
                "pipelines": {"items": []},
            }
            mock_pipeline = MagicMock(spec=Pipeline)
            mock_pipeline.name = pipeline_name
            mock_get_pipeline.return_value = mock_pipeline
            mock_get_pipelines_pages.return_value = {
                "items": [
                    {"name": "Pipeline1", "code": "code1"},
                    {"name": "Pipeline2", "code": "code2"},
                ],
                "totalPages": 2,
            }
            mock_upload_pipeline.return_value = {
                "versionName": version,
                "pipeline": {
                    "id": pipeline_id,
                    "permissions": {"createTemplateVersion": {"isAllowed": True}},
                    "template": template,
                },
                "id": pipeline_version_id,
            }

            result = self.runner.invoke(
                pipelines_push,
                [tmp, "--name", version, "--code", code],
                input="Y\nn\n",
            )
            self.assertEqual(result.exit_code, 0)
            self.assertNotIn("Which pipeline do you want to update?", result.output)
            self.assertTrue(mock_upload_pipeline.called)
            self.assertEqual(mock_upload_pipeline.call_args[0][0], code)
            self.assertIn(
                f"✅ New version '{version}' created! ",
                result.output,
            )

    @patch("openhexa.cli.cli.click.prompt")
    def test_select_pipeline(self, mock_prompt):
        workspace_pipelines = [
            {"name": "Pipeline1", "code": "code1"},
            {"name": "Pipeline2", "code": "code2"},
        ]
        pipeline = MagicMock()
        pipeline.name = "TestPipeline"

        mock_prompt.side_effect = [1]  # User selects the first pipeline

        selected_pipeline = select_pipeline(workspace_pipelines, 1, pipeline)

        self.assertEqual(selected_pipeline, workspace_pipelines[0])

    @patch("openhexa.cli.cli.click.prompt")
    def test_select_pipeline_create_new(self, mock_prompt):
        workspace_pipelines = []
        pipeline = MagicMock()
        pipeline.name = "TestPipeline"

        mock_prompt.side_effect = [1]  # User selects to create a new pipeline

        selected_pipeline = select_pipeline(workspace_pipelines, 1, pipeline)

        self.assertIsNone(selected_pipeline)

    @patch("openhexa.cli.cli.get_pipeline_from_code")
    @patch("openhexa.cli.cli.click.prompt")
    def test_select_pipeline_enter_code(self, mock_prompt, mock_get_pipeline_from_code):
        workspace_pipelines = []
        pipeline = MagicMock()
        pipeline.name = "TestPipeline"
        pipeline = MagicMock()
        pipeline.name = "Pipeline3"
        pipeline.code = "code3"
        mock_prompt.side_effect = [2, pipeline.code]  # User selects to enter a pipeline code and provides "code3"
        mock_get_pipeline_from_code.return_value = pipeline

        selected_pipeline = select_pipeline(workspace_pipelines, 2, pipeline)

        self.assertEqual(selected_pipeline, pipeline)
        mock_get_pipeline_from_code.assert_called_with(pipeline.code)

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

    @patch.dict(os.environ, {"HEXA_WORKSPACE": "test_workspace"})
    @patch("openhexa.cli.cli.OpenHexaClient")
    def test_pipelines_list_ssl_error(self, mock_client_class):
        """Test the pipelines list command handles SSL errors gracefully."""
        mock_client = mock_client_class.return_value
        mock_client.__enter__ = lambda self: mock_client
        mock_client.__exit__ = lambda self, *args: None
        ssl_error = GraphQLError(
            "SSL certificate verification failed. If you want to disable SSL verification, set the environment variable: HEXA_VERIFY_SSL=false"
        )
        mock_client.pipelines.side_effect = ssl_error

        result = self.runner.invoke(pipelines_list)
        self.assertEqual(result.exit_code, 1)
        self.assertIn("SSL certificate verification failed", result.output)
        self.assertIn("HEXA_VERIFY_SSL=false", result.output)

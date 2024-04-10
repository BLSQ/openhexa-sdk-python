"""API interactions test module."""

import base64
import io
import tempfile
from pathlib import Path
from unittest import mock
from zipfile import ZipFile

from openhexa.cli.api import create_pipeline_structure, upload_pipeline


def test_create_pipeline_structure(settings):
    """Test create_pipeline_structure function."""
    with tempfile.TemporaryDirectory() as temp_dir:
        pipeline_dir = create_pipeline_structure(
            "My pipeline",
            Path(temp_dir),
            workspace=settings.current_workspace,
            workflow_mode="manual",
        )

        assert (pipeline_dir / "pipeline.py").exists()
        assert (pipeline_dir / "workspace").exists()
        assert (pipeline_dir / "workspace.yaml").exists()

        assert (
            "name: Push pipeline on OpenHEXA"
            in (pipeline_dir / ".github" / "workflows" / "push-pipeline.yml").read_text()
        )
        assert "workflow_dispatch" in (pipeline_dir / ".github" / "workflows" / "push-pipeline.yml").read_text()

        assert "def my_pipeline(" in (pipeline_dir / "pipeline.py").read_text()


def test_upload_pipeline_success(settings):
    """Test upload API call."""
    with tempfile.TemporaryDirectory() as temp_dir:
        pipeline_dir = create_pipeline_structure(
            "my_pipeline",
            Path(temp_dir),
            workspace="workspace-slug",
        )

        # create a sample file inside workspace dir
        assert (Path(temp_dir) / "my_pipeline").exists()
        assert (pipeline_dir / "pipeline.py").exists()
        assert (pipeline_dir / "workspace").exists(), "Workspace directory not created"

        # Add files to the workspace directory
        with open(pipeline_dir / "workspace" / "dummy.txt", "w") as test_file:
            test_file.write("Test upload")

        # Add markdown file next to the pipeline.py
        with open(pipeline_dir / "readme.md", "w") as test_file:
            test_file.write("# README")

        with mock.patch("openhexa.cli.api.graphql") as mocked_graphql_client:
            mocked_graphql_client.return_value = {
                "uploadPipeline": {"pipelineVersion": {"name": "1"}, "success": True, "errors": []}
            }
            upload_pipeline(pipeline_dir, "version-name", "My description", "https://github.com/")
            args_input = mocked_graphql_client.call_args[0][1]["input"]
            assert args_input["code"] == "my-pipeline"
            assert args_input["workspaceSlug"] == "workspace-slug"
            assert args_input["timeout"] is None
            assert args_input["parameters"] == []
            assert args_input["name"] == "version-name"
            assert args_input["description"] == "My description"
            assert args_input["externalLink"] == "https://github.com/"

            # Check if the zipfile is correctly created
            with ZipFile(io.BytesIO(base64.b64decode(args_input["zipfile"]))) as zip_file:
                assert "readme.md" in zip_file.namelist()
                assert "pipeline.py" in zip_file.namelist()
                assert len(zip_file.namelist()) == 2

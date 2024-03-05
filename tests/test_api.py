"""API interactions test module."""

import base64
import io
import tempfile
from pathlib import Path
from unittest import mock
from zipfile import ZipFile

from openhexa.cli.api import create_pipeline_structure, upload_pipeline


def test_upload_pipeline_success(settings):
    """Test upload API call."""
    with tempfile.TemporaryDirectory() as temp_dir:
        pipeline_dir = create_pipeline_structure("my_pipeline", Path(temp_dir))

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
            mocked_graphql_client.return_value = {"uploadPipeline": {"version": 1, "success": True, "errors": []}}
            upload_pipeline(pipeline_dir)
            args_input = mocked_graphql_client.call_args[0][1]["input"]
            assert args_input["code"] == "my-pipeline"
            assert args_input["workspaceSlug"] == "workspace-slug"
            assert args_input["timeout"] is None
            assert args_input["parameters"] == []

            # Check if the zipfile is correctly created
            with ZipFile(io.BytesIO(base64.b64decode(args_input["zipfile"]))) as zip_file:
                assert zip_file.namelist() == ["readme.md", "pipeline.py"]

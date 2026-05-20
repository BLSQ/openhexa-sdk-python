"""API interactions test module."""

import base64
import io
import tempfile
from pathlib import Path
from unittest import mock
from zipfile import ZipFile

from openhexa.cli.api import create_pipeline, create_pipeline_structure, upload_pipeline


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
            upload_pipeline(
                "target_pipeline_code", pipeline_dir, "version-name", "My description", "https://github.com/"
            )
            args_input = mocked_graphql_client.call_args[0][1]["input"]
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


def test_create_pipeline_atomic_with_version(settings):
    """When a path is provided, create_pipeline sends pipeline + first version atomically."""
    with tempfile.TemporaryDirectory() as temp_dir:
        pipeline_dir = create_pipeline_structure(
            "my_pipeline",
            Path(temp_dir),
            workspace="workspace-slug",
        )

        with mock.patch("openhexa.cli.api.graphql") as mocked_graphql_client:
            mocked_graphql_client.return_value = {
                "createPipeline": {
                    "success": True,
                    "errors": [],
                    "pipeline": {
                        "id": "p-1",
                        "code": "my-pipeline",
                        "permissions": {"createTemplateVersion": {"isAllowed": False}},
                        "template": None,
                    },
                    "pipelineVersion": {
                        "id": "v-1",
                        "versionName": "v1",
                        "pipeline": {
                            "id": "p-1",
                            "code": "my-pipeline",
                            "permissions": {"createTemplateVersion": {"isAllowed": False}},
                            "template": None,
                        },
                    },
                }
            }

            create_pipeline(
                "My Pipeline",
                pipeline_dir,
                version_name="v1",
                version_description="first version",
                version_external_link="https://github.com/",
                functional_type="extraction",
                tags=["tag-a"],
            )

            args_input = mocked_graphql_client.call_args[0][1]["input"]

            # pipeline-level fields
            assert args_input["workspaceSlug"] == "workspace-slug"
            assert args_input["name"] == "My Pipeline"
            assert args_input["functionalType"] == "extraction"
            assert args_input["tags"] == ["tag-a"]

            # version sub-input
            version_input = args_input["version"]
            assert version_input["name"] == "v1"
            assert version_input["description"] == "first version"
            assert version_input["externalLink"] == "https://github.com/"
            assert version_input["parameters"] == []
            assert version_input["timeout"] is None

            with ZipFile(io.BytesIO(base64.b64decode(version_input["zipfile"]))) as zip_file:
                assert "pipeline.py" in zip_file.namelist()


def test_create_pipeline_without_version(settings):
    """When no path is given, create_pipeline omits the `version` sub-input."""
    with mock.patch("openhexa.cli.api.graphql") as mocked_graphql_client:
        mocked_graphql_client.return_value = {
            "createPipeline": {
                "success": True,
                "errors": [],
                "pipeline": {
                    "id": "p-1",
                    "code": "my-pipeline",
                    "permissions": {"createTemplateVersion": {"isAllowed": False}},
                    "template": None,
                },
                "pipelineVersion": None,
            }
        }

        create_pipeline("My Pipeline", functional_type="extraction", tags=["tag-a"])

        args_input = mocked_graphql_client.call_args[0][1]["input"]
        assert "version" not in args_input
        assert args_input["name"] == "My Pipeline"
        assert args_input["functionalType"] == "extraction"
        assert args_input["tags"] == ["tag-a"]

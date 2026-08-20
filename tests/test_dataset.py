"""Dataset test module."""

import os
from io import StringIO
from unittest import TestCase
from unittest.mock import patch

from httmock import HTTMock, all_requests, response

from openhexa.sdk.datasets import Dataset
from openhexa.sdk.datasets.dataset import DatasetVersion
from openhexa.sdk.workspaces import workspace


class DatasetTest(TestCase):
    """Dataset test class."""

    @patch.dict(
        os.environ,
        {
            "HEXA_WORKSPACE": "workspace-slug",
            "HEXA_TOKEN": "token",
            "HEXA_SERVER_URL": "http://server",
        },
    )
    def test_create_dataset_ok(self):
        """Ensure that datasets can be created."""

        @all_requests
        def graphql_responses(url, request):
            if b"createDataset" in request.body:
                return response(
                    200,
                    {
                        "data": {
                            "createDataset": {
                                "success": True,
                                "dataset": {
                                    "id": "dataset_id",
                                    "slug": "my-dataset",
                                    "name": "My Dataset",
                                    "description": "My Dataset description",
                                    "createdAt": "2021-01-01T00:00:00.000Z",
                                },
                            }
                        }
                    },
                    request=request,
                )
            elif b"getDataset" in request.body:
                return response(
                    200,
                    {
                        "data": {
                            "datasetLinkBySlug": {
                                "id": "link_id",
                                "dataset": {
                                    "id": "dataset_id",
                                    "slug": "my-dataset",
                                    "name": "My Dataset",
                                    "description": "My Dataset description",
                                    "workspace": {"slug": "source-workspace"},
                                },
                            }
                        }
                    },
                    request=request,
                )

        with HTTMock(graphql_responses):
            dataset = workspace.create_dataset("My Dataset", "My Dataset description")
            self.assertEqual(dataset.id, "dataset_id")
            self.assertEqual(dataset.slug, "my-dataset")

    @patch.dict(
        os.environ,
        {
            "HEXA_WORKSPACE": "workspace-slug",
            "HEXA_TOKEN": "token",
            "HEXA_SERVER_URL": "server",
        },
    )
    @patch("openhexa.sdk.datasets.dataset.graphql")
    def test_create_dataset_version(self, mock_graphql):
        """Ensure that dataset versions can be created."""
        d = Dataset(
            id="id",
            slug="my-dataset",
            name="My Dataset",
            description="My Dataset description",
        )

        mock_graphql.return_value = {
            "createDatasetVersion": {
                "success": True,
                "version": {
                    "id": "<newVersionId>",
                    "name": "Second version",
                    "description": "Description",
                    "createdAt": "2021-01-01T00:00:00.000Z",
                },
            }
        }

        v = d.create_version("Second version")
        self.assertEqual(v.id, "<newVersionId>")
        v = d.create_version("Second version")
        self.assertEqual(v.id, "<newVersionId>")

    @patch.dict(
        os.environ,
        {
            "HEXA_WORKSPACE": "workspace-slug",
            "HEXA_TOKEN": "token",
            "HEXA_SERVER_URL": "server",
        },
    )
    @patch("openhexa.sdk.datasets.dataset.requests.put")
    @patch("openhexa.sdk.datasets.dataset.graphql")
    def test_add_file_upload_headers(self, mock_graphql, mock_put):
        """Uploads to Azure Blob Storage must specify the blob type, other backends must not receive it."""
        cases = [
            (
                "https://account.blob.core.windows.net/hexa-datasets/version_id/file.csv?sig=signature",
                {"Content-Type": "application/octet-stream", "x-ms-blob-type": "BlockBlob"},
            ),
            (
                "https://storage.googleapis.com/hexa-datasets/version_id/file.csv?X-Goog-Signature=signature",
                {"Content-Type": "application/octet-stream"},
            ),
        ]

        for upload_url, expected_headers in cases:
            with self.subTest(upload_url=upload_url):
                mock_graphql.side_effect = [
                    {"generateDatasetUploadUrl": {"success": True, "uploadUrl": upload_url, "errors": []}},
                    {
                        "createDatasetVersionFile": {
                            "success": True,
                            "errors": [],
                            "file": {
                                "id": "file_id",
                                "filename": "file.csv",
                                "uri": "file.csv",
                                "contentType": "application/octet-stream",
                                "createdAt": "2021-01-01T00:00:00.000Z",
                            },
                        }
                    },
                ]
                version = DatasetVersion(dataset=None, id="version_id", name="v1", created_at=None)

                version.add_file(StringIO("foo,bar"), filename="file.csv")

                self.assertEqual(mock_put.call_args.args[0], upload_url)
                self.assertEqual(mock_put.call_args.kwargs["headers"], expected_headers)

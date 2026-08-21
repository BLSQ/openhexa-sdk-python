"""Dataset test module."""

import base64
import os
from io import BytesIO, StringIO
from unittest import TestCase
from unittest.mock import MagicMock, patch
from urllib.parse import quote

from httmock import HTTMock, all_requests, response

from openhexa.sdk.datasets import Dataset
from openhexa.sdk.datasets.dataset import DatasetVersion
from openhexa.sdk.workspaces import workspace

ENV = {"HEXA_WORKSPACE": "workspace-slug", "HEXA_TOKEN": "token", "HEXA_SERVER_URL": "server"}
UPLOAD_URL = "https://account.blob.core.windows.net/hexa-datasets/dataset_id/version_id/file.csv?sig=signature"
AZURE_HEADERS = {"Content-Type": "application/octet-stream", "x-ms-blob-type": "BlockBlob"}


def upload_url_response(upload_url=UPLOAD_URL, headers=None):
    """Build a generateDatasetUploadUrl mutation response."""
    return {"generateDatasetUploadUrl": {"success": True, "uploadUrl": upload_url, "headers": headers, "errors": []}}


def version_file_response():
    """Build a createDatasetVersionFile mutation response."""
    return {
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
    }


def block_id(index):
    """Build the block id the SDK generates for the block at the given index."""
    return base64.b64encode(f"{index:032d}".encode()).decode()


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

    @patch.dict(os.environ, ENV)
    @patch("openhexa.sdk.datasets.dataset.requests.put")
    @patch("openhexa.sdk.datasets.dataset.graphql")
    def test_add_file_upload_headers(self, mock_graphql, mock_put):
        """The upload request must carry the headers the backend generated the signed URL for."""
        cases = [
            # Azure Blob Storage requires the blob type on top of the content type
            (AZURE_HEADERS, AZURE_HEADERS),
            # Backends that do not need specific headers fall back to the content type
            (None, {"Content-Type": "application/octet-stream"}),
        ]

        for returned_headers, expected_headers in cases:
            with self.subTest(headers=returned_headers):
                mock_graphql.side_effect = [upload_url_response(headers=returned_headers), version_file_response()]
                version = DatasetVersion(dataset=None, id="version_id", name="v1", created_at=None)

                version.add_file(StringIO("foo,bar"), filename="file.csv")

                self.assertEqual(mock_put.call_args.args[0], UPLOAD_URL)
                self.assertEqual(mock_put.call_args.kwargs["headers"], expected_headers)

    @patch.dict(os.environ, ENV)
    @patch("openhexa.sdk.datasets.dataset.AZURE_MAX_SINGLE_PUT_SIZE", 8)
    @patch("openhexa.sdk.datasets.dataset.AZURE_BLOCK_SIZE", 4)
    @patch("openhexa.sdk.datasets.dataset.requests.put")
    @patch("openhexa.sdk.datasets.dataset.graphql")
    def test_add_file_too_large_for_a_single_request(self, mock_graphql, mock_put):
        """Content that does not fit in a single request is staged block by block, then committed."""
        mock_graphql.side_effect = [upload_url_response(headers=AZURE_HEADERS), version_file_response()]
        version = DatasetVersion(dataset=None, id="version_id", name="v1", created_at=None)

        version.add_file(BytesIO(b"0123456789"), filename="file.csv")

        block_urls = [f"{UPLOAD_URL}&comp=block&blockid={quote(block_id(i), safe='')}" for i in range(3)]
        self.assertEqual(
            [call.args[0] for call in mock_put.call_args_list],
            [*block_urls, f"{UPLOAD_URL}&comp=blocklist"],
        )
        self.assertEqual([call.kwargs["data"] for call in mock_put.call_args_list[:3]], [b"0123", b"4567", b"89"])

        commit = mock_put.call_args_list[-1]
        self.assertEqual(commit.kwargs["headers"], {"x-ms-blob-content-type": "application/octet-stream"})
        self.assertEqual(
            commit.kwargs["data"],
            '<?xml version="1.0" encoding="utf-8"?><BlockList>'
            f"<Latest>{block_id(0)}</Latest><Latest>{block_id(1)}</Latest><Latest>{block_id(2)}</Latest>"
            "</BlockList>".encode(),
        )

    @patch.dict(os.environ, ENV)
    @patch("openhexa.sdk.datasets.dataset.AZURE_MAX_SINGLE_PUT_SIZE", 2)
    @patch("openhexa.sdk.datasets.dataset.AZURE_BLOCK_SIZE", 4)
    @patch("openhexa.sdk.datasets.dataset.requests.put")
    @patch("openhexa.sdk.datasets.dataset.graphql")
    def test_add_file_signed_url_expired_during_upload(self, mock_graphql, mock_put):
        """A signed URL that expires while blocks are being uploaded is replaced by a fresh one."""
        refreshed_url = UPLOAD_URL.replace("signature", "refreshed_signature")
        mock_graphql.side_effect = [
            upload_url_response(headers=AZURE_HEADERS),
            upload_url_response(refreshed_url, headers=AZURE_HEADERS),
            version_file_response(),
        ]
        expired_response = MagicMock(status_code=403)
        mock_put.side_effect = [expired_response, MagicMock(status_code=201), MagicMock(status_code=201)]
        version = DatasetVersion(dataset=None, id="version_id", name="v1", created_at=None)

        version.add_file(BytesIO(b"0123"), filename="file.csv")

        block_query = f"comp=block&blockid={quote(block_id(0), safe='')}"
        self.assertEqual(
            [call.args[0] for call in mock_put.call_args_list],
            [
                f"{UPLOAD_URL}&{block_query}",
                f"{refreshed_url}&{block_query}",
                # The blocks are then committed through the refreshed URL as well
                f"{refreshed_url}&comp=blocklist",
            ],
        )
        expired_response.raise_for_status.assert_not_called()

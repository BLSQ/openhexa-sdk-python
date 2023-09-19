import os
from unittest import TestCase
from unittest.mock import patch

from openhexa.sdk.datasets import Dataset


class DatasetTest(TestCase):
    @patch.dict(
        os.environ,
        {"HEXA_WORKSPACE": "workspace-slug", "HEXA_TOKEN": "token", "HEXA_SERVER_URL": "server"},
    )
    @patch("openhexa.sdk.datasets.dataset.graphql")
    def test_create_dataset_version(self, mock_graphql):
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

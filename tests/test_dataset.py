import os
import uuid
from datetime import datetime, timezone
from io import BytesIO
from unittest import TestCase
from unittest.mock import patch, PropertyMock
import responses
import pandas as pd

from openhexa.sdk.datasets import Dataset, DatasetFile
from openhexa.sdk.datasets.dataset import DatasetVersion


class DatasetTest(TestCase):
    @patch.dict(
        os.environ,
        {"HEXA_WORKSPACE": "workspace-slug", "HEXA_TOKEN": "token", "HEXA_SERVER_URL": "server"},
    )
    @patch("openhexa.sdk.datasets.dataset.graphql")
    def test_create_dataset_version(self, mock_graphql):
        d = Dataset(
            dataset_id="id",
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
                    "createdAt": "2011-11-04T00:05:23Z",
                },
            }
        }

        v = d.create_version("Second version")
        self.assertEqual(v.id, "<newVersionId>")

    @responses.activate
    def test_dataset_file_read(self):
        responses.add(
            responses.GET,
            "http://download-url",
            body="a,b\r\n17,23",
            status=200,
        )

        dataset = Dataset(dataset_id=str(uuid.uuid4()), slug="dataset", name="My dataset", description="A cool dataset")
        version = DatasetVersion(
            dataset=dataset, version_id=str(uuid.uuid4()), name="v1", created_at=datetime.now(tz=timezone.utc)
        )
        file = DatasetFile(
            version=version,
            file_id=str(uuid.uuid4()),
            uri="some-uri",
            filename="test.csv",
            content_type="text/csv",
            created_at=datetime.now(tz=timezone.utc),
        )

        with patch("openhexa.sdk.datasets.dataset.DatasetFile.download_url", new_callable=PropertyMock) as patched:
            patched.return_value = "http://download-url"
            df = pd.read_csv(BytesIO(file.read()))
            assert len(df) == 1
            assert df.loc[0]["a"] == 17
            assert df.loc[0]["b"] == 23

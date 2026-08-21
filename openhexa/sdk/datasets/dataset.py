"""Dataset-related classes and functions.

See https://github.com/BLSQ/openhexa/wiki/User-manual#datasets and
https://github.com/BLSQ/openhexa/wiki/Using-the-OpenHEXA-SDK#working-with-datasets for more information about datasets.
"""

import base64
import io
import mimetypes
import typing
from os import PathLike
from pathlib import Path
from urllib.parse import quote

import requests

from openhexa.sdk.utils import Iterator, Page, Settings, content_size, graphql, read_content

AZURE_MAX_SINGLE_PUT_SIZE = 5000 * 1024 * 1024  # 5 GiB
AZURE_BLOCK_SIZE = 64 * 1024 * 1024  # 64 MiB to keep memory low


class DatasetFile:
    """Represent a single file within a dataset. Files are attached to dataset through versions."""

    _download_url = None
    version = None

    def __init__(
        self,
        version: any,
        id: str,
        uri: str,
        filename: str,
        content_type: str,
        created_at: str,
    ):
        self.version = version
        self.id = id
        self.uri = uri
        self.filename = filename
        self.content_type = content_type
        self.created_at = created_at

    def read(self):
        """Download the file content and return it."""
        response = requests.get(self.download_url, stream=True, verify=Settings.verify_ssl())
        response.raise_for_status()
        return response.content

    @property
    def download_url(self):
        """Build and return a pre-signed URL for the file."""
        if self._download_url is None:
            response = graphql(
                """
                mutation getDownloadUrl($input: PrepareVersionFileDownloadInput!) {
                    prepareVersionFileDownload(input: $input) {
                        downloadUrl
                        success
                        errors
                    }
                }
            """,
                {"input": {"fileId": self.id}},
            )
            if response["prepareVersionFileDownload"]["success"] is False:
                raise Exception(response["prepareVersionFileDownload"]["errors"])
            self._download_url = response["prepareVersionFileDownload"]["downloadUrl"]
        return self._download_url

    def __repr__(self) -> str:
        """Safe representation of the dataset file."""
        return f"<DatasetFile id={self.id} filename={self.filename}>"


class VersionsIterator(Iterator):
    """Custom iterator class to iterate versions using our GraphQL API."""

    def __init__(self, dataset: any, per_page: int = 10):
        super().__init__(per_page=per_page)

        self.item_to_value = lambda x: DatasetVersion(
            dataset=dataset, id=x["id"], name=x["name"], created_at=x["createdAt"]
        )
        self.dataset = dataset
        self.has_next_page = True

    def _next_page(self):
        if not self.has_next_page:
            return None

        res = graphql(
            """
            query getDatasetVersions($datasetId: ID!, $page: Int!, $perPage: Int) {
                dataset (id: $datasetId) {
                    versions (page: $page, perPage: $perPage) {
                        items {
                            id
                            name
                            createdAt
                        }
                        totalPages
                    }
                }
            }
            """,
            {
                "datasetId": self.dataset.id,
                "page": self.page_number + 1,
                "perPage": self.per_page,
            },
        )
        if res["dataset"] is None:
            raise ValueError(f"Dataset {self.dataset.id} does not exist")

        if res["dataset"]["versions"]["totalPages"] == self.page_number + 1:
            self.has_next_page = False

        return Page(
            parent=self,
            items=res["dataset"]["versions"]["items"],
            item_to_value=self.item_to_value,
        )


class VersionFilesIterator(Iterator):
    """Custom iterator class to iterate version files using our GraphQL API."""

    def __init__(self, version: any, per_page: int = 20):
        super().__init__(per_page=per_page)
        self.item_to_value = lambda x: DatasetFile(
            version=version,
            id=x["id"],
            uri=x["uri"],
            filename=x["filename"],
            content_type=x["contentType"],
            created_at=x["createdAt"],
        )

        self.version = version
        self.has_next_page = True

    def _next_page(self):
        if not self.has_next_page:
            return None

        res = graphql(
            """
            query getDatasetFiles($versionId: ID!, $page: Int!, $perPage: Int) {
                datasetVersion (id: $versionId) {
                    files (page: $page, perPage: $perPage) {
                        items {
                            id
                            uri
                            filename
                            contentType
                            createdAt
                        }
                        totalPages
                    }
                }
            }
            """,
            {
                "versionId": self.version.id,
                "page": self.page_number + 1,
                "perPage": self.per_page,
            },
        )
        if res["datasetVersion"] is None:
            raise ValueError(f"Dataset version {self.version.id} does not exist")

        if res["datasetVersion"]["files"]["totalPages"] == self.page_number + 1:
            self.has_next_page = False

        return Page(
            parent=self,
            items=res["datasetVersion"]["files"]["items"],
            item_to_value=self.item_to_value,
        )


class DatasetVersion:
    """Dataset files are not directly attached to a dataset, but rather to a version."""

    dataset = None

    def __init__(self, dataset: any, id: str, name: str, created_at: str):
        self.id = id
        self.name = name
        self.dataset = dataset
        self.created_at = created_at

    @property
    def files(self):
        """Build and return an iterator of files for this version."""
        if self.id is None:
            raise ValueError("This dataset version does not have an id.")
        return VersionFilesIterator(version=self, per_page=50)

    def get_file(self, filename: str) -> DatasetFile:
        """Get a file by name."""
        data = graphql(
            """
            query getDatasetFile($versionId: ID!, $filename: String!) {
                datasetVersion(id: $versionId) {
                    fileByName(name: $filename) {
                        id
                        uri
                        filename
                        contentType
                        createdAt
                    }
                }
            }
            """,
            {"versionId": self.id, "filename": filename},
        )

        file = data["datasetVersion"]["fileByName"]
        if file is None:
            raise FileExistsError(f"The file {filename} does not exist for version {self}")

        return DatasetFile(
            version=self,
            id=file["id"],
            uri=file["uri"],
            filename=file["filename"],
            content_type=file["contentType"],
            created_at=file["createdAt"],
        )

    def _generate_upload_url(self, filename: str, content_type: str) -> tuple[str, dict]:
        """Ask the backend for a signed upload URL, along with the headers that URL was signed for."""
        data = graphql(
            """
            mutation generateDatasetUploadUrl ($input: GenerateDatasetUploadUrlInput!) {
                generateDatasetUploadUrl(input: $input) {
                    uploadUrl
                    headers
                    success
                    errors
                }
            }
            """,
            {"input": {"versionId": self.id, "contentType": content_type, "uri": filename}},
        )
        result = data["generateDatasetUploadUrl"]
        if result["success"] is False:
            self.raise_upload_exception(result["errors"])

        # The backend tells us which headers the signed URL expects: Azure Blob Storage rejects a "Put Blob"
        # request that does not specify the blob type. Other backends only need the content type.
        return result["uploadUrl"], result["headers"] or {"Content-Type": content_type}

    def _azure_put(self, upload_url: str, query: str, filename: str, content_type: str, **kwargs) -> str:
        """Send a single upload request, and return the URL it was sent to.

        Signed URLs expire after an hour, which a large upload can outlive. When that happens we simply ask
        for a fresh one and try again, hence the URL being returned to the caller.
        """
        response = requests.put(f"{upload_url}&{query}", verify=Settings.verify_ssl(), **kwargs)
        if response.status_code in (401, 403):
            upload_url, _ = self._generate_upload_url(filename, content_type)
            response = requests.put(f"{upload_url}&{query}", verify=Settings.verify_ssl(), **kwargs)
        response.raise_for_status()

        return upload_url

    def _azure_upload_by_blocks(self, content: typing.IO | bytes, upload_url: str, filename: str, content_type: str):
        """Upload content to Azure Blob Storage block by block, then commit the blocks as a single blob.

        See https://learn.microsoft.com/en-us/rest/api/storageservices/put-block
        """
        if isinstance(content, bytes):
            content = io.BytesIO(content)

        block_ids = []
        while block := content.read(AZURE_BLOCK_SIZE):
            if isinstance(block, str):
                block = block.encode()
            # Block ids must be unique within the blob and share the same length once decoded
            block_id = base64.b64encode(f"{len(block_ids):032d}".encode()).decode()
            upload_url = self._azure_put(
                upload_url,
                f"comp=block&blockid={quote(block_id, safe='')}",
                filename,
                content_type,
                data=block,
            )
            block_ids.append(block_id)

        blocks = "".join(f"<Latest>{block_id}</Latest>" for block_id in block_ids)
        self._azure_put(
            upload_url,
            "comp=blocklist",
            filename,
            content_type,
            data=f'<?xml version="1.0" encoding="utf-8"?><BlockList>{blocks}</BlockList>'.encode(),
            # The content type of the blob itself, as opposed to the content type of this request
            headers={"x-ms-blob-content-type": content_type},
        )

    def add_file(
        self,
        source: str | PathLike[str] | typing.IO | bytes,
        filename: str | None = None,
    ) -> DatasetFile:
        """Create a new dataset file and add it to the dataset version."""
        mime_type = None
        if isinstance(source, (str | PathLike)):
            path = Path(source)
            filename = path.name if filename is None else filename
            mime_type, _ = mimetypes.guess_type(path)
        else:
            if filename is None:
                raise ValueError("A file name is required when you pass a buffer")

        if mime_type is None:
            mime_type = "application/octet-stream"

        upload_url, headers = self._generate_upload_url(filename, mime_type)
        with read_content(source) as content:
            size = content_size(content)
            # upload block by block for very large files (>5GiB) when on Azure
            if headers.get("x-ms-blob-type") and (size is None or size > AZURE_MAX_SINGLE_PUT_SIZE):
                self._azure_upload_by_blocks(content, upload_url, filename, mime_type)
            else:
                response = requests.put(upload_url, data=content, headers=headers, verify=Settings.verify_ssl())
                response.raise_for_status()

        data = graphql(
            """
                mutation CreateDatasetVersionFile ($input: CreateDatasetVersionFileInput!) {
                    createDatasetVersionFile(input: $input) {
                        file {
                            id
                            filename
                            uri
                            contentType
                            createdAt
                        }
                        success
                        errors
                    }
                }
        """,
            {
                "input": {
                    "versionId": self.id,
                    "contentType": mime_type,
                    "uri": filename,
                }
            },
        )

        if data["createDatasetVersionFile"]["success"] is False:
            errors = data["createDatasetVersionFile"]["errors"]
            self.raise_dataset_file_creation_exception(errors)
        result = data["createDatasetVersionFile"]

        return DatasetFile(
            version=self,
            id=result["file"]["id"],
            filename=result["file"]["filename"],
            content_type=result["file"]["contentType"],
            uri=result["file"]["uri"],
            created_at=result["file"]["createdAt"],
        )

    def exists(self, objectKey: str):
        """
        Check if an object with the specified key exists.

        This method checks if an object identified by `objectKey` exists in the dataset.

        Args:
            objectKey (str): The key of the object to check for existence.

        Returns
        -------
            bool: True if the object exists, False otherwise.
        """
        data = graphql(
            """
            query getDatasetFile($versionId: ID!, $filename: String!) {
                datasetVersion(id: $versionId) {
                    fileByName(name: $filename) {
                        id
                        uri
                        filename
                        contentType
                        createdAt
                    }
                }
            }
            """,
            {"versionId": self.id, "filename": objectKey},
        )

        return data["datasetVersion"]["fileByName"] is not None

    def raise_upload_exception(self, errors):
        """Raise an exception if an error occurs on upload."""
        if "LOCKED_VERSION" in errors:
            raise ValueError("This dataset version is locked. You can only add files to the latest version")
        elif "ALREADY_EXISTS" in errors:
            raise ValueError("A file with this name already exists in this dataset version")
        else:
            raise Exception(errors)

    def raise_dataset_file_creation_exception(self, errors):
        """Raise an exception if an error occurs on upload."""
        if "LOCKED_VERSION" in errors:
            raise ValueError("This dataset version is locked. You can only add files to the latest version")
        elif "PERMISSION_DENIED" in errors:
            raise ValueError("You do not have permission to add files to this dataset version")
        elif "ALREADY_EXISTS" in errors:
            raise ValueError("A file with this name already exists in this dataset version")
        else:
            raise Exception(errors)


class Dataset:
    """Datasets are versioned, documented files.

    See https://github.com/BLSQ/openhexa/wiki/Using-the-OpenHEXA-SDK#working-with-datasets for more information.
    """

    _latest_version = None

    def __init__(
        self,
        id: str,
        slug: str,
        name: str,
        description: str,
        source_workspace_slug: str = None,
    ):
        self.id = id
        self.slug = slug
        self.name = name
        self.description = description
        self.source_workspace_slug = source_workspace_slug

    def create_version(self, name: typing.Any) -> DatasetVersion:
        """Build a dataset version, save it and return it."""
        response = graphql(
            """
            mutation createDatasetVersion($input: CreateDatasetVersionInput!) {
                createDatasetVersion(input: $input) {
                    version {
                        id
                        name
                        description
                        createdAt
                    }
                    errors
                    success
                }
            }
        """,
            {
                "input": {
                    "datasetId": self.id,
                    "name": str(name),
                }
            },
        )
        data = response["createDatasetVersion"]
        if data["success"] is False:
            if "DUPLICATE_NAME" in data["errors"]:
                raise ValueError("A dataset version with this name already exists")
            raise Exception(data["errors"])

        version = data["version"]
        self._latest_version = DatasetVersion(
            dataset=self,
            id=version["id"],
            name=version["name"],
            created_at=version["createdAt"],
        )

        return self.latest_version

    @property
    def latest_version(self) -> DatasetVersion | None:
        """Return the latest version, if any.

        This property method will query the backend to try to fetch the latest version.
        """
        if self._latest_version is None:
            data = graphql(
                """
                query getLatestVersion($datasetId: ID!) {
                    dataset(id: $datasetId) {
                        latestVersion {
                            id
                            name
                            createdAt
                        }
                    }
                }
            """,
                {"datasetId": self.id},
            )

            if data["dataset"]["latestVersion"] is None:
                self._latest_version = None
            else:
                self._latest_version = DatasetVersion(
                    dataset=self,
                    id=data["dataset"]["latestVersion"]["id"],
                    name=data["dataset"]["latestVersion"]["name"],
                    created_at=data["dataset"]["latestVersion"]["createdAt"],
                )

        return self._latest_version

    @property
    def versions(self) -> VersionsIterator:
        """Build and return an iterator for versions."""
        return VersionsIterator(dataset=self, per_page=10)

    def __repr__(self) -> str:
        """Safe representation of the dataset."""
        return f"<Dataset slug={self.slug} id={self.id} source_workspace_slug={self.source_workspace_slug}>"


class FileNotFound(Exception):
    """Raised whenever an attempt is made to get a file that does not exist."""

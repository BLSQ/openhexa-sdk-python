"""Miscellaneous utility functions."""

import abc
import contextlib
import enum
import os
import typing

from openhexa.graphql import BaseOpenHexaClient
from openhexa.utils import create_requests_session


class Settings:
    """Centralized settings for the OpenHexa SDK."""

    @staticmethod
    def verify_ssl() -> bool:
        """Return the SSL verification flag from environment variables."""
        return os.getenv("HEXA_VERIFY_SSL", "True").lower() not in ("0", "false")

    @staticmethod
    def debug() -> bool:
        """Return the debug flag from environment variables."""
        return bool(os.getenv("DEBUG") or os.getenv("HEXA_DEBUG"))


class Environment(enum.Enum):
    """Enumeration of supported runtime environments."""

    LOCAL_PIPELINE = "LOCAL_PIPELINE"
    CLOUD_PIPELINE = "CLOUD_PIPELINE"
    CLOUD_JUPYTER = "CLOUD_JUPYTER"
    STANDALONE = "STANDALONE"


def get_environment():
    """Get the environment from the HEXA_ENVIRONMENT (see Environment enum)."""
    env = os.environ.get("HEXA_ENVIRONMENT", "STANDALONE").upper()

    try:
        return Environment[env]
    except KeyError:
        raise ValueError(f"Invalid environment: {env}")


def graphql(operation: str, variables: dict[str | typing.Any] | None = None) -> dict[str | typing.Any]:
    """Performa GraphQL query."""
    auth_token = os.environ[
        "HEXA_TOKEN"
    ]  # Works for notebooks with the membership token and pipelines with the run token
    headers = {"Authorization": f"Bearer {auth_token}"}
    session = create_requests_session(verify=Settings.verify_ssl())

    req = session.post(
        f"{os.environ['HEXA_SERVER_URL'].rstrip('/')}/graphql/",
        headers=headers,
        json={
            "query": operation,
            "variables": variables if variables is not None else {},
        },
    )
    req.raise_for_status()
    body = req.json()
    if "errors" in body:
        raise Exception(body["errors"])

    return body["data"]


class OpenHexaClient(BaseOpenHexaClient):
    """OpenHexaClient is a class that provides methods to interact with the OpenHexa GraphQL API."""

    def __init__(self, token: str | None = None, server_url: str | None = None):
        """Initialize the OpenHexaClient with the OpenHexa API URL and headers.

        Args:
            token: Authentication token. If not provided, will use HEXA_TOKEN environment variable.
            server_url: Server URL. If not provided, will use HEXA_SERVER_URL environment variable.
        """
        url = server_url or f"{os.environ['HEXA_SERVER_URL'].rstrip('/')}/graphql/"
        token = token or os.getenv("HEXA_TOKEN")

        super().__init__(url=url, token=token, verify=Settings.verify_ssl())


class Iterator(metaclass=abc.ABCMeta):
    """A generic class for iterating through API list responses."""

    def __init__(
        self,
        item_to_value=lambda x: x,
        per_page=None,
    ):
        self._started = False
        self.__active_iterator = None

        self.item_to_value = item_to_value
        """Callable[Iterator, Any]: Callable to convert an item from the type
            in the raw API response into the native object. Will be called with
            the iterator and a
            single item.
        """
        self.per_page = per_page

        # The attributes below will change over the life of the iterator.
        self.page_number = 0
        """int: The current page of results."""
        self.num_results = 0
        """int: The total number of results fetched so far."""

    def _items_iter(self):
        for page in self._page_iter(increment=False):
            for item in page:
                self.num_results += 1
                yield item

    def __iter__(self) -> typing.Generator[typing.Any, None, None]:
        """Implement __iter()."""
        if self._started:
            raise ValueError("Iterator has already started", self)
        self._started = True

        return self._items_iter()

    def __next__(self):
        """Implement next()."""
        if self.__active_iterator is None:
            self.__active_iterator = iter(self)

        return next(self.__active_iterator)

    def _page_iter(self, increment: bool):
        """Generate pages of API responses.

        Parameters
        ----------
        increment : bool
            Flag indicating if the total number of results should be incremented on each page.
            This is useful since a page iterator will want to increment by results per page while an
            items iterator will want to increment per item.
        """
        page = self._next_page()
        while page is not None:
            self.page_number += 1
            if increment:
                self.num_results += page.num_items
            yield page
            page = self._next_page()

    @abc.abstractmethod
    def _next_page(self):
        """Get the next page in the iterator.

        This does nothing and is intended to be over-ridden by subclasses
        to return the next :class:`Page`.

        Raises
        ------
            NotImplementedError: Always, this method is abstract.
        """
        raise NotImplementedError


class Page:
    """Single page of results in an iterator.

    Parameters
    ----------
    parent : Iterator
        The iterator that owns the current page.
    items: Sequence[Any]
        An iterable (that also defines __len__) of items from a raw API response.
    item_to_value: Callable[dict[str, Any], Any]:
        Callable to convert an item from the type in the raw API response into the native object.
        Will be called with the iterator and a single item.
    """

    def __init__(self, parent, items, item_to_value):
        self._parent = parent
        self._num_items = len(items)
        self._remaining = self._num_items
        self._item_iter = iter(items)
        self._item_to_value = item_to_value

    @property
    def num_items(self):
        """int: Total items in the page."""
        return self._num_items

    @property
    def remaining(self):
        """int: Remaining items in the page."""
        return self._remaining

    def __iter__(self):
        """Implement __iter__()."""
        return self

    def __next__(self):
        """Get the next value in the page."""
        item = next(self._item_iter)
        result = self._item_to_value(item)
        # Since we've successfully got the next value from the
        # iterator, we update the number of remaining.
        self._remaining -= 1
        return result


@contextlib.contextmanager
def read_content(source: str | os.PathLike[str] | typing.IO | bytes):
    """Read file content and return it as bytes."""
    try:
        if isinstance(source, bytes):
            yield source
        elif hasattr(source, "read"):
            yield source
        # If source is a string or PathLike object
        elif isinstance(source, (str | os.PathLike)):
            with open(os.fspath(source), "rb") as f:
                yield f

        else:
            raise ValueError("Unsupported type for source")
    finally:
        if hasattr(source, "close"):
            source.close()

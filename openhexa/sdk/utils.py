import abc
import enum
import os
import typing

import requests


class Environments(enum.Enum):
    LOCAL_PIPELINE = "LOCAL_PIPELINE"
    CLOUD_PIPELINE = "CLOUD_PIPELINE"
    CLOUD_JUPYTER = "CLOUD_JUPYTER"
    STANDALONE = "STANDALONE"


def get_environment():
    env = os.environ.get("HEXA_ENVIRONMENT", "STANDALONE").upper()
    if env not in Environments.__members__:
        raise ValueError(f"Invalid environment: {env}")
    return Environments[env]


def graphql(operation: str, variables: typing.Optional[typing.Dict[str, typing.Any]] = None):
    auth_token = os.environ[
        "HEXA_TOKEN"
    ]  # Works for notebooks with the membership token and pipelines with the run token
    headers = {"Authorization": f"Bearer {auth_token}"}

    req = requests.post(
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


class Iterator(object, metaclass=abc.ABCMeta):
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
        """Iterator for each item returned."""
        for page in self._page_iter(increment=False):
            for item in page:
                self.num_results += 1
                yield item

    def __iter__(self):
        """Iterator for each item returned.

        Returns:
            types.GeneratorType[Any]: A generator of items from the API.

        Raises:
            ValueError: If the iterator has already been started.
        """
        if self._started:
            raise ValueError("Iterator has already started", self)
        self._started = True
        return self._items_iter()

    def __next__(self):
        if self.__active_iterator is None:
            self.__active_iterator = iter(self)
        return next(self.__active_iterator)

    def _page_iter(self, increment):
        """Generator of pages of API responses.

        Args:
            increment (bool): Flag indicating if the total number of results
                should be incremented on each page. This is useful since a page
                iterator will want to increment by results per page while an
                items iterator will want to increment per item.

        Yields:
            Page: each page of items from the API.
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

        Raises:
            NotImplementedError: Always, this method is abstract.
        """
        raise NotImplementedError


class Page(object):
    """Single page of results in an iterator.

    Args:
        parent (Iterator): The iterator that owns
            the current page.
        items (Sequence[Any]): An iterable (that also defines __len__) of items
            from a raw API response.
        item_to_value (Callable[google.api_core.page_iterator.Iterator, Any]):
            Callable to convert an item from the type in the raw API response
            into the native object. Will be called with the iterator and a
            single item.
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
        """The :class:`Page` is an iterator of items."""
        return self

    def __next__(self):
        """Get the next value in the page."""
        item = next(self._item_iter)
        result = self._item_to_value(item)
        # Since we've successfully got the next value from the
        # iterator, we update the number of remaining.
        self._remaining -= 1
        return result


def read_content(source: typing.Union[str, os.PathLike[str], typing.IO], encoding: str = "utf-8") -> str:
    # If source is a string or PathLike object
    if isinstance(source, (str, os.PathLike)):
        with open(os.fspath(source), "rb") as f:
            return f.read()

    # If source is a buffer
    elif hasattr(source, "read"):
        return source.read().encode(encoding)

    raise ValueError("Unsupported type for source")

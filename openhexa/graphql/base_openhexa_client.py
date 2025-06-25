"""OpenHexaClient implementation for GraphQL API interaction."""

import logging
from importlib.metadata import version

from openhexa.graphql.graphql_client import Client


class BaseOpenHexaClient(Client):
    """OpenHexaClient is a class that provides methods to interact with the OpenHexa GraphQL API."""

    def __init__(self, url: str, token: str):
        """Initialize the OpenHexaClient with the OpenHexa API URL and headers.

        Args:
            url: GraphQL API URL.
            token: Authentication token.
        """
        self.token = token
        super().__init__(
            url=url,
            headers={
                "User-Agent": f"openhexa-sdk/{version('openhexa.sdk')}",
                "Authorization": f"Bearer {self.token}",
            },
        )
        logging.getLogger("httpx").setLevel(
            logging.WARNING
        )  # HTTPX logs queries by default, we disable them here with WARNING level

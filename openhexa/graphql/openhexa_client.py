"""OpenHexaClient is a class that provides methods to interact with the OpenHexa GraphQL API."""
import logging
from datetime import datetime
from pathlib import Path

import click
import requests
from graphql import build_client_schema, build_schema, get_introspection_query
from graphql.utilities import find_breaking_changes

from openhexa.cli.settings import settings
from openhexa.graphql.graphql_client import Client
from openhexa.utils import create_requests_session


class APIError(Exception):
    """Raised when an error occurs while interacting with the API."""

    pass


class InvalidTokenError(APIError):
    """Raised when the token is invalid."""

    pass


class GraphQLError(APIError):
    """Raised when a GraphQL request returns an error."""

    pass


class OpenHexaClient(Client):
    """OpenHexaClient is a class that provides methods to interact with the OpenHexa GraphQL API."""

    def __init__(self, *, api_url: str, token: str):
        """Initialize the OpenHexaClient with the OpenHexa API URL and headers."""
        self._url = settings.api_url + "/graphql/"
        self._token = token or settings.access_token

        if not self._token:
            raise InvalidTokenError("No token found for workspace")

        super().__init__(url=self._url, headers={})
        logging.getLogger("httpx").setLevel(
            logging.WARNING
        )  # HTTPX logs queries by default, we disable them here with WARNING level

    def execute(self, query, **kwargs):
        """Decorate parent execute method to log the GraphQL query  and response."""
        from openhexa.version import __version__

        self.headers["User-Agent"] = f"openhexa-cli/{__version__}"
        self.headers["Authorization"] = f"Bearer {self._token}"

        _detect_graphql_breaking_changes(token=self._token)

        if settings.debug:
            click.echo("")
            click.echo("Graphql Query:")
            click.echo(f"URL: {self.url}")
            click.echo(f"Query: {query}")
            variables = kwargs.get("variables", {})
            click.echo(f"Variables: {variables}")

        response = super().execute(query=query, **kwargs)

        if settings.debug:
            click.echo("")
            click.echo("Graphql Response:")
            click.echo(f"Response: {response}")

        return response


def _detect_graphql_breaking_changes_if_needed(token):
    """Detect breaking changes if not done recently between the schema referenced in the SDK and the server using graphql-core."""
    ONE_HOUR = 60 * 60
    now_timestamp = int(datetime.now().timestamp())
    if not settings.last_breaking_change_check or now_timestamp - settings.last_breaking_change_check > ONE_HOUR:
        _detect_graphql_breaking_changes(token)
        settings.last_breaking_change_check = now_timestamp


def _detect_graphql_breaking_changes(token):
    """Detect breaking changes between the schema referenced in the SDK and the server using graphql-core."""
    stored_schema_obj = build_schema((Path(__file__).parent / "graphql" / "schema.generated.graphql").open().read())
    server_schema_obj = build_client_schema(
        _query_graphql(get_introspection_query(input_value_deprecation=True), token=token)
    )

    breaking_changes = find_breaking_changes(stored_schema_obj, server_schema_obj)
    if breaking_changes:
        current_version, latest_version = get_library_versions()
        click.secho(
            f"⚠️ Breaking changes detected between the SDK (version {current_version}) and the server:",
            fg="red",
        )
        for change in breaking_changes:
            click.secho(f"- {change.description}", fg="yellow")
        click.secho(
            "This could lead to unexpected results.\n"
            f"Please update the SDK to the latest version {latest_version} "
            f"(using `pip install openhexa-sdk=={latest_version}`) or use a version of the SDK compatible with the server.",
            fg="red",
        )


def graphql(query: str, variables=None, token=None):
    """Check that there is no breaking change and perform a GraphQL request."""
    _detect_graphql_breaking_changes_if_needed(token)
    return _query_graphql(query, variables, token)


def _query_graphql(query: str, variables=None, token=None):
    """Perform a GraphQL request."""
    from openhexa.version import __version__

    url = settings.api_url + "/graphql/"
    if token is None:
        token = settings.access_token

    if token is None:
        raise InvalidTokenError("No token found for workspace")

    if settings.debug:
        click.echo("")
        click.echo("Graphql Query:")
        click.echo(f"URL: {url}")
        click.echo(f"Query: {query}")
        click.echo(f"Variables: {variables}")

    session = create_requests_session()

    response = session.post(
        url,
        headers={
            "User-Agent": f"openhexa-cli/{__version__}",
            "Authorization": f"Bearer {token}",
        },
        json={"query": query, "variables": variables},
    )
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise GraphQLError(str(e))

    data = response.json()

    if settings.debug:
        click.echo("Graphql Response:")
        click.echo(data)
        click.echo("")

    if data.get("errors"):
        if data.get("errors")[0].get("extensions", {}).get("code") == "UNAUTHENTICATED":
            raise InvalidTokenError
        raise GraphQLError(data["errors"])
    return data["data"]


def get_library_versions() -> tuple[str, str]:
    """Return the current version and the one on PyPi."""
    # Get the currently installed version
    from openhexa.version import __version__ as installed_version

    # Get the latest version available on PyPI
    try:
        response = requests.get("https://pypi.org/pypi/openhexa.sdk/json")
        latest_version = response.json()["info"]["version"]
        return installed_version, latest_version
    except requests.RequestException:
        logging.error(
            "Could not check for the latest version of the openhexa.sdk package.",
            exc_info=True,
        )
        return installed_version, installed_version

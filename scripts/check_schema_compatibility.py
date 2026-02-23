#!/usr/bin/env python
"""
Check for breaking changes between the SDK's bundled GraphQL schema and the production server schema.

Exits with code 1 when breaking changes are found. Emits ::warning:: annotations when running
in GitHub Actions so breaking changes are visible in the PR.
"""

import os
import sys
from pathlib import Path

import requests
from graphql import build_client_schema, build_schema, get_introspection_query
from graphql.utilities import find_breaking_changes

from openhexa.graphql import BUNDLED_SCHEMA_PATH

GITHUB_ACTIONS = os.getenv("GITHUB_ACTIONS") == "true"
REPO_ROOT = Path(__file__).parent.parent
SCHEMA_RELATIVE_PATH = BUNDLED_SCHEMA_PATH.relative_to(REPO_ROOT)

PRODUCTION_URL = "https://api.openhexa.org"


def fetch_server_schema(graphql_url: str):
    """Fetch the live GraphQL schema from the server via introspection."""
    response = requests.post(
        graphql_url,
        json={"query": get_introspection_query(input_value_deprecation=True)},
        timeout=30,
    )
    response.raise_for_status()
    body = response.json()
    if "errors" in body:
        raise RuntimeError(f"Introspection query returned errors: {body['errors']}")
    return build_client_schema(body["data"])


def main():
    """Execute main function."""
    stored_schema = build_schema(BUNDLED_SCHEMA_PATH.read_text())
    server_schema = fetch_server_schema(f"{PRODUCTION_URL}/graphql/")

    breaking_changes = find_breaking_changes(stored_schema, server_schema)
    if breaking_changes:
        print(f"⚠️  {len(breaking_changes)} breaking change(s) detected:")
        for change in breaking_changes:
            print(f"  - {change.description}")
            if GITHUB_ACTIONS:
                print(
                    f"::warning file={SCHEMA_RELATIVE_PATH},line=1,title=GraphQL schema breaking change ({PRODUCTION_URL})::{change.description}"
                )
        print(
            "\nThe server schema has diverged from openhexa/graphql/schema.generated.graphql."
            "\nUpdate the bundled schema by copying the latest schema from the OpenHEXA monorepo"
            " and re-running: python -m ariadne_codegen"
        )
        sys.exit(1)
    else:
        print("✅ No breaking changes detected.")


if __name__ == "__main__":
    main()

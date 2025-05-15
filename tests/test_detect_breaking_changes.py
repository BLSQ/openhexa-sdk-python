import time
from unittest import TestCase, mock

from openhexa.cli.api import detect_graphql_breaking_changes, graphql


class TestGraphQLFunctions(TestCase):
    @mock.patch("openhexa.cli.api._query_graphql")
    @mock.patch("openhexa.cli.api.get_library_versions")
    def test_detect_graphql_breaking_changes_with_mocked_server_schema(
        self, mock_get_library_versions, mock_query_graphql
    ):
        """Test detect_graphql_breaking_changes with a mocked server schema."""
        mock_get_library_versions.return_value = ["1.2.3", "1000.1.2"]
        mock_query_graphql.return_value = {
            "__schema": {
                "queryType": {"name": "Query"},
                "mutationType": None,
                "subscriptionType": None,
                "types": [
                    {
                        "kind": "OBJECT",
                        "name": "Query",
                        "fields": [
                            {
                                "name": "testField",
                                "args": [],
                                "type": {"kind": "SCALAR", "name": "String"},
                                "isDeprecated": False,
                                "deprecationReason": None,
                            }
                        ],
                        "interfaces": [],
                    },
                    {
                        "kind": "SCALAR",
                        "name": "String",
                    },
                ],
                "directives": [],
            }
        }
        stored_schema = """
        type Query {
            testField: Int
        }
        """
        with mock.patch("pathlib.Path.open", mock.mock_open(read_data=stored_schema)):
            with mock.patch("click.secho") as mock_click_secho:
                detect_graphql_breaking_changes("test_token")
                mock_click_secho.assert_any_call(
                    "⚠️ Breaking changes detected between the SDK (version 1.2.3) and the server:", fg="red"
                )
                mock_click_secho.assert_any_call("- Query.testField changed type from Int to String.", fg="yellow")

    @mock.patch("openhexa.cli.api._query_graphql")
    @mock.patch("openhexa.cli.api.update_last_checked")
    @mock.patch("openhexa.cli.api.detect_graphql_breaking_changes")
    @mock.patch("openhexa.cli.api.get_last_checked")
    def test_graphql(self, mock_get_last_checked, mock_detect_changes, mock_update_last_checked, mock_query_graphql):
        """Test that the graphql function is caching the breaking change detection for 1 hour."""
        mock_get_last_checked.return_value = time.time() - 59 * 60  # Last checked 59 minutes ago
        mock_query_graphql.return_value = {"data": "response"}

        response = graphql("query", token="test_token")
        mock_detect_changes.assert_not_called()
        mock_update_last_checked.assert_not_called()
        mock_query_graphql.assert_called_once_with("query", None, "test_token")
        self.assertEqual(response, {"data": "response"})

        mock_get_last_checked.return_value = time.time() - 3600  # Last checked 1 hour ago
        response = graphql("query", token="test_token")
        mock_detect_changes.assert_called_once_with("test_token")
        mock_update_last_checked.assert_called_once()
        self.assertEqual(response, {"data": "response"})

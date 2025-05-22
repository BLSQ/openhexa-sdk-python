import time
from unittest import TestCase, mock

from openhexa.cli.api import _detect_graphql_breaking_changes, graphql


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
                _detect_graphql_breaking_changes("test_token")
                mock_click_secho.assert_any_call(
                    "⚠️ Breaking changes detected between the SDK (version 1.2.3) and the server:", fg="red"
                )
                mock_click_secho.assert_any_call("- Query.testField changed type from Int to String.", fg="yellow")

    @mock.patch("openhexa.cli.api._query_graphql")
    @mock.patch("openhexa.cli.api._detect_graphql_breaking_changes")
    def test_graphql(self, mock_detect_graphql_breaking_changes, mock_query_graphql):
        """Test that the graphql function is caching the breaking change detection for 1 hour."""
        with mock.patch("openhexa.cli.api.settings") as mock_settings:
            mock_settings.last_breaking_change_check = time.time() - 59 * 60  # Last checked 59 minutes ago
            mock_query_graphql.return_value = {"data": "response"}

            response = graphql("query", token="test_token")
            mock_detect_graphql_breaking_changes.assert_not_called()
            mock_query_graphql.assert_called_once_with("query", None, "test_token")
            self.assertEqual(response, {"data": "response"})

            time_in_the_past = time.time() - 61 * 60  # Last checked 61 minutes ago
            mock_settings.last_breaking_change_check = time_in_the_past

            response = graphql("query", token="test_token")
            mock_detect_graphql_breaking_changes.assert_called_once_with("test_token")
            self.assertGreater(mock_settings.last_breaking_change_check, time_in_the_past)
            self.assertEqual(response, {"data": "response"})

from unittest import TestCase, mock

from openhexa.cli.api import detect_graphql_breaking_changes


class TestGraphQLFunctions(TestCase):
    @mock.patch("openhexa.cli.api.graphql")
    @mock.patch("openhexa.cli.api.get_library_versions")
    def test_detect_graphql_breaking_changes_with_mocked_server_schema(self, mock_get_library_versions, mock_graphql):
        """Test detect_graphql_breaking_changes with a mocked server schema."""
        mock_get_library_versions.return_value = ["1.2.3", "1000.1.2"]
        mock_graphql.return_value = {
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
                detect_graphql_breaking_changes()
                mock_click_secho.assert_any_call(
                    "⚠️ Breaking changes detected between the SDK (version 1.2.3) and the server:", fg="red"
                )
                mock_click_secho.assert_any_call("- Query.testField changed type from Int to String.", fg="yellow")

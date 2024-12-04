from unittest.mock import ANY, patch

from openhexa.sdk.pipelines.run import CurrentRun, LogLevel


@patch.object(CurrentRun, "_connected", True)
@patch("openhexa.sdk.pipelines.run.graphql")
def test_default_log_level(mock_graphql):
    current_run = CurrentRun()

    current_run.log_debug("This is a debug message")
    current_run.log_info("This is an info message")

    assert mock_graphql.call_count == 1
    mock_graphql.assert_any_call(ANY, {"input": {"priority": "INFO", "message": "This is an info message"}})


@patch.object(CurrentRun, "_connected", True)
@patch("openhexa.sdk.pipelines.run.graphql")
def test_filtering_log_messages_based_on_settings(mock_graphql, settings):
    settings.log_level = LogLevel.ERROR
    current_run = CurrentRun()

    current_run.log_warning("This is a warning message")
    current_run.log_error("This is an error message")
    current_run.log_critical("This is a critical message")

    assert mock_graphql.call_count == 2
    mock_graphql.assert_any_call(ANY, {"input": {"priority": "ERROR", "message": "This is an error message"}})
    mock_graphql.assert_any_call(ANY, {"input": {"priority": "CRITICAL", "message": "This is a critical message"}})

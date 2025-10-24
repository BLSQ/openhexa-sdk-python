"""Heartbeat test module."""

import time
from unittest.mock import Mock, patch

from openhexa.sdk.pipelines.heartbeat import HeartbeatThread, heartbeat_manager
from openhexa.sdk.pipelines.run import CurrentRun


@patch("openhexa.sdk.pipelines.heartbeat.OpenHexaClient")
def test_heartbeat_handles_exceptions(mock_client_class):
    """Test that heartbeat thread continues running despite exceptions."""
    mock_run_context = Mock(spec=CurrentRun)
    mock_client_class.side_effect = Exception("Network error")

    thread = HeartbeatThread(mock_run_context, interval=0.1)
    thread.start()
    time.sleep(0.25)
    thread.stop()
    thread.join(timeout=1)

    assert mock_client_class.call_count >= 2


@patch("openhexa.sdk.pipelines.heartbeat.OpenHexaClient")
def test_heartbeat_thread_runs_periodically(mock_client_class):
    """Test that heartbeat thread sends heartbeats periodically."""
    mock_run_context = Mock(spec=CurrentRun)
    mock_client_instance = Mock()
    mock_result = Mock(success=True, errors=[])
    mock_client_instance.update_pipeline_heartbeat.return_value = mock_result
    mock_client_class.return_value = mock_client_instance

    thread = HeartbeatThread(mock_run_context, interval=0.1)
    thread.start()
    time.sleep(0.35)
    thread.stop()
    thread.join(timeout=1)

    assert mock_client_instance.update_pipeline_heartbeat.call_count >= 2


@patch.object(CurrentRun, "_connected", True)
@patch("openhexa.sdk.pipelines.heartbeat.OpenHexaClient")
def test_heartbeat_manager_lifecycle(mock_client_class):
    """Test that heartbeat_manager starts and stops thread correctly."""
    mock_run_context = Mock(spec=CurrentRun)
    mock_run_context._connected = True
    mock_client_instance = Mock()
    mock_result = Mock(success=True, errors=[])
    mock_client_instance.update_pipeline_heartbeat.return_value = mock_result
    mock_client_class.return_value = mock_client_instance

    with heartbeat_manager(mock_run_context, interval=0.1) as thread:
        assert thread is not None
        assert thread.is_alive()

    assert not thread.is_alive()


@patch.object(CurrentRun, "_connected", False)
def test_heartbeat_manager_skips_when_not_connected():
    """Test that heartbeat_manager does nothing when not connected."""
    mock_run_context = Mock(spec=CurrentRun)
    mock_run_context._connected = False

    with heartbeat_manager(mock_run_context, interval=30) as thread:
        assert thread is None

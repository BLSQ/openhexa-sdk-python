"""Heartbeat test module."""

import time
from unittest.mock import MagicMock, Mock, patch

import pytest

from openhexa.sdk.pipelines.heartbeat import HeartbeatThread, heartbeat_manager
from openhexa.sdk.pipelines.run import CurrentRun


class TestHeartbeatThread:
    """Test suite for HeartbeatThread class."""

    def test_heartbeat_thread_initialization(self):
        """Test HeartbeatThread is initialized correctly."""
        mock_run_context = Mock(spec=CurrentRun)
        thread = HeartbeatThread(mock_run_context, interval=5)

        assert thread.run_context == mock_run_context
        assert thread.interval == 5
        assert thread.daemon is True
        assert thread.name == "PipelineHeartbeat"
        assert not thread.stop_event.is_set()

    @patch("openhexa.sdk.pipelines.heartbeat.graphql")
    def test_heartbeat_sends_graphql_mutation(self, mock_graphql):
        """Test that _send_heartbeat calls GraphQL mutation correctly."""
        mock_run_context = Mock(spec=CurrentRun)
        mock_graphql.return_value = {"data": {"updatePipelineHeartbeat": {"success": True, "errors": []}}}

        thread = HeartbeatThread(mock_run_context, interval=30)
        thread._send_heartbeat()

        # Verify GraphQL was called with correct mutation
        mock_graphql.assert_called_once()
        args, kwargs = mock_graphql.call_args
        mutation = args[0]
        variables = args[1]

        assert "updatePipelineHeartbeat" in mutation
        assert "UpdatePipelineHeartbeatInput" in mutation
        assert variables == {"input": {}}

    @patch("openhexa.sdk.pipelines.heartbeat.graphql")
    def test_heartbeat_handles_graphql_errors(self, mock_graphql):
        """Test that heartbeat handles GraphQL errors gracefully."""
        mock_run_context = Mock(spec=CurrentRun)
        mock_graphql.return_value = {
            "data": {
                "updatePipelineHeartbeat": {
                    "success": False,
                    "errors": ["PIPELINE_NOT_FOUND"],
                }
            }
        }

        thread = HeartbeatThread(mock_run_context, interval=30)
        # Should not raise exception
        thread._send_heartbeat()

        mock_graphql.assert_called_once()

    @patch("openhexa.sdk.pipelines.heartbeat.graphql")
    def test_heartbeat_handles_exceptions(self, mock_graphql):
        """Test that heartbeat handles exceptions without crashing."""
        mock_run_context = Mock(spec=CurrentRun)
        mock_graphql.side_effect = Exception("Network error")

        thread = HeartbeatThread(mock_run_context, interval=30)
        # Should not raise exception
        thread._send_heartbeat()

        mock_graphql.assert_called_once()

    @patch("openhexa.sdk.pipelines.heartbeat.graphql")
    def test_heartbeat_thread_runs_periodically(self, mock_graphql):
        """Test that heartbeat thread sends heartbeats periodically."""
        mock_run_context = Mock(spec=CurrentRun)
        mock_graphql.return_value = {"data": {"updatePipelineHeartbeat": {"success": True, "errors": []}}}

        thread = HeartbeatThread(mock_run_context, interval=0.1)  # 100ms for fast test
        thread.start()

        # Wait for multiple heartbeats
        time.sleep(0.35)  # Should send ~3 heartbeats
        thread.stop()
        thread.join(timeout=1)

        # Verify multiple calls were made
        assert mock_graphql.call_count >= 2

    def test_heartbeat_thread_stops_gracefully(self):
        """Test that heartbeat thread stops when stop() is called."""
        mock_run_context = Mock(spec=CurrentRun)

        with patch("openhexa.sdk.pipelines.heartbeat.graphql") as mock_graphql:
            mock_graphql.return_value = {"data": {"updatePipelineHeartbeat": {"success": True, "errors": []}}}

            thread = HeartbeatThread(mock_run_context, interval=10)
            thread.start()

            # Verify thread is running
            assert thread.is_alive()

            # Stop the thread
            thread.stop()
            thread.join(timeout=1)

            # Verify thread has stopped
            assert not thread.is_alive()
            assert thread.stop_event.is_set()


class TestHeartbeatManager:
    """Test suite for heartbeat_manager context manager."""

    @patch.object(CurrentRun, "_connected", True)
    @patch("openhexa.sdk.pipelines.heartbeat.graphql")
    def test_heartbeat_manager_starts_and_stops_thread(self, mock_graphql):
        """Test that heartbeat_manager starts thread on enter and stops on exit."""
        mock_run_context = Mock(spec=CurrentRun)
        mock_run_context._connected = True
        mock_graphql.return_value = {"data": {"updatePipelineHeartbeat": {"success": True, "errors": []}}}

        thread = None
        with heartbeat_manager(mock_run_context, interval=0.1) as hb_thread:
            thread = hb_thread
            assert thread is not None
            assert isinstance(thread, HeartbeatThread)
            assert thread.is_alive()

        # After exiting context, thread should be stopped
        assert not thread.is_alive()

    @patch.object(CurrentRun, "_connected", False)
    def test_heartbeat_manager_skips_when_not_connected(self):
        """Test that heartbeat_manager does nothing when not connected."""
        mock_run_context = Mock(spec=CurrentRun)
        mock_run_context._connected = False

        with heartbeat_manager(mock_run_context, interval=30) as thread:
            assert thread is None

    @patch.object(CurrentRun, "_connected", True)
    @patch("openhexa.sdk.pipelines.heartbeat.graphql")
    def test_heartbeat_manager_stops_thread_on_exception(self, mock_graphql):
        """Test that heartbeat_manager stops thread even when exception occurs."""
        mock_run_context = Mock(spec=CurrentRun)
        mock_run_context._connected = True
        mock_graphql.return_value = {"data": {"updatePipelineHeartbeat": {"success": True, "errors": []}}}

        thread = None
        with pytest.raises(ValueError):
            with heartbeat_manager(mock_run_context, interval=0.1) as hb_thread:
                thread = hb_thread
                assert thread.is_alive()
                raise ValueError("Simulated pipeline error")

        # Thread should still be stopped after exception
        time.sleep(0.2)  # Give thread time to stop
        assert not thread.is_alive()

    @patch.object(CurrentRun, "_connected", True)
    @patch("openhexa.sdk.pipelines.heartbeat.graphql")
    def test_heartbeat_manager_custom_interval(self, mock_graphql):
        """Test that heartbeat_manager respects custom interval."""
        mock_run_context = Mock(spec=CurrentRun)
        mock_run_context._connected = True
        mock_graphql.return_value = {"data": {"updatePipelineHeartbeat": {"success": True, "errors": []}}}

        with heartbeat_manager(mock_run_context, interval=60) as thread:
            assert thread.interval == 60

    @patch.object(CurrentRun, "_connected", True)
    @patch("openhexa.sdk.pipelines.heartbeat.graphql")
    def test_heartbeat_manager_sends_heartbeats_during_execution(self, mock_graphql):
        """Test that heartbeats are sent continuously during pipeline execution."""
        mock_run_context = Mock(spec=CurrentRun)
        mock_run_context._connected = True
        mock_graphql.return_value = {"data": {"updatePipelineHeartbeat": {"success": True, "errors": []}}}

        with heartbeat_manager(mock_run_context, interval=0.05):
            # Simulate pipeline work
            time.sleep(0.2)

        # Verify multiple heartbeats were sent
        assert mock_graphql.call_count >= 2

    @patch.object(CurrentRun, "_connected", True)
    @patch("openhexa.sdk.pipelines.heartbeat.HeartbeatThread")
    def test_heartbeat_manager_timeout_on_join(self, mock_thread_class):
        """Test that heartbeat_manager has timeout when joining thread."""
        mock_run_context = Mock(spec=CurrentRun)
        mock_run_context._connected = True

        # Mock thread that doesn't stop quickly
        mock_thread_instance = MagicMock()
        mock_thread_instance.is_alive.return_value = True
        mock_thread_class.return_value = mock_thread_instance

        with heartbeat_manager(mock_run_context, interval=30):
            pass

        # Verify join was called with timeout
        mock_thread_instance.join.assert_called_once_with(timeout=5)

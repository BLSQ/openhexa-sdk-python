"""Heartbeat management for OpenHEXA pipelines.

This module provides a background thread that sends periodic heartbeats to the
OpenHEXA backend to indicate that a pipeline is still running.
"""
import threading
from contextlib import contextmanager

from openhexa.sdk.pipelines.run import CurrentRun

from ..utils import OpenHexaClient, get_timestamp


class HeartbeatThread(threading.Thread):
    """Background thread that sends periodic heartbeats to the OpenHEXA backend."""

    def __init__(self, run_context: CurrentRun, interval: float = 30):
        """Initialize the heartbeat thread.

        Parameters
        ----------
        run_context : CurrentRun
            The current pipeline run context.
        interval : int, optional
            The interval in seconds between heartbeats (default: 30).
        """
        super().__init__(daemon=True, name="PipelineHeartbeat")
        self.run_context = run_context
        self.interval = interval
        self.stop_event = threading.Event()

    def run(self):
        """Send heartbeats periodically until stopped."""
        while not self.stop_event.is_set():
            try:
                result = OpenHexaClient().update_pipeline_heartbeat()
                if result.success:
                    print(f"{get_timestamp()} Heartbeat sent successfully")
                else:
                    print(f"{get_timestamp()} Heartbeat failed, returned errors: {result.errors}")
            except Exception as e:
                print(f"{get_timestamp()} Exception while trying to send heartbeat to Openhexa Backend: {e}")

            # Wait for next interval or stop signal
            self.stop_event.wait(self.interval)

    def stop(self):
        """Signal the thread to stop."""
        self.stop_event.set()


@contextmanager
def heartbeat_manager(run_context: CurrentRun, interval: float = 30):
    """Context manager for managing heartbeat thread lifecycle.

    Parameters
    ----------
    run_context : CurrentRun
        The current pipeline run context.
    interval : int, optional
        The interval in seconds between heartbeats (default: 30).

    Yields
    ------
    HeartbeatThread or None
        The heartbeat thread if connected, None if running locally.

    Examples
    --------
    >>> from openhexa.sdk.pipelines.run import current_run
    >>> with heartbeat_manager(current_run):
    ...     # Pipeline execution code
    ...     pass
    """
    if not run_context._connected:
        # Local execution - no heartbeat needed
        yield None
        return

    thread = HeartbeatThread(run_context, interval=interval)
    thread.start()
    print(f"{get_timestamp()} Heartbeat thread started")

    try:
        yield thread
    finally:
        thread.stop()
        thread.join(timeout=5)
        print(f"{get_timestamp()} Heartbeat thread stopped")

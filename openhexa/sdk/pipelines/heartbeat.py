"""Heartbeat management for OpenHEXA pipelines.

This module provides a background thread that sends periodic heartbeats to the
OpenHEXA backend to indicate that a pipeline is still running.
"""

import logging
import threading
from contextlib import contextmanager

from openhexa.sdk.pipelines.run import CurrentRun

from ..utils import OpenHexaClient

logger = logging.getLogger(__name__)


class HeartbeatThread(threading.Thread):
    """Background thread that sends periodic heartbeats to the OpenHEXA backend."""

    def __init__(self, run_context: CurrentRun, interval: int = 30):
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
        self.logger = logger

    def run(self):
        """Send heartbeats periodically until stopped."""
        while not self.stop_event.is_set():
            try:
                self._send_heartbeat()
            except Exception as e:
                self.logger.warning(f"Exception while trying to send heartbeat to Openhexa Backend: {e}")

            # Wait for next interval or stop signal
            self.stop_event.wait(self.interval)

    def _send_heartbeat(self):
        """Send a single heartbeat via GraphQL mutation."""
        result = OpenHexaClient().update_pipeline_heartbeat()
        if result.success:
            self.logger.debug("Heartbeat sent successfully")
        else:
            self.logger.warning(f"Heartbeat failed, returned errors: {result.errors}")

    def stop(self):
        """Signal the thread to stop."""
        self.stop_event.set()


@contextmanager
def heartbeat_manager(run_context: CurrentRun, interval: int = 30):
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
    logger.debug("Heartbeat thread started")

    try:
        yield thread
    finally:
        thread.stop()
        thread.join(timeout=5)
        logger.debug("Heartbeat thread stopped")

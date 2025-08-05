"""Current Pipeline context module."""
import os

from openhexa.sdk.utils import Environment, get_environment


class PipelineConfigError(Exception):
    """Raised whenever the system cannot find an environment variable required to configure the current pipeline."""

    pass


class CurrentPipeline:
    """It is used to view manage the current pipeline state and operations."""

    @property
    def code(self) -> str:
        """The unique slug of the workspace.

        Slugs are used to identify the workspace.
        """
        try:
            return os.environ["HEXA_PIPELINE_CODE"]
        except KeyError:
            raise PipelineConfigError("The pipeline code is not available in this environment.")

    @property
    def name(self) -> str:
        """The name of the current pipeline."""
        try:
            return os.environ["HEXA_PIPELINE_NAME"]
        except KeyError:
            raise PipelineConfigError("The pipeline name is not available in this environment.")

    @property
    def type(self) -> str:
        """The type of the current pipeline."""
        try:
            return os.environ["HEXA_PIPELINE_TYPE"]
        except KeyError:
            raise PipelineConfigError("The pipeline type is not available in this environment.")


if get_environment() == Environment.CLOUD_JUPYTER:
    current_pipeline = None
else:
    current_pipeline = CurrentPipeline()

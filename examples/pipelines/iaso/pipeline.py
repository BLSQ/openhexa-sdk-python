"""Example pipeline to get data elements from IASO."""

from openhexa.sdk import current_run, parameter, pipeline
from openhexa.sdk.pipelines.parameter import IASOWidget
from openhexa.sdk.workspaces.connection import IASOConnection


@pipeline(name="IASO Data Elements")
@parameter("iaso_con", type=IASOConnection, required=True)
@parameter(
    "forms",
    type=str,
    required=True,
    widget=IASOWidget.FORMS,
    multiple=True,
    connection="iaso_con",
)
def iaso(iaso_con, forms):
    """Get forms from IASO."""
    print_forms(iaso_con, forms)


@iaso.task
def print_forms(iaso_con, forms):
    """Print forms."""
    current_run.log_info("Printing forms")

    current_run.log_info(f"Forms: {forms}")


if __name__ == "__main__":
    iaso()

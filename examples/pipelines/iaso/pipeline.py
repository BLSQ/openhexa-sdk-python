"""Example pipeline to get data elements from IASO."""

from openhexa.sdk import current_run, parameter, pipeline
from openhexa.sdk.pipelines.parameter import IASOWidget
from openhexa.sdk.workspaces.connection import IASOConnection


@pipeline(name="IASO Data Elements")
@parameter("iaso_con", type=IASOConnection, required=True)
@parameter(
    "forms",
    type=int,
    required=True,
    widget=IASOWidget.IASO_FORMS,
    multiple=True,
    connection="iaso_con",
)
@parameter(
    "projects",
    type=int,
    required=True,
    widget=IASOWidget.IASO_PROJECTS,
    multiple=True,
    connection="iaso_con",
)
@parameter(
    "org_units",
    type=int,
    required=True,
    widget=IASOWidget.IASO_ORG_UNITS,
    multiple=True,
    connection="iaso_con",
)
def iaso(iaso_con, forms, org_units, projects):
    """Get forms from IASO."""
    print_forms(iaso_con, forms, org_units, projects)


@iaso.task
def print_forms(iaso_con, forms, org_units, projects):
    """Print forms."""
    current_run.log_info("Printing forms")

    current_run.log_info(f"Forms: {forms}, Org Units: {org_units}, Projects: {projects}")


if __name__ == "__main__":
    iaso()

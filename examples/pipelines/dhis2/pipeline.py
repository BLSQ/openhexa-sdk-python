"""Template for newly generated pipelines."""

from openhexa.sdk import current_run, parameter, pipeline
from openhexa.sdk.pipelines.parameter import ParameterWidget
from openhexa.sdk.workspaces.connection import DHIS2Connection


@pipeline("dhis2")
@parameter("dhis2_con", type=DHIS2Connection, required=True)
@parameter(
    "data_elements",
    type=str,
    required=True,
    widget=ParameterWidget.DHIS2_DATA_ELEMENTS,
    multiple=True,
    connection="dhis2_con",
)
def dhis2(dhis2_con, data_elements):
    """Get data elements from DHIS2."""
    print_data_elements(dhis2_con, data_elements)


@dhis2.task
def print_data_elements(dhis2_con, data_elements):
    """Print data elements."""
    current_run.log_info("Printing data elements")

    current_run.log_info(f"Data elements: {data_elements}")


if __name__ == "__main__":
    dhis2()

"""Simple module for a sample IO pipeline."""

import json

import pandas as pd
import requests
from sqlalchemy import create_engine

from openhexa.sdk import current_run, pipeline, workspace


@pipeline("Simple IO")
def simple_io():
    """Run a simple IO pipeline."""
    # Read and write from/to workspace files
    raw_files_data = load_files_data()
    transform_and_write_files_data(raw_files_data)

    # Read and write from/to workspace database
    raw_sql_data = load_data_from_postgresql()
    transform_and_write_sql_data(raw_sql_data)

    # Use connection
    load_dhis2_data()


@simple_io.task
def load_files_data():
    """Load data from workspace filesystem."""
    current_run.log_info("Loading files data...")

    return pd.read_csv(f"{workspace.files_path}/raw.csv")


@simple_io.task
def transform_and_write_files_data(raw_data: pd.DataFrame):
    """Simulate a transformation on the provided dataframe and write data to workspace filesystem."""
    current_run.log_info("Transforming files data...")

    transformed_data = raw_data.copy()
    transformed_data["foo"] = transformed_data["foo"].multiply(2)
    transformed_path = f"{workspace.files_path}/transformed.csv"
    transformed_data.to_csv(transformed_path, index=False)
    current_run.add_file_output(transformed_path)


@simple_io.task
def load_data_from_postgresql() -> pd.DataFrame:
    """Perform a simple SELECT query in the workspace database."""
    current_run.log_info("Loading Postgres data...")

    engine = create_engine(workspace.database_url)

    return pd.read_sql("SELECT * FROM foo", con=engine)


@simple_io.task
def transform_and_write_sql_data(raw_data: pd.DataFrame):
    """Simulate a transform operation on the provided data and load it in the workspace database."""
    current_run.log_info("Transforming postgres data...")

    engine = create_engine(workspace.database_url)
    transformed_data = raw_data.copy()
    transformed_data["bar"] = transformed_data["bar"].multiply(3)
    transformed_data.to_sql("baz", con=engine, index=False, if_exists="replace")
    current_run.add_database_output("baz")


@simple_io.task
def load_dhis2_data():
    """Load data from DHIS2."""
    current_run.log_info("Loading DHIS2 data...")

    connection = workspace.dhis2_connection("dhis2-play")
    base_url = f"{connection.url}/api"
    session = requests.Session()
    session.auth = (connection.username, connection.password)
    analytics_response = session.get(
        f"{base_url}/analytics",
        params={
            "aggregationType": "SUM",
            "dimension": [
                "dx:DE_GROUP-qfxEYY9xAl6",
                "pe:2021;2022",
                "ou:LEVEL-2",
            ],
        },
    )
    current_run.log_debug(f"Got {analytics_response.status_code} response from DHIS2")

    return json.loads(analytics_response.text)


if __name__ == "__main__":
    simple_io()

import pandas as pd
from sqlalchemy import create_engine

from openhexa.sdk.io import workspace_data
from openhexa.sdk.pipelines import current_run, pipeline


@pipeline("simple-io", name="Simple IO")
# @connection("dhis2_server", type=DHIS2Connection, name="DHIS2 server")
def simple_io():
    raw_files_data = load_files_data()
    transform_and_write_files_data(raw_files_data)
    raw_sql_data = load_data_from_postgresql()
    transform_and_write_sql_data(raw_sql_data)
    # dhis2_data = read_data_from_dhis2(dhis2_server)


@simple_io.task
def load_files_data():
    return pd.read_csv(workspace_data.files_path("raw.csv"))


@simple_io.task
def transform_and_write_files_data(raw_data: pd.DataFrame):
    transformed_data = raw_data.copy()
    transformed_data["foo"] = transformed_data["foo"].multiply(2)
    transformed_path = workspace_data.files_path("transformed.csv")
    transformed_data.to_csv(transformed_path, index=False)
    current_run.add_file_output(transformed_path, name="Transformed data")


@simple_io.task
def load_data_from_postgresql() -> pd.DataFrame:
    engine = create_engine(workspace_data.database_url)

    return pd.read_sql("SELECT * FROM foo", con=engine)


@simple_io.task
def transform_and_write_sql_data(raw_data: pd.DataFrame):
    engine = create_engine(workspace_data.database_url)
    transformed_data = raw_data.copy()
    transformed_data["bar"] = transformed_data["bar"].multiply(3)
    transformed_data.to_sql("baz", con=engine, index=False, if_exists="replace")
    current_run.add_database_output("baz", name="Baz table")


# @simple_io.task
# def read_data_from_dhis2(dhis2_server: DHIS2Connection):
#     with dhis2_server.simulate() as something:  # what is DHIS2 server is not usable?
#         data = requests.get(f"{dhis2_server.api_url}/some-endpoint")
#
#     return data


if __name__ == "__main__":
    simple_io()

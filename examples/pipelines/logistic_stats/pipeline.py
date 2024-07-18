"""Simple module for a sample logistic pipeline."""

import json
import typing
from io import BytesIO

import geopandas as gpd
import pandas as pd
import rasterio
import requests
from rasterstats import zonal_stats

from openhexa.sdk import parameter, pipeline, workspace


@pipeline("logistic-stats", name="Logistic stats")
@parameter(
    "deg",
    name="Data element group",
    type=str,
    help="The ID of the data element group in DHIS2.",
)
@parameter(
    "periods",
    type=str,
    multiple=True,
    help="A list of DHIS2 periods, separated by a newline.",
)
@parameter("oul", name="Organisation unit level", type=int, default=2)
def logistic_stats(deg: str, periods: str, oul: int):
    """Run a basic logistic stats pipeline."""
    dhis2_data = dhis2_download(deg, periods, oul)
    gadm_data = gadm_download()
    worldpop_data = worldpop_download()

    model(dhis2_data, gadm_data, worldpop_data)


@logistic_stats.task
def dhis2_download(data_element_group: str, periods: str, org_unit_level: int) -> dict[str, typing.Any]:
    """Download DHIS2 data."""
    connection = workspace.dhis2_connection("dhis2-play")
    base_url = f"{connection.url}/api"
    session = requests.Session()
    session.auth = (connection.username, connection.password)

    # Store config in a static file
    dx = [f"DE_GROUP-{data_element_group}"]

    analytics_response = session.get(
        f"{base_url}/analytics",
        params={
            "aggregationType": "SUM",
            # "fields": "id",
            "dimension": [
                f"dx:{';'.join(dx)}",
                f"pe:{';'.join(periods)}",
                f"ou:LEVEL-{org_unit_level}",
            ],
        },
    )

    return json.loads(analytics_response.text)


@logistic_stats.task
def gadm_download():
    """Download administrative boundaries data from UCDavis."""
    url = "https://geodata.ucdavis.edu/gadm/gadm4.1/gpkg/gadm41_SLE.gpkg"
    r = requests.get(url, timeout=30)

    return r.content


@logistic_stats.task
def worldpop_download():
    """Download population data from worldpop.org."""
    base_url = "https://data.worldpop.org/"
    url = f"{base_url}GIS/Population/Global_2000_2020_Constrained/2020/maxar_v1/SLE/sle_ppp_2020_UNadj_constrained.tif"
    r = requests.get(url)

    return r.content


@logistic_stats.task
def model(dhis2_data: dict[str, typing.Any], gadm_data, worldpop_data):
    """Build a basic data model."""
    # Load DHIS2 data
    dhis2_df = pd.DataFrame(dhis2_data["rows"], columns=[h["column"] for h in dhis2_data["headers"]])
    dhis2_df = dhis2_df.rename(columns={"Data": "Data element id", "Organisation unit": "Organisation unit id"})
    dhis2_df["Value"] = pd.to_numeric(dhis2_df["Value"], downcast="integer")
    dhis2_df["Period"] = pd.PeriodIndex(dhis2_df["Period"], freq="Q")
    dhis2_df["Organisation unit"] = dhis2_df["Organisation unit id"].map(
        lambda ouid: dhis2_data["metaData"]["items"][ouid]["name"]
    )
    dhis2_df["Data element"] = dhis2_df["Data element id"].map(
        lambda deid: dhis2_data["metaData"]["items"][deid]["name"]
    )

    print(f"Load DHIS2 DF - {len(dhis2_df)} rows")

    # Load & compute population data
    administrative_areas = gpd.read_file(BytesIO(gadm_data), layer="ADM_ADM_2")
    with rasterio.open(BytesIO(worldpop_data)) as src:
        stats = zonal_stats(
            administrative_areas,  # the geometries
            src.read(1),  # the source raster data
            affine=src.meta["transform"],  # affine transform of the source raster
            stats=["sum"],  # the zonal stats we want to compute
            nodata=src.meta["nodata"],  # nodata value in the source raster
        )

    population_df = pd.Series(data=[stat["sum"] for stat in stats], index=administrative_areas.index)
    population_df = pd.DataFrame({"District": administrative_areas["NAME_2"], "Population": population_df})
    corrected_population_df = population_df.copy()
    corrected_population_df.loc[
        corrected_population_df["District"].str.startswith("Western"), "District"
    ] = "Western Area"

    corrected_population_df = corrected_population_df.groupby("District").sum()

    print(f"Built population DF - {len(population_df)} rows")

    # Compute stats
    pivot_df = dhis2_df.pivot(index=["Period", "Organisation unit"], columns="Data element", values="Value")
    combined_df = pivot_df.reset_index().merge(
        corrected_population_df,
        how="left",
        left_on="Organisation unit",
        right_index=True,
    )
    combined_df = combined_df.set_index(["Period", "Organisation unit"])
    # TODO: replace by something dynamic
    # combined_df["Oral Rehydration Salts by 100000 inh."] = combined_df[
    #     "Commodities - Oral Rehydration Salts"
    # ] / (combined_df["Population"] / 100000)
    # combined_df["Oxytocin by 100000 inh."] = combined_df["Commodities - Oxytocin"] / (
    #     combined_df["Population"] / 100000
    # )

    # Save to CSV

    # TODO: variable path / helper for workspace path
    combined_df.to_csv(f"{workspace.files_path}/stats.csv")


if __name__ == "__main__":
    logistic_stats()

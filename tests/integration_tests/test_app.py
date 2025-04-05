from influxdb_client.client.query_api import QueryApi
import pytest
import os

from solaredge_influxdb.app import app

from solaredge_influxdb.influxdb import InfluxDBClient

from test_influx import create_influx_config


def test_app(create_influx_config) -> None:
    """Test the app function."""
    os.environ["API_KEY"] = "L4QLVQ1LOKCQX2193VSEICXW61NP6B1O"

    app("tests/integration_tests/test_config.toml")

    # Add assertions or checks to verify the expected behavior of the app function
    # For example, you can check if the data was written to InfluxDB correctly
    # or if the API calls were made successfully.

    influxQueryAPI: QueryApi = InfluxDBClient("tests/integration_tests/test_config.toml").client.query_api()
    energy_result = influxQueryAPI.query(
        'from(bucket: "energy") |> range(start: -1h) |> filter(fn: (r) => r._measurement == "test_measurement")'
    )
    for table in energy_result:
        assert len(table.records) > 0, "No data returned from InfluxDB query."

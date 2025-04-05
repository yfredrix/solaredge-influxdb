from solaredge_influxdb.influxdb import InfluxDBClient

from influxdb_client.client.query_api import QueryApi
from datetime import datetime, timedelta, tzinfo

import pytest
import os
import pytz


@pytest.fixture(scope="module")
def create_influx_config() -> None:
    """Create a config file for InfluxDB"""
    with open("tests/integration_tests/test_config.toml", "w") as f:
        f.write(
            f"""
            [influx2]
            url = "http://localhost:8086"
            org = "test-org"
            token = {os.getenv("INFLUXDB_ADMIN_TOKEN")}
            """
        )


def test_write_api(create_influx_config) -> None:
    """Test the write API of InfluxDB"""

    InfluxClient = InfluxDBClient("tests/integration_tests/test_config.toml")

    event_time = datetime.now().replace(tzinfo=pytz.utc) + timedelta(minutes=-15)

    test_data = InfluxClient.convert_to_point(
        event_time,
        "test_measurement",
        [("field1", 123), ("field2", 456)],
        [("tag1", "value1"), ("tag2", "value2")],
    )

    InfluxClient.write(test_data, "test")
    print("Test data written to InfluxDB successfully.")

    influxQueryAPI: QueryApi = InfluxClient.client.query_api()
    result = influxQueryAPI.query(
        'from(bucket: "test") |> range(start: -1h) |> filter(fn: (r) => r._measurement == "test_measurement")'
    )
    output = result.to_values(columns=["_time", "_measurement", "_field", "_value"])
    assert len(output) > 0, "No data returned from InfluxDB query."
    assert output[0][1] == "test_measurement", "Measurement name does not match."
    assert output[0][2] == "field1", "Field name does not match."
    assert output[0][3] == 123, "Field value does not match."
    assert output[1][2] == "field2", "Field name does not match."
    assert output[1][3] == 456, "Field value does not match."
    assert output[0][0].replace(microsecond=0) == event_time.replace(microsecond=0), "Time does not match."
    print("Test data verified successfully.")

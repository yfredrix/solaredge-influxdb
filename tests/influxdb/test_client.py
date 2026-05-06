from unittest.mock import Mock, patch

from solaredge_influxdb.influxdb.client import InfluxDBClient


def test_write_logs_serialized_record_for_point_payload():
    influx_client = InfluxDBClient.__new__(InfluxDBClient)
    influx_client.write_api = Mock()
    point = Mock()
    point.to_line_protocol.return_value = "solar,serial_number=INV-1 total_energy=2.5 1746568800000"

    with patch("solaredge_influxdb.influxdb.client.logger.debug") as mock_debug:
        influx_client.write(point, "energy")

    mock_debug.assert_called_once_with(
        "Writing record to InfluxDB bucket='{}': {}",
        "energy",
        "solar,serial_number=INV-1 total_energy=2.5 1746568800000",
    )
    influx_client.write_api.write.assert_called_once_with(bucket="energy", record=point)


def test_write_logs_string_payload():
    influx_client = InfluxDBClient.__new__(InfluxDBClient)
    influx_client.write_api = Mock()
    payload = "solar,serial_number=INV-1 total_energy=2.5 1746568800000"

    with patch("solaredge_influxdb.influxdb.client.logger.debug") as mock_debug:
        influx_client.write(payload, "energy")

    mock_debug.assert_called_once_with(
        "Writing record to InfluxDB bucket='{}': {}",
        "energy",
        payload,
    )
    influx_client.write_api.write.assert_called_once_with(bucket="energy", record=payload)
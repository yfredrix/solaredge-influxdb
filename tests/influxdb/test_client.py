from unittest.mock import Mock, patch, create_autospec

import influxdb_client

from solaredge_influxdb.influxdb.client import InfluxDBClient


def test_write_logs_serialized_record_for_point_payload():
    influx_client = InfluxDBClient.__new__(InfluxDBClient)
    influx_client.write_api = Mock()
    point = create_autospec(influxdb_client.Point, instance=True)
    point.to_line_protocol.return_value = "solar,serial_number=INV-1 total_energy=2.5 1746568800000"

    mock_lazy_logger = Mock()
    with patch("solaredge_influxdb.influxdb.client.logger.opt", return_value=mock_lazy_logger) as mock_opt:
        influx_client.write(point, "energy")

    mock_opt.assert_called_once_with(lazy=True)
    mock_lazy_logger.debug.assert_called_once()
    call_args = mock_lazy_logger.debug.call_args[0]
    assert call_args[0] == "Writing record to InfluxDB bucket='{}': {}"
    assert call_args[1]() == "energy"
    assert call_args[2]() == "solar,serial_number=INV-1 total_energy=2.5 1746568800000"
    point.to_line_protocol.assert_called_once()
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
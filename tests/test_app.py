from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import Mock, call, patch

from solaredge_influxdb.app import app


def _build_telemetry():
    return SimpleNamespace(
        operationMode="operating",
        inverterMode="production",
        date=datetime(2026, 5, 6, 22, 0, 0),
        totalEnergy=2500,
        totalActivePower=1200,
        vL1To2=230,
        vL2To3=231,
        vL3To1=229,
        dcVoltage=400,
    )


@patch("solaredge_influxdb.app.get_sunset")
@patch("solaredge_influxdb.app.get_sunrise")
@patch("solaredge_influxdb.app.datetime")
@patch("solaredge_influxdb.app.InfluxDBClient")
@patch("solaredge_influxdb.app.Equipment")
def test_app_skips_collection_after_sundown(mock_equipment, mock_influxdb_client, mock_datetime, mock_get_sunrise, mock_get_sunset):
    # 20:00 UTC = 22:00 CEST, which is still May 6 in Amsterdam and after sunset
    current_time = datetime(2026, 5, 6, 20, 0, 0, tzinfo=timezone.utc)
    sunrise = datetime(2026, 5, 6, 3, 30, 0, tzinfo=timezone.utc)
    sunset = datetime(2026, 5, 6, 17, 0, 0, tzinfo=timezone.utc)
    mock_datetime.now.return_value = current_time
    mock_get_sunrise.return_value = sunrise
    mock_get_sunset.return_value = sunset

    app(api_key="api-key")

    mock_equipment.assert_not_called()
    mock_influxdb_client.return_value.write.assert_not_called()


@patch("solaredge_influxdb.app.get_sunset")
@patch("solaredge_influxdb.app.get_sunrise")
@patch("solaredge_influxdb.app.datetime")
@patch("solaredge_influxdb.app.InfluxDBClient")
@patch("solaredge_influxdb.app.Equipment")
def test_app_collects_after_sundown_when_forced(mock_equipment, mock_influxdb_client, mock_datetime, mock_get_sunrise, mock_get_sunset):
    # 20:00 UTC = 22:00 CEST, which is still May 6 in Amsterdam and after sunset
    current_time = datetime(2026, 5, 6, 20, 0, 0, tzinfo=timezone.utc)
    sunrise = datetime(2026, 5, 6, 3, 30, 0, tzinfo=timezone.utc)
    sunset = datetime(2026, 5, 6, 17, 0, 0, tzinfo=timezone.utc)
    telemetry = _build_telemetry()
    equipment_client = Mock()
    equipment_client.inverters = [SimpleNamespace(serialNumber="INV-1", model="SE5000")]
    equipment_client.get_technical_data.return_value = SimpleNamespace(telemetries=[telemetry])
    influx_client = mock_influxdb_client.return_value
    influx_client.convert_to_point.side_effect = ["energy-point", "power-point", "voltage-point"]

    mock_datetime.now.return_value = current_time
    mock_get_sunrise.return_value = sunrise
    mock_get_sunset.return_value = sunset
    mock_equipment.return_value = equipment_client

    app(api_key="api-key", force=True)

    mock_equipment.assert_called_once_with("api-key")
    equipment_client.get_technical_data.assert_called_once()
    assert influx_client.write.call_args_list == [
        call("energy-point", "energy"),
        call("power-point", "energy_flow"),
        call("voltage-point", "voltage_current"),
    ]

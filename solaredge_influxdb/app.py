import os
from suntime import Sun, SunTimeException
from datetime import datetime, timedelta, timezone
import pytz
from loguru import logger

from solaredge_influxdb.solaredge import Equipment, Meter
from solaredge_influxdb.influxdb import InfluxDBClient


def app(
    config_path: str = "./solaredge_influxdb/config.toml",
    latitude: float = os.getenv("LATITUDE", 52.3676),
    longitude: float = os.getenv("LONGITUDE", 4.9041),
    api_key: str = os.getenv("API_KEY"),
    additional_time_window: int = 60,
    timezone_str: str = "Europe/Amsterdam",
):
    sun = Sun(latitude, longitude)
    current_time = datetime.now(timezone.utc)
    logger.debug(f"Current time: {current_time}")
    try:
        sunrise = sun.get_sunrise_time()
        sunset = sun.get_sunset_time()
        logger.debug(f"Sunrise: {sunrise}, Sunset: {sunset}")

    except SunTimeException:
        logger.error("Failed to retrieve sunrise/sunset times")
        raise Exception(
            "Application requires sunset and sunrise times to prevent unnecessary API calls"
        )
    InfluxClient = InfluxDBClient(config_path)
    _timezone = pytz.timezone(timezone_str)

    if (
        sunrise - timedelta(minutes=additional_time_window)
        < current_time
        < sunset + timedelta(minutes=additional_time_window)
    ):
        logger.debug("The Sun is shining bright, let's collect some data!")
        EquipmentClient = Equipment(api_key)
        MeterClient = Meter(api_key)
        current_time = current_time.astimezone(_timezone)
        for inverter in EquipmentClient.inverters:
            tech_data = EquipmentClient.get_technical_data(
                inverter.serialNumber,
                current_time - timedelta(minutes=15),
                current_time,
            )
            if tech_data is None:
                logger.error("Failed to retrieve technical data")
                continue

            for telemetry in tech_data.telemetries:
                tags = [
                    ("serial_number", inverter.serialNumber),
                    ("model", inverter.model),
                    ("operation_mode", telemetry.operationMode),
                    ("inverter_mode", telemetry.inverterMode),
                ]
                telemetry_date = _timezone.localize(telemetry.date)
                energy_point = InfluxClient.convert_to_point(
                    telemetry_date,
                    "solar",
                    [
                        ("total_energy", telemetry.totalEnergy / 1000),
                    ],
                    tags,
                )
                power_point = InfluxClient.convert_to_point(
                    telemetry_date,
                    "solar",
                    [
                        ("ac_power", telemetry.totalActivePower / 1000),
                    ],
                    tags,
                )
                voltage_point = InfluxClient.convert_to_point(
                    telemetry_date,
                    "solar",
                    [
                        ("dc_voltage", telemetry.dcVoltage),
                        ("voltage_l1_to_2", telemetry.vL1To2),
                        ("voltage_l2_to_3", telemetry.vL2To3),
                        ("voltage_l3_to_1", telemetry.vL3To1),
                    ],
                    tags,
                )
                InfluxClient.write(energy_point, "energy")
                InfluxClient.write(power_point, "energy_flow")
                InfluxClient.write(voltage_point, "voltage_current")
    else:
        logger.info("It's dark outside, no need to collect data")

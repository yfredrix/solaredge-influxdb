import os
from suntime import Sun, SunTimeException
from datetime import datetime, timedelta, timezone
from loguru import logger

from solaredge_influxdb.solaredge import Equipment, Meter
from solaredge_influxdb.influxdb import InfluxDBClient

sun = Sun(os.getenv("LATITUDE", 52.3676), os.getenv("LONGITUDE", 4.9041))
current_time = datetime.now(timezone.utc)
try:
    sunrise = sun.get_sunrise_time()
    sunset = sun.get_sunset_time()

except SunTimeException:
    logger.error("Failed to retrieve sunrise/sunset times")
    raise Exception(
        "Application requires sunset and sunrise times to prevent unnecessary API calls"
    )

InfluxClient = InfluxDBClient("./solaredge_influxdb/config.toml")

if current_time > sunset - timedelta(minutes=30) or current_time < sunrise + timedelta(
    minutes=30
):
    EquipmentClient = Equipment(os.getenv("API_KEY"))
    MeterClient = Meter(os.getenv("API_KEY"))

    for inverter in EquipmentClient.inverters:
        tech_data = EquipmentClient.get_technical_data(
            inverter.serialNumber,
            current_time - timedelta(hours=12, minutes=15),
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
            energy_point = InfluxClient.convert_to_point(
                telemetry.date,
                "solar",
                [
                    ("total_energy", telemetry.totalEnergy),
                ],
                tags,
            )
            power_point = InfluxClient.convert_to_point(
                telemetry.date,
                "solar",
                [
                    ("ac_power", telemetry.totalActivePower),
                ],
                tags,
            )
            voltage_point = InfluxClient.convert_to_point(
                telemetry.date,
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

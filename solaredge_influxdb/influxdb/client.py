from datetime import datetime
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from typing import Union, List, Tuple, Optional


class InfluxDBClient:
    def __init__(self, path: str):
        self.client = influxdb_client.InfluxDBClient.from_config_file(path)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)

    def write(self, data: str, bucket: str) -> None:
        """Write data to InfluxDB"""
        self.write_api.write(bucket=bucket, record=data)

    def convert_to_point(
        self,
        time: datetime,
        measurement: str,
        field_values: List[Tuple[str, Union[str, int, float]]],
        tags: Optional[List[Tuple[str, str]]] = None,
    ) -> influxdb_client.Point:
        """Convert a dictionary to an InfluxDB point"""
        if tags is None:
            tags = []
        point = influxdb_client.Point(measurement)
        for fieldvalue in field_values:
            point = point.field(fieldvalue[0], fieldvalue[1])
        for tag in tags:
            point = point.tag(tag[0], tag[1])
        point.time(time, write_precision="ms")
        return point

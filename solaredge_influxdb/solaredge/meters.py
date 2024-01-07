from .models import MeterDataResponse
from .client import SolarEdgeClient
from datetime import datetime
from loguru import logger
from typing import Union, List


class Meter(SolarEdgeClient):
    def __init__(self, api_key: str):
        super().__init__(api_key)

    def get_meters_data(
        self,
        start_time: datetime,
        end_time: datetime,
        time_unit: Union[str, None] = None,
        meters: Union[List[str], None] = None,
    ) -> Union[MeterDataResponse, None]:
        """
        Retrieves meter data from the SolarEdge API for the specified time range.

        Args:
            start_time (datetime): The start time of the data range.
            end_time (datetime): The end time of the data range.
            time_unit (str, optional): The time unit for the data aggregation. Must be one of
                "QUARTER_OF_AN_HOUR", "HOUR", "DAY", "WEEK", "MONTH", "YEAR". Defaults to None.
            meters (list[str], optional): A list of meter names to retrieve data for. Defaults to None.

        Returns:
            MeterDataResponse | None: The meter data response object if successful, None otherwise.
        """

        if time_unit:
            if time_unit not in [
                "QUARTER_OF_AN_HOUR",
                "HOUR",
                "DAY",
                "WEEK",
                "MONTH",
                "YEAR",
            ]:
                raise ValueError(
                    "time_unit must be one of QUARTER_OF_AN_HOUR, HOUR, DAY, WEEK, MONTH, YEAR"
                )
        url = f"{self.url}/site/{self.site_id}/meters"
        if meters:
            meters = ",".join(meters)
        query_params = {
            "api_key": self.api_key,
            "startTime": start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "endTime": end_time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        if time_unit:
            query_params["timeUnit"] = time_unit
        if meters:
            query_params["meters"] = meters

        response = self.session.get(url, params=query_params)
        if response.ok:
            data = response.json()
            return MeterDataResponse(**data)
        logger.error("Failed to retrieve meter data")
        return None

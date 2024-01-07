from datetime import datetime
from .client import SolarEdgeClient
from .models import (
    TelemetryResponse,
    ChangeLogResponse,
    InventoryResponse,
    ComponentsListResponse,
    Inverter,
)
from loguru import logger
from requests import Response
from typing import Union, Dict, List

import os
import json


class Equipment(SolarEdgeClient):
    query_params: Dict[str, str]

    def __init__(
        self, api_key: str, inverters: Union[List[Inverter], None] = None
    ) -> None:
        super().__init__(api_key)
        self.query_params = {"api_key": self.api_key}
        if not inverters:
            inverters = self.get_inverters()
        self.inverters = inverters

    def get_request(cls, url: str) -> Response:
        return cls.session.get(url, params=cls.query_params)

    def get_inverters(self) -> List[Inverter]:
        """Get list of inverters from SolarEdge API or from disk"""
        if os.path.isfile("inverters.json"):
            with open("inverters.json", "r") as f:
                return [Inverter(**i) for i in json.load(f)]
        inverters = self.get_components()
        if inverters:
            inverters = inverters.list
            with open("inverters.json", "w") as f:
                json.dump([dict(i) for i in inverters], f)
            return inverters
        logger.error("Failed to retrieve inverters")
        raise AttributeError("Inverters must be defined and valid")

    def get_components(self) -> Union[ComponentsListResponse, None]:
        """Collect the components list from your site.
        Inputs:
            solarEdgeClient: The solarEdgeClient object you created earlier.
        Outputs:
            data: A dictionary containing the components list of your site.

        Example:
            Input:
                    solarEdgeClient: site_id: 2; api_key: "4QLVQ1LOKCQX2193VSEICXW61NP6B1O"
            Output:
            {
                "list": [
                    {
                        "name": "Inverter 1",
                        "manufacturer": "SolarEdge",
                        "model": "SE16K",
                        "serialNumber": "12345678-00"
                    },
                    {
                        "name": "Inverter 1",
                        "manufacturer": "SolarEdge",
                        "model": "SE16K",
                        "serialNumber": "12345678-00"
                    },
                    {
                        "name": "Inverter 1",
                        "manufacturer": "SolarEdge",
                        "model": "SE16K",
                        "serialNumber": "12345678-00"
                    },
                    {
                        "name": "Inverter 1",
                        "manufacturer": "SolarEdge",
                        "model": "SE16K",
                        "serialNumber": "12345678-65"
                    }
                ]
            }
        """
        url = f"{self.url}/equipment/{self.site_id}/list"
        response = self.get_request(url)
        if response.ok:
            data = response.json()
            return ComponentsListResponse(**data["reporters"])
        logger.error(f"Failed to get components for site {self.site_id}")
        return None

    def get_inventory(self) -> Union[InventoryResponse, None]:
        """Collect the inventory data from your site.
        Inputs:
            solarEdgeClient: The solarEdgeClient object you created earlier.
        Outputs:
            data: A dictionary containing the inventory data of your site.

        Example:
            Input:
                    solarEdgeClient: site_id: 2; api_key: "4QLVQ1LOKCQX2193VSEICXW61NP6B1O"
            Output:
            {
                "Inventory": {
                    "meters": [
                        {
                            "name": "Production Meter",
                            "manufacturer": "WattNode",
                            "model": "WNC-3Y-480-MB",
                            "firmwareVersion": "0013",
                            "connectedSolaredgeDeviceSN": "12345678-00",
                            "type": "Production",
                            "form": "physical"
                        }
                    ],
                    "sensors": [
                        {
                            "connectedSolaredgeDeviceSN": "12345678-00",
                            "id": "SensorDirectIrradiance",
                            "connectedTo": "Gateway 1",
                            "category": "IRRADIANCE",
                            "type": "Direct irradiance"
                        },
                        {
                            "connectedSolaredgeDeviceSN": "12345678-00",
                            "id": "SensorPlaneOfArrayIrradiance",
                            "connectedTo": "Gateway 1",
                            "category": "IRRADIANCE",
                            "type": "Plane of array irradiance"
                        }
                    ],
                    "gateways": [
                        {
                            "name": "Gateway 1",
                            "firmwareVersion": "2.956.0",
                            "SN": "12345678-00"
                        }
                    ],
                    "batteries": [
                        {
                            "name": "Battery 1.1",
                            "manufacturer": "NAME",
                            "model": "10KWh",
                            "firmwareVersion": "2.0",
                            "connectedInverterSn": "12345678-01",
                            "nameplateCapacity": 6400.0,
                            "SN": "T123456789"
                        }
                    ],
                    "inverters": [
                        {
                            "model": "SE20K",
                            "firmwareVersion": "2.19.233",
                            "SN": "12345678-01",
                            "connectedOptimizers": 76
                        },
                        {
                            "name": "Inverter 2",
                            "manufacturer": "SolarEdge",
                            "model": "SE20K",
                            "firmwareVersion": "2.19.233",
                            "SN": "12345678-02",
                            "connectedOptimizers": 76
                        }
                    ]
                }
            }
        """
        url = f"{self.url}/site/{self.site_id}/inventory"
        response = self.get_request(url)
        if response.ok:
            data = response.json()
            return InventoryResponse(**data)
        logger.error(f"Failed to get inventory for site {self.site_id}")
        return None

    def get_technical_data(
        self,
        inverter_id: str,
        start_time: datetime,
        end_time: datetime,
    ) -> Union[TelemetryResponse, None]:
        """Collect the technical data from the inverter within your site.
        Inputs:
            solarEdgeClient: The solarEdgeClient object you created earlier.
            inverter_id: The ID of the inverter you want to collect data from.
            start_time: The start time of the data collection.
            end_time: The end time of the data collection.
        Outputs:
            data: A dictionary containing the technical data of the inverter.

        Example:
            Input:
                    solarEdgeClient: site_id: 2; api_key: "4QLVQ1LOKCQX2193VSEICXW61NP6B1O"
                    inverter_id: "12345678-9"
                    start_time: "2013-05-5 11:00:00"
                    end_time: "2013-05-05 13:00:00"
            Output:
            {
                "data": {
                    "count": 2,
                    "telemetries": [
                        {
                            "threePhaseInverterTelemetry": [
                                {
                                    "date": "2013-06-04 11:05:00",
                                    "totalActivePower": null,
                                    "dcVoltage": 46.9757,
                                    "groundFaultResistance": 6672.34,
                                    "powerLimit": 78.4159,
                                    "totalEnergy": 1.26533E7,
                                    "temperature": 54.8134,
                                    "inverterMode": "MPPT",
                                    "operationMode": 0,
                                    "L1Data": {
                                        "acCurrent": 22.653,
                                        "acVoltage": 11.6201,
                                        "acFrequency": 41.3468,
                                        "apparentPower": 1964.0,
                                        "activePower": 1954.0,
                                        "reactivePower": -89.0,
                                        "cosPhi": 1.0
                                    },
                                    "vL1To2": 394.312,
                                    "vL2To3": 393.781,
                                    "vL3To1": 392.5,
                                    "L2Data": {
                                        "acCurrent": 22.653,
                                        "acVoltage": 11.6201,
                                        "acFrequency": 41.3468,
                                        "apparentPower": 1964.0,
                                        "activePower": 1954.0,
                                        "reactivePower": -89.0,
                                        "cosPhi": 1.0
                                    },
                                    "L3Data": {
                                        "acCurrent": 22.653,
                                        "acVoltage": 11.6201,
                                        "acFrequency": 41.3468,
                                        "apparentPower": 1964.0,
                                        "activePower": 1954.0,
                                        "reactivePower": -89.0,
                                        "cosPhi": 1.0
                                    }
                                }
                            ]
                        }
                    ]
                }
            }
        """
        url = f"{self.url}/equipment/{self.site_id}/{inverter_id}/data.json"
        query_params = {
            "startTime": start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "endTime": end_time.strftime("%Y-%m-%d %H:%M:%S"),
            "api_key": self.api_key,
        }
        response = self.session.get(url=url, params=query_params)
        if response.ok:
            data = response.json()
            return TelemetryResponse(**data["data"])
        logger.error(f"Failed to get technical data for inverter {inverter_id}")
        return None

    def get_change_log(
        self,
        serial_number: str,
    ) -> Union[ChangeLogResponse, None]:
        """Collect the change log data from the equipment within your site.
        Inputs:
            solarEdgeClient: The solarEdgeClient object you created earlier.
            serial_number: The ID of the equipment you want to collect data from.
        Outputs:
            data: A dictionary containing the change log data of the inverter.

        Example:
            Input:
                    solarEdgeClient: site_id: 2; api_key: "L4QLVQ1LOKCQX2193VSEICXW61NP6B1O"
                    serial_number: "1234567-38"
            Output:
            {
                "ChangeLog": {
                    "count": 1,
                    "list": {
                        "serialNumber": "1234567-3A",
                        "partNumber": null,
                        "date": "2017-08-30"
                    }
                }
            }
        """
        url = f"{self.url}/equipment/{self.site_id}/{serial_number}/changeLog"
        response = self.get_request(url)
        if response.ok:
            data = response.json()
            return ChangeLogResponse(**data)
        logger.error(f"Failed to get change log for equipment {serial_number}")
        return None

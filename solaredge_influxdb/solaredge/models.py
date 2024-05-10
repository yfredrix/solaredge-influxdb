from typing import List, Optional
from pydantic import BaseModel, NaiveDatetime


class TelemetryData(BaseModel):
    date: NaiveDatetime
    totalActivePower: Optional[float]
    dcVoltage: Optional[float]
    groundFaultResistance: Optional[float] = None
    powerLimit: float
    totalEnergy: float
    temperature: Optional[float] = None
    inverterMode: str
    operationMode: int
    vL1To2: Optional[float] = None
    vL2To3: Optional[float] = None
    vL3To1: Optional[float] = None

    class L1Data(BaseModel):
        acCurrent: float
        acVoltage: float
        acFrequency: float
        apparentPower: float
        activePower: float
        reactivePower: float
        cosPhi: float

    class L2Data(BaseModel):
        acCurrent: float
        acVoltage: float
        acFrequency: float
        apparentPower: float
        activePower: float
        reactivePower: float
        cosPhi: float

    class L3Data(BaseModel):
        acCurrent: float
        acVoltage: float
        acFrequency: float
        apparentPower: float
        activePower: float
        reactivePower: float
        cosPhi: float

    threePhaseInverterTelemetry: Optional[List[dict]] = None


class TelemetryResponse(BaseModel):
    count: int
    telemetries: List[TelemetryData]


class ChangeLog(BaseModel):
    serialNumber: str
    partNumber: Optional[str]
    date: str


class ChangeLogResponse(BaseModel):
    count: int
    list: ChangeLog


class Meter(BaseModel):
    name: str
    manufacturer: str
    model: str
    firmwareVersion: str
    connectedSolaredgeDeviceSN: str
    type: str
    form: str


class Sensor(BaseModel):
    connectedSolaredgeDeviceSN: str
    id: str
    connectedTo: str
    category: str
    type: str


class Gateway(BaseModel):
    name: str
    firmwareVersion: str
    SN: str


class Battery(BaseModel):
    name: str
    manufacturer: str
    model: str
    firmwareVersion: str
    connectedInverterSn: str
    nameplateCapacity: float
    SN: str


class InventoryInverter(BaseModel):
    model: str
    firmwareVersion: str
    SN: str
    connectedOptimizers: int


class Inventory(BaseModel):
    meters: List[Meter]
    sensors: List[Sensor]
    gateways: List[Gateway]
    batteries: List[Battery]
    inverters: List[InventoryInverter]


class InventoryResponse(BaseModel):
    Inventory: Inventory


class Inverter(BaseModel):
    name: str
    manufacturer: str
    model: str
    serialNumber: str


class ComponentsListResponse(BaseModel):
    count: int
    list: List[Inverter]


class Location(BaseModel):
    country: str
    state: Optional[str] = None
    city: str
    address: str
    address2: Optional[str] = None
    zip: str
    timeZone: str


class Site(BaseModel):
    id: int
    name: str
    accountId: int
    status: str
    peakPower: float
    currency: str
    installationDate: str
    ptoDate: Optional[str]
    notes: str
    type: str
    location: Location
    alertQuantity: Optional[int] = None
    alertSeverity: Optional[str] = None
    uris: dict
    publicSettings: dict


class SitesResponse(BaseModel):
    count: int
    site: List[Site]


class MeterEnergyValue(BaseModel):
    date: str
    value: int


class MeterEnergyMeter(BaseModel):
    meterSerialNumber: str
    connectedSolaredgeDeviceSN: str
    model: str
    meterType: str
    values: List[MeterEnergyValue]


class MeterEnergyDetails(BaseModel):
    timeUnit: str
    unit: str
    meters: List[MeterEnergyMeter]


class MeterDataResponse(BaseModel):
    meterEnergyDetails: MeterEnergyDetails

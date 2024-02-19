from influxdb_client import StatusRule
import pytest
from solaredge_influxdb.solaredge.site import list_sites
from solaredge_influxdb.solaredge.models import SitesResponse


class MockSolarEdgeClient:
    def __init__(self, url, api_key):
        self.url = url
        self.api_key = api_key
        self.session = None


class MockSession:
    def __init__(self, response):
        self.response = response

    def get(self, url, params):
        return self.response


class MockResponse:
    def __init__(self, json_data, ok):
        self.json_data = json_data
        self.ok = ok

    def json(self):
        return self.json_data


def test_list_sites_success():
    client = MockSolarEdgeClient("https://api.solaredge.com", "your_api_key")
    response_data = {
        "sites": {
            "count": 2,
            "site": [
                {
                    "id": 123,
                    "name": "Site 1",
                    "accountId": 456,
                    "status": "Active",
                    "peakPower": 1000.0,
                    "currency": "USD",
                    "installationDate": "2022-01-01",
                    "ptoDate": None,
                    "notes": "This is an example site.",
                    "type": "Residential",
                    "location": {
                        "country": "United States",
                        "state": "California",
                        "city": "San Francisco",
                        "address": "123 Main St",
                        "address2": None,
                        "zip": "12345",
                        "timeZone": "PST",
                    },
                    "alertQuantity": None,
                    "alertSeverity": None,
                    "uris": {},
                    "publicSettings": {},
                },
                {
                    "id": 234,
                    "name": "Site 2",
                    "accountId": 456,
                    "status": "Active",
                    "peakPower": 1000.0,
                    "currency": "USD",
                    "installationDate": "2022-01-01",
                    "ptoDate": None,
                    "notes": "This is an example site.",
                    "type": "Residential",
                    "location": {
                        "country": "United States",
                        "state": "California",
                        "city": "San Francisco",
                        "address": "123 Main St",
                        "address2": None,
                        "zip": "12345",
                        "timeZone": "PST",
                    },
                    "alertQuantity": None,
                    "alertSeverity": None,
                    "uris": {},
                    "publicSettings": {},
                },
            ],
        }
    }
    response = MockResponse(response_data, True)
    client.session = MockSession(response)

    result = list_sites(client)

    assert result is not None
    assert isinstance(result, SitesResponse)
    assert len(result.site) == 2
    assert result.site[0].id == 123
    assert result.site[0].name == "Site 1"
    assert result.site[1].id == 234
    assert result.site[1].name == "Site 2"


def test_list_sites_failure():
    client = MockSolarEdgeClient("https://api.solaredge.com", "your_api_key")
    response = MockResponse({}, False)
    client.session = MockSession(response)

    result = list_sites(client)

    assert result is None

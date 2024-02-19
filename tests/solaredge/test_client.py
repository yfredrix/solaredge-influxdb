import pytest
from unittest.mock import Mock, mock_open, patch
from solaredge_influxdb.solaredge.client import SolarEdgeClient


class TestSolarEdgeClient:

    def test_init_session(self):
        client = SolarEdgeClient("api_key")
        assert client.session.headers["Accept"] == "application/json"

    @patch("solaredge_influxdb.solaredge.client.os.path.isfile", return_value=True)
    @patch("solaredge_influxdb.solaredge.client.open", mock_open(read_data="123"))
    def test_get_site_from_file(self, mock_isfile):
        client = SolarEdgeClient("api_key")
        site_id = client.get_site()
        assert site_id == 123

    @patch(
        "solaredge_influxdb.solaredge.client.os.path.isfile",
        return_value=False,
    )
    @patch("solaredge_influxdb.solaredge.client.list_sites")
    def test_get_site_from_api(self, mock_list_sites, mock_isfile):
        mock_list_sites.return_value = Mock(count=1, site=[Mock(id=123)])
        client = SolarEdgeClient("api_key")
        site_id = client.get_site()
        assert site_id == 123

    @patch(
        "solaredge_influxdb.solaredge.client.os.path.isfile",
        return_value=False,
    )
    @patch("solaredge_influxdb.solaredge.client.list_sites")
    def test_get_site_no_site(self, mock_list_sites, mock_isfile):
        mock_list_sites.return_value = None
        with pytest.raises(AttributeError):
            client = SolarEdgeClient("api_key")
            client.get_site()

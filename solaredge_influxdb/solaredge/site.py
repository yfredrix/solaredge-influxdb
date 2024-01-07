from typing import Union
from .models import SitesResponse
from loguru import logger


def list_sites(SolarEdgeClient) -> Union[SitesResponse, None]:
    """ "Request a list of sites from SolarEdge API"""

    url = f"{SolarEdgeClient.url}/sites/list"
    query_params = {"api_key": SolarEdgeClient.api_key}

    response = SolarEdgeClient.session.get(url, params=query_params)

    if response.ok:
        data = response.json()
        return SitesResponse(**data["sites"])
    logger.error("Failed to retrieve list of sites")
    return None

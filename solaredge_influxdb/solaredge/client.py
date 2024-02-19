import os

from urllib3.util import Retry
from requests import Session
from requests.adapters import HTTPAdapter
from loguru import logger
from typing import Union

from .site import list_sites


class SolarEdgeClient:
    url = "https://monitoringapi.solaredge.com"
    session = Session()

    def __init__(self, api_key: str, site_id: Union[int, None] = None):
        self.api_key = api_key
        self.__init_session()
        if not site_id:
            site_id = self.get_site()

        self.site_id = site_id

    def __init_session(self):
        retries = Retry(
            total=3,
            backoff_factor=0.1,
            status_forcelist=[429, 502, 503, 504],
            allowed_methods={"GET"},
        )
        self.session.headers.update({"Accept": "application/json"})
        self.session.mount("https://", HTTPAdapter(max_retries=retries))

    def get_site(self) -> int:
        """Get site ID from SolarEdge API or from disk"""
        if os.path.isfile("site_id.txt"):
            with open("site_id.txt", "r") as f:
                return int(f.read())
        site_response = list_sites(self)
        if site_response:
            if site_response.count > 1:
                logger.warning(
                    "More than one site found; Only first site is currently supported"
                )
                # TODO: Extend for multiple sites
            with open("site_id.txt", "w") as f:
                f.write(str(site_response.site[0].id))
            return site_response.site[0].id
        logger.error("Failed to retrieve site ID")
        raise AttributeError("Site ID must be defined and valid")

from typing import List

from bs4 import BeautifulSoup
from core.schemas import Parameter

from crawler.base import BaseCrawler


class Parameters(BaseCrawler):
    def get_parameters(self, station_uid: str) -> List[Parameter]:
        res = self.get(self.parameters_url, params={"sites": station_uid})

        soup = BeautifulSoup(res.text, "html.parser")
        return [
            Parameter(uid=o["value"], nome=o.text.replace("■", "").strip())
            for o in soup.find_all("option")
        ]

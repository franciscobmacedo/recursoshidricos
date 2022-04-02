from typing import List

from bs4 import BeautifulSoup
from common.schemas import Network

from crawler.base import BaseCrawler


class Networks(BaseCrawler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self) -> List[Network]:
        res = self.session.get(self.home_url)
        soup = BeautifulSoup(res.text, "html.parser")
        networks = soup.find("select", {"name": "f_redes_todas[]"})
        return [
            Network(id=n["value"], nome=n.text) for n in networks.find_all("option")
        ]

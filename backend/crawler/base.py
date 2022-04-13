import logging
from typing import Optional, Type

import requests

import time


class BaseCrawler:
    BASE_URL = "https://snirh.apambiente.pt"

    def __init__(
        self,
        session: Optional[Type[requests.Session]] = None,
        network_uid: str = None,
        new_network=True,
        *args,
        **kwargs,
    ):
        self.home_url = f"{self.BASE_URL}/index.php?idMain=2&idItem=1"
        self.stations_url = (
            f"{self.BASE_URL}/snirh/_dadosbase/site/xml/xml_listaestacoes.php"
        )
        self.stations_details_url = (
            f"{self.BASE_URL}/snirh/_dadosbase/site/janela.php?obj_janela=INFO_ESTACOES"
        )
        self.parameters_url = (
            f"{self.BASE_URL}/snirh/_dadosbase/site/_ajax_listaparscomdados.php"
        )
        self.data_url = f"{self.BASE_URL}/snirh/_dadosbase/site/janela_verdados.php"

        if session:
            self._session = session
        else:
            self.start_session()

        self.network_uid = network_uid
        if self.network_uid and new_network:
            self.select_network()

    def start_session(self):
        self._session = requests.Session()
        self._session.get(self.home_url)

    def select_network(self):
        data = {"f_redes_seleccao[]": self.network_uid, "aplicar_filtro": 1}
        self.post(self.home_url, data=data)

    def get(self, url, params=None):
        try:
            return self._session.get(url, params=params)
        except requests.exceptions.ConnectionError:
            logging.error(
                f"failed to get {url} with params {params}. Will try again in 2 secs.."
            )
            time.sleep(2)
            return self.get(url, params)

    def post(self, url, data):
        try:
            return self._session.post(url, data=data)
        except requests.exceptions.ConnectionError:
            logging.error(
                f"failed to post {url} with data {data}. Will try again in 2 secs.."
            )
            time.sleep(2)
            return self.post(url, data)

from typing import List

from bs4 import BeautifulSoup
from core.schemas import Station

from crawler.base import BaseCrawler
from crawler.networks import Networks


class Stations(BaseCrawler):
    def get_stations_uids(self):
        """return a dict with station code and uid: {'22E/01UG': '920686062', ... ,'18B/04UG': '920685966'}"""
        res = self.get(self.stations_url)
        soup = BeautifulSoup(res.text, "html.parser")
        data = {}
        markers = soup.find_all("marker")
        if markers:
            for station in markers:
                code = (
                    station["estacao"].split("(")[-1].split(")")[0].strip("■").strip()
                )
                data[code] = station["site"]
        else:
            res = self.get(self.home_url)
            soup = BeautifulSoup(res.text, "html.parser")
            stations = soup.find("select", {"name": "f_estacoes[]"})
            for station in stations.find_all("option"):
                code = station.text.split("(")[-1].strip(")").strip("■").strip()
                uid = station["value"]
                data[code] = uid
        return data

    def get_stations_details(self):
        res = self.get(self.stations_details_url)
        soup = BeautifulSoup(res.text, "html.parser")
        headers_dom = soup.find("thead").find("tr")
        headers = [h.text for h in headers_dom.find_all("td")]

        data = []
        for row in soup.find("tbody").find_all("tr"):
            row_data = {}
            for index, cell in enumerate(row.find_all("td")):
                row_data[headers[index]] = cell.text
            data.append(row_data)
        return data

    def get_stations(self) -> List[Station]:
        uids = self.get_stations_uids()
        stations = self.get_stations_details()
        formatted_stations = []
        for station in stations[:]:
            try:
                formatted_stations.append(
                    Station(
                        uid=uids[station["CÓDIGO"]],
                        codigo=station.get("CÓDIGO"),
                        nome=station.get("NOME"),
                        altitude=station.get("ALTITUDE (m)"),
                        latitude=station.get("LATITUDE (ºN)"),
                        longitude=station.get("LONGITUDE (ºW)"),
                        coord_x=station.get("COORD_X (m)"),
                        coord_y=station.get("COORD_Y (m)"),
                        bacia=station.get("BACIA"),
                        distrito=station.get("DISTRITO"),
                        concelho=station.get("CONCELHO"),
                        freguesia=station.get("FREGUESIA"),
                        entidade_responsavel_automatica=station.get(
                            "ENTIDADE RESPONSÁVEL (AUTOMÁTICA)"
                        ),
                        entidade_responsavel_convencional=station.get(
                            "ENTIDADE RESPONSÁVEL (CONVENCIONAL)"
                        ),
                        tipo_estacao_automatica=station.get(
                            "TIPO ESTAÇÃO (AUTOMÁTICA)"
                        ),
                        tipo_estacao_convencional=station.get(
                            "TIPO ESTAÇÃO (CONVENCIONAL)"
                        ),
                        entrada_funcionamento_convencional=station.get(
                            "ENTRADA FUNCIONAMENTO (CONVENCIONAL)"
                        ),
                        entrada_funcionamento_automatica=station.get(
                            "ENTRADA FUNCIONAMENTO (AUTOMÁTICA)"
                        ),
                        encerramento_convencional=station.get(
                            "ENCERRAMENTO (CONVENCIONAL)"
                        ),
                        encerramento_automatica=station.get(
                            "ENCERRAMENTO (AUTOMÁTICA)"
                        ),
                        telemetria=station.get("TELEMETRIA") == "SIM",
                        estado=station.get("ESTADO")
                        if station.get("ESTADO") not in ["-", ""]
                        else None,
                        indice_qualidade=station.get("ÍNDICE QUALIDADE*"),
                    )
                )
            except KeyError:
                continue
        return formatted_stations


def get_all_stations_states():
    networks = Networks().get_networks()
    station_states = []
    for network in networks:
        stations = Stations(network_uid=network.uid).get_stations_details()
        for station in stations:
            station_state = station.get("ESTADO", None)
            if station_state not in station_states:
                station_states.append(station_state)
    return station_states

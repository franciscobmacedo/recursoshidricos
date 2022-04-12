import datetime
import crawler
from crawler.tests import expected_responses
from unittest import mock
from django.test import TestCase


def open_mock_response(file):
    with open(f"crawler/tests/mock_data/{file}", "r") as f:
        mock_respnse = f.read()
    return mock_respnse


from requests_mock import Mocker


class CrawlerTestCase(TestCase):
    def test_networks(self):
        with Mocker() as mocker:
            mocker.get(
                f"https://snirh.apambiente.pt/index.php?idMain=2&idItem=1",
                text=open_mock_response("home.txt"),
            )
            networks = crawler.Networks().get()

        self.assertEqual(networks, expected_responses.networks)

    def test_stations(self):
        with Mocker() as mocker:
            mocker.get(
                f"https://snirh.apambiente.pt/index.php?idMain=2&idItem=1",
                text=open_mock_response("home.txt"),
            )
            mocker.get(
                "https://snirh.apambiente.pt/index.php?idMain=2&idItem=1",
                text=open_mock_response("home.txt"),
            )
            mocker.get(
                "https://snirh.apambiente.pt/snirh/_dadosbase/site/xml/xml_listaestacoes.php",
                text=open_mock_response("stations.txt"),
            )
            mocker.get(
                "https://snirh.apambiente.pt/snirh/_dadosbase/site/janela.php?obj_janela=INFO_ESTACOES",
                text=open_mock_response("stations_detail.txt"),
            )
            stations = crawler.Stations().get()

        self.assertEqual(stations, expected_responses.stations)

    def test_parameters(self):
        with Mocker() as mocker:
            mocker.get(
                "https://snirh.apambiente.pt/index.php?idMain=2&idItem=1",
                text=open_mock_response("home.txt"),
            )
            mocker.get(
                "https://snirh.apambiente.pt/snirh/_dadosbase/site/_ajax_listaparscomdados.php",
                text=open_mock_response("parameters.txt"),
            )
            parameters = crawler.Parameters().get(station_uid="1627743378")

        self.assertEqual(parameters, expected_responses.parameters)

    def test_data(self):
        with Mocker() as mocker:
            mocker.get(
                "https://snirh.apambiente.pt/index.php?idMain=2&idItem=1",
                text=open_mock_response("home.txt"),
            )
            mocker.get(
                "https://snirh.apambiente.pt/snirh/_dadosbase/site/janela_verdados.php",
                text=open_mock_response("data.txt"),
            )
            response = crawler.GetData().get_data(
                station_uid="1627743378",
                tmin=datetime.datetime(1980, 1, 1),
                tmax=datetime.datetime(1980, 6, 1),
                parameter_uid=1849,
            )

        self.assertEqual(response, expected_responses.data)

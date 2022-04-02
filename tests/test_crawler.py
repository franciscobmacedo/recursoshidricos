import datetime

import crawler

from tests import expected_responses


def open_mock_response(file):
    with open(f"tests/mock_data/{file}", "r") as f:
        mock_respnse = f.read()
    return mock_respnse


def test_networks(requests_mock):

    requests_mock.get(
        "https://snirh.apambiente.pt/index.php?idMain=2&idItem=1",
        text=open_mock_response("home.txt"),
    )

    assert expected_responses.networks == crawler.Networks().get()


def test_stations(requests_mock):
    requests_mock.get(
        "https://snirh.apambiente.pt/index.php?idMain=2&idItem=1",
        text=open_mock_response("home.txt"),
    )
    requests_mock.get(
        "https://snirh.apambiente.pt/snirh/_dadosbase/site/xml/xml_listaestacoes.php",
        text=open_mock_response("stations.txt"),
    )
    requests_mock.get(
        "https://snirh.apambiente.pt/snirh/_dadosbase/site/janela.php?obj_janela=INFO_ESTACOES",
        text=open_mock_response("stations_detail.txt"),
    )

    assert expected_responses.stations == crawler.Stations().get()


def test_parameters(requests_mock):
    requests_mock.get(
        "https://snirh.apambiente.pt/index.php?idMain=2&idItem=1",
        text=open_mock_response("home.txt"),
    )
    requests_mock.get(
        "https://snirh.apambiente.pt/snirh/_dadosbase/site/_ajax_listaparscomdados.php",
        text=open_mock_response("parameters.txt"),
    )

    assert expected_responses.parameters == crawler.Parameters().get(
        station_id="1627743378"
    )


def test_data(requests_mock):
    requests_mock.get(
        "https://snirh.apambiente.pt/index.php?idMain=2&idItem=1",
        text=open_mock_response("home.txt"),
    )
    requests_mock.get(
        "https://snirh.apambiente.pt/snirh/_dadosbase/site/janela_verdados.php",
        text=open_mock_response("data.txt"),
    )
    response = crawler.GetData().get_data(
        station_id="1627743378",
        tmin=datetime.datetime(1980, 1, 1),
        tmax=datetime.datetime(1980, 6, 1),
        parameter_id=1849,
    )
    assert expected_responses.data == response

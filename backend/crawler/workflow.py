import json
from pprint import pprint
from typing import Union

from utils import parse_datetime

from .data import GetData
from .networks import Networks
from .parameters import Parameters
from .stations import Stations
import datetime
import os
import logging


DATA_DIR = "data"
LOGS_DIR = "logs"


NETWORKS_FILE = os.path.join(DATA_DIR, "networks.json")
STATIONS_FILE = os.path.join(DATA_DIR, "stations-network_{network_uid}.json")
PARAMETERS_FILE = os.path.join(DATA_DIR, "parameters-stations_{stations}.json")
DATA_FILE = os.path.join(
    DATA_DIR,
    "data-stations_{stations}-parameters_{parameters}-tmin_{tmin}-tmax_{tmax}.json",
)


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def create_data_dir():
    if not os.path.exists(DATA_DIR):
        os.mkdir(DATA_DIR)


def create_logs_dir():
    if not os.path.exists(LOGS_DIR):
        os.mkdir(LOGS_DIR)


def setup_logs(filename: str):
    create_logs_dir()
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s %(message)s",
        handlers=[
            logging.FileHandler(os.path.join(LOGS_DIR, f"{filename}_{now}.log")),
            logging.StreamHandler(),
        ],
        level=logging.DEBUG,
    )


def dump(filename: str, data: Union[list, dict, str]):
    create_data_dir()
    with open(filename, "w") as f:
        json.dump(data, f)


def dump_networks():
    print(f"{bcolors.UNDERLINE}\nFetching networks...\n{bcolors.ENDC}")
    bot = Networks()
    networks = [n.dict() for n in bot.get_networks()]
    pprint(networks)
    dump(NETWORKS_FILE, networks)
    print(f"\nNetworks dumped to  {bcolors.OKGREEN}{NETWORKS_FILE}\n{bcolors.ENDC}")


def dump_stations(network_uid: str):
    print(
        f"\nFetching stations for network {bcolors.OKGREEN}{network_uid}{bcolors.ENDC}...\n"
    )
    bot = Stations(network_uid=network_uid)
    stations = [s.dict() for s in bot.get_stations()]
    pprint(stations)
    stations_file = STATIONS_FILE.format(network_uid=network_uid)
    dump(stations_file, stations)
    print(f"\n Stations dumped to {bcolors.OKGREEN}{stations_file}\n{bcolors.ENDC}")


def dump_parameters(network_uid: str, station_uids: list[str]):
    stations_rep = ",".join(station_uids)

    print(
        f"\nFetching parameters for station {bcolors.OKGREEN}{stations_rep}{bcolors.ENDC} (from network {bcolors.OKGREEN}{network_uid}{bcolors.ENDC})...\n"
    )
    bot = Parameters(network_uid=network_uid)
    parameters = [s.dict() for s in bot.get_parameters(station_uids)]
    parameters_file = PARAMETERS_FILE.format(stations=stations_rep)
    pprint(parameters)
    dump(parameters_file, parameters)
    print(f"\n Parameters dumped to {bcolors.OKGREEN}{parameters_file}\n{bcolors.ENDC}")


def dump_data(station_uids: list[str], parameter_uids: list[str], tmin: str, tmax: str):
    stations_rep = ",".join(station_uids)
    parameters_rep = ",".join(parameter_uids)
    print(stations_rep)
    print(
        f"""\nFetching data for 
        station(s) {bcolors.OKGREEN}{stations_rep}{bcolors.ENDC} 
        parameter(s) {bcolors.OKGREEN}{parameters_rep}{bcolors.ENDC} 
        between {bcolors.OKGREEN}{tmin}{bcolors.ENDC} and {bcolors.OKGREEN}{tmax}{bcolors.ENDC}\n
        """
    )
    bot = GetData()
    data = bot.get_data(
        station_uids=station_uids,
        parameter_uids=parameter_uids,
        tmin=parse_datetime(tmin, format="%Y-%m-%d"),
        tmax=parse_datetime(tmax, format="%Y-%m-%d"),
    )
    data_file = DATA_FILE.format(
        stations=stations_rep, parameters=parameters_rep, tmin=tmin, tmax=tmax
    )
    dump(data_file, data.json())
    print(f"\n Data dumped to {bcolors.OKGREEN}{data_file}\n{bcolors.ENDC}")

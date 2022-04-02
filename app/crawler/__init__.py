import json
from pprint import pprint
from typing import Union

from common.settings import (
    DATA_FILE,
    NETWORKS_FILE,
    PARAMETERS_FILE,
    STATIONS_FILE,
    bcolors,
    create_data_dir,
)
from common.utils import parse_datetime

from .data import GetData
from .networks import Networks
from .parameters import Parameters
from .stations import Stations


def dump(filename: str, data: Union[list, dict, str]):
    create_data_dir()
    with open(filename, "w") as f:
        json.dump(data, f)


def dump_networks():
    print(f"{bcolors.UNDERLINE}\nFetching networks...\n{bcolors.ENDC}")
    bot = Networks()
    networks = [n.dict() for n in bot.get()]
    pprint(networks)
    dump(NETWORKS_FILE, networks)
    print(f"\nNetworks dumped to  {bcolors.OKGREEN}{NETWORKS_FILE}\n{bcolors.ENDC}")


def dump_stations(network_id: str):
    print(
        f"\nFetching stations for network {bcolors.OKGREEN}{network_id}{bcolors.ENDC}...\n"
    )
    bot = Stations(network_id=network_id)
    stations = [s.dict() for s in bot.get()]
    pprint(stations)
    stations_file = STATIONS_FILE.format(network_id=network_id)
    dump(stations_file, stations)
    print(f"\n Stations dumped to {bcolors.OKGREEN}{stations_file}\n{bcolors.ENDC}")


def dump_parameters(network_id: str, station_id: str):
    print(
        f"\nFetching parameters for station {bcolors.OKGREEN}{station_id}{bcolors.ENDC} (from network {bcolors.OKGREEN}{network_id}{bcolors.ENDC})...\n"
    )
    bot = Parameters(network_id=network_id)
    parameters = [s.dict() for s in bot.get(station_id)]
    parameters_file = PARAMETERS_FILE.format(station_id=station_id)
    pprint(parameters)
    dump(parameters_file, parameters)
    print(f"\n Parameters dumped to {bcolors.OKGREEN}{parameters_file}\n{bcolors.ENDC}")


def dump_data(station_id: str, parameter_id: str, tmin: str, tmax: str):
    print(
        f"""\nFetching data for 
        parameter {bcolors.OKGREEN}{parameter_id}{bcolors.ENDC} 
        station {bcolors.OKGREEN}{station_id}{bcolors.ENDC} 
        between {bcolors.OKGREEN}{tmin}{bcolors.ENDC} and {bcolors.OKGREEN}{tmax}{bcolors.ENDC}\n
        """
    )
    bot = GetData()
    data = bot.get_data(
        station_id=station_id,
        parameter_id=parameter_id,
        tmin=parse_datetime(tmin, format="%Y-%m-%d"),
        tmax=parse_datetime(tmax, format="%Y-%m-%d"),
    )
    data_file = DATA_FILE.format(
        station_id=station_id, parameter_id=parameter_id, tmin=tmin, tmax=tmax
    )
    dump(data_file, data.json())
    print(f"\n Data dumped to {bcolors.OKGREEN}{data_file}\n{bcolors.ENDC}")

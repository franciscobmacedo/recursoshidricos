import json
from pprint import pprint
from typing import Union
from django.conf import settings


from utils import parse_datetime

from .data import GetData
from .networks import Networks
from .parameters import Parameters
from .stations import Stations


def dump(filename: str, data: Union[list, dict, str]):
    settings.create_data_dir()
    with open(filename, "w") as f:
        json.dump(data, f)


def dump_networks():
    print(
        f"{settings.bcolors.UNDERLINE}\nFetching networks...\n{settings.bcolors.ENDC}"
    )
    bot = Networks()
    networks = [n.dict() for n in bot.get()]
    pprint(networks)
    dump(settings.NETWORKS_FILE, networks)
    print(
        f"\nNetworks dumped to  {settings.bcolors.OKGREEN}{settings.NETWORKS_FILE}\n{settings.bcolors.ENDC}"
    )


def dump_stations(network_id: str):
    print(
        f"\nFetching stations for network {settings.bcolors.OKGREEN}{network_id}{settings.bcolors.ENDC}...\n"
    )
    bot = Stations(network_id=network_id)
    stations = [s.dict() for s in bot.get()]
    pprint(stations)
    stations_file = settings.STATIONS_FILE.format(network_id=network_id)
    dump(stations_file, stations)
    print(
        f"\n Stations dumped to {settings.bcolors.OKGREEN}{stations_file}\n{settings.bcolors.ENDC}"
    )


def dump_parameters(network_id: str, station_id: str):
    print(
        f"\nFetching parameters for station {settings.bcolors.OKGREEN}{station_id}{settings.bcolors.ENDC} (from network {settings.bcolors.OKGREEN}{network_id}{settings.bcolors.ENDC})...\n"
    )
    bot = Parameters(network_id=network_id)
    parameters = [s.dict() for s in bot.get(station_id)]
    parameters_file = settings.PARAMETERS_FILE.format(station_id=station_id)
    pprint(parameters)
    dump(parameters_file, parameters)
    print(
        f"\n Parameters dumped to {settings.bcolors.OKGREEN}{parameters_file}\n{settings.bcolors.ENDC}"
    )


def dump_data(station_id: str, parameter_id: str, tmin: str, tmax: str):
    print(
        f"""\nFetching data for 
        parameter {settings.bcolors.OKGREEN}{parameter_id}{settings.bcolors.ENDC} 
        station {settings.bcolors.OKGREEN}{station_id}{settings.bcolors.ENDC} 
        between {settings.bcolors.OKGREEN}{tmin}{settings.bcolors.ENDC} and {settings.bcolors.OKGREEN}{tmax}{settings.bcolors.ENDC}\n
        """
    )
    bot = GetData()
    data = bot.get_data(
        station_id=station_id,
        parameter_id=parameter_id,
        tmin=parse_datetime(tmin, format="%Y-%m-%d"),
        tmax=parse_datetime(tmax, format="%Y-%m-%d"),
    )
    data_file = settings.DATA_FILE.format(
        station_id=station_id, parameter_id=parameter_id, tmin=tmin, tmax=tmax
    )
    dump(data_file, data.json())
    print(
        f"\n Data dumped to {settings.bcolors.OKGREEN}{data_file}\n{settings.bcolors.ENDC}"
    )

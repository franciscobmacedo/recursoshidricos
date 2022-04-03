import logging
import os
import datetime

DATA_DIR = "data"
LOGS_DIR = "logs"


NETWORKS_FILE = os.path.join(DATA_DIR, "networks.json")
STATIONS_FILE = os.path.join(DATA_DIR, "stations-network_{network_id}.json")
PARAMETERS_FILE = os.path.join(DATA_DIR, "parameters-station_{station_id}.json")
DATA_FILE = os.path.join(
    DATA_DIR,
    "data-station_{station_id}-parameter_{parameter_id}-tmin_{tmin}-tmax_{tmax}.json",
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
    logging.basicConfig(filename=os.path.join(LOGS_DIR, f"{filename}_{now}.log"), level=logging.DEBUG)
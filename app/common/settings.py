import os

DATA_DIR = "data"


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

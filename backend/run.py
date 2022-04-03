import argparse

import uvicorn

import crawler
from api.workflow import populate_database


class Mode:
    api = "api"
    crawler = "crawler"


class CrawlerType:
    networks = "networks"
    stations = "stations"
    parameters = "parameters"
    data = "data"


def run_api():
    uvicorn.run("api.main:app", reload=True, debug=True, host="0.0.0.0", port=8000)


class Run:
    def __init__(self) -> None:
        parser = argparse.ArgumentParser(description="snirh crawler and api.")
        subparsers = parser.add_subparsers(
            help='set the run mode: "api" or "crawler"', required=True, dest="run_mode"
        )
        self.api_parser = subparsers.add_parser(Mode.api, help="run the api")
        self.crawler_parser = subparsers.add_parser(
            Mode.crawler, help="run the crawler with extra arguments"
        )
        self.crawler_parser.add_argument(
            "CrawlerType",
            metavar="crawler_type",
            type=str,
            help='set the crawler type: "networks", "stations", "parameters" or "data"',
            choices=[
                CrawlerType.networks,
                CrawlerType.stations,
                CrawlerType.parameters,
                CrawlerType.data,
            ],
        )

        self.api_parser.add_argument(
            "-p",
            "--populate_database",
            help="populate api database",
            action="store_true",
        )
        self.api_parser.add_argument(
            "-r",
            "--replace",
            help="replace existing data",
            action="store_true",
        )

        args, _ = parser.parse_known_args()
        if args.run_mode == Mode.api:
            if args.populate_database:
                populate_database(args.replace)
            else:
                run_api()

        elif args.CrawlerType == CrawlerType.networks:
            crawler.dump_networks()
        elif args.CrawlerType == CrawlerType.data:
            self.add_station_arg()
            self.add_param_arg()
            self.add_tmin_arg()
            self.add_tmax_arg()
            args = parser.parse_args()
            crawler.dump_data(args.station, args.parameter, args.tmin, args.tmax)

        else:
            self.add_network_arg()
            if args.CrawlerType == CrawlerType.stations:
                args = parser.parse_args()
                crawler.dump_stations(args.network)

            if args.CrawlerType == CrawlerType.parameters:
                self.add_station_arg()
                args = parser.parse_args()
                crawler.dump_parameters(args.network, args.station)

    def add_network_arg(self):
        self.crawler_parser.add_argument(
            "-n", "--network", help="network id", required=True
        )

    def add_station_arg(self):
        self.crawler_parser.add_argument(
            "-s", "--station", help="station id", required=True
        )

    def add_param_arg(self):
        self.crawler_parser.add_argument(
            "-p", "--parameter", help="parameter id", required=True
        )

    def add_tmin_arg(self):
        self.crawler_parser.add_argument(
            "-f", "--tmin", help="from tmin (format 'yyyy-mm-dd')", required=True
        )

    def add_tmax_arg(self):
        self.crawler_parser.add_argument(
            "-t", "--tmax", help="to tmax (format 'yyyy-mm-dd')", required=True
        )


if __name__ == "__main__":
    Run()

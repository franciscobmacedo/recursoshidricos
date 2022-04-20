from django.core.management.base import BaseCommand, CommandError
from crawler import workflow as wf


class CrawlerType:
    networks = "networks"
    stations = "stations"
    parameters = "parameters"
    data = "data"


class Command(BaseCommand):
    help = "Get data from SNIRH and write it to json files"

    def add_arguments(self, parser):
        self.parser = parser

        self.parser.add_argument(
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
        self.parser.add_argument("-n", "--network", help="network uid", required=False)
        self.parser.add_argument(
            "-s", "--stations", nargs="+", help="stations uid", required=False
        )

        self.parser.add_argument(
            "-p", "--parameters", nargs="+", help="parameters uid", required=False
        )
        self.parser.add_argument(
            "-f", "--tmin", help="from tmin (format 'yyyy-mm-dd')", required=False
        )
        self.parser.add_argument(
            "-t", "--tmax", help="to tmax (format 'yyyy-mm-dd')", required=False
        )

    def handle(self, *args, **options):
        crawler_type = options["CrawlerType"]
        network = options["network"]
        stations = options["stations"]
        parameters = options["parameters"]
        tmin = options["tmin"]
        tmax = options["tmax"]

        if crawler_type == CrawlerType.networks:
            wf.dump_networks()

        elif crawler_type == CrawlerType.stations:
            if not network:
                raise CommandError('"network" argument is required')
            wf.dump_stations(network)

        elif crawler_type == CrawlerType.parameters:
            if not network:
                raise CommandError('"network" argument is required')
            if not stations:
                raise CommandError('"stations" argument is required')
            wf.dump_parameters(network, stations)

        elif crawler_type == CrawlerType.data:
            if not stations:
                raise CommandError('"stations" argument is required')
            if not parameters:
                raise CommandError('"parameters" argument is required')
            if not tmin:
                raise CommandError('"tmin" argument is required')
            if not tmax:
                raise CommandError('"tmax" argument is required')
            wf.dump_data(stations, parameters, tmin, tmax)

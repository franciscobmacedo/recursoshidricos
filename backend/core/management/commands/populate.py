from django.core.management.base import BaseCommand, CommandError
from core.workflow import populate_static_data, populate_variable_data


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        parser.add_argument("-s", "--static", action="store_true")
        parser.add_argument("-t", "--timeseries", action="store_true")
        parser.add_argument("-r", "--replace", action="store_true")
        parser.add_argument("-n", "--network_uid", type=str, required=False)
        parser.add_argument("-st", "--station_uid", type=str, required=False)
        parser.add_argument("-tmin", "--tmin", type=str, required=False)
        parser.add_argument("-tmax", "--tmax", type=str, required=False)
        parser.add_argument("-f", "--frequency", type=str, required=False)

    def handle(self, *args, **options):
        if options["static"]:
            populate_static_data(options["replace"])
        elif options["timeseries"]:
            populate_variable_data(
                options["replace"],
                options["network_uid"],
                options["station_uid"],
                options["tmin"],
                options["tmax"],
                options["frequency"],
            )
        else:
            print("choose a valid option (-s or -t)")

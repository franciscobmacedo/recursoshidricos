from django.core.management.base import BaseCommand, CommandError
from core.workflow import populate_static_data, populate_variable_data


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        parser.add_argument("-s", "--static", action="store_true")
        parser.add_argument("-t", "--timeseries", action="store_true")
        parser.add_argument("-r", "--replace", action="store_true")

    def handle(self, *args, **options):
        if options["static"]:
            populate_static_data(options["replace"])
        elif options["timeseries"]:
            populate_variable_data(options["replace"])
        else:
            print("choose a valid option (-s or -t)")
